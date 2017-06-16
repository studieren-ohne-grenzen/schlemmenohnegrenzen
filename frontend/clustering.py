from scipy.cluster.hierarchy import linkage, fcluster
from geopy.distance import vincenty
import cProfile, pstats, io
from operator import itemgetter
from frontend.models import Household, Cluster, VisitingGroup

def custom_dist(x, y):
    return vincenty(x, y).m

def initial_clusters(datapoints, clusters):
    listOfCoords = []
    print(len(datapoints))
    numOfClusters = len(datapoints) // 9
    for elem in datapoints:
        listOfCoords.append([elem.latitude, elem.longitude])
    z = linkage(listOfCoords, method='complete', metric=custom_dist)
    tmp = fcluster(z, numOfClusters, criterion='maxclust')
    numOfClusters = len(datapoints) // 9
    for i in range(len(tmp)):
        datapoints[i].cluster = clusters[tmp[i] - 1]
        datapoints[i].save()

def clustersHaveWrongSize(clusters):
    for cluster in clusters:
        if cluster["size"] > 9:
            return True
        else:
            False

def getDistanceToCluster(point, cluster, set):
    maxDist = 0.0
    for elem in set:
        dist = custom_dist((point["latitude"], point["longitude"]), (elem["latitude"], elem["longitude"]))
        maxDist = max(dist, maxDist)
    return maxDist

def balance_clusters(datapoints, clusters):
    new_clusters = []
    new_households = []
    for cluster in clusters:
        elems = cluster.household_set.all()
        for e in elems:
            new_households.append({"longitude": e.longitude, "latitude": e.latitude, "id": e.id, "cluster": len(new_clusters)})
        new_clusters.append({"size": len(elems), "clusterNum": cluster.clusterNum})

    while clustersHaveWrongSize(new_clusters):
        currentMinDistance = 10000000000
        currentSrcElem = None
        currentDstCluster = None

        for point in new_households:
            if new_clusters[point["cluster"]]["size"] > 9:
                pointCurrMinDist = 1000000000
                pointCurrDstClust = None
                for c in range(len(new_clusters)):
                    if new_clusters[c]["size"] < 9:
                        set = []
                        for p in new_households:
                            if p["cluster"] == c:
                                set.append(p)
                        dist = getDistanceToCluster(point, cluster, set)
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

def get_score(households, elems, dist, norm):
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

def recur(households, curr_elems, curr_score, dist, norm):
    curr_elems.append(-1)
    for i in range(9):
        if i not in curr_elems:
            curr_elems[-1] = i
            if len(curr_elems) < 9:
                recur(households, curr_elems, curr_score, dist, norm)
            else:
                score = get_score(households, curr_elems, dist, norm)
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

        recur(households, [], currscore, dist, maxdist * 27.0)
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
        
        h1.puzzle = 91;
        h2.puzzle = 92;
        h3.puzzle = 93;
        h4.puzzle = 94;
        h5.puzzle = 95;
        h6.puzzle = 96;
        h7.puzzle = 97;
        h8.puzzle = 98;
        h9.puzzle = 99;

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
    #pr.disable()
    #s = io.StringIO()
    #ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    #ps.print_stats()
    #print(s.getvalue())
