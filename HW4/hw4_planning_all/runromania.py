from planner import *

############################

goal_state = State(['at_bucharest'])
init_state = State(["at_arad"])

# Cities in the map
cities = ["arad", "bucharest", "craiova", "dobreta", "eforie", "fagaras",
		  "giurgiu", "hirsova", "iasi", "lugoj", "mehadia", "neamt", "oradea",
		  "pitesti", "rimnicu", "sibiu", "timisoara", "urziceni", "vaslui",
		  "zerind"]
# undirected paths and distances (city1, city2, distance)
paths = [("arad", "zerind", 75), ("arad", "sibiu", 140), ("arad", "timisoara", 118),
		 ("bucharest", "fagaras", 211), ("bucharest", "giurgiu", 90), ("bucharest", "pitesti", 101), ("bucharest", "urziceni", 85),
		 ("craiova", "dobreta", 120), ("craiova", "rimnicu", 146), ("craiova", "pitesti", 138),
		 ("dobreta", "mehadia", 75),
		 ("eforie", "hirsova", 86),
		 ("fagaras", "sibiu", 99), ("fagaras", "bucharest", 211),
		 ("hirsova", "urziceni", 98),
		 ("iasi", "neamt", 87), ("iasi", "vaslui", 92),
		 ("lugoj", "timisoara", 111), ("lugoj", "mehadia", 70),
		 ("oradea", "zerind", 71), ("oradea", "sibiu", 151),
		 ("pitesti", 'rimnicu', 97),
		 ("rimnicu", "sibiu", 80),
		 ("urziceni", "vaslui", 142)
		 ]
# Create actions
actions = []
# Try each pair of cities to see if they are connected
# If so, create an action
for city1 in cities:
	for city2 in cities:
		for path in paths:
			# If there is a path from city1 to city2, create an action
			if (path[0] == city1 and path[1] == city2) or (path[0] == city2 and path[1] == city1):
				# Create an action
				actions.append(Action('move_' + city1 + '_' + city2,
									  preconditions = ['at_' + city1],
									  add_list = ['at_' + city2],
									  delete_list = ['at_' + city1],
									  cost=path[2]))
# This is the straight line heuristic 
# Currently we only have values for the goal of bucharest
straight_lines = {"bucharest": {"arad": 366, 
			                    "bucharest": 0, 
			                    "craiova": 160, 
			                    "dobreta": 242, 
			                    "eforie": 161, 
			                    "fagaras": 176,
		  					    "giurgiu": 77, 
		  					    "hirsova": 151, 
		  					    "iasi": 226, 
		  					    "lugoj": 244, 
		  					    "mehadia": 241, 
		  					    "neamt": 234, 
		  					    "oradea": 380,
		  					    "pitesti": 100, 
		  					    "rimnicu": 193, 
		  					    "sibiu": 253, 
		  					    "timisoara": 329, 
		  					    "urziceni": 80, 
		  					    "vaslui": 199,
		  					    "zerind": 374}
		  					  }

# Use the straight line heurist
def straight_line_heuristic(current_state, goal_state, actions):
	start = list(current_state.propositions)[0].split('_')[1]
	end = list(goal_state.propositions)[0].split('_')[1]
	return straight_lines[end][start]


############################
### Tests

tests = [State(['at_' + city]) for city in cities]

#############################
### Run planner without heuristic

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

##################
### Test planner with straight line heuristic

print("TESTING astar with straight line heuristic")

for n, state in enumerate(tests):
	print("TEST", n)
	the_planner = Planner()
	the_planner.compute_heuristic = straight_line_heuristic
	the_planner.initial_state = state
	the_planner.goal_state = goal_state
	the_planner.actions = actions

	plan, closed = the_planner.astar(state, goal_state, actions[::-1])
	for act in plan:
		print(act.name)
	print("states visited", len(closed))


###################
### Testing compute_heuristic

print("TESTING compute_heuristic")

the_planner = Planner()
for n, state in enumerate(tests):
	h = the_planner.compute_heuristic(state, goal_state, actions)
	print("TEST", n, "h=", h)

##################
### Testing planner with HSP heuristic

print("TESTING astar with HSP heuristic")

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
