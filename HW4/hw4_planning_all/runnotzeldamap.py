import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from greedynavigator2 import *
from planner import *
from npcworld import *
from mybuildpathnetwork import *
from clonenav import *


#############################
### init state and goal state

init_state = State(propositions=['at_agent_bed_0', 
                                 'at_key_3_table_3', 'at_key_4_table_4',
                                 'at_key_1_table_1', 'at_key_2_table_2',
                                 'at_gold_chest',
                                 'at_key_7_table_7', 'at_key_8_table_8',
                                 'locked_door_7', 'locked_door_8',
                                 'at_key_6_table_6', 'at_key_5_table_5',
                                 'locked_door_5', 'locked_door_6',
                                 'locked_door_3', 'locked_door_4',
                                 'locked_door_1', 'locked_door_2',
                                 'path_bed_0_door_7', 'path_bed_0_door_8',
                                 'path_bed_0_table_7', 'path_bed_0_table_8',
                                 'path_bed_0_crack_1',
                                 'path_table_7_table_8', 'path_table_7_crack_1',
                                 'path_table_7_door_7', 'path_table_7_door_8',
                                 'path_door_7_crack_1', 'path_door_7_door_8',
                                 'path_door_7_table_7', 'path_door_7_table_8',
                                 'path_table_8_table_7', 'path_table_8_crack_1',
                                 'path_table_8_door_7', 'path_table_8_door_8',
                                 'path_door_8_crack_1', 'path_door_8_door_7',
                                 'path_door_8_table_7', 'path_door_8_table_8',
                                 'path_table_5_table_6', 'path_table_5_door_5',
                                 'path_table_6_table_5', 'path_table_6_door_5',
                                 'path_door_5_table_5', 'path_door_5_table_6',
                                 'path_statue_5_door_3', 'path_statue_5_door_4',
                                 'path_statue_5_door_1', 'path_statue_5_door_2',
                                 'path_door_3_door_1', 'path_door_3_door_2',
                                 'path_door_3_door_4',
                                 'path_door_4_door_3', 'path_door_4_door_1',
                                 'path_door_4_door_2',
                                 'at_npc_bed_1',
                                 'path_bed_1_table_5', 'path_bed_1_table_6', 
                                 'path_bed_1_door_5',
                                 'path_statue_5_crack_2', 'path_crack_2_statue_5', 
                                 'path_crack_2_door_3',
                                 'path_crack_2_door_4',
                                 'path_crack_2_door_1', 'path_crack_2_door_2',
                                 'path_door_1_door_2', 'path_door_1_door_3',
                                 'path_door_1_door_4', 'path_door_1_statue_5',
                                 'path_door_2_door_3', 'path_door_2_statue_5',
                                 'path_door_2_door_4', 'path_door_2_door_1'
                                 ])
goal_state = State(propositions=['has_npc_gold'])

#####################
### ACTIONS

### PICKUP
pickup_key_3_table_3 = TriggerAction('pickup_key_3_table_3', 
                                    preconditions=['at_{name}_table_3', 'at_key_3_table_3'],
                                    add_list=['has_{name}_key_3'], 
                                    delete_list=['at_key_3_table_3'])
pickup_key_4_table_4 = TriggerAction('pickup_key_4_table_4', 
                                    preconditions=['at_{name}_table_4', 'at_key_4_table_4'],
                                    add_list=['has_{name}_key_4'], 
                                    delete_list=['at_key_4_table_4'])
pickup_key_7_table_7 = TriggerAction('pickup_key_7_table_7', 
                                    preconditions=['at_{name}_table_7', 'at_key_7_table_7'],
                                    add_list=['has_{name}_key_7'], 
                                    delete_list=['at_key_7_table_7'])
pickup_key_8_table_8 = TriggerAction('pickup_key_8_table_8', 
                                    preconditions=['at_{name}_table_8', 'at_key_8_table_8'],
                                    add_list=['has_{name}_key_8'], 
                                    delete_list=['at_key_8_table_8'])
pickup_key_5_table_5 = TriggerAction('pickup_key_5_table_5', 
                                    preconditions=['at_{name}_table_5', 'at_key_5_table_5'],
                                    add_list=['has_{name}_key_5'], 
                                    delete_list=['at_key_5_table_5'])
pickup_key_6_table_6 = TriggerAction('pickup_key_6_table_6', 
                                    preconditions=['at_{name}_table_6', 'at_key_6_table_6'],
                                    add_list=['has_{name}_key_6'], 
                                    delete_list=['at_key_6_table_6'])
pickup_key_1_table_1 = TriggerAction('pickup_key_1_table_1', 
                                    preconditions=['at_{name}_table_1', 'at_key_1_table_1'],
                                    add_list=['has_{name}_key_1'], 
                                    delete_list=['at_key_1_table_1'])
