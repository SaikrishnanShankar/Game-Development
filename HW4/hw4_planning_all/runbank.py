from planner import *

############################
### Full goal state and initial state

goal_state = State(['has_food', 'has_money'])
init_state = State(["gun_for_sale", "ammo_for_sale", 'bunny_alive', 'money_in_bank', 'dirty'])

###########################
### ACTIONS

buy_gun = Action('buy_gun', 
					preconditions = ["gun_for_sale"], 
					add_list = ["has_gun"], 
					delete_list = ["gun_for_sale"])
buy_ammo = Action('buy_ammo', 
					preconditions = ['ammo_for_sale'], 
					add_list = ['has_ammo'], 
					delete_list = ['ammo_for_sale'])
load_gun = Action('load_gun', 
					preconditions = ['has_gun', 'has_ammo'], 
					add_list = ['gun_loaded'], 
					delete_list = ['has_ammo'])
shoot_bunny = Action('shoot_bunny', 
					preconditions = ['has_gun', 'gun_loaded'], 
					add_list = ['has_food'], 
					delete_list = ['bunny_alive', 'gun_loaded'])
rob_bank = Action('rob_bank', 
					preconditions = ['has_gun', 'gun_loaded', 'money_in_bank'], 
					add_list = ['has_money'], 
					delete_list = ['money_in_bank'])
take_bath = Action('take_bath', 
					preconditions = ['dirty'], 
					add_list = ['wet'], 
					delete_list = ['dirty'])
dry_off = Action('dry_off', 
					preconditions = ['wet'], 
					add_list = [], 
					delete_list = ['wet'])

actions = [buy_gun, buy_ammo, load_gun, shoot_bunny, rob_bank, take_bath, dry_off]

############################
### Tests

state7 = init_state
state6 = State(["has_gun", "ammo_for_sale", 'bunny_alive', 'money_in_bank', 'dirty'])
state5 = State(["gun_for_sale", "has_ammo", 'bunny_alive', 'money_in_bank', 'dirty'])
state4 = State(["has_gun", "has_ammo", 'bunny_alive', 'money_in_bank', 'dirty'])
state3 = State(["has_gun", "gun_loaded", 'bunny_alive', 'money_in_bank', 'dirty'])
state2 = State(["has_gun", 'bunny_alive', 'gun_loaded', 'dirty', 'has_money'])
state1 = State(["has_gun", 'bunny_alive', 'has_food', 'dirty', 'has_money'])

tests = [state1, state2, state3, state4, state5, state6, state7]

#############################
### Testing planner with heuristic

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


############################
### Testing the heuristic


print("TESTING compute_heuristic")

the_planner = Planner()
for n, state in enumerate(tests):
	h = the_planner.compute_heuristic(state, goal_state, actions)
	print("TEST", n, "h=", h)

#############################
### Testing planner with heuristic

print("TESTING astar with heuristic")

for n, state in enumerate(tests):
	print("TEST", n)
	the_planner = Planner()
	the_planner.initial_state = state
	the_planner.goal_state = goal_state
	the_planner.actions = actions

	plan, closed = the_planner.astar(state, goal_state, actions)
	for act in plan:
		print(act.name)
	print("states visited", len(closed))


