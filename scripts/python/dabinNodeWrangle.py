import hou
from typing import Union


class DabinNodeWrangle:
    def __init__(self, nodes):
        self.nodes: list[hou.Node] = nodes

    # Moving Nodes
    # ------------------------------------------------------------------------
    def shiftNodes(self, up: float, right: float):
        for n in self.nodes:
            pos: hou.Vector2 = n.position()
            n.setPosition(hou.Vector2([pos[0] + right, pos[1] + up]))

    # Aligning Nodes
    # ------------------------------------------------------------------------
    def verticalAlign(self, pivot=0):
        """ Align nodes vertically
        Parameters:
        pivot: 0: Oldest, 1: youngest
        """
        if pivot == 0:
            pivotNode = self.getOldestNode()
        else:
            pivotNode = self.getYoungestNode()
        if pivotNode is None:
            raise hou.Error("no pivot node was found.")
            return
        pivotPos = pivotNode.position()
        for n in self.nodes:
            pos: hou.Vector2 = n.position()
            n.setPosition(hou.Vector2([pivotPos[0], pos[1]]))

    def horizontalAlign(self, pivot=0):
        """ Align nodes horizontally
        Parameters:
        pivot: 0: Farthest Left, 1: Farthest Right
        """
        if pivot == 0:
            pivotNode = self.getFarthestLeftNode()
        else:
            pivotNode = self.getFarthestRightNode()
        if pivotNode is None: 
            raise hou.Error("no pivot node was found.")    
            return
        pivotPos: hou.Vector2 = pivotNode.position()
        for n in self.nodes:
            pos: hou.Vector2 = n.position()
            n.setPosition(hou.Vector2([pos[0], pivotPos[1]]))

    # Fetching Nodes
    # ------------------------------------------------------------------------
    def getFarthestLeftNode(self):
        minX = 1000000
        selected = None
        for n in self.nodes:
            posX = n.position()[0]
            if posX < minX:
                minX = posX
                selected = n
        return selected

    def getFarthestRightNode(self):
        maxX = -1000000
        selected = None
        for n in self.nodes:
            posX = n.position()[0]
            if posX > maxX:
                maxX = posX
                selected = n
        return selected

    def getYoungestNode(self):
        maxParents = -1
        selected = None
        for n in self.nodes:
            parents = []
            self.getMainLineNodes(n, parents)
            nParents = len(parents)
            if nParents > maxParents:
                maxParents = nParents
                selected = n
        return selected

    def getOldestNode(self) -> Union[hou.Node, None]:
        minNParents = 10000
        selected = None
        for n in self.nodes:
            parents = []
            self.getMainLineNodes(n, parents)
            nParents = len(parents)
            if nParents < minNParents:
                minNParents = nParents
                selected = n
        return selected

    def getMainLineNodes(self, itNode, parents):
        parents.append(itNode.name())
        inputs = itNode.inputs()
        if len(inputs) > 0 and inputs[0] is not None:
            self.getMainLineNodes(inputs[0], parents)