pickup_key_2_table_2 = TriggerAction('pickup_key_2_table_2', 
                                    preconditions=['at_{name}_table_2', 'at_key_2_table_2'],
                                    add_list=['has_{name}_key_2'], 
                                    delete_list=['at_key_2_table_2'])
pickup_key_3_crack_2 = TriggerAction('pickup_key_3_crack_2', 
                                    preconditions=['at_{name}_crack_2', 'at_key_3_crack_2'],
                                    add_list=['has_{name}_key_3'], 
                                    delete_list=['at_key_3_crack_2'])
pickup_key_4_crack_2 = TriggerAction('pickup_key_4_crack_2', 
                                    preconditions=['at_{name}_crack_2', 'at_key_4_crack_2'],
                                    add_list=['has_{name}_key_4'], 
                                    delete_list=['at_key_4_crack_2'])
pickup_gold = TriggerAction('pickup_gold', 
                                    preconditions=['at_{name}_chest', 'at_gold_chest'],
                                    add_list=['has_{name}_gold'], 
                                    delete_list=['at_gold_chest'])
### DROP
drop_key_3 = TriggerAction('drop_key_3', 
                        preconditions=['has_{name}_key_3', 'at_{name}_crack_1'],
                        add_list=['at_key_3_crack_2'],
                        delete_list=['has_{name}_key_3'])
drop_key_4 = TriggerAction('drop_key_4', 
                        preconditions=['has_{name}_key_4', 'at_{name}_crack_1'],
                        add_list=['at_key_4_crack_2'],
                        delete_list=['has_{name}_key_4'])
### OPEN DOORS
open_door_7 = DoorAction('open_door_7',
                            preconditions=['at_{name}_door_7', 'has_{name}_key_7', 'locked_door_7'],
                            add_list=['path_door_7_table_4', 'path_table_4_door_7', 'unlocked_door_7'],
                            delete_list=['has_{name}_key_7', 'locked_door_7'])
open_door_8 = DoorAction('open_door_8',
                            preconditions=['at_{name}_door_8', 'has_{name}_key_8', 'locked_door_8'],
                            add_list=['path_door_8_table_3', 'path_table_3_door_8', 'unlocked_door_8'],
                            delete_list=['has_{name}_key_8', 'locked_door_8'])
open_door_5 = DoorAction('open_door_5',
                            preconditions=['at_{name}_door_5', 'has_{name}_key_5', 'locked_door_5'],
                            add_list=['path_statue_5_door_5', 'path_door_5_statue_5', 'unlocked_door_5'],
                            delete_list=['has_{name}_key_5', 'locked_door_5'])
open_door_6 = DoorAction('open_door_6',
                            preconditions=['at_{name}_door_6', 'has_{name}_key_6', 'locked_door_6'],
                            add_list=['path_chest_door_5', 'path_door_6_chest', 'unlocked_door_6'],
                            delete_list=['has_{name}_key_6', 'locked_door_6'])
open_door_3 = DoorAction('open_door_3',
                            preconditions=['at_{name}_door_3', 'has_{name}_key_3', 'locked_door_3'],
                            add_list=['path_table_2_door_3', 'path_door_3_table_2', 'unlocked_door_3'],
                            delete_list=['has_{name}_key_3', 'locked_door_3'])
open_door_4 = DoorAction('open_door_4',
                            preconditions=['at_{name}_door_4', 'has_{name}_key_4', 'locked_door_4'],
                            add_list=['path_table_1_door_4', 'path_door_4_table_1', 'unlocked_door_4'],
                            delete_list=['has_{name}_key_4', 'locked_door_4'])
open_door_1 = DoorAction('open_door_1',
                            preconditions=['at_{name}_door_1', 'has_{name}_key_1', 'locked_door_1'],
                            add_list=['path_door_6_door_1', 'path_door_1_door_6', 'unlocked_door_1'],
                            delete_list=['has_{name}_key_1', 'locked_door_1'])
open_door_2 = DoorAction('open_door_2',
                            preconditions=['at_{name}_door_2', 'has_{name}_key_2', 'locked_door_2'],
                            add_list=['path_door_6_door_2', 'path_door_2_door_6', 'unlocked_door_2'],
                            delete_list=['has_{name}_key_2', 'locked_door_2'])
### MOVE FROM BED
move_bed_0_table_8 = MoveAction("move_bed_0_table_8", 
                              preconditions=['at_{name}_bed_0', 'path_bed_0_table_8'],
                              add_list=['at_{name}_table_8'],
                              delete_list=['at_{name}_bed_0'])
move_bed_0_table_7 = MoveAction("move_bed_0_table_7", 
                              preconditions=['at_{name}_bed_0', 'path_bed_0_table_7'],
                              add_list=['at_{name}_table_7'],
                              delete_list=['at_{name}_bed_0'])
