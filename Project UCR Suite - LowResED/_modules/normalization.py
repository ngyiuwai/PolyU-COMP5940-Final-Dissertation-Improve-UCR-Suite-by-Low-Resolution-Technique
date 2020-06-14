"""
This module is for normalize queries.
Functions:  forQuery(query) --> (normalzied query, query mean, query standard deviation)
            forLowResQuery(query) --> (normalzied low resolution query upperbound, normalzied low resolution query lowerbound)
"""


import matplotlib.pyplot as plt


def forQuery(query: list, n: int):
    """
    This function is for normalize the query.
    ================================================================
    Input:
      query: [], unnormalized query
      n:     int, query number
    Output:
      normQuery: [], normalized query
      queryMean: float, mean of query
      queryStd : float, standard deviation of query
    """
    queryMean = sum(query) / len(query)
    queryStd = 0
    for i in range(0, len(query)):
        queryStd = queryStd + query[i]*query[i]
    queryStd = (queryStd/len(query) - queryMean*queryMean) ** 0.5

    normQuery = []
    for i in range(0, len(query)):
        normQuery.append((query[i] - queryMean) / queryStd)

    plt.plot(normQuery)
    plt.title('Normalized Query #' + str(n + 1))
    plt.show()

    return (normQuery, queryMean, queryStd)


def forLowResQuery(normQuery: list, lowResLen: int, n: int):
    """
    This function is for finding low resolution upper bound and lower bound of normalized query.
    ================================================================
    Input:
      normQuery:  [], normalized query
      lowResLen:  int, length of low resolution block
      n:          int, query number
    Output:
      lowResNormQuery: [[max of normalized block], [min of normalized block]]
    """
    lowResNormQuery = [[], []]
    for i in range(0, len(normQuery) // lowResLen):
        lowResNormQuery[0].append(max(normQuery[i*lowResLen:(i+1)*lowResLen]))
        lowResNormQuery[1].append(min(normQuery[i*lowResLen:(i+1)*lowResLen]))

    lowResNormQuery_MaxVector = []
    lowResNormQuery_MinVector = []
    for i in range(0, len(normQuery) // lowResLen):
        for j in range(0, lowResLen):
            lowResNormQuery_MaxVector.append(lowResNormQuery[0][i])
            lowResNormQuery_MinVector.append(lowResNormQuery[1][i])
    plt.title('Normalized Query' + str(n + 1) + ' with Low Resolution Bounds')
    plt.plot(normQuery, linewidth=1)
    plt.plot(lowResNormQuery_MaxVector, linestyle='--', linewidth=0.5)
    plt.plot(lowResNormQuery_MinVector, linestyle='--', linewidth=0.5)
    plt.show()

    return lowResNormQuery
