#!/usr/bin/env python2
# the indices of values from joy message:
# index number of / joy.buttons:
# 0 - A
# 1 - B
# 2 - X
# 3 - Y
# 4 - LB
# 5 - RB
# 6 - back
# 7 - start
# 8 - power
# 9 - Button stick left
# 10 - Button stick right

# index number of / joy.axis:
# 0 - Left / Right Axis stick left
# 1 - Up / Down Axis stick left
# 2 - LT
# 3 - Left / Right Axis stick right
# 4 - Up / Down Axis stick right
# 5 - RT
# 6 - cross key left / right
# 7 - cross key up / down
from lxml import etree
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from std_msgs.msg import Bool
import glob

class ControlScheme:
    def __init__(self):
        """
		    initializes an instance of a control scheme
	    """
        # this will contain an 2D array of different control schemes where the nth control scheme will be designated
        # from axesTarget[n] and the target for the mth index axis will be axesTarget[n][m]
        self.axesTarget = []
        self.buttonsTarget = []

        self.currentLight = Bool()
        self.currentLight.data = False
        self.previousLightButton = 0

        self.buttonNames = {
            "A": 0,
            "B": 1,
            "X": 2,
            "Y": 3,
            "LB": 4,
            "RB": 5,
            "Back": 6,
            "Start": 7,
            "LeftStick": 8,
            "RightStick": 9
        }
        self.axesNames = {
            "LeftStickX": 0,
            "LeftStickY": 1,
            "LeftTrigger": 2,
            "RightStickX": 3,
            "RightStickY": 4,
            "RightTrigger": 5,
            "DpadX": 6,
            "DpadY": 7
        }

        # Dictionary created whenever a joy message is received that matches a target control
        # designated by the ControlScheme with a value from the joy message
        self.targetControls = {}

        # Array of all of the different ControlScheme files to be parsed
        self.XMLfileNames = glob.glob("./scheme_*.xml")
        self.index = 0

        self.transXPublisher = rospy.Publisher('transXPID', Float64, queue_size=10)
        self.transYPublisher = rospy.Publisher('transYPID', Float64, queue_size=10)
        self.transZPublisher = rospy.Publisher('transZPID', Float64, queue_size=10)
        self.angXYPublisher = rospy.Publisher('angXYPID', Float64, queue_size=10)
        self.angXZPublisher = rospy.Publisher('angXZPID', Float64, queue_size=10)
    self.angYZPublisher = rospy.Publisher('angYZPID', Float64, queue_size=10)

        self.togglePublisher = rospy.Publisher('Toggle', Bool, queue_size=10)

    # Parses all of the xml files with names in the XMLfileNames array and creates an array
    # of axes and buttons to append to the axesTarget and buttonsTarget arrays respectively
    # This is done so that all of the xml files can be read in at the same time and
    # switching between them can be done by switching the index
    def parseXML(self):
        """
        Parse through all xml files in XMLfileNames to create control scheme
	    """
        for fileName in self.XMLfileNames:
            tree = etree.parse(fileName)
            root = tree.getroot()

            axes = [None]*8
            buttons = [None]*11

            for axis in root.findall("axis"):
                axes[self.axesNames[axis.get("name")]] = axis.get("target")

            for button in root.findall("button"):
                buttons[self.buttonNames[button.get("name")]] = button.get("target")

            self.axesTarget.append(axes)
            self.buttonsTarget.append(buttons)

    # Populates the dictionary of targetControls by matching the incoming values with the designated targets
    def interpretJoyMsg(self, axes_values, buttons_values):
        """
	    Populates the dictionary of targetControls by matching the incoming
	    values with the designated targets
	
	    Keyword arguements:
	
	    axes_values -- Incoming axes values coming from 360 controller
	    buttons_values -- Incoming buttons values from 360 controller
	    """
        for i in range(len(axes_values)):
            if(not self.axesTarget[self.index][i] == None):
                self.targetControls[self.axesTarget[self.index][i]] = axes_values[i]

        for i in range(len(buttons_values)):
            if(not self.buttonsTarget[self.index][i] == None):
                self.targetControls[self.buttonsTarget[self.index][i]] = buttons_values[i]

    # changes the index of control schemes
    def setIndex(self, n):
        """
	    changes the index of control schemes
	
	    Keyword arguements:
	
	    n -- the index value of control scheme to be changed to
	    """
        if n < len(self.axesTarget) and n < len(self.buttonsTarget) and n >= 0:
            self.index = n

    def sendTargetMessage(self):
        """
	    publish twist message with linear x,y,z and angular x,y,z
	    """
        self.transXPublisher.publish(self.targetControls["linear_x"])
        self.transYPublisher.publish(self.targetControls["linear_y"])
        self.transZPublisher.publish(self.targetControls["linear_z"])
        self.angXYPublisher.publish(self.targetControls["angular_xy"])
        self.angXZPublisher.publish(self.targetControls["angular_xz"])
        self.angYZPublisher.publish(self.targetControls["angular_yz"])


    def sendToggleMessage(self):
	"""
		Publish boolean message indicating the current state of light
		"""
	if not (self.targetControls["light"] == self.previousLightButton):

            if(self.targetControls["light"] == 1):
                self.currentLight.data = not self.currentLight.data
                self.togglePublisher.publish(self.currentLight)
        self.previousLightButton = self.targetControls["light"]
