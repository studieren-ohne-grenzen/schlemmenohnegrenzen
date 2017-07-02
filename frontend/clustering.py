from scipy.cluster.hierarchy import linkage, fcluster
from geopy.distance import vincenty
import cProfile, pstats, io, math
from operator import itemgetter
from frontend.models import Household, Cluster, VisitingGroup
from munkres import Munkres, print_matrix, DISALLOWED

def custom_dist(x, y):
    return vincenty(x, y).m

def initial_clusters(datapoints, clusters):
    listOfCoords = []
    numOfClusters = len(datapoints) // 9
    for elem in datapoints:
        listOfCoords.append([elem.latitude, elem.longitude])
    z = linkage(listOfCoords, method='complete', metric=custom_dist)
    tmp = fcluster(z, numOfClusters, criterion='maxclust')
    for i in range(len(tmp)):
        datapoints[i].cluster = clusters[tmp[i] - 1]
        datapoints[i].save()

def clustersHaveWrongSize(clusters):
    num_below = 0
    num_above = 0
    for cluster in clusters:
        #if cluster["is12"] and cluster["size"] > 12:
        #    num_above += 1
        if not cluster["is12"] and cluster["size"] > 9:
            num_above += 1
        if not cluster["is12"] and cluster["size"] < 9:
            num_below += 1

    print(str(num_above) + 'too lare, ' + str(num_below)+ ' too small')
    return num_above > 0

def getMinDistanceToCluster(point, set):
    minDist = float('inf')
    for elem in set:
        dist = custom_dist((point["latitude"], point["longitude"]), (elem["latitude"], elem["longitude"]))
        minDist = min(dist, minDist)
    return minDist

def getMaxDistanceToCluster(point, set):
    maxDist = float('-inf')
    for elem in set:
        dist = custom_dist((point["latitude"], point["longitude"]), (elem["latitude"], elem["longitude"]))
        maxDist = max(dist, maxDist)
    return maxDist

def getMeanDistanceToCluster(point, set):
    meanDistance = 0.0
    for elem in set:
        dist = custom_dist((point["latitude"], point["longitude"]), (elem["latitude"], elem["longitude"]))
        meanDistance = meanDistance + dist / len(set)
    return meanDistance

def get_cluster_overweight(cluster):
    if (cluster["is12"]):
        return cluster["size"] - 12
    else:
        return cluster["size"] - 9

def rebalancingIteration(new_households, new_clusters):
    currentMinDistance = 10000000000
    currentSrcElem = None
    currentDstCluster = None

    for point in new_households:
        srcOverweight = get_cluster_overweight(new_clusters[point["cluster"]])
        if (srcOverweight > 0):
            #cluster of this household is to big
            pointCurrMinDist = 1000000000
            pointCurrDstClust = None
            for c in range(len(new_clusters)):
                if (srcOverweight > (get_cluster_overweight(new_clusters[c]) + 1)):
                    #cluster is smaller
                    set_ = []
                    for p in new_households:
                        if p["cluster"] == c:
                            set_.append(p)
                    dist = getMinDistanceToCluster(point, set_)
                    if dist < pointCurrMinDist:
                        pointCurrMinDist = dist
                        pointCurrDstClust = c
            if pointCurrMinDist < currentMinDistance:
                currentMinDistance = pointCurrMinDist
                currentDstCluster = pointCurrDstClust
                currentSrcElem = point

    tmp_cluster = currentSrcElem["cluster"]
    currentSrcElem["cluster"] = currentDstCluster
    new_clusters[tmp_cluster]["size"] -= 1
    new_clusters[currentDstCluster]["size"] += 1

