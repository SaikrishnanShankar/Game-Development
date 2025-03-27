from planner import *


#############################
### init state and goal state

init_state = State(propositions=['at_npc_bed_0', 
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
                                 'path_bed_0_door_5',
                                 'path_bed_0_table_5', 'path_bed_0_table_6'
                                 'path_table_7_table_8', 'path_table_7_crack_1',
                                 'path_table_7_door_7', 'path_table_7_door_8',
                                 'path_table_7_door_5',
                                 'path_table_7_table_5', 'path_table_7_table_6',
                                 'path_door_7_crack_1', 'path_door_7_door_8',
                                 'path_door_7_table_7', 'path_door_7_table_8',
                                 'path_door_7_door_5',
                                 'path_door_7_table_5', 'path_door_7_table_6'
                                 'path_table_8_table_7', 'path_table_8_crack_1',
                                 'path_table_8_door_7', 'path_table_8_door_8',
                                 'path_table_8_door_5',
                                 'path_table_8_table_5', 'path_table_8_table_6',
                                 'path_door_8_crack_1', 'path_door_8_door_7',
                                 'path_door_8_table_7', 'path_door_8_table_8',
                                 'path_door_8_door_5',
                                 'path_door_8_table_5', 'path_door_8_table_6',
                                 'path_table_5_table_6', 'path_table_5_door_5',
                                 'path_table_6_table_5', 'path_table_6_door_5',
                                 'path_door_5_table_5', 'path_door_5_table_6',
                                 'path_statue_5_door_3', 'path_statue_5_door_4',
                                 'path_statue_5_door_1', 'path_statue_5_door_2',
                                 'path_door_3_door_1', 'path_door_3_door_2',
                                 'path_door_3_door_4',
                                 'path_door_4_door_3', 'path_door_4_door_1',
                                 'path_door_4_door_2',
                                 # 'path_bed_1_table_5', 'path_bed_1_table_6', 
                                 # 'path_bed_1_door_5',
                                 'path_statue_5_crack_2', 'path_crack_2_statue_5',
                                 'path_crack_2_door_3',
                                 'path_crack_2_door_4'
                                 'path_crack_2_door_1', 'path_crack_2_door_2',
                                 'path_door_1_door_2', 'path_door_1_door_3',
                                 'path_door_1_door_4', 'path_door_1_statue_5',
                                 'path_door_2_door_3', 'path_door_2_statue_5',
                                 'path_door_2_door_4', 'path_door_2_door_1'
                                 ])
goal_state = State(propositions=['has_npc_gold'])

#######################
### ACTIONS

### PICKUP
pickup_key_3_table_3 = Action('pickup_key_3_table_3', 
                                    preconditions=['at_npc_table_3', 'at_key_3_table_3'],
                                    add_list=['has_npc_key_3'], 
                                    delete_list=['at_key_3_table_3'])
pickup_key_4_table_4 = Action('pickup_key_4_table_4', 
                                    preconditions=['at_npc_table_4', 'at_key_4_table_4'],
                                    add_list=['has_npc_key_4'], 
                                    delete_list=['at_key_4_table_4'])
pickup_key_7_table_7 = Action('pickup_key_7_table_7', 
                                    preconditions=['at_npc_table_7', 'at_key_7_table_7'],
                                    add_list=['has_npc_key_7'], 
                                    delete_list=['at_key_7_table_7'])
pickup_key_8_table_8 = Action('pickup_key_8_table_8', 
                                    preconditions=['at_npc_table_8', 'at_key_8_table_8'],
                                    add_list=['has_npc_key_8'], 
                                    delete_list=['at_key_8_table_8'])
pickup_key_5_table_5 = Action('pickup_key_5_table_5', 
                                    preconditions=['at_npc_table_5', 'at_key_5_table_5'],
                                    add_list=['has_npc_key_5'], 
                                    delete_list=['at_key_5_table_5'])
pickup_key_6_table_6 = Action('pickup_key_6_table_6', 
                                    preconditions=['at_npc_table_6', 'at_key_6_table_6'],
                                    add_list=['has_npc_key_6'], 
                                    delete_list=['at_key_6_table_6'])