move_bed_0_door_7 = MoveAction("move_bed_0_door_7", 
                              preconditions=['at_{name}_bed_0', 'path_bed_0_door_7'],
                              add_list=['at_{name}_door_7'],
                              delete_list=['at_{name}_bed_0'])
move_bed_0_door_8 = MoveAction("move_bed_0_door_8", 
                              preconditions=['at_{name}_bed_0', 'path_bed_0_door_8'],
                              add_list=['at_{name}_door_8'],
                              delete_list=['at_{name}_bed_0'])
move_bed_0_crack_1 = MoveAction("move_bed_0_crack_1", 
                              preconditions=['at_{name}_bed_0', 'path_bed_0_crack_1'],
                              add_list=['at_{name}_crack_1'],
                              delete_list=['at_{name}_bed_0'])
### MOVE FROM TABLE 7
move_table_7_table_8 = MoveAction("move_table_7_table_8", 
                              preconditions=['at_{name}_table_7', 'path_table_7_table_8'],
                              add_list=['at_{name}_table_8'],
                              delete_list=['at_{name}_table_7'])
move_table_7_crack_1 = MoveAction("move_table_7_crack_1", 
                              preconditions=['at_{name}_table_7', 'path_table_7_crack_1'],
                              add_list=['at_{name}_crack_1'],
                              delete_list=['at_{name}_table_7'])
move_table_7_door_7 = MoveAction("move_table_7_door_7", 
                              preconditions=['at_{name}_table_7', 'path_table_7_door_7'],
                              add_list=['at_{name}_door_7'],
                              delete_list=['at_{name}_table_7'])
move_table_7_door_8 = MoveAction("move_table_7_door_8", 
                              preconditions=['at_{name}_table_7', 'path_table_7_door_8'],
                              add_list=['at_{name}_door_8'],
                              delete_list=['at_{name}_table_7'])
### MOVE FROM DOOR 7
move_door_7_table_4 = MoveAction("move_door_7_table_4", 
                              preconditions=['at_{name}_door_7', 'path_door_7_table_4'],
                              add_list=['at_{name}_table_4'],
                              delete_list=['at_{name}_door_7'])
move_door_7_crack_1 = MoveAction("move_door_7_crack_1", 
                              preconditions=['at_{name}_door_7', 'path_door_7_crack_1'],
                              add_list=['at_{name}_crack_1'],
                              delete_list=['at_{name}_door_7'])
move_door_7_door_8 = MoveAction("move_door_7_door_8", 
                              preconditions=['at_{name}_door_7', 'path_door_7_door_8'],
                              add_list=['at_{name}_door_8'],
                              delete_list=['at_{name}_door_7'])
move_door_7_table_7 = MoveAction("move_door_7_table_7", 
                              preconditions=['at_{name}_door_7', 'path_door_7_table_7'],
                              add_list=['at_{name}_table_7'],
                              delete_list=['at_{name}_door_7'])
move_door_7_table_8 = MoveAction("move_door_7_table_8", 
                              preconditions=['at_{name}_door_7', 'path_door_7_table_8'],
                              add_list=['at_{name}_table_8'],
                              delete_list=['at_{name}_door_7'])
### MOVE FROM TABLE 8
move_table_8_table_7 = MoveAction("move_table_8_table_7", 
                              preconditions=['at_{name}_table_8', 'path_table_8_table_7'],
                              add_list=['at_{name}_table_7'],
                              delete_list=['at_{name}_table_8'])
move_table_8_crack_1 = MoveAction("move_table_8_crack_1", 
                              preconditions=['at_{name}_table_8', 'path_table_8_crack_1'],
                              add_list=['at_{name}_crack_1'],
                              delete_list=['at_{name}_table_8'])
move_table_8_door_8 = MoveAction("move_table_8_door_8", 
                              preconditions=['at_{name}_table_8', 'path_table_8_door_8'],
                              add_list=['at_{name}_door_8'],
                              delete_list=['at_{name}_table_8'])
move_table_8_door_7 = MoveAction("move_table_8_door_7", 
                              preconditions=['at_{name}_table_8', 'path_table_8_door_7'],
                              add_list=['at_{name}_door_7'],
                              delete_list=['at_{name}_table_8'])
### MOVE FROM DOOR 8
move_door_8_crack_1 = MoveAction("move_door_8_crack_1", 
                              preconditions=['at_{name}_door_8', 'path_door_8_crack_1'],
                              add_list=['at_{name}_crack_1'],
                              delete_list=['at_{name}_door_8'])
move_door_8_table_7 = MoveAction("move_door_8_table_7", 
                              preconditions=['at_{name}_door_8', 'path_door_8_table_7'],
                              add_list=['at_{name}_table_7'],
                              delete_list=['at_{name}_door_8'])
