import hou
import re
import dabinUtils as utils


class PromoteParms:
    def __init__(self, nodes):
        self.nodes = nodes
        self.node = nodes[0]

        self.parmNames = ["t", "r", "s"]
        self.parmDims = ["X", "Y", "Z"]

    def modifyName(self, parmName, nodeName):
        return nodeName + "_" + parmName

    def countLockedParms(self, parmTuple):
        count = 0
        for parm in parmTuple:
            count += 1 if parm.isLocked() else 0
        return count

    def getParmLabel(self, parmTupleTemp, i):
        return parmTupleTemp.label() + " " + self.parmDims[i]

    def appendParmTemplate(
        self, parmTempGroup, parmTemp: hou.FloatParmTemplate, groupName
    ):
        parmTemp.setName(self.modifyName(parmTemp.name(), self.node.name()))
        parmTemp.setLabel(groupName + " " + parmTemp.label())
        # Remove conditionals
        parmTemp.setConditional(hou.parmCondType.DisableWhen, "")
        # Update parameter template group
        parmTempGroup.append(parmTemp)

    def promoteRigParms(self):
        hdadef = self.node.parent().type().definition()
        parmTempGroup = hdadef.parmTemplateGroup()

        iGroups = self.node.parm("transformations").eval()

        # Append Parameters to HDA
        # ----------------------------------------------------------------------
        for i in range(iGroups):  # over groups
            si = str(i)
            group = self.node.parm("group" + si)
            groupName = re.sub("_group", "", group.alias())
            groupName = utils.snakeCaseToSpaced(groupName)

            for parmName in self.parmNames:  # over parameters rows
                parmTuple: hou.ParmTuple = self.node.parmTuple(parmName + si)
                lockCount = self.countLockedParms(parmTuple)

                parmTupleTemp = parmTuple.parmTemplate()
                if lockCount == 0:  # Promote as tuple
                    parmTupleTemp.setDefaultValue(parmTuple.eval())
                    self.appendParmTemplate(parmTempGroup, parmTupleTemp, groupName)
                elif lockCount < 3:  # Promote each parm
                    for i, parm in enumerate(parmTuple):  # over parameter cells
                        if parm.isLocked():
                            continue
                        parmTemp = hou.FloatParmTemplate(
                            parm.name(), self.getParmLabel(parmTupleTemp, i), 1
                        )
                        parmTemp.setMinValue(-1)
                        parmTemp.setMaxValue(1)
                        parmTemp.setDefaultValue((parm.eval(),))
                        self.appendParmTemplate(parmTempGroup, parmTemp, groupName)

        # Update definition
        hdadef.setParmTemplateGroup(parmTempGroup, rename_conflicting_parms=True)

        # Link parameters to original parameters
        # ----------------------------------------------------------------------
        for i in range(iGroups):  # over groups
            si = str(i)

            for parmName in self.parmNames:  # over parameter rows
                parmTuple = self.node.parmTuple(parmName + si)
                # Set links
                for parm in parmTuple:  # over parameter cells
                    if parm.isLocked():
                        continue
                    name = self.modifyName(parm.name(), self.node.name())
                    parm.setExpression(f'ch("../{name}")')