def rebalancingIterationPicking(new_households, new_clusters):
    currentMinDistance = float('inf')
    currentSrcElem = None
    currentDstCluster = None

    for cluster in range(len(new_clusters)):
        targetOverweight = get_cluster_overweight(new_clusters[cluster])
        if (targetOverweight < 0):
            #cluster of this household is to small
            pointCurrMinDist = float('inf')
            currentSrcElem = None
            currentDstCluster = cluster
            set_ = []
            for p in new_households:
                if p["cluster"] == cluster:
                    set_.append(p)

            for point in new_households:
                if (point['cluster'] != cluster and targetOverweight < (get_cluster_overweight(new_clusters[point['cluster']] ) - 1)):
                    #cluster is bigger
                    dist = getMinDistanceToCluster(point, set_)
                    if dist < pointCurrMinDist:
                        pointCurrMinDist = dist
                        currentSrcElem= point

            tmp_cluster = currentSrcElem["cluster"]
            currentSrcElem["cluster"] = currentDstCluster
            new_clusters[tmp_cluster]["size"] -= 1
            new_clusters[currentDstCluster]["size"] += 1

def rebalancingIterationGlobalOpt(new_households, new_clusters, iteration):
    print('starting iteration #'+str(iteration))
    current_cost = judgeClusterDistribution(new_households, new_clusters, iteration-1)
    sorted_clusters = sorted(new_clusters, reverse=True, key=lambda cluster: judgeCluster(cluster, new_households, new_clusters, iteration))
    improvements = []
    for c, cluster in enumerate(sorted_clusters):
        if cluster['size'] > 9:
            continue
        # sort points by proximity to this cluster
        dist = dict()
        set_ = []
        for p in new_households:
            if p["cluster"] == c:
                set_.append(p)
        for p, point in enumerate(new_households):
            dist[p] = getMeanDistanceToCluster(point, set_)
        # sort asc. by distance
        closest_points = [(i, new_households[i]) for i in range(len(new_households))]
        closest_points = sorted(closest_points, key=lambda p: dist[p[0]])
        closest_points = [p[1] for p in closest_points]
        
        # try adding a close point to a needy cluster
        target = c
        for p, point in enumerate(closest_points):
            if point['cluster'] == target:
                continue
            source = point['cluster']
            new_clusters[source]['size'] -= 1
            new_clusters[target]['size'] += 1
            point['cluster'] = target
            new_cost = judgeClusterDistribution(new_households, new_clusters, iteration)
            new_clusters[source]['size'] += 1
            new_clusters[target]['size'] -= 1
            point['cluster'] = source
            if current_cost > new_cost:
                print(current_cost - new_cost)
                improvements.append((
                   new_households.index(point),
                   source,
                   target,
                   current_cost - new_cost
                ))
    if len(improvements) == 0:
      return False
    sorted_improvements = sorted(improvements, reverse=True, key=itemgetter(3))
    improvement = sorted_improvements[0]
    print("improvement:"+str(improvement))
    new_clusters[improvement[1]]['size'] -= 1
    new_clusters[improvement[2]]['size'] += 1
    new_households[improvement[0]]['cluster'] = improvement[2]
    return True

def judgeClusterDistribution(households, clusters, iteration):
    score = 0
    for cluster in clusters:
        score += judgeCluster(cluster, households, clusters, iteration)
    score = score / len(clusters)
    return score

def judgeCluster(cluster, households, clusters, iteration): 
    # get mean score of the points in this cluster
    score = 0
    for point in households:
        if (clusters[point['cluster']] == cluster):
              score += judgePoint(point, households, clusters)
    if cluster['size'] == 0:
        return 0
    density_score = score / cluster['size']

    size_score = abs(9 - cluster['size']) / 9
    #score *= 2**abs((cluster['size'] - 9) * (1+math.log(iteration))); # CLUSTER_SIZE
    score = (2**(size_score*50)  + 4*density_score ) /2
    return score

def judgePoint(point, households, clusters):
    # get mean reciprocal distance of this cluster
    set_ = []
    for p in households:
        if p["cluster"] == point['cluster'] and p != point:
            set_.append(p)
    mean_dist = getMeanDistanceToCluster(point, set_)
    min_dist = getMinDistanceToCluster(point, set_)
    
    if mean_dist == 0:
        return 0
    
    distance_score = mean_dist

    return distance_score

