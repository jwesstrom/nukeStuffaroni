import nuke



nuke.knobDefault('Roto.output','alpha')
nuke.knobDefault('Blur.label','[value size]')
nuke.knobDefault('Dilate.label','[value size]')
nuke.knobDefault('Dilate.label','[value size]')
nuke.knobDefault('TimeOffset.label','[value time_offset]')
nuke.knobDefault('Tracker4.label','[value reference_frame]')
nuke.knobDefault('TimeWarp.label','[value filter]')
nuke.knobDefault('Retime.label','[value filter]')
nuke.knobDefault('PostageStamp.tile_color', '4278190335')
nuke.knobDefault('Write.jpeg._jpeg_quality', '.9')
nuke.knobDefault("Write.jpeg._jpeg_sub_sampling", "4:4:4")
nuke.knobDefault("RotoPaint.toolbox", '''clone {
{ brush ltt 0 h 1}
{ clone ltt 0 h 0 opc 0.01 }
{ blur ltt 0}
{ sharpen ltt 0}
{ smear ltt 0}
{ eraser ltt 0}
{ reveal ltt 0}
{ dodge ltt 0}
{ burn ltt 0}
}''')
nuke.knobDefault('Grid.number', '10 {number.0/(width/height)}')

######################################################################################################################################################
######################################################################################################################################################
def Stencil():
    Stencil = nuke.createNode('Merge2')
    Stencil.knob('operation').setValue('stencil')
nuke.menu("Nodes").addCommand("Merge/Merges/Stencil", "Stencil()", icon = "Merge.png")

def DifferenceMerge():
    DifferenceMerge = nuke.createNode('Merge2')
    DifferenceMerge.knob('operation').setValue('difference')
nuke.menu("Nodes").addCommand("Merge/Merges/differenceMerge", "DifferenceMerge()", icon = "Merge.png")

def Mask():
    Mask = nuke.createNode('Merge2')
    Mask.knob('operation').setValue('mask')
nuke.menu("Nodes").addCommand("Merge/Merges/Mask", "Mask()", icon = "Merge.png")

def From():
    Mask = nuke.createNode('Merge2')
    Mask.knob('operation').setValue('from')
nuke.menu("Nodes").addCommand("Merge/Merges/From", "From()", icon = "Merge.png")

def Divide():
    Mask = nuke.createNode('Merge2')
    Mask.knob('operation').setValue('divide')
nuke.menu("Nodes").addCommand("Merge/Merges/Divide", "Divide()", icon = "Merge.png")



######################################################################################################################################################
######################################################################################################################################################
def FrameHoldCurFrame():
    fh = nuke.thisNode()
    fh.knob('first_frame').setValue(nuke.frame())
 
nuke.addOnUserCreate(FrameHoldCurFrame, nodeClass='FrameHold')
######################################################################################################################################################
######################################################################################################################################################

######################################################################################################################################################
######################################################################################################################################################
def updateFrameRange():

    for readNodes in nuke.selectedNodes():

        name = readNodes.knob('file').getValue().split('/')[-1].split('%')[0]
        fileType = readNodes.knob('file').getValue().split('/')[-1].split('.')[-1]
        path = '/'.join(readNodes.knob('file').getValue().split('/')[:-1])+'/'
        fRange = ''

        for frameNumbers in nuke.getFileNameList(path):
            if name in frameNumbers:
                if fileType in frameNumbers:
                    fRange = frameNumbers.split(' ')[-1]
        readNodes.knob('first').setValue(int(fRange.split('-')[0]))
        readNodes.knob('last').setValue(int(fRange.split('-')[1]))
        readNodes.knob('origfirst').setValue(int(fRange.split('-')[0]))
        readNodes.knob('origlast').setValue(int(fRange.split('-')[1]))


