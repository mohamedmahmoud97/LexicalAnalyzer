from LexicalAnalyzer.StateNode import StateNode


def convertRE(rule):
    startOfRule = True
    global currentState  # globally declared to be accessible in the next below for loop

    if (rule[0] == '['):  # if first char is [ so it's punctuation
        for char in range(1, len(rule)):
            print(currentState)
            print("Heyeyeyyeyeyeyeyyeye")
            if (rule[char] != '' and rule[char] != '\\' and rule[char] != ']' and
                        rule[char].isalpha() == False):
                currentState = StateNode()
                nextState = StateNode()

                startState.next.append(
                    currentState)  # adding start state link to each punct as each one is a path or rule
                currentState.setInput("\L")

                currentState.next.append(nextState)
                nextState.setIsAccepted(True)
                nextState.setInput(rule[char])

                currentState = nextState  # swap nextState to cuurState to be reused in the next itiration


            elif (char != '' and char == '\\'):
                continue

            elif (rule[char] == ' '):  # if it's a space
                continue

            else:  # if anything else it should print an error at the wrong char
                print(rule + "\n")
                for x in range(char):
                    if (x == char):
                        print("^")
                    print(" ")

                print("Error at this char/s")


    elif (rule[0] == '{'):  # if first char is { so it's reserved symbols
        for char in range(1, len(rule)):
            if (rule[char] != '' and rule[char] != '}' and
                        rule[char].isalpha() == True):  # must be reserved word with all chars alpha

                currentState = StateNode(rule[char])
                nextState = StateNode()

                if (startOfRule == True):
                    startState.next.append(
                        currentState)  # adding start state link to each punct as each one is a path or rule
                    currentState.setInput("\L")
                    startOfRule = False

                currentState.next.append(nextState)
                nextState.setInput(rule[char])

                if (rule[char + 1].isalpha() == False):
                    nextState.setIsAccepted(True)
                    startOfRule = True

                currentState = nextState  # swap nextState to cuurState to be reused in the next itiration

            elif (rule[char] == ' '):  # if it's a space
                continue

            else:
                print(rule + "\n")  # if anything else it should print an error at the wrong char
                for x in range(char):
                    if (x == char):
                        print("^")
                    print(" ")

                print("Error at this char/s")

    elif (rule[0].isalpha() == True):  # if first char is a char so it's a regular expression
        pass


f = open("lexicalRules", "r")

rule = f.readline()
if (rule != ''):
    print(rule)
    startState = StateNode()
    convertRE(rule)

print(StateNode.nodesDictionary)
