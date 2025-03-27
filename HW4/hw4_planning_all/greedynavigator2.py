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

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *

from queue import PriorityQueue


def distance(p1, p2):
    return (((p2[0]-p1[0])**2) + ((p2[1]-p1[1])**2))**0.5
  
def crossProduct(p1, p2, p3):
    dx1 = p2[0] - p1[0]
    dy1 = p2[1] - p1[1]
    dx2 = p3[0] - p2[0]
    dy2 = p3[1] - p2[1]
    return (dx1*dy2) - (dy1*dx2)
    
def dotProduct(p1, p2):
    return (p1[0]*p2[0]) + (p1[1]*p2[1])
  
def minimumDistance(line, point):
    d2 = distance(line[1], line[0])**2.0
    if d2 == 0.0: 
        return distance(point, line[0])
    # Consider the line extending the segment, parameterized as line[0] + t (line[1] - line[0]).
    # We find projection of point p onto the line. 
    # It falls where t = [(point-line[0]) . (line[1]-line[0])] / |line[1]-line[0]|^2
    p1 = (point[0] - line[0][0], point[1] - line[0][1])
    p2 = (line[1][0] - line[0][0], line[1][1] - line[0][1])
    t = dotProduct(p1, p2) / d2  # numpy.dot(p1, p2) / d2
    if t < 0.0: 
        return distance(point, line[0]) # Beyond the line[0] end of the segment
    elif t > 1.0: 
        return distance(point, line[1]) # Beyond the line[1] end of the segment
    p3 = (line[0][0] + (t * (line[1][0] - line[0][0])), line[0][1] + (t * (line[1][1] - line[0][1]))) # projection falls on the segment
    return distance(point, p3)

# Calc the gradient 'm' of a line between p1 and p2
def calculateGradient(p1, p2):
  
    # Ensure that the line is not vertical
    if (p1[0] != p2[0]):
        m = (p1[1] - p2[1]) / float(p1[0] - p2[0])
        return m
    else:
        return None

def calculateYAxisIntersect(p, m):
    return  p[1] - (m * p[0])

def getIntersectPoint(p1, p2, p3, p4):
    m1 = calculateGradient(p1, p2)
    m2 = calculateGradient(p3, p4)
      
    # See if the the lines are parallel
    if (m1 != m2):
        # Not parallel
      
        # See if either line is vertical
        if (m1 is not None and m2 is not None):
            # Neither line vertical           
            b1 = calculateYAxisIntersect(p1, m1)
            b2 = calculateYAxisIntersect(p3, m2)  
            x = (b2 - b1) / float(m1 - m2)       
            y = (m1 * x) + b1           
        else:
            # Line 1 is vertical so use line 2's values
            if (m1 is None):
                b2 = calculateYAxisIntersect(p3, m2)   
                x = p1[0]
                y = (m2 * x) + b2
            # Line 2 is vertical so use line 1's values               
            elif (m2 is None):
                b1 = calculateYAxisIntersect(p1, m1)
                x = p3[0]
                y = (m1 * x) + b1           
            else:
                assert false
              
        return ((x,y),)
    else:
        # Parallel lines with same 'b' value must be the same line so they intersect
        # everywhere. In this case we return the start and end points of both lines
        # the calculateIntersectPoint method will sort out which of these points
        # lays on both line segments
        b1, b2 = None, None # vertical lines have no b value
        if m1 is not None:
            b1 = calculateYAxisIntersect(p1, m1)
          
        if m2 is not None:   
            b2 = calculateYAxisIntersect(p3, m2)
      
        # If these parallel lines lay on one another   
        if b1 == b2:
            return p1,p2,p3,p4
        else:
            return None  

def between(p, p1, p2):
    return p + EPSILON >= min(p1, p2) and p - EPSILON <= max(p1, p2)

def calculateIntersectPoint(p1, p2, p3, p4):
    p = getIntersectPoint(p1, p2, p3, p4)
    if p is not None:
        p = p[0]
        if between(p[0], p1[0], p2[0]) and between(p[1], p1[1], p2[1]) and between(p[0], p3[0], p4[0]) and between(p[1], p3[1], p4[1]):
            return p
    return None


def rayTrace(p1, p2, line):
    return calculateIntersectPoint(line[0], line[1], p1, p2)

def rayTraceWorld(p1, p2, worldLines):
    for l in worldLines:
        hit = rayTrace(p1, p2, l)
        if hit != None:
            return hit
    return None


###############################
### AStarNavigator2
###
### Creates a path node network and implements the A* algorithm to create a path to the given destination.
            
