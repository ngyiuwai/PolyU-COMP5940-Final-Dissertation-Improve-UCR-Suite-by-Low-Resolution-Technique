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


# Declare variable/ define parameter for Low Resolution Data
# lowResData =  [
#                   [μ of this block],
#                   [σ of this block],
#                   [max of this block],
#                   [min of block]
#               ] where max & min are non-normalized data points
# lowResLen = number of data points represented by one block, which is also the minimun length of query
#   (assumption:   lowResLen >> k , where k stands for k-nearest neighbour)
lowResData = [[], [], [], []]
lowResLen = 16

###-----------------------------###

# Early abandon by lower resolution sequences #
# Loop 1        : Generate lower resolution sequences WITH overhead, which allows renormalization #
# Loop 2 to k   : Early abandon with lower resolution (which needs to be renormalized)
#
#   Final Product:  LB_LowResED
#
# How to use LB_LowResED?
# >   LB_LowResED is a modification of UCR Suite. It is one of the cascade lower bound.
#
# >     If we are interested in similarity search for Euclidean distance, we shall use lower bounds in below order.
#       ED:       LB_LowResED
#                 Then ED
#
# >     If we are interested in similarity search for DTW distance, we shall use lower bounds in below order.
#       DTW:      LB_Kim
#                 LB_LowResED (Given that LB_Keogh is a case-base ED)
#                 LB_Keogh
#                 Then LB_Keogh, DTW
#
#   In my report, I would interseted in the time needed for below.
#   i.e. compare
#       (1) Pass LB_Kim, Test LB_Keogh, and run DTW.                    [Raw UCR Suite]
#       (2) Pass LB_Kim, Test LB_LowResED, Test LB_Keogh, and run DTW.  [My research]
#   It is equivalent to measuring LB_Keogh is a problem Euclidean distance .
#   Hence, I will only test the usefulness of LB_LowResED for solving similarity search for Euclidean distance


# Read query and data
# For fair comparision, all query, metadata and raw data are loaded in memory.
scriptPath = os.path.dirname(__file__)
rawQuery = fileIO.readQuery(scriptPath)
data = fileIO.readData(scriptPath)


timeCount = 0

