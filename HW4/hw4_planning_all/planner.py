from constants import *
from utils import *
from core import *
import pdb
import copy
from functools import reduce

from statesactions import *

import graphviz
import pydot

from functools import reduce

############################
## HELPERS

### Return true if the given state object is a goal. Goal is a State object too.
def is_goal(state, goal):
  return len(goal.propositions.difference(state.propositions)) == 0

### Return true if the given state is in a set of states.
def state_in_set(state, set_of_states):
  for s in set_of_states:
    if s.propositions == state.propositions:
      return True
  return False

### For debugging, print each state in a list of states
def print_states(states):
  for s in states:
    ca = None
    if s.causing_action is not None:
      ca = s.causing_action.name
    print(s.id, s.propositions, ca, s.get_g(), s.get_h(), s.get_f())





############################
### Planner 
###
### The planner knows how to generate a plan using a-star and heuristic search planning.
### It also knows how to execute plans in a continuous, time environment.

class Planner():

  def __init__(self, name = 'agent'):
    self.running = False              # is the planner running?
    self.world = None                 # pointer back to the world
    self.the_plan = []                # the plan (when generated)
    self.initial_state = None         # Initial state (State object)
    self.goal_state = None            # Goal state (State object)
    self.actions = []                 # list of actions (Action objects)
    self.name = name

  ### Start running
  def start(self):
    self.running = True
    
  ### Stop running
  def stop(self):
    self.running = False

  ### Called every tick. Executes the plan if there is one
  def update(self, delta = 0):
    result = False # default return value
    if self.running and len(self.the_plan) > 0:
      # I have a plan, so execute the first action in the plan
      self.the_plan[0].agent = self
      result = self.the_plan[0].execute(delta)
      if result == False:
        # action failed
        print("AGENT FAILED")
        self.the_plan = []
      elif result == True:
        # action succeeded
        done_action = self.the_plan.pop(0)
        print("ACTION", done_action.name, "SUCCEEDED")
        done_action.reset()
    # If the result is None, the action is still executing
    return result

  ### Call back from Action class. Pass through to world
  def check_preconditions(self, preconds):
    if self.world is not None:
      return self.world.check_preconditions(preconds)
    return False

  def update_world(self, add, delete):
    if self.world is not None:
      self.world.update_world(add, delete)

  ### Call back from Action class. Pass through to world
  def get_x_y_for_label(self, label):
    if self.world is not None:
      return self.world.get_x_y_for_label(label)
    return None

  ### Call back from Action class. Pass through to world
  def trigger(self, action):
    if self.world is not None:
      return self.world.trigger(action)
    return False

  ### Generate a plan. Init and goal are State objects. Actions is a list of Action objects
  ### Return the plan and the closed list
  def astar(self, init, goal, actions):
      plan = []    # the final plan
      open = []    # the open list holding State objects
      closed = []  # the closed list (already visited states). Holds state objects
      ### YOUR CODE BELOW HERE
      init.h = 0
      init.g = 0
      open.append(init)
      while len(open) > 0:
        # Find the state with the lowest f value
        current = min(open, key=lambda state: state.get_f())
        open.remove(current)
        if is_goal(current, goal):
          while current.causing_action is not None:
            plan.append(current.causing_action)
            current = current.parent
          plan.reverse()
          return plan, closed
        if not state_in_set(current, closed):
          closed.append(current)
        for action in actions:
          if action.preconditions.issubset(current.propositions):
            new_state = State(current.propositions)
            new_state.propositions.update(action.add_list)
            new_state.propositions.difference_update(action.delete_list)
            new_state.parent = current
            new_state.causing_action = action
            new_state.g = current.g + action.cost
            new_state.h = self.compute_heuristic(new_state, goal, actions)
            if state_in_set(new_state, closed):
              continue
            open.append(new_state)
      ### YOUR CODE ABOVE HERE
      return plan, closed



  ### Compute the heuristic value of the current state using the HSP technique.
  ### Current_state and goal_state are State objects.
  def compute_heuristic(self, current_state, goal_state, actions):
    h = 0
    ### YOUR CODE BELOW HERE
    if is_goal(current_state, goal_state):
      return 0
    
    dummy_start = Action("dummy_start", set(), current_state.propositions, set(), 1)
    dummy_goal = Action("dummy_goal", goal_state.propositions, set(), set(), 0)
    
    all_actions = actions.copy()
    all_actions.append(dummy_start)
    all_actions.append(dummy_goal)
  
    edges = []
    
    for action1 in all_actions:
      for action2 in all_actions:
        if action1 != action2:
          matching_props = action1.add_list.intersection(action2.preconditions)
          for prop in matching_props:
            edges.append((action1, prop, action2))
    adjacency_list = {}
    for edge in edges:
      if edge[0] not in adjacency_list:
        adjacency_list[edge[0]] = []
      adjacency_list[edge[0]].append((edge[1], edge[2]))
    
    proposition_to_dist = {}
    for action in all_actions:
      for prop in action.add_list:
        if prop not in proposition_to_dist:
          proposition_to_dist[prop] = float('inf')
      for prop in action.preconditions:
        if prop not in proposition_to_dist:
          proposition_to_dist[prop] = float('inf')
    for prop in dummy_start.add_list:
      proposition_to_dist[prop] = 0
    
    
    action_to_incoming_edges = {action.name: [] for action in all_actions}
    for edge in edges:
      action_to_incoming_edges[edge[2].name].append((edge[0], edge[1]))
    
    queue = []
    visited = set()
    
    queue.append(dummy_start)
    visited.add(dummy_start.name)
    
    action_distances = {dummy_start.name: 0}
    
    while queue:
      current_action = queue.pop(0)
      current_distance = action_distances.get(current_action.name, 0)
      if current_action.name == dummy_goal.name:
        continue
      for prop, next_action in adjacency_list.get(current_action, []):
        proposition_to_dist[prop] = min(proposition_to_dist[prop], current_distance + current_action.cost)
        maximum_distance = 0
        for _, incoming_prop in action_to_incoming_edges[next_action.name]:
          maximum_distance = max(maximum_distance, proposition_to_dist[incoming_prop])
        if maximum_distance < float('inf'):
          if next_action.name not in visited or action_distances[next_action.name] > maximum_distance:
            queue.append(next_action)
            visited.add(next_action.name)
            action_distances[next_action.name] = maximum_distance
    for _, prop in action_to_incoming_edges[dummy_goal.name]:
      h = max(h, proposition_to_dist[prop])
        ### YOUR CODE ABOVE HERE
    return h

#############################################

def visualize(actions, arcs, prop_distances, filename="graph"):
  # Create graphviz root container
  dot = graphviz.Digraph()
  for action in actions:
    dot.node(name=action.name, label=action.name, color="black")
  for arc in arcs:
    dot.edge(arc[0].name, arc[2].name, label=arc[1] + ' ' + str(prop_distances[arc[1]]))
  # Render to file
  dot.render(filename + '.gv', view=False)
  (graph,) = pydot.graph_from_dot_file(filename + '.gv')
  graph.write_png(filename + '.png') 