class GreedyNavigator2(NavMeshNavigator):


                
    ### Finds the shortest path from the source to the destination using A*.
    ### self: the navigator object
    ### source: the place the agent is starting from (i.e., its current location)
    ### dest: the place the agent is told to go to
    def computePath(self, source, dest):
        self.setPath(None)
        ### Make sure the next and dist matrices exist
        if self.agent != None and self.world != None: 
            self.source = source
            self.destination = dest
            ### Step 1: If the agent has a clear path from the source to dest, then go straight there.
            ### Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
            ### Tell the agent to move to dest
            if clearShot(source, dest, self.world.getLinesWithoutBorders(), self.world.getPoints(), self.agent):
                self.agent.moveToTarget(dest)
            else:
                ### Step 2: If there is an obstacle, create the path that will move around the obstacles.
                ### Find the path nodes closest to source and destination.
                start = getOnPathNetwork(source, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
                end = getOnPathNetwork(dest, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
                if start != None and end != None:
                    ### Remove edges from the path network that intersect gates
                    newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates(), self.world)
                    closedlist = []
                    ### Create the path by traversing the pathnode network until the path node closest to the destination is reached
                    path, closedlist = greedy_astar(start, end, newnetwork)
                    if path is not None and len(path) > 0:
                        ### Determine whether shortcuts are available
                        path = shortcutPath(source, dest, path, self.world, self.agent)
                        ### Store the path by calling self.setPath()
                        self.setPath(path)
                        if self.path is not None and len(self.path) > 0:
                            ### Tell the agent to move to the first node in the path (and pop the first node off the path)
                            first = self.path.pop(0)
                            self.agent.moveToTarget(first)
        return None
        
    ### Called when the agent gets to a node in the path.
    ### self: the navigator object
    def checkpoint(self):
        myCheckpoint(self)
        return None

    ### This function gets called by the agent to figure out if some shortcuts can be taken when traversing the path.
    ### This function should update the path and return True if the path was updated.
    def smooth(self):
        return mySmooth(self)

    def update(self, delta):
        myUpdate(self, delta)


### Removes any edge in the path network that intersects a worldLine (which should include gates).
def unobstructedNetwork(network, worldLines, world):
    newnetwork = []
    for l in network:
        hit = rayTraceWorld(l[0], l[1], worldLines)
        if hit == None:
            newnetwork.append(l)
    return newnetwork



### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
    ## YOUR CODE GOES BELOW HERE ###
    threshold = agent.getMaxRadius()
    collide = rayTraceWorld(p1, p2, worldLines)
    if collide is None:
        tooclose = False
        for p in worldPoints:
            if minimumDistance((p1, p2), p) < threshold:
                tooclose = True
        if not tooclose:
            return True
    ## YOUR CODE GOES ABOVE HERE ###
    return False

### Given a location, find the closest pathnode that the agent can get to without collision
### agent: the agent
### location: the location to check from (typically where the agent is starting from or where the agent wants to go to) as an (x, y) point
### pathnodes: a list of pathnodes, where each pathnode is an (x, y) point
### world: pointer to the world
def getOnPathNetwork(location, pathnodes, worldLines, agent):
    node = None
    ### YOUR CODE GOES BELOW HERE ###
    dist = INFINITY
    for pathnode in pathnodes:
        if rayTraceWorld(location, pathnode, worldLines) == None:
            maxRadius = agent.getMaxRadius()
            flag = True
            for worldLine in worldLines:
                if minimumDistance(worldLine, location) > maxRadius and minimumDistance(worldLine, pathnode) > maxRadius:
                    pass
                else:
                    flag = False
                    break
            if flag:
                d = distance(location, pathnode)
                if node == None or d < dist:
                    node = pathnode
                    dist = d
    ### YOUR CODE GOES ABOVE HERE ###
    return node

#PART OF SOLUTION
# def insert(x, list, func = lambda x: x):
#   for i in range(len(list)):
#       if func(x) < func(list[i]):
#           list.insert(i, x)
#           return list
#   list.append(x)
#   return list

def insert_sort(new_item, the_list, criterion_fn = lambda x: x):
    i = 0
    for item in the_list:
        if criterion_fn(new_item) < criterion_fn(item):
            break
        i = i + 1
    return the_list[:i] + [new_item] + the_list[i:]

### Implement the a-star algorithm
### Given:
### Init: a pathnode (x, y) that is part of the pathnode network
### goal: a pathnode (x, y) that is part of the pathnode network
### network: the pathnode network
### Return two values: 
### 1. the path, which is a list of states that are connected in the path network
### 2. the closed list, the list of pathnodes visited during the search process
def greedy_astar(init, goal, network):
    open = [init]
    closed = set()
    current = init
    parents = {current: None}
    path = []
    count = 0
    while current != goal and len(open) > 0:
        current = open.pop(0)
        closed.add(current)
        successors = get_successors(current, network)
        for s in successors:
            if s not in closed:
                parents[s] = current
                # open.append(s)
                open = insert_sort(s, open, lambda s: h_func(s, goal))
        count = count + 1
    if current == goal:
        cur = current
        while parents[cur] is not None:
            cur = parents[cur]
            path.append(cur)
        path = list(reversed(path)) + [goal]
    # path = []
    # open = []
    # closed = []
    # ### YOUR CODE GOES BELOW HERE ###
    # #print("astar")
    # ### Node: (state, g, h, parent)
    # init = (init, 0, distance(init, goal), None)
    # closed = set()
    # nodes = set()
    # open = [init]
    # current = init
    
    # # search
    # while current is not None and current[0] != goal and len(open) > 0:
    #   closed.add(current[0])
    #   nodes.add(current)
    #   open.pop(0)
    #   suc = successors(current, network, goal)
    #   for s in suc:
    #       if s[0] not in closed:
    #           insert(s, open, lambda x:x[1]+x[2])
    #   if len(open) > 0:
    #       current = open[0]
    #   else:
    #       current = None

    # # Reconstruct path
    # if current is not None:
    #   while current[3] is not None:
    #       path.append(current[0])
    #       parent = current[3]
    #       for n in list(nodes):
    #           if parent == n[0]:
    #               current = n
    #               break
    #   path.append(current[0])
    #   path.reverse()
    # closed = list(closed)
    ### YOUR CODE GOES ABOVE HERE ###
    return path, closed


# def successors(node, network, goal):
#   states = []
#   for l in network:
#       if l[0] == node[0]:
#           states.append((l[1], node[1]+distance(l[0], l[1]), distance(l[1], goal), node[0]))
#       elif l[1] == node[0]:
#           states.append((l[0], node[1]+distance(l[0], l[1]), distance(l[0], goal), node[0]))
#   return states

def get_successors(state, network):
    successors = []
    for edge in network:
        if edge[0] == state:
            successors.append(edge[1])
        elif edge[1] == state:
            successors.append(edge[0])
    return successors

def h_func(state, goal):
    return distance(state, goal)


def myUpdate(nav, delta):
    ### YOUR CODE GOES BELOW HERE ###
    # if nav.getPath() is not None:
    #   gates = nav.world.getGates()
    #   last = nav.agent.getLocation()
    #   for p in nav.getPath() + [nav.getDestination()]:
    #       if last is not None:
    #           hit = rayTraceWorld(last, p, gates)
    #           if hit is not None:
    #               #nav.computePath(nav.agent.getLocation(), nav.getDestination())
    #               nav.setPath(None)
    #               nav.agent.stopMoving()
    #               return None
    #       last = p
        ### YOUR CODE GOES ABOVE HERE ###
        return None




def myCheckpoint(nav):
    return None





### PART OF SOLUTION
def myCheckForShortcut(nav):
    # if nav.path != None and nav.agent.moveTarget != nav.destination:
    #   hit = rayTraceWorld(nav.agent.rect.center, nav.destination, nav.world.getLines())
    #   if hit == None:
    #       tooclose = False
    #       for p in nav.world.getPoints():
    #           if minimumDistance((nav.agent.rect.center, nav.destination), p) < nav.agent.getRadius()*2.0:
    #               tooclose = True
    #       if not tooclose:
    #           return True
    return False

### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
    # path = copy.deepcopy(path)
    # ### YOUR CODE GOES BELOW HERE ###
    # alllines = world.getLines()
    # newstart = None
    # newend = None
    # for p in path:
    #     fronthit = rayTraceWorld(source, p, alllines)
    #     if fronthit == None:
    #         tooclose = False
    #         for p1 in world.getPoints():
    #             if minimumDistance((source, p), p1) < world.agent.getRadius()*2.0:
    #                 tooclose = True
    #         if not tooclose:
    #             newstart = p
    #     if newend == None:
    #         backhit = rayTraceWorld(p, dest, alllines)
    #         if backhit == None:
    #             tooclose = False
    #             for p1 in world.getPoints():
    #                 if minimumDistance((dest, p), p1) < world.agent.getRadius()*2.0:
    #                     tooclose = True
    #             if not tooclose:
    #                 newend = p
    # newpath = []
    # start = False
    # end = False
    # for p in path:
    #     if end == False:
    #         if start == False:
    #             if p == newstart:
    #                 newpath.append(p)
    #                 start = True
    #         else:
    #             newpath.append(p)
    #         if p == newend:
    #             newpath.append(p)
    #             end = True
    # path = newpath
    # if len(path) >= 2 and path[-1] == path[-2]:
    #     path.pop()
    ### YOUR CODE GOES BELOW HERE ###
    return path


### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
    ### YOUR CODE GOES BELOW HERE ###
    # if nav.path != None and nav.agent.moveTarget != nav.destination:
    #   if myCheckForShortcut(nav):
    #       nav.path = []
    #       nav.agent.moveToTarget(nav.destination)
    #       return True
    #   elif canSmooth(nav):
    #       next = nav.path.pop(0)
    #       nav.agent.moveToTarget(next)
    #       return True
    ### YOUR CODE GOES ABOVE HERE ###
    return False

# PART OF SOLUTION
def canSmooth(nav):
    # if nav.path != None and len(nav.path) > 0:
    #   next = nav.path[0]
    #   hit = rayTraceWorld(nav.agent.rect.center, next, nav.world.getLines())
    #   if hit == None:
    #       tooclose = False
    #       for p in nav.world.getPoints():
    #           if minimumDistance((nav.agent.rect.center, next), p) < nav.agent.getRadius()*2.0:
    #               tooclose = True
    #       if tooclose:
    #           return False
    #       else:
    #           return True
    return False