pickup_key_1_table_1 = Action('pickup_key_1_table_1', 
                                    preconditions=['at_npc_table_1', 'at_key_1_table_1'],
                                    add_list=['has_npc_key_1'], 
                                    delete_list=['at_key_1_table_1'])
pickup_key_2_table_2 = Action('pickup_key_2_table_2', 
                                    preconditions=['at_npc_table_2', 'at_key_2_table_2'],
                                    add_list=['has_npc_key_2'], 
                                    delete_list=['at_key_2_table_2'])
pickup_key_3_crack_2 = Action('pickup_key_3_crack_2', 
                                    preconditions=['at_npc_crack_2', 'at_key_3_crack_2'],
                                    add_list=['has_npc_key_3'], 
                                    delete_list=['at_key_3_crack_2'])
pickup_key_4_crack_2 = Action('pickup_key_4_crack_2', 
                                    preconditions=['at_npc_crack_2', 'at_key_4_crack_2'],
                                    add_list=['has_npc_key_4'], 
                                    delete_list=['at_key_4_crack_2'])
pickup_gold = Action('pickup_gold', 
                                    preconditions=['at_npc_chest', 'at_gold_chest'],
                                    add_list=['has_npc_gold'], 
                                    delete_list=['at_gold_chest'])
### DROP
drop_key_3 = Action('drop_key_3', 
                        preconditions=['has_npc_key_3', 'at_npc_crack_1'],
                        add_list=['at_key_3_crack_2'],
                        delete_list=['has_npc_key_3'])
drop_key_4 = Action('drop_key_4', 
                        preconditions=['has_npc_key_4', 'at_npc_crack_1'],
                        add_list=['at_key_4_crack_2'],
                        delete_list=['has_npc_key_4'])
### OPEN DOORS
open_door_7 = Action('open_door_7',
                            preconditions=['at_npc_door_7', 'has_npc_key_7', 'locked_door_7'],
                            add_list=['path_door_7_table_4', 'path_table_4_door_7', 'unlocked_door_7'],
                            delete_list=['has_npc_key_7', 'locked_door_7'])
open_door_8 = Action('open_door_8',
                            preconditions=['at_npc_door_8', 'has_npc_key_8', 'locked_door_8'],
                            add_list=['path_door_8_table_3', 'path_table_3_door_8', 'unlocked_door_8'],
                            delete_list=['has_npc_key_8', 'locked_door_8'])
open_door_5 = Action('open_door_5',
                            preconditions=['at_npc_door_5', 'has_npc_key_5', 'locked_door_5'],
                            add_list=['path_statue_5_door_5', 'path_door_5_statue_5', 'unlocked_door_5'],
                            delete_list=['has_npc_key_5', 'locked_door_5'])
open_door_6 = Action('open_door_6',
                            preconditions=['at_npc_door_6', 'has_npc_key_6', 'locked_door_6'],
                            add_list=['path_chest_door_5', 'path_door_6_chest', 'unlocked_door_6'],
                            delete_list=['has_npc_key_6', 'locked_door_6'])
open_door_3 = Action('open_door_3',
                            preconditions=['at_npc_door_3', 'has_npc_key_3', 'locked_door_3'],
                            add_list=['path_table_2_door_3', 'path_door_3_table_2', 'unlocked_door_3'],
                            delete_list=['has_npc_key_3', 'locked_door_3'])
open_door_4 = Action('open_door_4',
                            preconditions=['at_npc_door_4', 'has_npc_key_4', 'locked_door_4'],
                            add_list=['path_table_1_door_4', 'path_door_4_table_1', 'unlocked_door_4'],
                            delete_list=['has_npc_key_4', 'locked_door_4'])
open_door_1 = Action('open_door_1',
                            preconditions=['at_npc_door_1', 'has_npc_key_1', 'locked_door_1'],
                            add_list=['path_door_6_door_1', 'path_door_1_door_6', 'unlocked_door_1'],
                            delete_list=['has_npc_key_1', 'locked_door_1'])
open_door_2 = Action('open_door_2',
                            preconditions=['at_npc_door_2', 'has_npc_key_2', 'locked_door_2'],
                            add_list=['path_door_6_door_2', 'path_door_2_door_6', 'unlocked_door_2'],
                            delete_list=['has_npc_key_2', 'locked_door_2'])