move_door_8_door_7 = MoveAction("move_door_8_door_7", 
                              preconditions=['at_{name}_door_8', 'path_door_8_door_7'],
                              add_list=['at_{name}_door_7'],
                              delete_list=['at_{name}_door_8'])
move_door_8_table_8 = MoveAction("move_door_8_table_8", 
                              preconditions=['at_{name}_door_8', 'path_door_8_table_8'],
                              add_list=['at_{name}_table_8'],
                              delete_list=['at_{name}_door_8'])
move_door_8_table_3 = MoveAction("move_door_8_table_3", 
                              preconditions=['at_{name}_door_8', 'path_door_8_table_3'],
                              add_list=['at_{name}_table_3'],
                              delete_list=['at_{name}_door_8'])

### MOVE FROM TABLE 3
move_table_3_door_8 = MoveAction("move_table_3_door_8", 
                              preconditions=['at_{name}_table_3', 'path_table_3_door_8'],
                              add_list=['at_{name}_door_8'],
                              delete_list=['at_{name}_table_3'])
### MOVE FROM TABLE 4
move_table_4_door_7 = MoveAction("move_table_4_door_7", 
                              preconditions=['at_{name}_table_4', 'path_table_4_door_7'],
                              add_list=['at_{name}_door_7'],
                              delete_list=['at_{name}_table_4'])
### MOVE FROM TABLE 5
move_table_5_table_6 = MoveAction("move_table_5_table_6", 
                              preconditions=['at_{name}_table_5', 'path_table_5_table_6'],
                              add_list=['at_{name}_table_6'],
                              delete_list=['at_{name}_table_5'])
move_table_5_door_5 = MoveAction("move_table_5_door_5", 
                              preconditions=['at_{name}_table_5', 'path_table_5_door_5'],
                              add_list=['at_{name}_door_5'],
                              delete_list=['at_{name}_table_5'])
### MOVE FROM TABLE 6
move_table_6_table_5 = MoveAction("move_table_6_table_5", 
                              preconditions=['at_{name}_table_6', 'path_table_6_table_5'],
                              add_list=['at_{name}_table_5'],
                              delete_list=['at_{name}_table_6'])
move_table_6_door_5 = MoveAction("move_table_6_door_5", 
                              preconditions=['at_{name}_table_6', 'path_table_6_door_5'],
                              add_list=['at_{name}_door_5'],
                              delete_list=['at_{name}_table_6'])
### MOVE FROM DOOR 5
move_door_5_statue_5 = MoveAction("move_door_5_statue_5", 
                              preconditions=['at_{name}_door_5', 'path_door_5_statue_5'],
                              add_list=['at_{name}_statue_5'],
                              delete_list=['at_{name}_door_5'])
move_door_5_table_5 = Action("move_door_5_table_5", 
                              preconditions=['at_npc_door_5', 'path_door_5_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_door_5'])
move_door_5_table_6 = Action("move_door_5_table_6", 
                              preconditions=['at_npc_door_5', 'path_door_5_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_door_5'])

### MOVE FROM STATUE 5
move_statue_5_door_3 = MoveAction("move_statue_5_door_3", 
                              preconditions=['at_{name}_statue_5', 'path_statue_5_door_3'],
                              add_list=['at_{name}_door_3'],
                              delete_list=['at_{name}_statue_5'])
move_statue_5_door_4 = MoveAction("move_statue_5_door_4", 
                              preconditions=['at_{name}_statue_5', 'path_statue_5_door_4'],
                              add_list=['at_{name}_door_4'],
                              delete_list=['at_{name}_statue_5'])
move_statue_5_crack_2 = MoveAction("move_statue_5_crack_2", 
                              preconditions=['at_{name}_statue_5', 'path_statue_5_crack_2'],
                              add_list=['at_{name}_crack_2'],
                              delete_list=['at_{name}_statue_5'])
move_statue_5_door_1 = MoveAction("move_statue_5_door_1", 
                              preconditions=['at_{name}_statue_5', 'path_statue_5_door_1'],
                              add_list=['at_{name}_door_1'],
                              delete_list=['at_{name}_statue_5'])
move_statue_5_door_2 = MoveAction("move_statue_5_door_2", 
                              preconditions=['at_{name}_statue_5', 'path_statue_5_door_2'],
                              add_list=['at_{name}_door_2'],
                              delete_list=['at_{name}_statue_5'])
### MOVE FROM DOOR 3
move_door_3_table_2 = MoveAction("move_door_3_table_2", 
                              preconditions=['at_{name}_door_3', 'path_door_3_table_2'],
                              add_list=['at_{name}_table_2'],
                              delete_list=['at_{name}_door_3'])
