#!/usr/bin/env python
import sys
sys.path.append("/root/catkin_ws/src/Task_Module")
import unittest
from geometry_msgs.msg import Pose, PoseStamped, Point
from tasks.src.movement import UpdatePoseState
from uuv_control_msgs.msg import Waypoint
import rospy
from tasks.src.example import YourStateMachine
from tasks.src.data import shared_data, initialize_subscribers
import os
import smach


from tasks.src.movement import UpdatePoseState, UpdatePoseToObjectState, HoldPositionTask,Rotate90DegreesState


##########################################################
#Singleton States Machines for Testing individual States#*
##########################################################
class TestBasicMovementMachine(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['success', 'failure'])
        with self:
            smach.StateMachine.add('move', UpdatePoseState( edge_case_callback= lambda x: True, next_state_callback = None), transitions={'success':'ANOTHER_STATE', 'aborted':'failure', 'edge_case_detected':'failure'})


class TestObjectMovementMachine(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['success', 'failure'])
        with self:
            smach.StateMachine.add('move', UpdatePoseState( edge_case_callback= lambda x: True, next_state_callback = None), transitions={'success':'ANOTHER_STATE', 'aborted':'failure', 'edge_case_detected':'failure'})


class TestRotationMachine(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, outcomes=['success', 'failure'])
        with self:
            smach.StateMachine.add('move', UpdatePoseState( edge_case_callback= lambda x: True, next_state_callback = None), transitions={'success':'ANOTHER_STATE', 'aborted':'failure', 'edge_case_detected':'failure'})

##########################################################
#Singleton States Machines for Testing individual States#*
##########################################################


class TestMovementsinStateMachine(unittest.TestCase):

    def setUp(self):
        rospy.init_node('your_state_machine_node')
        file_path = os.path.join(os.path.dirname(__file__), 'test_data/test_topics.yml')
        initialize_subscribers(file_path)
        sm = YourStateMachine()
        outcome = sm.execute()


    # def setUp(self):
    #     self.state = UpdatePoseState( edge_case_callback= lambda x: True, next_state_callback = None)
    #     self.random_waypoints = self.state.generate_waypoints(1)
    #     self.waypoint_1 = self.random_waypoints[0]

    def controls_movement_simulation(self):
        #  This should test wheter it makes a substational movement to see wheter 
        #  The movement command from the controls systems works acoordingly.
        self.state.execute()
        self.assertTrue(True)


    def reach_to_destination(self):
        #  This test check if the internal loop inside the Movement statemachine
        #  works correctly and stops when as reach its destination.
        pass




if __name__ == '__main__':
    state = UpdatePoseState( edge_case_callback= lambda x: False, next_state_callback = None)
    random_waypoints = state.generate_waypoints(1)
    waypoint_1 = random_waypoints[0]
    state.execute()
    # unittest.main()

