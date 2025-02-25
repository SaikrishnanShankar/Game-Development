
'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
''' 

from collections import defaultdict, deque
from itertools import combinations
import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

#helper functions

#finds if a point is too close to the obstacle
def is_too_close_to_obstacles(point, buffer_distance, obstacles):
        for obstacle in obstacles:
            if obstacle.pointInside(point) or min(
                [minimumDistance(line, point) for line in obstacle.getLines()]
            ) < buffer_distance:
                return True
        return False


#finds if an edge is valid
def edge_is_valid(edge, obstacles, agent, obstacle_lines):
	if rayTraceWorld(edge[0], edge[1], obstacle_lines) is not None:
		return False
	buffer_distance = 1* agent.getMaxRadius()
	num_samples = 10  
	x1, y1 = edge[0]
	x2, y2 = edge[1]
	for i in range(num_samples + 1):
		t = i / num_samples
		sample_point = (x1 + t * (x2 - x1), y1 + t * (y2 - y1)) 
		for obstacle in obstacles:
			if min([minimumDistance(line, sample_point) for line in obstacle.getLines()]) < buffer_distance:
				return False
	return True


def myCreatePathNetwork(world, agent=None):
    nodes = []
    edges = []
    polys = []

    obstacles = world.getObstacles()
    obstacle_lines = world.getLinesWithoutBorders()

    # Generate Voronoi points from obstacle vertices
    points = world.getPoints()
    candidate_nodes = set()
    for point1, point2 in combinations(points, 2):
        midpoint = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
        if not is_too_close_to_obstacles(midpoint, 1 * agent.getMaxRadius(), obstacles):
            if len(candidate_nodes) < 99:
                candidate_nodes.add(midpoint)

    nodes = list(candidate_nodes)

    for node1, node2 in combinations(nodes, 2):
        if edge_is_valid((node1, node2), obstacles, agent, obstacle_lines) and rayTraceWorldNoEndPoints(node1, node2, edges) is None:
            edges.append((node1, node2))

    # Remove the smaller component if the graph has two components
    nodes, edges = remove_smaller_component(nodes, edges)

    return nodes, edges, polys


def remove_smaller_component(nodes, edges):
    graph = defaultdict(list)
    for edge in edges:
        graph[edge[0]].append(edge[1])
        graph[edge[1]].append(edge[0])

    # Find connected components using BFS
    visited = set()
    components = []

    def bfs(start_node):
        queue = deque([start_node])
        component = set()
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                component.add(node)
                queue.extend(graph[node])
        return component

    for node in nodes:
        if node not in visited:
            component = bfs(node)
            components.append(component)

    # If there are exactly two components, remove the smaller one
    if len(components) == 2:
        smaller_component = min(components, key=len)
        nodes = [node for node in nodes if node not in smaller_component]
        edges = [edge for edge in edges if edge[0] not in smaller_component and edge[1] not in smaller_component]

    return nodes, edges