move_door_3_door_1 = MoveAction("move_door_3_door_1", 
                              preconditions=['at_{name}_door_3', 'path_door_3_door_1'],
                              add_list=['at_{name}_door_1'],
                              delete_list=['at_{name}_door_3'])
move_door_3_door_2 = MoveAction("move_door_3_door_2", 
                              preconditions=['at_{name}_door_3', 'path_door_3_door_2'],
                              add_list=['at_{name}_door_2'],
                              delete_list=['at_{name}_door_3'])
move_door_3_door_4 = MoveAction("move_door_3_door_4", 
                              preconditions=['at_{name}_door_3', 'path_door_3_door_4'],
                              add_list=['at_{name}_door_4'],
                              delete_list=['at_{name}_door_3'])
### MOVE FROM DOOR 4
move_door_4_table_1 = MoveAction("move_door_4_table_1", 
                              preconditions=['at_{name}_door_4', 'path_door_4_table_1'],
                              add_list=['at_{name}_table_1'],
                              delete_list=['at_{name}_door_4'])
move_door_4_door_1 = MoveAction("move_door_4_door_1", 
                              preconditions=['at_{name}_door_4', 'path_door_4_door_1'],
                              add_list=['at_{name}_door_1'],
                              delete_list=['at_{name}_door_4'])
move_door_4_door_2 = MoveAction("move_door_4_door_2", 
                              preconditions=['at_{name}_door_4', 'path_door_4_door_2'],
                              add_list=['at_{name}_door_2'],
                              delete_list=['at_{name}_door_4'])
move_door_4_door_3 = MoveAction("move_door_4_door_3", 
                              preconditions=['at_{name}_door_4', 'path_door_4_door_3'],
                              add_list=['at_{name}_door_3'],
                              delete_list=['at_{name}_door_4'])
### MOVE FROM TABLE 2
move_table_2_door_3 = MoveAction("move_table_2_door_3", 
                              preconditions=['at_{name}_table_2', 'path_table_2_door_3'],
                              add_list=['at_{name}_door_3'],
                              delete_list=['at_{name}_table_2'])
### MOVE FROM TABLE 1
move_table_1_door_4 = MoveAction("move_table_1_door_4", 
                              preconditions=['at_{name}_table_1', 'path_table_1_door_4'],
                              add_list=['at_{name}_door_4'],
                              delete_list=['at_{name}_table_1'])
### MOVE FROM DOOR 1
move_door_1_door_6 = MoveAction("move_door_1_door_6", 
                              preconditions=['at_{name}_door_1', 'path_door_1_door_6'],
                              add_list=['at_{name}_door_6'],
                              delete_list=['at_{name}_door_1'])
move_door_1_door_2 = MoveAction("move_door_1_door_2", 
                              preconditions=['at_{name}_door_1', 'path_door_1_door_2'],
                              add_list=['at_{name}_door_2'],
                              delete_list=['at_{name}_door_1'])
move_door_1_door_3 = MoveAction("move_door_1_door_3", 
                              preconditions=['at_{name}_door_1', 'path_door_1_door_3'],
                              add_list=['at_{name}_door_3'],
                              delete_list=['at_{name}_door_1'])
move_door_1_door_4 = MoveAction("move_door_1_door_4", 
                              preconditions=['at_{name}_door_1', 'path_door_1_door_4'],
                              add_list=['at_{name}_door_4'],
                              delete_list=['at_{name}_door_1'])
move_door_1_statue_5 = MoveAction("move_door_1_statue_5", 
                              preconditions=['at_{name}_door_1', 'path_door_1_statue_5'],
                              add_list=['at_{name}_statue_5'],
                              delete_list=['at_{name}_door_1'])

### MOVE FROM DOOR 2
move_door_2_door_6 = MoveAction("move_door_2_door_6", 
                              preconditions=['at_{name}_door_2', 'path_door_2_door_6'],
                              add_list=['at_{name}_door_6'],
                              delete_list=['at_{name}_door_2'])
move_door_2_door_1 = MoveAction("move_door_2_door_1", 
                              preconditions=['at_{name}_door_2', 'path_door_2_door_1'],
                              add_list=['at_{name}_door_1'],
                              delete_list=['at_{name}_door_2'])
move_door_2_door_3 = MoveAction("move_door_2_door_3", 
                              preconditions=['at_{name}_door_2', 'path_door_2_door_3'],
                              add_list=['at_{name}_door_3'],
                              delete_list=['at_{name}_door_2'])
move_door_2_door_4 = MoveAction("move_door_2_door_4", 
                              preconditions=['at_{name}_door_2', 'path_door_2_door_4'],
                              add_list=['at_{name}_door_4'],
                              delete_list=['at_{name}_door_2'])
