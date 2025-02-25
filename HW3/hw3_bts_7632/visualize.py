import pydot
import graphviz
import re
  
def visualize(root, filename="tree"):
  # Create graphviz root container
  dot = graphviz.Digraph()
  # Queue for exhaustive search through tree
  queue = [(root, None)]
  # Iterate while there are remaining nodes
  while len(queue) > 0:
    # Get current node
    node, parent = queue.pop(0)
    # make label
    label = str(node.id) 
    match = re.search(r'\<class \'[a-zA-Z]+\.([a-zA-Z]+)', str(type(node)))
    if match is not None:
      label = match.group(1)
    # Create the node, with unique identifier for node. Terminal states will be red.
    dot.node(name=str(node.id), label=label + " " + str(node.id), color="red" if len(node.children) == 0 else "black")
    # If there is a parent, create an edge, label it with action name
    if parent is not None:
      dot.edge(str(parent.id), str(node.id))
    # Grab children and add to queue
    for child in node.children:
      queue.append((child, node))
  # Render to file
  dot.render(filename + '.gv', view=False)
  (graph,) = pydot.graph_from_dot_file(filename + '.gv')
  graph.write_png(filename + '.png') 