for n in range(0, len(rawQuery)):

    query = rawQuery[n]

    #   For ED, we create Low Resolution Quary
    #   For DTW, we create Low Resolution Query MBR
    #   This is a python program for ED. Hence, build low resolution query. Not MBR.
    #   Also note that quary is truncated to fit block length.
    #
    #   e.g.    len(query) = 52. len(block) = 10.
    #   then    len(query_truncated) = 50. len(query_lowRes) = 5.
    #
    #   The problems for comparing low resolution query and low resolution data are
    #   1)  Normalization of raw data is needed. But we have transformed it to low resolution block. CANNOT NORMALIZE DIRECTLY.
    #           * AND this problem is raised up by UCR paper.
    #   2)  Shifting window & truncation of query
    #           * We trucate the query.
    #           * Because distance(truncated_query, raw_data_truncated_lenght) < distance(query, raw_data_raw_lenght).
    #           * It is fine to use truncated_query as low bound.
    #           * Shifting window should be solve by UpperBound_Renormalization & LowerBound_Renormalization.
    #   Note that we are making block comparison. i.e.
    #       if (qi > si) then return (min(query_block_position_of_i) - max(sequence_block_position_of_i))
    #       if (qi < si) then return (max(query_block_position_of_i) - min(sequence_block_position_of_i))
    #
    #   Will solve problems in comparison in LB_LowResED. See note at there.

    # Normalize query and low resolution normalized query
    # lowResNormQuery =  [
    #                   [max of block],
    #                   [min of block]
    #               ]
    normQuery, queryMean, queryStd = normalization.forQuery(query, n)
    lowResNormQuery = normalization.forLowResQuery(normQuery, lowResLen, n)

    # Define best-so-far, as we are returning query distance < bsf
    # It is k-nearest neighor search, so bsf is initially set to INF.
    bsf = float("inf")
    print('query mean   =', queryMean)
    print('query std    =', queryStd)
    print('query len    =', len(query))
    print('best-so-far  =', bsf)
    print('kNN neighbor =', k)
    _, sortingOrder = sort.bubbleSort(normQuery)

    lowResNormQueryAbs = []
    for i in range(0, len(lowResNormQuery[0])):
        lowResNormQueryAbs.append(
            min(abs(lowResNormQuery[0][i]), abs(lowResNormQuery[1][i])))
    _, sortingOrderNorm = sort.bubbleSort(lowResNormQueryAbs)
    # print('ordering for ED     =', sortingOrder)
    # print('ordering for LB_LowResED     =', sortingOrderNorm)

    # Run ED

    input('Please Enter to run similarity search by UCR_ED')
    print('......', time.ctime(), ' start running UCR_ED ......')
    timeStart = time.time()

    match = []

    # 1st query:
    # NEED TO BUILD LOW RESOLUTION DATA
    if (n == 0):
        # First k subsequence are assume to be nearest neigbour.

        # Prepare sum of x and sum of x^2 for fast mean and std calculation.
        # 1st subsequence : Full computation
        subseq = data[0:len(query)]
        subSeqSum = 0
        subSeqSum2 = 0
        lowResblockCount = 0
        lowResblockSum = 0
        lowResblockSum2 = 0
        lowResblockMean = 0
        lowResblockStd = 0

        for i in range(0, len(query)):
            subSeqSum = subSeqSum + data[i]
            subSeqSum2 = subSeqSum2 + data[i]*data[i]
            subseqMean = subSeqSum / len(query)
            subseqStd = (subSeqSum2 / len(query) -
                         subseqMean * subseqMean) ** 0.5
            # Also calculate mean & sd of low resolution blocks, then save.
            lowResblockSum = lowResblockSum + data[i]
            lowResblockSum2 = lowResblockSum2 + data[i]*data[i]
            if ((i+1) % lowResLen == 0):
                lowResblockMean = lowResblockSum / lowResLen
                lowResblockStd = (lowResblockSum2 / lowResLen -
                                  lowResblockMean * lowResblockMean) ** 0.5
                lowResblockSum = 0
                lowResblockSum2 = 0
                lowResblockCount = lowResblockCount + 1
                lowResData[0].append(lowResblockMean)
                lowResData[1].append(lowResblockStd)
                lowResData[2].append(max(data[i+1-lowResLen:i+1]))
                lowResData[3].append(min(data[i+1-lowResLen:i+1]))

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
            subseqStd = (subSeqSum2 / len(query) -
                         subseqMean * subseqMean) ** 0.5
            # Also calculate mean & sd of low resolution blocks, then save.
            lowResblockSum = lowResblockSum + new
            lowResblockSum2 = lowResblockSum2 + new*new
            if ((len(query)+i+1) % lowResLen == 0):
                lowResblockMean = lowResblockSum / lowResLen
                lowResblockStd = (lowResblockSum2 / lowResLen -
                                  lowResblockMean * lowResblockMean) ** 0.5
                lowResblockSum = 0
                lowResblockSum2 = 0
                lowResblockCount = lowResblockCount + 1
                lowResData[0].append(lowResblockMean)
                lowResData[1].append(lowResblockStd)
                lowResData[2].append(
                    max(data[i+len(query)+1-lowResLen:i+len(query)+1]))
                lowResData[3].append(
                    min(data[i+len(query)+1-lowResLen:i+len(query)+1]))
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
            subseqStd = (subSeqSum2 / len(query) -
                         subseqMean * subseqMean) ** 0.5
            # Also normalize low resolution blocks, then save.
            lowResblockSum = lowResblockSum + new
            lowResblockSum2 = lowResblockSum2 + new*new
            if ((len(query)+i+1) % lowResLen == 0):
                lowResblockMean = lowResblockSum / lowResLen
                lowResblockStd = (lowResblockSum2 / lowResLen -
                                  lowResblockMean * lowResblockMean) ** 0.5
                lowResblockSum = 0
                lowResblockSum2 = 0
                lowResblockCount = lowResblockCount + 1
                lowResData[0].append(lowResblockMean)
                lowResData[1].append(lowResblockStd)
                lowResData[2].append(
                    max(data[i+len(query)+1-lowResLen:i+len(query)+1]))
                lowResData[3].append(
                    min(data[i+len(query)+1-lowResLen:i+len(query)+1]))
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

        print('Prune by LB_LowResED: N/A')
        print('kNN: ')
        print(match)
        print()

        '''
        # !!!!!----- Visualize Low Resolution Data. For testing & debugging. ----- !!!!!
        lowResData_MeanVector = []
        lowResData_StdVector = []
        lowResData_MaxVector = []
        lowResData_MinVector = []
        for i in range(0, lowResblockCount):
            for j in range(0, lowResLen):
                lowResData_MeanVector.append(lowResData[0][i])
                lowResData_MaxVector.append(lowResData[2][i])
                lowResData_MinVector.append(lowResData[3][i])

        plt.title('Raw Data')
        plt.plot(data, linewidth=1)
        plt.show()

        plt.title('Low Res Data')
        plt.plot(lowResData_MeanVector, linewidth=1)
        plt.plot(lowResData_MaxVector, linestyle='--', linewidth=0.5)
        plt.plot(lowResData_MinVector, linestyle='--', linewidth=0.5)
        plt.show()
        '''

        # Plot results
        if plotResult_Flag:
            for i in range(0, k):
                plt.plot(data[match[i][1]:match[i][1]+len(query)])
                plt.title(match[i][1])
                plt.show()

    #   2nd to k-th queries:
    #   USE LOW RESOLUTION AS LOWER BOUND

    else:

        # Now start comparsion. Exactly the same algorithm as 1st query, but we have low bound function LB_LowResED.

        # First k subsequence are assume to be nearest neigbour.

        # Prepare sum of x and sum of x^2 for fast mean and std calculation.
        # 1st subsequence : Full computation

        pruningCount = 0
        match = []

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
        # For 2nd to k-th, they are assumed to be the k-nearest. Will be replaced.
        for i in range(0, k-1):
            old = subseq.pop(0)
            new = data[i+len(query)]
            subseq.append(new)
            subSeqSum = subSeqSum - old + new
            subSeqSum2 = subSeqSum2 - old*old + new*new
            subseqMean = subSeqSum / len(query)
            subseqStd = (subSeqSum2 / len(query) -
                         subseqMean * subseqMean) ** 0.5
            dist = distance.squareEuclidean(
                normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
            match.append([dist, i+1])

        match.sort()

        positionFirstBlock = len(query) // lowResLen * lowResLen
        positionLastBlock = (len(data)-len(query)) // lowResLen * lowResLen

        # The initial k-nearest neigbout are set. Now replace these k-nearest neigbour if dist is shorter.
        # For k-th to [len(query) // lowResLen * lowResLen] , it is meaningless to use LB_LowResED.
        # It is because if a subsequence pass LB_LowResED, we will compute the euclidean distance for the next len(query) point.
        # It can avoid unneccesary full computing of mean & standard deviation (we skip mean/ sd computing if a point failed in LB_LowResED).
        # We can still take advantage from online update.
        bsf = match[k-1][0]

        for i in range(k-1, positionFirstBlock):
            old = subseq.pop(0)
            new = data[i+len(query)]
            subseq.append(new)
            subSeqSum = subSeqSum - old + new
            subSeqSum2 = subSeqSum2 - old*old + new*new
            subseqMean = subSeqSum / len(query)
            subseqStd = (subSeqSum2 / len(query) -
                         subseqMean * subseqMean) ** 0.5
            dist = distance.squareEuclidean(
                normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
            if (dist < float('inf')):
                replaced = match.pop()
                match.append([dist, i+1])
                match.sort()
                bsf = match[k-1][0]
                # print('Replacing #', replaced[1], ' by #', i)

        # For [len(query) // lowResLen * lowResLen] to [(len(data)-len(query)) // lowResLen * lowResLen], we will use LB_LowResED.
        i = positionFirstBlock
        while (i + len(query) < positionLastBlock):

            # LB_LowResED testing.
            #   Step 1: Renormalized SubSeq
            #   LB_LowResED can speed up the search by
            #    1)  Read/ Write low resolution data, but not raw data. Require less I/O.
            #    2)  Make less comparision
            #   Also note that length of low resolution subquence is one block longer than query, which allows renormalization.
            lowResED_Flag = True
            lowResSubSeqMax = []
            lowResSubSeqMin = []
            lowResSubSeqTruncatedSum = 0
            lowResSubSeqTruncatedSum2 = 0

            # Retrive low resolution sequence blocks
            for j in range(i // lowResLen, (i + len(query)) // lowResLen):
                lowResSubSeqTruncatedSum = (
                    lowResSubSeqTruncatedSum + lowResData[0][j] * lowResLen)
                lowResSubSeqTruncatedSum2 = (
                    lowResSubSeqTruncatedSum2 + (lowResData[1][j] * lowResData[1][j] + lowResData[0][j] * lowResData[0][j]) * lowResLen)
                lowResSubSeqMax.append(lowResData[2][j])
                lowResSubSeqMin.append(lowResData[3][j])

            # Renormalize using next block's max & min
            lowResSubSeqNextMax = lowResData[2][(i + len(query)) // lowResLen]
            lowResSubSeqNextMin = lowResData[3][(i + len(query)) // lowResLen]
            lowResSubSeqNextMax2 = max(
                lowResSubSeqNextMax*lowResSubSeqNextMax,
                lowResSubSeqNextMin*lowResSubSeqNextMin)
            lowResSubSeqNextMin2 = min(
                lowResSubSeqNextMax*lowResSubSeqNextMax,
                lowResSubSeqNextMin*lowResSubSeqNextMin)
            lowResSubSeqMeanMax = (lowResSubSeqTruncatedSum
                                   + lowResSubSeqNextMax * (len(query) % lowResLen)) / len(query)
            lowResSubSeqMeanMin = (lowResSubSeqTruncatedSum
                                   + lowResSubSeqNextMin * (len(query) % lowResLen)) / len(query)
            lowResSubSeqMeanMax2 = max(lowResSubSeqMeanMax*lowResSubSeqMeanMax,
                                       lowResSubSeqMeanMin*lowResSubSeqMeanMin)
            lowResSubSeqMeanMin2 = min(lowResSubSeqMeanMax*lowResSubSeqMeanMax,
                                       lowResSubSeqMeanMin*lowResSubSeqMeanMin)
            lowResSubSeqSDMax2 = (lowResSubSeqTruncatedSum2
                                  + lowResSubSeqNextMax2 * (len(query) % lowResLen)) / len(query) - lowResSubSeqMeanMin2
            lowResSubSeqSDMin2 = (lowResSubSeqTruncatedSum2
                                  + lowResSubSeqNextMin2 * (len(query) % lowResLen)) / len(query) - lowResSubSeqMeanMax2

            # Possible to generate roundinh error in complex number due to limitation of Python.
            # Remove such rounding error
            if (type(lowResSubSeqSDMax2) == complex):
                lowResSubSeqSDMax2 = float(lowResSubSeqSDMax2.real)
            if (type(lowResSubSeqSDMin2) == complex):
                lowResSubSeqSDMin2 = float(lowResSubSeqSDMin2.real)

            if (lowResSubSeqSDMax2 > 0):
                lowResSubSeqSDMax = lowResSubSeqSDMax2 ** 0.5
            else:
                lowResSubSeqSDMax = 0
            if (lowResSubSeqSDMin2 > 0):
                lowResSubSeqSDMin = lowResSubSeqSDMin2 ** 0.5
            else:
                lowResSubSeqSDMin = 0

            if (lowResSubSeqSDMin <= 0):
                # If minimum(true sd) = 0, then LB_LowResED is infinity. Flag should be false
                lowResED_Flag = False
            else:
                # If minimum(true sd) > 0, then we can renormalize subsequence.
                # We can obtain a upperbound/ lowerbound of normalized subsequence.
                #   lowResNormSubSeq[[Upper Bound of Subsequence], [Lower Bound of Subsequence]]
                lowResNormSubSeq = [[], []]
                for j in range(0, len(query) // lowResLen):
                    lowResNormSubSeqBound = [
                        (lowResSubSeqMax[j] -
                         lowResSubSeqMeanMax) / lowResSubSeqSDMax,
                        (lowResSubSeqMax[j] -
                         lowResSubSeqMeanMin) / lowResSubSeqSDMax,
                        (lowResSubSeqMax[j] -
                         lowResSubSeqMeanMax) / lowResSubSeqSDMin,
                        (lowResSubSeqMax[j] -
                         lowResSubSeqMeanMin) / lowResSubSeqSDMin,
                        (lowResSubSeqMin[j] -
                         lowResSubSeqMeanMax) / lowResSubSeqSDMax,
                        (lowResSubSeqMin[j] -
                         lowResSubSeqMeanMin) / lowResSubSeqSDMax,
                        (lowResSubSeqMin[j] -
                         lowResSubSeqMeanMax) / lowResSubSeqSDMin,
                        (lowResSubSeqMin[j] -
                         lowResSubSeqMeanMin) / lowResSubSeqSDMin
                    ]
                    lowResNormSubSeqBound.sort()
                    lowResNormSubSeq[0].append(lowResNormSubSeqBound[7])
                    lowResNormSubSeq[1].append(lowResNormSubSeqBound[0])

                #   Step 2: Compute LB_LowResEQ using lowResNormQuery & lowResNormSubSeq
                dist_LB_LowResED = distance.LB_LowResED(
                    lowResNormQuery, lowResNormSubSeq, lowResLen, sortingOrderNorm, bsf)
                if (dist_LB_LowResED < float('inf')):
                    lowResED_Flag = False

            '''
            # !!!!!----- Visualize Low Resolution Subsequence. For testing & debugging ----- !!!!!
            lowResSubSeq = [[], [], [], []]
            for j in range(i // lowResLen, (i + len(query)) // lowResLen):
                lowResSubSeq[0].append(lowResData[0][j])
                lowResSubSeq[1].append(lowResData[1][j])
                lowResSubSeq[2].append(lowResData[2][j])
                lowResSubSeq[3].append(lowResData[3][j])
            subseq = data[i: i + len(query)]
            lowResData_MeanVector = []
            lowResData_StdVector = []
            lowResData_MaxVector = []
            lowResData_MinVector = []
            for p in range(0, len(lowResSubSeq[0])):
                for q in range(0, lowResLen):
                    lowResData_MeanVector.append(lowResSubSeq[0][p])
                    lowResData_MaxVector.append(lowResSubSeq[2][p])
                    lowResData_MinVector.append(lowResSubSeq[3][p])
            plt.title('Low Resolution Subsequence at ' + str(i))
            plt.plot(subseq, linewidth=1, color='blue')
            # plt.plot(lowResData_MeanVector, linewidth=1, color='black')
            plt.plot(lowResData_MaxVector, linestyle='--',
                     linewidth=0.8, color='blue')
            plt.plot(lowResData_MinVector, linestyle='--',
                     linewidth=0.8, color='blue')
            plt.show()

            # !!!!!----- Visualize Normalized Low Resolution Subsequence. DELETE THIS PART AT FINAL PRODUCT ----- !!!!!
            if (lowResSubSeqSDMin != 0):
                lowResData_MaxVector = []
                lowResData_MinVector = []
                lowResQuery_MaxVector = []
                lowResQuery_MinVector = []
                for p in range(0, len(lowResNormQuery[0])):
                    for q in range(0, lowResLen):
                        lowResData_MaxVector.append(lowResNormSubSeq[0][p])
                        lowResData_MinVector.append(lowResNormSubSeq[1][p])
                        lowResQuery_MaxVector.append(lowResNormQuery[0][p])
                        lowResQuery_MinVector.append(lowResNormQuery[1][p])
                plt.title('Low Normalized Resolution Subsequence at ' + str(i))
                plt.plot(normQuery, linewidth=1, color='red')
                plt.plot(lowResQuery_MaxVector, linestyle='--',
                         linewidth=0.5, color='red')
                plt.plot(lowResQuery_MinVector, linestyle='--',
                         linewidth=0.5, color='red')
                plt.plot(lowResData_MaxVector, linestyle='--',
                         linewidth=0.8, color='blue')
                plt.plot(lowResData_MinVector, linestyle='--',
                         linewidth=0.8, color='blue')
                plt.show()
            '''

            if (lowResED_Flag):
                # If LB > bsf:
                #   Skip that block
                pruningCount = pruningCount + lowResLen
                i = i + lowResLen

            else:
                # If LB < bsf
                #   Compute mean and sd at first point of block begin
                #   Online update for the next len(query) // lowResLen * lowResLen points
                subseq = data[i: i + len(query)]
                subSeqSum = 0
                subSeqSum2 = 0
                for j in range(i, i + len(query)):
                    subSeqSum = subSeqSum + data[j]
                    subSeqSum2 = subSeqSum2 + data[j]*data[j]
                subseqMean = subSeqSum / len(query)
                subseqStd = (subSeqSum2 / len(query) -
                             subseqMean * subseqMean) ** 0.5

                dist = distance.squareEuclidean(
                    normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
                if (dist < float('inf')):
                    replaced = match.pop()
                    match.append([dist, i])
                    match.sort()
                    bsf = match[k-1][0]
                i = i + 1

                for j in range(1, len(query) // lowResLen * lowResLen):
                    old = subseq.pop(0)
                    new = data[i+len(query)-1]
                    subseq.append(new)
                    subSeqSum = subSeqSum - old + new
                    subSeqSum2 = subSeqSum2 - old*old + new*new
                    subseqMean = subSeqSum / len(query)
                    subseqStd = (subSeqSum2 / len(query) -
                                 subseqMean * subseqMean) ** 0.5
                    dist = distance.squareEuclidean(
                        normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
                    if (dist < float('inf')):
                        replaced = match.pop()
                        match.append([dist, i])
                        match.sort()
                        bsf = match[k-1][0]
                        # print('Replacing #', replaced[1], ' by #', i)
                    i = i + 1

         # For [(len(data)-len(query)) // lowResLen * lowResLen], we will use compute mean and sd again.
         # It is after final block. Cannot use LB_LowResED. Need full computation.
        subseq = data[positionLastBlock: positionLastBlock + len(query)]
        subSeqSum = 0
        subSeqSum2 = 0
        for i in range(positionLastBlock, positionLastBlock + len(query)):
            subSeqSum = subSeqSum + data[i]
            subSeqSum2 = subSeqSum2 + data[i]*data[i]
        subseqMean = subSeqSum / len(query)
        subseqStd = (subSeqSum2 / len(query) - subseqMean * subseqMean) ** 0.5

        dist = distance.squareEuclidean(
            normQuery, subseq, subseqMean, subseqStd, sortingOrder, bsf)
        if (dist < float('inf')):
            replaced = match.pop()
            match.append([dist, i])
            match.sort()
            bsf = match[k-1][0]

        # For [(len(data)-len(query)) // lowResLen * lowResLen] to ending, we will use online update.
        for i in range(positionLastBlock + len(query) + 1, len(data)-len(query)):
            old = subseq.pop(0)
            new = data[i+len(query)]
            subseq.append(new)
            subSeqSum = subSeqSum - old + new
            subSeqSum2 = subSeqSum2 - old*old + new*new
            subseqMean = subSeqSum / len(query)
            subseqStd = (subSeqSum2 / len(query) -
                         subseqMean * subseqMean) ** 0.5
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

        print('Prune by LB_LowResED:', pruningCount / len(data))
        print('kNN: ')
        print(match)
        print()

        # Plot results
        if plotResult_Flag:
            for i in range(0, k):
                plt.plot(data[match[i][1]:match[i][1]+len(query)])
                plt.title(match[i][1])
                plt.show()

print('> Total time for answering ', len(rawQuery),
      "query(s) is ", timeCount, 'seconds.')