move_door_2_statue_5 = MoveAction("move_door_2_statue_5", 
                              preconditions=['at_{name}_door_2', 'path_door_2_statue_5'],
                              add_list=['at_{name}_statue_5'],
                              delete_list=['at_{name}_door_2'])

### MOVE FROM DOOR 6
move_door_6_chest = MoveAction("move_door_6_chest", 
                              preconditions=['at_{name}_door_6', 'path_door_6_chest'],
                              add_list=['at_{name}_chest'],
                              delete_list=['at_{name}_door_6'])
### MOVE FROM BED 1
move_bed_1_door_5 = MoveAction("move_bed_1_door_5", 
                              preconditions=['at_{name}_bed_1', 'path_bed_1_door_5'],
                              add_list=['at_{name}_door_5'],
                              delete_list=['at_{name}_bed_1'])
move_bed_1_table_5 = MoveAction("move_bed_1_table_5", 
                              preconditions=['at_{name}_bed_1', 'path_bed_1_table_5'],
                              add_list=['at_{name}_table_5'],
                              delete_list=['at_{name}_bed_1'])
move_bed_1_table_6 = MoveAction("move_bed_1_table_6", 
                              preconditions=['at_{name}_bed_1', 'path_bed_1_table_6'],
                              add_list=['at_{name}_table_6'],
                              delete_list=['at_{name}_bed_1'])
### MOVE FROM CRACK 2
move_crack_2_door_3 = MoveAction("move_crack_2_door_3", 
                              preconditions=['at_{name}_crack_2', 'path_crack_2_door_3'],
                              add_list=['at_{name}_door_3'],
                              delete_list=['at_{name}_crack_2'])
move_crack_2_door_4 = MoveAction("move_crack_2_door_4", 
                              preconditions=['at_{name}_crack_2', 'path_crack_2_door_4'],
                              add_list=['at_{name}_door_4'],
                              delete_list=['at_{name}_crack_2'])
move_crack_2_door_1 = MoveAction("move_crack_2_door_1", 
                              preconditions=['at_{name}_crack_2', 'path_crack_2_door_1'],
                              add_list=['at_{name}_door_1'],
                              delete_list=['at_{name}_crack_2'])
move_crack_2_door_2 = MoveAction("move_crack_2_door_2", 
                              preconditions=['at_{name}_crack_2', 'path_crack_2_door_2'],
                              add_list=['at_{name}_door_2'],
                              delete_list=['at_{name}_crack_2'])
move_crack_2_statue_5 = MoveAction("move_crack_2_statue_5", 
                              preconditions=['at_{name}_crack_2', 'path_crack_2_statue_5'],
                              add_list=['at_{name}_statue_5'],
                              delete_list=['at_{name}_crack_2'])


actions = [pickup_key_3_table_3, pickup_key_4_table_4,
           pickup_key_7_table_7, pickup_key_8_table_8,
           pickup_key_1_table_1, pickup_key_2_table_2,
           pickup_gold,
           pickup_key_4_crack_2, pickup_key_3_crack_2,
           drop_key_3, drop_key_4,
           open_door_7, open_door_8, 
           open_door_5, open_door_6,
           open_door_3, open_door_4,
           open_door_2, open_door_1,
           move_bed_0_table_7, move_bed_0_table_8,
           move_bed_0_door_7, move_bed_0_door_8,
           move_door_7_crack_1, move_table_7_door_7,
           move_table_7_table_8, move_table_7_door_8,
           move_table_8_table_7, move_table_8_door_7,
           move_table_8_crack_1, move_table_8_door_8,
           move_door_7_crack_1, move_door_7_table_4,
           move_door_7_table_7, move_door_7_table_8,
           move_door_7_door_8,
           move_door_8_crack_1, move_door_8_table_3,
           move_door_8_table_7, move_door_8_table_8,
           move_door_8_door_7, 
           move_table_3_door_8, move_table_4_door_7,
           move_table_5_table_6, move_table_5_door_5,
           move_table_6_table_5, move_table_6_door_5,
           move_door_5_statue_5,
           move_door_5_table_5, move_door_5_table_6,
           move_statue_5_door_3, move_statue_5_door_4,
           move_statue_5_door_1, move_statue_5_door_2,
           move_door_3_table_2, move_door_3_door_1,
           move_door_3_door_4, move_door_3_door_2,
           move_door_4_door_1, move_door_4_door_2,
           move_door_4_door_3, move_door_4_table_1,
           move_table_1_door_4, move_table_2_door_3,
           move_door_1_door_6, 
           move_door_1_door_2, move_door_1_door_3,
           move_door_1_door_4, move_door_1_statue_5,
           move_door_2_door_6,
           move_door_2_door_1, move_door_2_door_3,
           move_door_2_door_4, move_door_2_statue_5,
           move_door_6_chest,
           pickup_key_5_table_5, pickup_key_6_table_6,
           move_bed_1_door_5, move_bed_1_table_5,
           move_bed_1_table_6,
           move_crack_2_door_3,
           move_crack_2_door_4,
           move_crack_2_door_1,
           move_crack_2_door_2,
           move_statue_5_crack_2, move_crack_2_statue_5
           ]