nuke.menu('Nuke').addMenu('Script').addCommand( 'Update frame range', 'updateFrameRange()', "Shift+g")
######################################################################################################################################################
######################################################################################################################################################
def splitRoto():
    
    if nuke.selectedNode().Class() == 'RotoPaint':
        roto = nuke.selectedNode().knob('curves').rootLayer
        for i in roto:
            tempRoto = nuke.createNode('RotoPaint')
            tempRoto.knob('curves').rootLayer.append(i.clone())
    elif nuke.selectedNode().Class() == 'Roto':
        roto = nuke.selectedNode().knob('curves').rootLayer
        for i in roto:
            tempRoto = nuke.createNode('Roto')
            tempRoto.knob('curves').rootLayer.append(i.clone())
    else:
        nuke.message('No roto/paint node selected')

nuke.menu('Nuke').addMenu('Script').addCommand( 'split out rotoshapes', 'splitRoto()')
######################################################################################################################################################
######################################################################################################################################################
# enable/disable behavior
multiSelect = False
# grab artist's current SelectedColor preference
defaultHighlight = nuke.toNode('preferences').knob('SelectedColor').value()

def multiselectCallback():
    global multiSelect
    if multiSelect:
        n = nuke.thisNode()
        k = nuke.thisKnob()
        nodes = nuke.selectedNodes()
        dontbother=['selected','xpos','ypos'] # might need to add to this list
        if (not(k.name() in dontbother) and (n in nodes)): # node is selected, and knob is not in ignored list
            # this is nice for debugging:
            # print str(k.name()) +' : '+ str(k.value()) 
            for node in nuke.selectedNodes():
                if node is not n:
                    if k.name() in node.knobs().keys():
                        node.knob(k.name()).setValue(k.value())
                        # need to test for keyed knobs and set setKey instead of setValue

def toggleMultSelect():
    # you could remove / add the callback here
    # instead of keeping it all the time and
    # using a boolean to enable/disable the behavior
    # not sure which would be more effecient,
    # probably removing/adding callback?
    global multiSelect
    global defaultHighlight
    multiSelect = not multiSelect
    if multiSelect:
        status = 'on'
        # make the SelectedColor a gross red
        nuke.toNode('preferences').knob('SelectedColor').setValue(4278190335)
    else:
        status = 'off'
        nuke.toNode('preferences').knob('SelectedColor').setValue(defaultHighlight)
    nuke.message('Multisection Modification is turned '+status)

nuke.menu('Nuke').addMenu('Script').addCommand( 'Multiselected Modification', "toggleMultSelect()", 'ctrl+m')
nuke.addKnobChanged(multiselectCallback)


######################################################################################################################################################
######################################################################################################################################################
import merge_transforms_v2
nuke.menu('Nuke').addMenu('Script').addCommand( 'merge transforms', 'merge_transforms_v2.start()')



nuke.menu('Nuke').addMenu('Script').addCommand( 'loadOffline', 'load_offline_references()', "Shift+v")


try:
    import shortcuteditor
    shortcuteditor.nuke_setup()
except Exception:
    import traceback
    traceback.print_exc()




import lock_viewer_pipes
lock_viewer_pipes.register_viewer_locks()




######################################################################################################################################################
######################################################################################################################################################

import nuke

# TODO remove duplicate code
def nuke_version_corresponds(nuke_version):
    import nuke
    current_nuke_version = str(nuke.NUKE_VERSION_MAJOR) + '.' + str(nuke.NUKE_VERSION_MINOR)
    return current_nuke_version == nuke_version

def os_corresponds(os_suffix):
    from sys import platform
    if os_suffix == 'WIN':
        return platform == "win32"
    if os_suffix == 'LINUX':
        return platform == "linux" or platform == "linux2"
    if os_suffix == 'OSX':
        return platform == "darwin"
    assert(False)

def check_nuke_version_and_os(nuke_version, os_suffix, print_error_message=False):
    if not os_corresponds(os_suffix):
        if print_error_message:
            print('platform doesn\'t match')
        return False
    if not nuke_version_corresponds(nuke_version):
        if print_error_message:
            print('nuke version doesn\'t match')
        return False
    return True

