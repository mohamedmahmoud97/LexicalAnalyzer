class StateNode:
    nodesCount = 0
    nodesDictionary = {}

    def __init__(self):
        self.label = self.nodesCount
        self.input = ''
        self.nodesDictionary[self.nodesCount] = self
        self.nodesCount = self.nodesCount + 1  # here there is a counter on the nodes
        self.next = []  # here the node will have a list of next nodes
        self.isAccepted = False

    def __init__(self, input):
        self.label = self.nodesCount
        self.input = input
        self.nodesDictionary[self.nodesCount] = self
        self.nodesCount = self.nodesCount + 1  # here there is a counter on the nodes
        self.next = []  # here the node will have a list of next nodes
        self.isAccepted = False

    def getLabel(self):
        return self.label

    def getInput(self):
        return self.input

    def setInput(self, input):
        self.input = input

    def getNodesList(self):
        return self.nodesDictionary

    def setIsAccepted(self, boolen):
        self.isAccepted = boolen

    def getIsAccepted(self):
        return self.isAccepted