#############################
### Get the Game World up and running

terrain = [[(700,0), (1800, 0), (1800, 1800), (1400, 1800), 
            (1400, 1600), (1500, 1600), (1500, 1700), (1700, 1700),
            (1700, 1400), (1500, 1400), (1500, 1500), (1400, 1500),
            (1400, 1400), (1300, 1400), (1300, 1300), (1700, 1300),
            (1700, 100), (1500, 100), (1500, 400), (1300, 400),
            (1300, 300), (1400, 300), (1400, 100), (1100, 100),
            (1100, 300), (1200, 300), (1200, 400), (1000, 400),
            (1000, 100), (725, 100), (725, 250), (700, 250)
            ],
           [(725, 275), (725, 425), (800, 425),
            (800, 1300), (1200, 1300), (1200, 1400), (1100, 1400),
            (1100, 1500), (1000, 1500), (1000, 1400), 
            (800, 1400),
            (800, 1700), (1000, 1700), (1000, 1600), (1100, 1600),
            (1100, 1800), (700, 1800), (700, 275)
            ],
            [(1000, 500), (1100, 500), (1100, 600), (1400, 600),
             (1400, 500), (1500, 500), (1500, 800), (1400, 800),
             (1400, 700), (1275, 700), (1275, 1000), (1400, 1000),
             (1400, 900), (1500, 900), (1500, 1100), (1000, 1100),
             (1000, 900), (1100, 900), (1100, 1000), (1225, 1000),
             (1225, 700), (1100, 700), (1100, 800), (1000, 800)
            ],
            [(0, 0), (690, 0), (690, 100), (100, 100), (100, 1800),
            (0, 1800)],
            [(690, 425), (300, 425), (300, 600), (400, 600), (400, 500), 
             (600, 500), (600, 700), (300, 700), (300, 900), 
             (400, 900), (400, 800), (600, 800), (600, 1100), (400, 1100),
             (400, 1000), (300, 1000), (300, 1200), (600, 1200),
             (600, 1700), (200, 1700),
             (200, 1800), (690, 1800)]
            
           ]

pathnodes = [(150, 250), (500, 250), (150, 650), (500, 650), (150, 950),
             (500, 950), (150, 1400),
             (150, 1850), (1250, 1850),
             (900, 1550), (1250, 1550), (1600, 1550),
             (900, 1200), (1250, 1200), (1600, 1200),
             (900, 850), (1150, 850), (1350, 850), (1600, 850),
             (900, 450), (1250, 450), (1600, 450),
             (1250, 200)
    ]





nav = GreedyNavigator2()

world = NPCWorld(SEED, (1800, 1800), SCREEN, init_state.propositions)

agent = NPCAgent(AGENT, (SCREEN[0]/2, SCREEN[1]/2), 0, SPEED, world, name='agent')
agent.initial_state = init_state
agent.goal_state = goal_state
agent.actions = actions

world.initializeTerrain(terrain, (0, 0, 0), 4) 
world.setPlayerAgent(agent)

nav.pathnodes = pathnodes
nav.pathnetwork = myBuildPathNetwork(pathnodes, world, agent)