if check_nuke_version_and_os('10.0', 'LINUX'):
    # add KeenTools menu to Nodes toolbar
    toolbar = nuke.menu('Nodes')
    kt_menu = toolbar.addMenu('KeenTools', icon='KeenTools.png')
    kt_menu.addCommand('GeoTracker', lambda: nuke.createNode('GeoTracker'), icon='GeoTracker.png')
    kt_menu.addCommand('PinTool', lambda: nuke.createNode('PinTool'), icon='PinTool.png')
    kt_menu.addCommand('ReadRiggedGeo', lambda: nuke.createNode('ReadRiggedGeo'), icon='ReadRiggedGeo.png')
    if 'ON' == 'ON':
        kt_menu.addCommand('FaceBuilder (beta)', lambda: nuke.createNode('FaceBuilder'), icon='FaceBuilder.png')
    if 'ON' == 'ON':
        kt_menu.addCommand('FaceTracker (beta)', lambda: nuke.createNode('FaceTracker'), icon='FaceTracker.png')
    if 'OFF' == 'ON':
        kt_menu.addCommand('FlowEvaluationTool', lambda: nuke.createNode('FlowEvaluationTool'), icon='KeenTools.png')



######################################################################################################################################################
######################################################################################################################################################

import sb_convertCornerPin
nuke.menu('Nuke').addMenu('Script').addCommand('convertCornerPin', 'sb_convertCornerPin.sb_convertCornerPin()')

import sb_convertTracker
nuke.menu('Nuke').addMenu('Script').addCommand('ConvertTracker', 'sb_convertTracker.sb_convertTracker()')



######################################################################################################################################################
######################################################################################################################################################
def linkRoto():

    if nuke.selectedNode().Class() == 'Tracker4' or nuke.selectedNode().Class() =='Transform':
        lnkNde = nuke.selectedNode()   
        lnkName = lnkNde.knob('name').getValue()
        n = nuke.nodes.Roto()
        
        n.knob('curves').rootLayer.getTransform().getTranslationAnimCurve(0).expressionString = 'parent.'+lnkName+'.translate'
        n.knob('curves').rootLayer.getTransform().getTranslationAnimCurve(0).useExpression = True
        
        n.knob('curves').rootLayer.getTransform().getTranslationAnimCurve(1).expressionString = 'parent.'+lnkName+'.translate'
        n.knob('curves').rootLayer.getTransform().getTranslationAnimCurve(1).useExpression = True
        
        
        
        n.knob('curves').rootLayer.getTransform().getRotationAnimCurve(2).expressionString = 'parent.'+lnkName+'.rotate'
        n.knob('curves').rootLayer.getTransform().getRotationAnimCurve(2).useExpression = True
        
        
        
        n.knob('curves').rootLayer.getTransform().getScaleAnimCurve(0).expressionString = 'parent.'+lnkName+'.scale'
        n.knob('curves').rootLayer.getTransform().getScaleAnimCurve(0).useExpression = True
        
        n.knob('curves').rootLayer.getTransform().getScaleAnimCurve(1).expressionString = 'parent.'+lnkName+'.scale'
        n.knob('curves').rootLayer.getTransform().getScaleAnimCurve(1).useExpression = True
        
        
        
        n.knob('curves').rootLayer.getTransform().getPivotPointAnimCurve(0).expressionString = 'parent.'+lnkName+'.center'
        n.knob('curves').rootLayer.getTransform().getPivotPointAnimCurve(0).useExpression = True
        
        n.knob('curves').rootLayer.getTransform().getPivotPointAnimCurve(1).expressionString = 'parent.'+lnkName+'.center'
        n.knob('curves').rootLayer.getTransform().getPivotPointAnimCurve(1).useExpression = True
        
        
        n.knob('output').setValue('alpha')
        n.knob('selected').setValue(True)
        n.showControlPanel()
        
        lnkNde.knob('selected').setValue(False)

nuke.menu('Nuke').addMenu('Script').addCommand('linkRoto', 'linkRoto()')