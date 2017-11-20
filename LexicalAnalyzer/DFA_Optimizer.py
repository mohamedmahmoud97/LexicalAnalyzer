def minimizeDFA(startState, F, S):
    partitionII = []
    S_ = []
    inputs = []

    # This will get all inputs and put it in a list to be reused in partitioning
    # To do: iterate on all next states of each state
    for x in S:
        if S.__getitem__(x) not in inputs:
            inputs.append(S.__getitem__(x))
            print(S.__getitem__(x))
    print(len(S))
    print(inputs, "<-- inputs")
    # This will put non-accepting states in a list called S_ skipping the first state '0'
    for x in iter(S):
        if x not in F:  # if the state not in the F states so add it to S-F states
            S_.append(x)

    # We will make an initial partition with two groups of accepting states F and non-accepting states S_
    partitionII.append(F)
    partitionII.append(S_)
    print(partitionII)
    # Here we will make a while loop to get the new partition after partitioning process and iterating on all G group in each partition
    print(len(inputs), "<-inputs")
    partitionIInew = []
    while (True):
        print(partitionII, "<----should be shit here bardo")
        print(partitionIInew, "<----should be shit here bardo")
        tempList = []
        print(len(partitionII), "<- Partition Length")
        # Here we will iterate on each G group in the partition
        for x in range(len(partitionII)):
            G = partitionII[x]
            G_ = []
            print(x, "<- Group No.")
            print(len(G), "<- Group Length\\", G, "<- Group Content")

            # Here we will iterate on each state in G with all the inputs to compare state s and t, where s is G[0] and t is G[y]
            if len(G) == 1:
                G_.append(G[0])
                partitionIInew.append(G_)
                print("Break")
                continue  # if the G group has only one state so break from this loop

            for y in iter(G):  # Here we will iterate on states in G

                isDistinguishable = False
                for z in range(len(inputs) - 1):  # Here we will iterate on all inputs of

                    outputX, inputX = S.get(G[0])[z]  # to get the input and output of each input z in s
                    outputY, inputY = S.get(G[y])[z]  # to get the input and output of each input z in t
                    print("X:", outputX, "Y:", outputY)
                    if outputX != outputY and (outputY not in G):
                        # tempList.append(y)
                        # print(tempList , "<-- TempList")
                        isDistinguishable = True
                        # elif (y not in G_):
                        #    G_.append(
                        #        y)  # if it's not distinguishable so add it to G_ which will be added to partitionIInew

                if (isDistinguishable == False):
                    G_.append(y)
                else:
                    tempList.append(y)

                print(G_, "<-- New Group_")

            partitionIInew.append(G_)  # add list G_ to partitionIInew
            print(partitionIInew, "<-- New Partition")

        # we want to put the tempList in the partitionIInew at last step
        partitionIInew.append(tempList)
        print(partitionIInew, "<-- Now PartitionIInew is like this")

        if partitionIInew == partitionII:
            partitionII = partitionIInew
            break
        else:
            partitionII = partitionIInew
            print(partitionII, "<-- Now partitionII is like this")
            partitionIInew.clear()

    # Here we create the dictionary for all states to identify each representative
    repDict = {}

    for x in range(len(partitionII)):
        if len(partitionII[x]) < 2:
            repDict.update({partitionII[x][0]: partitionII[x][0]})
        else:
            for y in iter(partitionII[x]):
                repDict.update({partitionII[x][y]: partitionII[x][0]})

    # Now we should replace each state with its representative in the dict S the old one which contains all the states
    for x in S:
        for y in S.get(x):
            print(S.get(x), "<--Sex", y)
            outputX, inputX = S.get(x, y)
            print(outputX, "OutX", inputX, "InX")
            repState = repDict.get(outputX)
            lst = list(S.get(x,y))
            lst[0] = repState
            lst[1] = inputX
            S.get(x)[y] = tuple(lst)
            # X= tuple(lst)
            print(X, "<------TUPLE")
    return S


startStates, fStates, sStates = (
    0
    ,
    [
        4
    ]
    ,
    {0: [
        (1, 'a'),
        (2, 'b')
    ],
        1: [
            (1, 'a'),
            (3, 'b')
        ],
        2: [
            (1, 'a'),
            (2, 'b')
        ],
        3: [
            (1, 'a'),
            (4, 'b')
        ],
        4: [
            (1, 'a'),
            (2, 'b')
        ]
    }
)

minimizeDFA(startStates, fStates, sStates)
print("##### End #####")
#print(sStates)
