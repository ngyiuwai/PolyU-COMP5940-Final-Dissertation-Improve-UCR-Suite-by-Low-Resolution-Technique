from _modules import distance
from _modules import fileIO
from _modules import normalization
from _modules import sort
import os
import time
import json
import matplotlib.pyplot as plt

###---Setting Global Variable---###

# Search for how many nearest neighbour?
k = 3

# Plot result?
plotResult_Flag = False

###-----------------------------###

# Simply repeating Euclidean Distance #
# Experiment Control Group #


# Read query and data
# For fair comparision, ALL query, metadata and raw data are loaded in memory.
scriptPath = os.path.dirname(__file__)
rawQuery = fileIO.readQuery(scriptPath)
data = fileIO.readData(scriptPath)


timeCount = 0

for n in range(0, len(rawQuery)):

    query = rawQuery[n]

    # Normalize query
    normQuery, queryMean, queryStd = normalization.forQuery(query, n)

    # Define best-so-far, as we are returning query distance < bsf
    # It is k-nearest neighor seacrch, so bsf is initially set to INF.
    bsf = float("inf")
    print('query mean   =', queryMean)
    print('query std    =', queryStd)
    print('query len    =', len(query))
    print('best-so-far  =', bsf)
    print('kNN neighbor =', k)
    _, sortingOrder = sort.bubbleSort(normQuery)
    # print('ordering     =', sortingOrder)

    # Run ED

    input('Please Enter to run similarity search by UCR_ED')
    print('......', time.ctime(), ' start running UCR_ED ......')
    timeStart = time.time()

    match = []

    # First k subsequence are assume to be nearest neigbour.

    # Prepare sum of x and sum of x^2 for fast mean and std calculation.
    # 1st subsequence : Full computation
    subseq = data[0:len(query)]
    subSeqSum = 0
    subSeqSum2 = 0
    for i in range(0, len(query)):
        subSeqSum = subSeqSum + data[i]
        subSeqSum2 = subSeqSum2 + data[i]*data[i]
    subseqMean = subSeqSum / len(query)
    subseqStd = (subSeqSum2 / len(query) - subseqMean * subseqMean) ** 0.5
    dist = distance.squareEuclidean(
        normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
    match.append([dist, i])

    # 2nd to len(query) subsequence : Online update
    for i in range(0, k-1):
        old = subseq.pop(0)
        new = data[i+len(query)]
        subseq.append(new)
        subSeqSum = subSeqSum - old + new
        subSeqSum2 = subSeqSum2 - old*old + new*new
        subseqMean = subSeqSum / len(query)
        subseqStd = (subSeqSum2 / len(query) - subseqMean * subseqMean) ** 0.5
        dist = distance.squareEuclidean(
            normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
        match.append([dist, i+1])

    match.sort()

    # Replace k-nearest neigbour if dist is shorter.
    bsf = match[k-1][0]

    for i in range(k-1, len(data)-len(query)):
        old = subseq.pop(0)
        new = data[i+len(query)]
        subseq.append(new)
        subSeqSum = subSeqSum - old + new
        subSeqSum2 = subSeqSum2 - old*old + new*new
        subseqMean = subSeqSum / len(query)
        subseqStd = (subSeqSum2 / len(query) - subseqMean * subseqMean) ** 0.5
        dist = distance.squareEuclidean(
            normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
        if (dist < float('inf')):
            replaced = match.pop()
            match.append([dist, i+1])
            match.sort()
            bsf = match[k-1][0]
            # print('Replacing #', replaced[1], ' by #', i)

    timeEnd = time.time()
    print('......', time.ctime(), ' finish running UCR_ED ......')
    print('...... Processing time: ', timeEnd - timeStart)
    timeCount = timeCount + timeEnd - timeStart

    print('kNN: ')
    print(match)
    print()
    print()

    # Plot results
    if plotResult_Flag:
        for i in range(0, k):
            plt.plot(data[match[i][1]:match[i][1]+len(query)])
            plt.title(match[i][1])
            plt.show()

print('> Total time for answering ', len(rawQuery),
      "query(s) is ", timeCount, 'seconds.')
