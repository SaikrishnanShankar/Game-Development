import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from greedynavigator2 import *
from planner import *
from npcworld import *
from mybuildpathnetwork import *

#############################
### init state and goal state

init_state = State(propositions=['at_bed', 'blue_key_at_bed', 'red_key_at_table', 'gold_at_chest', 
                    'red_door_locked', 'blue_door_locked',
                    'path_bed_to_blue_door', 'path_table_to_red_door',
                    'path_blue_door_to_bed', 'path_red_door_to_table'])
goal_state = State(propositions=['has_gold'])

###########################
### ACTIONS


pickup_blue_key = TriggerAction('pickup_blue_key', preconditions=['at_bed', 'blue_key_at_bed'],
    add_list=['has_blue_key'], delete_list=['blue_key_at_bed'])

open_blue_door = DoorAction('open_blue_door', preconditions=['at_blue_door', 'has_blue_key', 'blue_door_locked'],
    add_list=['path_blue_door_to_table', 'path_table_to_blue_door'], delete_list=['blue_door_locked'])

pickup_red_key = TriggerAction('pickup_red_key', preconditions=['at_table', 'red_key_at_table'],
    add_list=['has_red_key'], delete_list=['red_key_at_table'])

open_red_door = DoorAction('open_red_door', preconditions=['at_red_door', 'has_red_key', 'red_door_locked'],
    add_list=['path_red_door_to_chest', 'path_chest_to_red_door'], delete_list=['red_door_locked'])

pickup_gold = TriggerAction('pickup_gold', preconditions=['at_chest', 'gold_at_chest'],
    add_list=['has_gold'], delete_list=['gold_at_chest'])

move_bed_to_blue_door = MoveAction('move_bed_to_blue_door', preconditions=['at_bed', 'path_bed_to_blue_door'],
    add_list=['at_blue_door'], delete_list=['at_bed'])

move_blue_door_to_bed = Action('move_blue_door_to_bed', 
                         preconditions = ['at_blue_door', 'path_blue_door_to_bed'], 
                         add_list = ['at_bed'], 
                         delete_list = ['at_blue_door'])

move_blue_door_to_table = MoveAction('move_blue_door_to_table', preconditions=['at_blue_door', 'path_blue_door_to_table'],
    add_list=['at_table'], delete_list=['at_blue_door'])

move_table_to_blue_door = Action('move_table_to_blue_door', 
                         preconditions = ['at_blue_door', 'path_table_to_blue_door'], 
                         add_list = ['at_blue_door'], 
                         delete_list = ['at_table'])

move_table_to_red_door = MoveAction('move_table_to_red_door', preconditions=['at_table', 'path_table_to_red_door'],
    add_list=['at_red_door'], delete_list=['at_table'])

move_red_door_to_table = Action('move_red_door_to_table', 
                         preconditions = ['at_table', 'path_red_door_to_table'], 
                         add_list = ['at_table'], 
                         delete_list = ['at_red_door'])

move_red_door_to_chest = MoveAction('move_red_door_to_chest', preconditions=['at_red_door', 'path_red_door_to_chest'],
    add_list=['at_chest'], delete_list=['at_red_door'])

move_chest_to_red_door = Action('move_chest_to_red_door', 
                         preconditions = ['at_red_door', 'path_chest_to_red_door'], 
                         add_list = ['at_red_door'], 
                         delete_list = ['at_chest'])

actions = [pickup_blue_key, open_blue_door, pickup_red_key, open_red_door, pickup_gold, 
           move_bed_to_blue_door, move_blue_door_to_table, move_table_to_red_door, move_red_door_to_chest,
           move_blue_door_to_bed, move_table_to_blue_door, move_chest_to_red_door,
           move_red_door_to_table]





#############################
### Get the Game World up and running

terrain = [[(600, 5), (600, 100), (700, 100), (700, 5)],
           [(600, 200), (600, 600), (350, 600), (350, 5), (250, 5), (250, 700), (750, 700), (750, 600), (700, 600), (700, 200)],
           [(850, 600), (1010, 600), (1010, 700), (850, 700)]
           ]

pathnodes = [(500, 500), (500, 150), (800, 150), (800, 500), (800, 740), (150, 740), (150, 150)]


nav = GreedyNavigator2()

world = NPCWorld(SEED, WORLD, SCREEN, init_state.propositions)

agent = NPCAgent(AGENT, (SCREEN[0]/2, SCREEN[1]/2), 0, SPEED, world)
agent.initial_state = init_state
agent.goal_state = goal_state
agent.actions = actions

world.initializeTerrain(terrain, (0, 0, 0), 4) 
world.setPlayerAgent(agent)

nav.pathnodes = pathnodes
nav.pathnetwork = myBuildPathNetwork(pathnodes, world, agent)

bed = Place("bed", "at_bed", (450, 350), 100, 100, world, color=(255, 0, 255), linewidth=4)
bed.possible_triggers = [pickup_blue_key]
blue_door = DoorPlace("blue_door", "at_blue_door", (450, 100), 100, 100, world, (650, 100), (650, 200), color=(0, 0, 255), linewidth=4)
blue_door.possible_triggers = [open_blue_door]
table = Place("table", "at_table", (750, 100), 100, 100, world, color=(0, 255, 0), linewidth=4)
table.possible_triggers = [pickup_red_key]
red_door = DoorPlace("red_door", "at_red_door", (750, 450), 100, 100, world, (750, 650), (850, 650), color=(255, 0, 0), linewidth=4)
red_door.possible_triggers = [open_red_door]
chest = Place("chest", "at_chest", (100, 500), 100, 100, world, color=(0, 255, 255), linewidth=4)
chest.possible_triggers = [pickup_gold]
world.add_place(bed)
world.add_place(blue_door)
world.add_place(table)
world.add_place(red_door)
world.add_place(chest)



nav.setWorld(world)
agent.setNavigator(nav)

for n in pathnodes:
  drawCross(world.debug, n)
nav.drawPathNetwork(world.debug)

agent.start()
print("THE PLAN")
if agent.the_plan is not None:
	for act in agent.the_plan:
		print(act.name)

world.debugging = True
world.run()