def rebalancingIterationHungarian(households, clusters, iteration):
    current_cost = judgeClusterDistribution(households, clusters, iteration)
    # prepare matrix
    matrix = [[None for i in range(len(clusters)*12)] for i in range(len(households))]
    for c, cluster in enumerate(clusters):
        # prepare cluster list
        set_ = []
        for p, point in enumerate(households):
            if point["cluster"] == c:
                set_.append(point)
        for p, point in enumerate(households):
            dist = getMeanDistanceToCluster(point, set_)
            for i in range(12):
                matrix[p][c+len(clusters)*i] = dist
                if i >= 9 and not cluster['is12']:
                    matrix[p][c+len(clusters)*i] = DISALLOWED

    munkres = Munkres()
    indeces = munkres.compute(matrix)

    for p,c in indeces:
        source = households[p]['cluster']
        target = c % len(clusters)
        clusters[source]['size'] -= 1
        clusters[target]['size'] += 1
        households[p]['cluster'] = target
    
    new_cost = judgeClusterDistribution(households, clusters, iteration)
     
    return new_cost < current_cost
         


def balance_clusters(datapoints, clusters, numOf12Clusters):
    print(numOf12Clusters)
    new_clusters = []
    new_households = []
    cl12 = 0
    for cluster in clusters:
        elems = cluster.household_set.all()
        for e in elems:
            new_households.append({"longitude": e.longitude, "latitude": e.latitude, "id": e.id, "cluster": len(new_clusters)})
        new_clusters.append({"size": len(elems), "clusterNum": cluster.clusterNum, "is12": False})
        if cl12 < numOf12Clusters:
            cluster.is12 = True
            cluster.save()
            new_clusters[-1]["is12"] = True # TODO: Sort by max size
            cl12 += 1

    while clustersHaveWrongSize(new_clusters):
        #rebalancingIteration(new_households, new_clusters)
        #rebalancingIterationPicking(new_households, new_clusters)
        #improved = rebalancingIterationGlobalOpt(new_households, new_clusters, i)
        rebalancingIterationHungarian(new_households, new_clusters, 1)

    for point in new_households:
        for e in datapoints:
            if e.id == point["id"]:
                for c in clusters:
                    if c.clusterNum == new_clusters[point["cluster"]]["clusterNum"]:
                        e.cluster = c
                        e.save()
                        break
                break

def visiting_collision(h1, h2, h3):
    # TODO: PLZ
    if h1['street'] == h2['street'] or h1['street'] == h3['street'] or h2['street'] == h3['street']:
        return True
    else:
        return False

def get_traveling_distance(elems, dist, norm):
    total = 0.0
    total += dist[elems[0]][elems[1]] + dist[elems[0]][elems[2]]
    total += dist[elems[4]][elems[3]] + dist[elems[4]][elems[5]]
    total += dist[elems[6]][elems[7]] + dist[elems[6]][elems[8]]

    total += dist[elems[3]][elems[0]] + dist[elems[3]][elems[6]] + dist[elems[3]][elems[4]]
    total += dist[elems[1]][elems[4]] + dist[elems[1]][elems[6]] + dist[elems[1]][elems[0]]
    total += dist[elems[2]][elems[0]] + dist[elems[2]][elems[4]] + dist[elems[2]][elems[6]]

    total += dist[elems[8]][elems[3]] + dist[elems[8]][elems[1]] + dist[elems[8]][elems[2]]
    total += dist[elems[5]][elems[1]] + dist[elems[5]][elems[2]] + dist[elems[5]][elems[3]]
    total += dist[elems[7]][elems[2]] + dist[elems[7]][elems[3]] + dist[elems[7]][elems[1]]

    return total / norm

def get_score(households, elems, dist, norm, is12):
    # TODO: is12
    score = 0.0
    h1 = households[elems[0]]
    h2 = households[elems[1]]
    h3 = households[elems[2]]
    h4 = households[elems[3]]
    h5 = households[elems[4]]
    h6 = households[elems[5]]
    h7 = households[elems[6]]
    h8 = households[elems[7]]
    h9 = households[elems[8]]
    if visiting_collision(h1, h2, h3) or visiting_collision(h4, h5, h6) or visiting_collision(h7, h8, h9):
        score += 1.0
    if visiting_collision(h1, h4, h7) or visiting_collision(h2, h5, h8) or visiting_collision(h3, h6, h9):
        score += 1.0
    if visiting_collision(h1, h5, h9) or visiting_collision(h2, h6, h7) or visiting_collision(h3, h4, h8):
        score += 1.0

    # keine zwei gleichzeitigen visiting groups in der selben kueche
    if visiting_collision(h1, h5, h7) or visiting_collision(h4, h2, h3) or visiting_collision(h9, h6, h8):
        score += 10.0

    score += get_traveling_distance(elems, dist, norm)

    return score

