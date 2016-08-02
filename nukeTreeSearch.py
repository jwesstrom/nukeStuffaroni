class nodeList(object):
    def __init__(self):
        self.nodeList = []


    def addToList(self):

        self.nodeList.insert(0, nuke.thisNode())
        if len(self.nodeList) >14:
            del self.nodeList[14]
        print 'added ' + nuke.thisNode().knob('name').getValue() 
   

    def deleteFromList(self):
        for i in range(len(self.nodeList)):
            if nuke.thisNode().knob('name').getValue() in self.nodeList[i].knob('name').getValue():
                print 'delete' + str(self.nodeList[i].knob('name').getValue())
                del self.nodeList[i]
                break

a = nodeList()

nuke.addOnUserCreate(a.addToList)
nuke.addOnDestroy(a.deleteFromList)





from PySide import QtCore, QtGui
#import sys
import nuke

class myWidget(QtGui.QDialog):
    def __init__(self):
        super(myWidget, self).__init__()

        # self.setWindowFlags(QtCore.Qt.Tool) # without this the win will not stay ontop
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)



        self.setMinimumSize(200, 300)
        self.setMaximumSize(200, 300)

        # Input box
        self.input = QtGui.QLineEdit()
        self.things = QtGui.QListWidget()
        print self.input.text()

        
        for i in a.nodeList:
            self.things.addItem(i.knob('name').getValue())

        

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.things)

        # Remove margins
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.things.currentRowChanged.connect(self.update)
        self.input.textChanged.connect(self.lineChange)
        self.row = -1

    def event(self, event):
        

        is_keypress = event.type() == QtCore.QEvent.KeyPress

        if is_keypress and event.key() == QtCore.Qt.Key_Up:
            if self.row < 0:
                self.row = -1
            else:
                self.row = self.row - 1
                self.things.setCurrentRow(self.row)

        elif is_keypress and event.key() == QtCore.Qt.Key_Down:
            self.row = self.row+ 1
            self.things.setCurrentRow(self.row)
        else:
            return super(myWidget, self).event(event)

    def update(self):
        nuke.selectAll()
        nuke.invertSelection()
        a.nodeList[self.things.currentRow()].knob('selected').setValue(True)
        node = nuke.selectedNode()
        xC = node.xpos() + node.screenWidth()/2
        yC = node.ypos() + node.screenHeight()/2
        nuke.zoom( 2, [ xC, yC ])

    def lineChange(self):
        if not self.input.text():
            for i in a.nodeList:
                self.things.addItem(i.knob('name').getValue())
        else:
            self.things.clear()
            selNodes = []
            for i in nuke.allNodes():
                if self.input.text().lower() in i.knob('name').getValue().lower():
                    selNodes.append(i)
                    self.things.addItem(i.knob('name').getValue())
        
        
            self.things.setCurrentRow(0)


t = myWidget()
t.show()
