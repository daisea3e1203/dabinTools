import hou


def getClickStates(kwargs: dict):
    shiftclick = kwargs["shiftclick"] if ("shiftclick" in kwargs) else False
    ctrlclick = kwargs["ctrlclick"] if ("ctrlclick" in kwargs) else False
    return (shiftclick, ctrlclick)


def getSelectedNodes():
    selectedNodes = hou.selectedNodes()

    if len(selectedNodes) == 0:
        hou.ui.displayMessage("Please select a node.")
        return None

    return selectedNodes


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
