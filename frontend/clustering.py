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
    for i in range(len(tmp)):
        datapoints[i].cluster.add(clusters[tmp[i] - 1])

def clustersHaveWrongSize(clusterSizes):
    for e in clusterSizes:
        if e > 9:
            return True
    return False

def getDistanceToCluster(point, clusterNum, datapoints):
    maxDist = 0
    for e in datapoints:
        if e.cluster == (clusterNum + 1):
            dist = custom_dist((point.latitude, point.longitude), (e.latitude, e.longitude))
            if dist > maxDist:
                maxDist = dist
    return maxDist

def balance_clusters(datapoints):
    clusterSizes = []
    numOfClusters = len(datapoints) // 9
    for i in range(numOfClusters):
        clusterSizes.append(0)
    for e in datapoints:
        clusterSizes[e.cluster - 1] += 1
    #print(clusterSizes)

    while clustersHaveWrongSize(clusterSizes):
        currentMinDistance = 10000000000
        currentSrcElem = -1
        currentDstCluster = -1

        for pointi in range(len(datapoints)):
            point = datapoints[pointi]
            if clusterSizes[point.cluster - 1] > 9:
                pointCurrMinDist = 100000000
                pointCurrDstClust = -1
                for i in range(numOfClusters):
                    if clusterSizes[i] < 9:
                        dist = getDistanceToCluster(point, i, datapoints)
                        if dist < pointCurrMinDist:
                            pointCurrMinDist = dist
                            pointCurrDstClust = i
                if pointCurrMinDist < currentMinDistance:
                    currentMinDistance = pointCurrMinDist
                    currentDstCluster = pointCurrDstClust
                    currentSrcElem = pointi

        currCluster = datapoints[currentSrcElem].cluster
        clusterSizes[currCluster - 1] -= 1
        clusterSizes[currentDstCluster] += 1
        datapoints[currentSrcElem].cluster = currentDstCluster + 1
        #print("Moving datapoint", currentSrcElem, "from", currCluster - 1, "to", currentDstCluster + 1)
        #print(clusterSizes)
    #print(clusterSizes)