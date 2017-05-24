from scipy.cluster.hierarchy import linkage, fcluster
from geopy.distance import vincenty

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
