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
        if cluster.household_set.count() > 9:
            return True
        else:
            False

def getDistanceToCluster(point, cluster):
    maxDist = 0
    set = cluster.household_set.all()
    for elem in set:
        dist = custom_dist((point.latitude, point.longitude), (elem.latitude, elem.longitude))
        maxDist = max(dist, maxDist)
    return maxDist

def balance_clusters(datapoints, clusters):
    while clustersHaveWrongSize(clusters):
        currentMinDistance = 10000000000
        currentSrcElem = None
        currentDstCluster = None

        for point in datapoints:
            if point.cluster.household_set.count() > 9:
                pointCurrMinDist = 1000000000
                pointCurrDstClust = None
                for cluster in clusters:
                    if cluster.household_set.count() < 9:
                        dist = getDistanceToCluster(point, cluster)
                        if dist < pointCurrMinDist:
                            pointCurrMinDist = dist
                            pointCurrDstClust = cluster
                if pointCurrMinDist < currentMinDistance:
                    currentMinDistance = pointCurrMinDist
                    currentDstCluster = pointCurrDstClust
                    currentSrcElem = point

        currentSrcElem.cluster = currentDstCluster
        currentSrcElem.save()
