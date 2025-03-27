from planner import *

############################
### Goal state and init state

goal_state = State(['a_on_b', 'b_on_c'])
init_state = State(["a_on_table", "b_on_table", 'c_on_table',
	                 'a_clear', 'b_clear', 'c_clear'])

#########################
### ACTIONS

move_a_from_table_to_b = Action('move_a_from_table_to_b', 
					            preconditions = ["a_on_table", "a_clear", "b_clear"], 
					            add_list = ["a_on_b"], 
					            delete_list = ["a_on_table", "b_clear"])
move_a_from_table_to_c = Action('move_a_from_table_to_c', 
					            preconditions = ["a_on_table", "a_clear", "c_clear"], 
					            add_list = ["a_on_c"], 
					            delete_list = ["a_on_table", "c_clear"])
move_a_from_b_to_c = Action('move_a_from_b_to_c', 
					            preconditions = ["a_on_b", "a_clear", "c_clear"], 
					            add_list = ["a_on_c", "b_clear"], 
					            delete_list = ["a_on_b", "c_clear"])
move_a_from_c_to_b = Action('move_a_from_c_to_b', 
					            preconditions = ["a_on_c", "a_clear", "b_clear"], 
					            add_list = ["a_on_b", "c_clear"], 
					            delete_list = ["a_on_c", "b_clear"])
move_a_from_b_to_table = Action('move_a_from_b_to_table', 
					            preconditions = ["a_on_b", "a_clear"], 
					            add_list = ["a_on_table", "b_clear"], 
					            delete_list = ["a_on_b"])
move_a_from_c_to_table = Action('move_a_from_c_to_table', 
					            preconditions = ["a_on_c", "a_clear"], 
					            add_list = ["a_on_table", "c_clear"], 
					            delete_list = ["a_on_c"])

move_b_from_table_to_a = Action('move_b_from_table_to_a', 
					            preconditions = ["b_on_table", "b_clear", "a_clear"], 
					            add_list = ["b_on_a"], 
					            delete_list = ["b_on_table", "a_clear"])
move_b_from_table_to_c = Action('move_b_from_table_to_c', 
					            preconditions = ["b_on_table", "b_clear", "c_clear"], 
					            add_list = ["b_on_c"], 
					            delete_list = ["b_on_table", "c_clear"])
move_b_from_a_to_c = Action('move_b_from_a_to_c', 
					            preconditions = ["b_on_a", "b_clear", "c_clear"], 
					            add_list = ["b_on_c", "a_clear"], 
					            delete_list = ["b_on_a", "c_clear"])
move_b_from_c_to_a = Action('move_b_from_c_to_a', 
					            preconditions = ["b_on_c", "b_clear", "a_clear"], 
					            add_list = ["b_on_a", "c_clear"], 
					            delete_list = ["b_on_c", "a_clear"])
move_b_from_a_to_table = Action('move_b_from_a_to_table', 
					            preconditions = ["b_on_a", "b_clear"], 
					            add_list = ["b_on_table", "a_clear"], 
					            delete_list = ["b_on_a"])
move_b_from_c_to_table = Action('move_b_from_c_to_table', 
					            preconditions = ["b_on_c", "b_clear"], 
					            add_list = ["b_on_table", "c_clear"], 
					            delete_list = ["b_on_c"])

move_c_from_table_to_a = Action('move_c_from_table_to_a', 
					            preconditions = ["c_on_table", "c_clear", "a_clear"], 
					            add_list = ["c_on_a"], 
					            delete_list = ["c_on_table", "a_clear"])
move_c_from_table_to_b = Action('move_c_from_table_to_b', 
					            preconditions = ["c_on_table", "c_clear", "b_clear"], 
					            add_list = ["c_on_b"], 
					            delete_list = ["c_on_table", "b_clear"])
move_c_from_a_to_b = Action('move_c_from_a_to_b', 
					            preconditions = ["c_on_a", "c_clear", "b_clear"], 
					            add_list = ["c_on_b", "a_clear"], 
					            delete_list = ["c_on_a", "b_clear"])
move_c_from_b_to_a = Action('move_c_from_b_to_a', 
					            preconditions = ["c_on_b", "c_clear", "a_clear"], 
					            add_list = ["c_on_a", "b_clear"], 
					            delete_list = ["c_on_b", "a_clear"])
move_c_from_a_to_table = Action('move_c_from_a_to_table', 
					            preconditions = ["c_on_a", "c_clear"], 
					            add_list = ["c_on_table", "a_clear"], 
					            delete_list = ["c_on_a"])
move_c_from_b_to_table = Action('move_c_from_b_to_table', 
					            preconditions = ["c_on_b", "c_clear"], 
					            add_list = ["c_on_table", "b_clear"], 
					            delete_list = ["c_on_b"])

actions = [move_a_from_table_to_b,
		   move_a_from_table_to_c,
		   move_a_from_b_to_c,
		   move_a_from_c_to_b,
		   move_a_from_b_to_table,
   		   move_a_from_c_to_table,
		   move_b_from_table_to_a,
		   move_b_from_table_to_c,
		   move_b_from_a_to_c,
		   move_b_from_c_to_a,
		   move_b_from_a_to_table,
		   move_b_from_c_to_table,
		   move_c_from_table_to_a,
		   move_c_from_table_to_b,
		   move_c_from_a_to_b,
		   move_c_from_b_to_a,
		   move_c_from_a_to_table,
		   move_c_from_b_to_table
		   ]

########################
### TESTS

state1 = State(["a_on_table", "c_on_table", "b_on_c", "a_clear", "b_clear"])
state2 = State(["a_on_table", "b_on_table", "c_on_table", "a_clear", "b_clear", "c_clear"])
state3 = State(["a_on_c", "b_on_table", "c_on_table", "a_clear", "b_clear"])
state4 = State(["a_on_table", "b_on_a", "c_on_b", "c_clear"])
state5 = State(["b_on_table", "a_on_b", "c_on_a", "c_clear"])

tests = [state1, state2, state3, state4, state5]

#############################
### Testing planner without heuristic

print("TESTING astar without heuristic")

for n, state in enumerate(tests):
	print("TEST", n)
	the_planner = Planner()
	the_planner.compute_heuristic = lambda *args: 0
	the_planner.initial_state = state
	the_planner.goal_state = goal_state
	the_planner.actions = actions

	plan, closed = the_planner.astar(state, goal_state, actions[::-1])
	for act in plan:
		print(act.name)
	print("states visited", len(closed))


############################
### Test the heuristic


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

	plan, closed = the_planner.astar(state, goal_state, actions[::-1])
	for act in plan:
		print(act.name)
	print("states visited", len(closed))
