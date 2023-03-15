import hou


def getClickStates(kwargs: dict):
    shiftclick = kwargs["shiftclick"] if ("shiftclick" in kwargs) else False
    ctrlclick = kwargs["ctrlclick"] if ("ctrlclick" in kwargs) else False
    return (shiftclick, ctrlclick)


def getSelectedNodes():
    selectedNodes = hou.selectedNodes()

    if len(selectedNodes) == 0:
        raise hou.Error("Please select a node.")

    return selectedNodes

def getSingleSelectedNode():
    selectedNodes = hou.selectedNodes()

    if len(selectedNodes) == 0:
        raise hou.Error("Please select a node.")
    elif len(selectedNodes) > 1:
        raise hou.Error("Please select no more than 1 node.")

    return selectedNodes[0]

# String Manipulation
# -----------------------------------------------------------------------------
def safeCapitalize(s):
    if len(s) <= 1:
        return s.capitalize()
    else:
        first = s[0].capitalize()
        return first + s[1:]


def snakeCaseToSpaced(s: str):
    words = s.split("_")
    words = list(map(safeCapitalize, words))
    return " ".join(words)