def recur(households, curr_elems, curr_score, dist, norm, is12):
    #if (len(curr_elems) < 4):
    #    print(curr_elems)

    curr_elems.append(-1)
    if is12:
        cnt = 12
        if curr_score[0] < 1.0:
            return
    else:
        cnt = 9

    for i in range(cnt):
        if i not in curr_elems:
            curr_elems[-1] = i
            if len(curr_elems) < cnt:
                recur(households, curr_elems, curr_score, dist, norm, is12)
            else:
                score = get_score(households, curr_elems, dist, norm, is12)
                if is12 and score < 1.0:
                    curr_score[0] = score
                    curr_score[1] = curr_elems[:]
                    return
                if curr_score[0] > score:
                    curr_score[0] = score
                    curr_score[1] = curr_elems[:]
    curr_elems.pop()

def generate_visiting_groups(clusters):
    curr_v_num = 0
    #pr = cProfile.Profile()
    #pr.enable()

    for cluster in clusters:
        currscore = [100000000000.0, []]
        households = []
        household_a = cluster.household_set.all()
        for h in household_a:
            households.append({'street': h.street, 'plz': h.plz, 'longitude': h.longitude, 'latitude': h.latitude})

        # generate distance matrix
        dist = []
        maxdist = 0.0
        for h in households:
            tmp = []
            for j in households:
                d = custom_dist((h["latitude"], h["longitude"]), (j["latitude"], j["longitude"]))
                maxdist = max(maxdist, d)
                tmp.append(d)
            dist.append(tmp)

        recur(households, [], currscore, dist, maxdist * 27.0, cluster.is12)
        print(currscore)
        score = currscore[1]
        h1 = household_a[score[0]]
        h2 = household_a[score[1]]
        h3 = household_a[score[2]]
        h4 = household_a[score[3]]
        h5 = household_a[score[4]]
        h6 = household_a[score[5]]
        h7 = household_a[score[6]]
        h8 = household_a[score[7]]
        h9 = household_a[score[8]]
        if cluster.is12:
            print(len(household_a))
            h10 = household_a[score[9]]
            h11 = household_a[score[10]]
            h12 = household_a[score[11]]

        v1 = VisitingGroup()
        v1.visiting_group_num = curr_v_num
        v1.dinner = 0
        v1.save()
        curr_v_num += 1
        v2 = VisitingGroup()
        v2.visiting_group_num = curr_v_num
        v2.dinner = 0
        v2.save()
        curr_v_num += 1
        v3 = VisitingGroup()
        v3.visiting_group_num = curr_v_num
        v3.dinner = 0
        v3.save()
        curr_v_num += 1
        v4 = VisitingGroup()
        v4.visiting_group_num = curr_v_num
        v4.dinner = 1
        v4.save()
        curr_v_num += 1
        v5 = VisitingGroup()
        v5.visiting_group_num = curr_v_num
        v5.dinner = 1
        v5.save()
        curr_v_num += 1
        v6 = VisitingGroup()
        v6.visiting_group_num = curr_v_num
        v6.dinner = 1
        v6.save()
        curr_v_num += 1
        v7 = VisitingGroup()
        v7.visiting_group_num = curr_v_num
        v7.dinner = 2
        v7.save()
        curr_v_num += 1
        v8 = VisitingGroup()
        v8.visiting_group_num = curr_v_num
        v8.dinner = 2
        v8.save()
        curr_v_num += 1
        v9 = VisitingGroup()
        v9.visiting_group_num = curr_v_num
        v9.dinner = 2
        v9.save()
        curr_v_num += 1
        if cluster.is12:
            v10 = VisitingGroup()
            v10.visiting_group_num = curr_v_num
            v10.dinner = 0
            v10.save()
            curr_v_num += 1
            v11 = VisitingGroup()
            v11.visiting_group_num = curr_v_num
            v11.dinner = 1
            v11.save()
            curr_v_num += 1
            v12 = VisitingGroup()
            v12.visiting_group_num = curr_v_num
            v12.dinner = 2
            v12.save()
            curr_v_num += 1

        v1.gastgeber = h1
        v2.gastgeber = h5
        v3.gastgeber = h7
        h1.first_visit = v1
        h2.first_visit = v1
        h3.first_visit = v1
        h4.first_visit = v2
        h5.first_visit = v2
        h6.first_visit = v2
        h7.first_visit = v3
        h8.first_visit = v3
        h9.first_visit = v3
        if cluster.is12:
            h10.first_visit = v10
            h11.first_visit = v10
            h12.first_visit = v10
            v10.gastgeber = h10

        if not cluster.is12:
            h1.puzzle = 91;
            h2.puzzle = 92;
            h3.puzzle = 93;
            h4.puzzle = 94;
            h5.puzzle = 95;
            h6.puzzle = 96;
            h7.puzzle = 97;
            h8.puzzle = 98;
            h9.puzzle = 99;
        else:
            h1.puzzle = 1201;
            h2.puzzle = 1202;
            h3.puzzle = 1203;
            h4.puzzle = 1204;
            h5.puzzle = 1205;
            h6.puzzle = 1206;
            h7.puzzle = 1207;
            h8.puzzle = 1208;
            h9.puzzle = 1209;
            h10.puzzle = 1210;
            h11.puzzle = 1211;
            h12.puzzle = 1212;

        if not cluster.is12:
            v4.gastgeber = h4
            v5.gastgeber = h2
            v6.gastgeber = h3
            h1.second_visit = v4
            h4.second_visit = v4
            h7.second_visit = v4
            h2.second_visit = v5
            h5.second_visit = v5
            h8.second_visit = v5
            h3.second_visit = v6
            h6.second_visit = v6
            h9.second_visit = v6
        else:
            v4.gastgeber = h4
            v5.gastgeber = h2
            v6.gastgeber = h12
            v11.gastgeber = h3
            h1.second_visit = v4
            h4.second_visit = v4
            h10.second_visit = v4
            h2.second_visit = v5
            h11.second_visit = v5
            h8.second_visit = v5
            h12.second_visit = v6
            h6.second_visit = v6
            h9.second_visit = v6
            h7.second_visit = v11
            h5.second_visit = v11
            h3.second_visit = v11

        if not cluster.is12:
            v7.gastgeber = h9
            v8.gastgeber = h6
            v9.gastgeber = h8
            h1.third_visit = v7
            h5.third_visit = v7
            h9.third_visit = v7
            h2.third_visit = v8
            h6.third_visit = v8
            h7.third_visit = v8
            h3.third_visit = v9
            h4.third_visit = v9
            h8.third_visit = v9
        else:
            v7.gastgeber = h11
            v8.gastgeber = h6
            v9.gastgeber = h8
            v12.gastgeber = h9
            h1.third_visit = v7
            h5.third_visit = v7
            h11.third_visit = v7
            h10.third_visit = v8
            h6.third_visit = v8
            h7.third_visit = v8
            h3.third_visit = v9
            h12.third_visit = v9
            h8.third_visit = v9
            h9.third_visit = v12
            h2.third_visit = v12
            h4.third_visit = v12

        v1.save()
        v2.save()
        v3.save()
        v4.save()
        v5.save()
        v6.save()
        v7.save()
        v8.save()
        v9.save()

        h1.save()
        h2.save()
        h3.save()
        h4.save()
        h5.save()
        h6.save()
        h7.save()
        h8.save()
        h9.save()

        if cluster.is12:
            v10.save()
            v11.save()
            v12.save()
            h10.save()
            h11.save()
            h12.save()
    #pr.disable()
    #s = io.StringIO()
    #ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    #ps.print_stats()
    #print(s.getvalue())