### MOVE FROM BED
move_bed_0_table_8 = Action("move_bed_0_table_8", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_table_8'],
                              add_list=['at_npc_table_8'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_table_7 = Action("move_bed_0_table_7", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_table_7'],
                              add_list=['at_npc_table_7'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_door_7 = Action("move_bed_0_door_7", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_door_7'],
                              add_list=['at_npc_door_7'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_door_8 = Action("move_bed_0_door_8", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_door_8'],
                              add_list=['at_npc_door_8'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_crack_1 = Action("move_bed_0_crack_1", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_crack_1'],
                              add_list=['at_npc_crack_1'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_door_5 = Action("move_bed_0_door_5", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_table_5 = Action("move_bed_0_table_5", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_bed_0'])
move_bed_0_table_6 = Action("move_bed_0_table_6", 
                              preconditions=['at_npc_bed_0', 'path_bed_0_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_bed_0'])
### MOVE FROM TABLE 7
move_table_7_table_8 = Action("move_table_7_table_8", 
                              preconditions=['at_npc_table_7', 'path_table_7_table_8'],
                              add_list=['at_npc_table_8'],
                              delete_list=['at_npc_table_7'])
move_table_7_crack_1 = Action("move_table_7_crack_1", 
                              preconditions=['at_npc_table_7', 'path_table_7_crack_1'],
                              add_list=['at_npc_crack_1'],
                              delete_list=['at_npc_table_7'])
move_table_7_door_7 = Action("move_table_7_door_7", 
                              preconditions=['at_npc_table_7', 'path_table_7_door_7'],
                              add_list=['at_npc_door_7'],
                              delete_list=['at_npc_table_7'])
move_table_7_door_8 = Action("move_table_7_door_8", 
                              preconditions=['at_npc_table_7', 'path_table_7_door_8'],
                              add_list=['at_npc_door_8'],
                              delete_list=['at_npc_table_7'])
move_table_7_door_5 = Action("move_table_7_door_5", 
                              preconditions=['at_npc_table_7', 'path_table_7_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_table_7'])
move_table_7_table_5 = Action("move_table_7_table_5", 
                              preconditions=['at_npc_table_7', 'path_table_7_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_table_7'])
move_table_7_table_6 = Action("move_table_7_table_6", 
                              preconditions=['at_npc_table_7', 'path_table_7_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_table_7'])
### MOVE FROM DOOR 7
move_door_7_table_4 = Action("move_door_7_table_4", 
                              preconditions=['at_npc_door_7', 'path_door_7_table_4'],
                              add_list=['at_npc_table_4'],
                              delete_list=['at_npc_door_7'])
move_door_7_crack_1 = Action("move_door_7_crack_1", 
                              preconditions=['at_npc_door_7', 'path_door_7_crack_1'],
                              add_list=['at_npc_crack_1'],
                              delete_list=['at_npc_door_7'])
move_door_7_door_8 = Action("move_door_7_door_8", 
                              preconditions=['at_npc_door_7', 'path_door_7_door_8'],
                              add_list=['at_npc_door_8'],
                              delete_list=['at_npc_door_7'])
move_door_7_table_7 = Action("move_door_7_table_7", 
                              preconditions=['at_npc_door_7', 'path_door_7_table_7'],
                              add_list=['at_npc_table_7'],
                              delete_list=['at_npc_door_7'])
move_door_7_table_8 = Action("move_door_7_table_8", 
                              preconditions=['at_npc_door_7', 'path_door_7_table_8'],
                              add_list=['at_npc_table_8'],
                              delete_list=['at_npc_door_7'])
move_door_7_door_5 = Action("move_door_7_door_5", 
                              preconditions=['at_npc_door_7', 'path_door_7_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_door_7'])
move_door_7_table_5 = Action("move_door_7_table_5", 
                              preconditions=['at_npc_door_7', 'path_door_7_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_door_7'])
move_door_7_table_6 = Action("move_door_7_table_6", 
                              preconditions=['at_npc_door_7', 'path_door_7_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_door_7'])
### MOVE FROM TABLE 8
move_table_8_table_7 = Action("move_table_8_table_7", 
                              preconditions=['at_npc_table_8', 'path_table_8_table_7'],
                              add_list=['at_npc_table_7'],
                              delete_list=['at_npc_table_8'])
move_table_8_crack_1 = Action("move_table_8_crack_1", 
                              preconditions=['at_npc_table_8', 'path_table_8_crack_1'],
                              add_list=['at_npc_crack_1'],
                              delete_list=['at_npc_table_8'])
move_table_8_door_8 = Action("move_table_8_door_8", 
                              preconditions=['at_npc_table_8', 'path_table_8_door_8'],
                              add_list=['at_npc_door_8'],
                              delete_list=['at_npc_table_8'])
move_table_8_door_7 = Action("move_table_8_door_7", 
                              preconditions=['at_npc_table_8', 'path_table_8_door_7'],
                              add_list=['at_npc_door_7'],
                              delete_list=['at_npc_table_8'])
move_table_8_door_5 = Action("move_table_8_door_5", 
                              preconditions=['at_npc_table_8', 'path_table_8_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_table_8'])
move_table_8_table_5 = Action("move_table_8_table_5", 
                              preconditions=['at_npc_table_8', 'path_table_8_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_table_8'])
move_table_8_table_6 = Action("move_table_8_table_6", 
                              preconditions=['at_npc_table_8', 'path_table_8_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_table_8'])
### MOVE FROM DOOR 8
move_door_8_crack_1 = Action("move_door_8_crack_1", 
                              preconditions=['at_npc_door_8', 'path_door_8_crack_1'],
                              add_list=['at_npc_crack_1'],
                              delete_list=['at_npc_door_8'])
move_door_8_table_7 = Action("move_door_8_table_7", 
                              preconditions=['at_npc_door_8', 'path_door_8_table_7'],
                              add_list=['at_npc_table_7'],
                              delete_list=['at_npc_door_8'])
move_door_8_door_7 = Action("move_door_8_door_7", 
                              preconditions=['at_npc_door_8', 'path_door_8_door_7'],
                              add_list=['at_npc_door_7'],
                              delete_list=['at_npc_door_8'])
move_door_8_table_8 = Action("move_door_8_table_8", 
                              preconditions=['at_npc_door_8', 'path_door_8_table_8'],
                              add_list=['at_npc_table_8'],
                              delete_list=['at_npc_door_8'])
move_door_8_table_5 = Action("move_door_8_table_5", 
                              preconditions=['at_npc_door_8', 'path_door_8_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_door_8'])
move_door_8_door_5 = Action("move_door_8_door_5", 
                              preconditions=['at_npc_door_8', 'path_door_8_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_door_8'])
move_door_8_table_6 = Action("move_door_8_table_6", 
                              preconditions=['at_npc_door_8', 'path_door_8_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_door_8'])
move_door_8_table_3 = Action("move_door_8_table_3", 
                              preconditions=['at_npc_door_8', 'path_door_8_table_3'],
                              add_list=['at_npc_table_3'],
                              delete_list=['at_npc_door_8'])

### MOVE FROM TABLE 3
move_table_3_door_8 = Action("move_table_3_door_8", 
                              preconditions=['at_npc_table_3', 'path_table_3_door_8'],
                              add_list=['at_npc_door_8'],
                              delete_list=['at_npc_table_3'])
### MOVE FROM TABLE 4
move_table_4_door_7 = Action("move_table_4_door_7", 
                              preconditions=['at_npc_table_4', 'path_table_4_door_7'],
                              add_list=['at_npc_door_7'],
                              delete_list=['at_npc_table_4'])
### MOVE FROM TABLE 5
move_table_5_table_6 = Action("move_table_5_table_6", 
                              preconditions=['at_npc_table_5', 'path_table_5_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_table_5'])
move_table_5_door_5 = Action("move_table_5_door_5", 
                              preconditions=['at_npc_table_5', 'path_table_5_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_table_5'])
### MOVE FROM TABLE 6
move_table_6_table_5 = Action("move_table_6_table_5", 
                              preconditions=['at_npc_table_6', 'path_table_6_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_table_6'])
move_table_6_door_5 = Action("move_table_6_door_5", 
                              preconditions=['at_npc_table_6', 'path_table_6_door_5'],
                              add_list=['at_npc_door_5'],
                              delete_list=['at_npc_table_6'])
### MOVE FROM DOOR 5
move_door_5_statue_5 = Action("move_door_5_statue_5", 
                              preconditions=['at_npc_door_5', 'path_door_5_statue_5'],
                              add_list=['at_npc_statue_5'],
                              delete_list=['at_npc_door_5'])
move_door_5_table_5 = Action("move_door_5_table_5", 
                              preconditions=['at_npc_door_5', 'path_door_5_table_5'],
                              add_list=['at_npc_table_5'],
                              delete_list=['at_npc_door_5'])
move_door_5_table_6 = Action("move_door_5_table_6", 
                              preconditions=['at_npc_door_5', 'path_door_5_table_6'],
                              add_list=['at_npc_table_6'],
                              delete_list=['at_npc_door_5'])

### MOVE FROM STATUE 5
move_statue_5_door_3 = Action("move_statue_5_door_3", 
                              preconditions=['at_npc_statue_5', 'path_statue_5_door_3'],
                              add_list=['at_npc_door_3'],
                              delete_list=['at_npc_statue_5'])
move_statue_5_door_4 = Action("move_statue_5_door_4", 
                              preconditions=['at_npc_statue_5', 'path_statue_5_door_4'],
                              add_list=['at_npc_door_4'],
                              delete_list=['at_npc_statue_5'])
move_statue_5_crack_2 = Action("move_statue_5_crack_2", 
                              preconditions=['at_npc_statue_5', 'path_statue_5_crack_2'],
                              add_list=['at_npc_crack_2'],
                              delete_list=['at_npc_statue_5'])
move_statue_5_door_1 = MoveAction("move_statue_5_door_1", 
                              preconditions=['at_npc_statue_5', 'path_statue_5_door_1'],
                              add_list=['at_npc_door_1'],
                              delete_list=['at_npc_statue_5'])
move_statue_5_door_2 = MoveAction("move_statue_5_door_2", 
                              preconditions=['at_npc_statue_5', 'path_statue_5_door_2'],
                              add_list=['at_npc_door_2'],
                              delete_list=['at_npc_statue_5'])
### MOVE FROM DOOR 3
move_door_3_table_2 = Action("move_door_3_table_2", 
                              preconditions=['at_npc_door_3', 'path_door_3_table_2'],
                              add_list=['at_npc_table_2'],
                              delete_list=['at_npc_door_3'])
move_door_3_door_1 = Action("move_door_3_door_1", 
                              preconditions=['at_npc_door_3', 'path_door_3_door_1'],
                              add_list=['at_npc_door_1'],
                              delete_list=['at_npc_door_3'])
move_door_3_door_2 = Action("move_door_3_door_2", 
                              preconditions=['at_npc_door_3', 'path_door_3_door_2'],
                              add_list=['at_npc_door_2'],
                              delete_list=['at_npc_door_3'])
move_door_3_door_4 = Action("move_door_3_door_4", 
                              preconditions=['at_npc_door_3', 'path_door_3_door_4'],
                              add_list=['at_npc_door_4'],
                              delete_list=['at_npc_door_3'])
### MOVE FROM DOOR 4
move_door_4_table_1 = Action("move_door_4_table_1", 
                              preconditions=['at_npc_door_4', 'path_door_4_table_1'],
                              add_list=['at_npc_table_1'],
                              delete_list=['at_npc_door_4'])
move_door_4_door_1 = Action("move_door_4_door_1", 
                              preconditions=['at_npc_door_4', 'path_door_4_door_1'],
                              add_list=['at_npc_door_1'],
                              delete_list=['at_npc_door_4'])
move_door_4_door_2 = Action("move_door_4_door_2", 
                              preconditions=['at_npc_door_4', 'path_door_4_door_2'],
                              add_list=['at_npc_door_2'],
                              delete_list=['at_npc_door_4'])
move_door_4_door_3 = Action("move_door_4_door_3", 
                              preconditions=['at_npc_door_4', 'path_door_4_door_3'],
                              add_list=['at_npc_door_3'],
                              delete_list=['at_npc_door_4'])
### MOVE FROM TABLE 2
move_table_2_door_3 = Action("move_table_2_door_3", 
                              preconditions=['at_npc_table_2', 'path_table_2_door_3'],
                              add_list=['at_npc_door_3'],
                              delete_list=['at_npc_table_2'])
### MOVE FROM TABLE 1
move_table_1_door_4 = Action("move_table_1_door_4", 
                              preconditions=['at_npc_table_1', 'path_table_1_door_4'],
                              add_list=['at_npc_door_4'],
                              delete_list=['at_npc_table_1'])
### MOVE FROM DOOR 1
move_door_1_door_6 = Action("move_door_1_door_6", 
                              preconditions=['at_npc_door_1', 'path_door_1_door_6'],
                              add_list=['at_npc_door_6'],
                              delete_list=['at_npc_door_1'])
move_door_1_door_2 = MoveAction("move_door_1_door_2", 
                              preconditions=['at_npc_door_1', 'path_door_1_door_2'],
                              add_list=['at_npc_door_2'],
                              delete_list=['at_npc_door_1'])
move_door_1_door_3 = MoveAction("move_door_1_door_3", 
                              preconditions=['at_npc_door_1', 'path_door_1_door_3'],
                              add_list=['at_npc_door_3'],
                              delete_list=['at_npc_door_1'])
move_door_1_door_4 = MoveAction("move_door_1_door_4", 
                              preconditions=['at_npc_door_1', 'path_door_1_door_4'],
                              add_list=['at_npc_door_4'],
                              delete_list=['at_npc_door_1'])
move_door_1_statue_5 = MoveAction("move_door_1_statue_5", 
                              preconditions=['at_npc_door_1', 'path_door_1_statue_5'],
                              add_list=['at_npc_statue_5'],
                              delete_list=['at_npc_door_1'])
### MOVE FROM DOOR 2
move_door_2_door_6 = Action("move_door_2_door_6", 
                              preconditions=['at_npc_door_2', 'path_door_2_door_6'],
                              add_list=['at_npc_door_6'],
                              delete_list=['at_npc_door_2'])
move_door_2_door_1 = MoveAction("move_door_2_door_1", 
                              preconditions=['at_npc_door_2', 'path_door_2_door_1'],
                              add_list=['at_npc_door_1'],
                              delete_list=['at_npc_door_2'])
move_door_2_door_3 = MoveAction("move_door_2_door_3", 
                              preconditions=['at_npc_door_2', 'path_door_2_door_3'],
                              add_list=['at_npc_door_3'],
                              delete_list=['at_npc_door_2'])
move_door_2_door_4 = MoveAction("move_door_2_door_4", 
                              preconditions=['at_npc_door_2', 'path_door_2_door_4'],
                              add_list=['at_npc_door_4'],
                              delete_list=['at_npc_door_2'])
move_door_2_statue_5 = MoveAction("move_door_2_statue_5", 
                              preconditions=['at_npc_door_2', 'path_door_2_statue_5'],
                              add_list=['at_npc_statue_5'],
                              delete_list=['at_npc_door_2'])
### MOVE FROM DOOR 6
move_door_6_chest = Action("move_door_6_chest", 
                              preconditions=['at_npc_door_6', 'path_door_6_chest'],
                              add_list=['at_npc_chest'],
                              delete_list=['at_npc_door_6'])
### MOVE FROM BED 1
# move_bed_1_door_5 = Action("move_bed_1_door_5", 
#                               preconditions=['at_npc_bed_1', 'path_bed_1_door_5'],
#                               add_list=['at_npc_door_5'],
#                               delete_list=['at_npc_bed_1'])
# move_bed_1_table_5 = Action("move_bed_1_table_5", 
#                               preconditions=['at_npc_bed_1', 'path_bed_1_table_5'],
#                               add_list=['at_npc_table_5'],
#                               delete_list=['at_npc_bed_1'])
# move_bed_1_table_6 = Action("move_bed_1_table_6", 
#                               preconditions=['at_npc_bed_1', 'path_bed_1_table_6'],
#                               add_list=['at_npc_table_6'],
#                               delete_list=['at_npc_bed_1'])
### MOVE FROM CRACK 2
move_crack_2_door_3 = Action("move_crack_2_door_3", 
                              preconditions=['at_npc_crack_2', 'path_crack_2_door_3'],
                              add_list=['at_npc_door_3'],
                              delete_list=['at_npc_crack_2'])
move_crack_2_door_4 = Action("move_crack_2_door_4", 
                              preconditions=['at_npc_crack_2', 'path_crack_2_door_4'],
                              add_list=['at_npc_door_4'],
                              delete_list=['at_npc_crack_2'])
move_crack_2_door_1 = MoveAction("move_crack_2_door_1", 
                              preconditions=['at_npc_crack_2', 'path_crack_2_door_1'],
                              add_list=['at_npc_door_1'],
                              delete_list=['at_npc_crack_2'])
move_crack_2_door_2 = MoveAction("move_crack_2_door_2", 
                              preconditions=['at_npc_crack_2', 'path_crack_2_door_2'],
                              add_list=['at_npc_door_2'],
                              delete_list=['at_npc_crack_2'])
move_crack_2_statue_5 = MoveAction("move_crack_2_statue_5", 
                              preconditions=['at_npc_crack_2', 'path_crack_2_statue_5'],
                              add_list=['at_npc_statue_5'],
                              delete_list=['at_npc_crack_2'])

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
           move_bed_0_door_5,
           move_bed_0_table_5, move_bed_0_table_6,
           move_door_7_crack_1, move_table_7_door_7,
           move_table_7_table_8, move_table_7_door_8,
           move_table_7_door_5,
           move_table_7_table_5, move_table_7_table_6,
           move_table_8_table_7, move_table_8_door_7,
           move_table_8_crack_1, move_table_8_door_8,
           move_table_8_door_5,
           move_table_8_table_5, move_table_8_table_6,
           move_door_7_crack_1, move_door_7_table_4,
           move_door_7_door_5,
           move_door_7_table_7, move_door_7_table_8,
           move_door_7_door_8,
           move_door_7_table_5, move_door_7_table_6,
           move_door_8_crack_1, move_door_8_table_3,
           move_door_8_door_7, 
           move_door_8_door_5,
           move_door_8_table_5, move_door_8_table_6,
           move_table_3_door_8, 
           move_table_4_door_7,
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
           # move_bed_1_door_5, move_bed_1_table_5,
           # move_bed_1_table_6,
           move_crack_2_door_3,
           move_crack_2_door_4,
           move_crack_2_door_1,
           move_crack_2_door_2,
           move_statue_5_crack_2, move_crack_2_statue_5
           ]

#######################
### TESTS

state5 = init_state
state4 = list(init_state.propositions)[:]
state4.remove('at_key_3_table_3')
state4.append('at_key_3_crack_2')
state4 = State(state4)
state3 = list(init_state.propositions)[:]
state3.remove('at_key_4_table_4')
state3.append('at_key_4_crack_2')
state3 = State(state3)
state2 = list(init_state.propositions)[:]
state2.remove('at_key_4_table_4')
state2.append('has_npc_key_4')
state2 = State(state2)
state1 = list(init_state.propositions)[:]
state1.remove('at_key_3_table_3')
state1.append('has_npc_key_3')
state1 = State(state1)
state0 = list(filter(lambda p: 'at_key' not in p, list(init_state.propositions)))
state0 = state0 + ['has_npc_key_' + str(n) for n in range(1, 9)]
state0 = State(state0)

tests = [state0, state1, state2, state3, state4, state5]

########################
### Testing planner without heuristic

print("TESTING astar without heuristic")


for n, state in enumerate(tests):
     print("TEST", n)
     the_planner = Planner()
     the_planner.compute_heuristic = lambda *args: 0
     the_planner.initial_state = state
     the_planner.goal_state = goal_state
     the_planner.actions = actions

     plan, closed = the_planner.astar(state, goal_state, actions)
     for act in plan:
          print(act.name)
     print("states visited", len(closed))

#####################
### Testing heuristic

print("TESTING compute_heuristic")


the_planner = Planner()
for n, state in enumerate(tests):
    h = the_planner.compute_heuristic(state, goal_state, actions)
    print("TEST", n, "h=", h)