bed_0 = Place("bed_0", "at_{name}_bed_0", ((SCREEN[0]/2)-50, (SCREEN[1]/2)-50), 80, 80, world, color=(255, 255, 0), linewidth=4)
table_3 = Place("table_3", "at_{name}_table_3", (425, 525), 100, 100, world, color=(255, 0, 255), linewidth=4)
table_3.possible_triggers = [pickup_key_3_table_3]
table_4 = Place("table_4", "at_{name}_table_4", (425, 825), 100, 100, world, color=(255, 0, 255), linewidth=4)
table_4.possible_triggers = [pickup_key_4_table_4]
crack_1 = Place("crack in wall 1", "at_{name}_crack_1", (600, 225), 75, 75, world, color=(125, 125, 125), linewidth=4)
crack_1.possible_triggers = [drop_key_3, drop_key_4]#, slide_key_3, slide_key_4]
crack_2 = Place("crack in wall 2", "at_{name}_crack_2", (750, 225), 75, 75, world, color=(125, 125, 125), linewidth=4)
crack_2.possible_triggers = [pickup_key_3_crack_2, pickup_key_4_crack_2]
chest = Place("chest", "at_{name}_chest", (1150, 150), 80, 80, world, color=(255, 255, 0), linewidth=4)
chest.possible_triggers = [pickup_gold]
table_2 = Place("table_2", "at_{name}_table_2", (1125, 725), 80, 80, world, color=(0, 255, 255), linewidth=4)
table_2.possible_triggers = [pickup_key_2_table_2]
table_1 = Place("table_1", "at_{name}_table_1", (1300, 750), 80, 80, world, color=(0, 255, 255), linewidth=4)
table_1.possible_triggers = [pickup_key_1_table_1]
table_7 = Place("table_7", "at_{name}_table_7", (400, 1300), 100, 100, world, color=(0, 255, 255), linewidth=4)
table_7.possible_triggers = [pickup_key_7_table_7]
table_8 = Place("table_8", "at_{name}_table_8", (400, 1450), 100, 100, world, color=(0, 255, 255), linewidth=4)
table_8.possible_triggers = [pickup_key_8_table_8]
door_7 = DoorPlace("door_7", "at_{name}_door_7", (275, 925), 50, 50, world, (350, 900), (350, 1000), color=(255, 0, 255), linewidth=4)
door_7.possible_triggers = [open_door_7]
door_8 = DoorPlace("door_8", "at_{name}_door_8", (275, 625), 50, 50, world, (350, 600), (350, 700), color=(255, 0, 255), linewidth=4)
door_8.possible_triggers = [open_door_8]
table_6 = Place("table_6", "at_{name}_table_6", (850, 1425), 100, 100, world, color=(0, 255, 255), linewidth=4)
table_6.possible_triggers = [pickup_key_6_table_6]
table_5 = Place("table_5", "at_{name}_table_5", (1550, 1425), 100, 100, world, color=(0, 255, 255), linewidth=4)
table_5.possible_triggers = [pickup_key_5_table_5]
door_5 = DoorPlace("door_5", "at_{name}_door_5", (1225, 1425), 50, 50, world, (1200, 1350), (1300, 1350), color=(255, 0, 255), linewidth=4)
door_5.possible_triggers = [open_door_5]
statue_5 = Place("statue_5", "at_{name}_statue_5", (1225, 1175), 50, 50, world, color=(125, 125, 125), linewidth=4)
door_3 = DoorPlace("door_3", "at_{name}_door_3", (950, 825), 50, 50, world, (1050, 800), (1050, 900), color=(255, 0, 255), linewidth=4)
door_3.possible_triggers = [open_door_3]
door_4 = DoorPlace("door_4", "at_{name}_door_4", (1500, 825), 50, 50, world, (1450, 800), (1450, 900), color=(255, 0, 255), linewidth=4)
door_4.possible_triggers = [open_door_4]
door_6 = DoorPlace("door_6", "at_{name}_door_6", (1225, 375), 50, 50, world, (1200, 350), (1300, 350), color=(255, 0, 255), linewidth=4)
door_6.possible_triggers = [open_door_6]
door_1 = DoorPlace("door_1", "at_{name}_door_1", (950, 425), 50, 50, world, (1050, 400), (1050, 500), color=(255, 0, 255), linewidth=4)
door_1.possible_triggers = [open_door_1]
door_2 = DoorPlace("door_2", "at_{name}_door_2", (1500, 425), 50, 50, world, (1450, 400), (1450, 500), color=(255, 0, 255), linewidth=4)
door_2.possible_triggers = [open_door_2]
bed_1 = Place("bed_1", "at_{name}_door_1", (1225, 1600), 100, 100, world, color=(255, 255, 0), linewidth=4)



world.add_place(bed_0)
world.add_place(table_3)
world.add_place(table_4)
world.add_place(crack_1)
world.add_place(crack_2)
world.add_place(chest)
world.add_place(table_2)
world.add_place(table_1)
world.add_place(table_7)
world.add_place(table_8)
world.add_place(door_7)
world.add_place(door_8)
world.add_place(table_5)
world.add_place(table_6)
world.add_place(door_5)
world.add_place(statue_5)
world.add_place(door_3)
world.add_place(door_4)
world.add_place(door_6)
world.add_place(door_1)
world.add_place(door_2)
world.add_place(bed_1)

nav.setWorld(world)
agent.setNavigator(nav)

for n in pathnodes:
  drawCross(world.debug, n)
nav.drawPathNetwork(world.debug)

npc = NPCAgent(ELITE, bed_1.position, 0, SPEED, world, name='npc')
npc.initial_state = init_state
npc.goal_state = goal_state
npc.actions = actions
npc.setNavigator(cloneAStarNavigator(nav))
world.addNPC(npc)

agent.compute_heuristic = lambda *args: 0
npc.compute_heuristic = lambda *args: 0
agent.start()
npc.start()

world.debugging = True
world.run()