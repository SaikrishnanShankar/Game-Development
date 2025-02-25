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
from moba2 import *
from btnode import *
from Hunter2 import *

###########################
### SET UP BEHAVIOR TREE


def treeSpec(agent):
	myid = str(agent.getTeam())
	spec = None
	### YOUR CODE GOES BELOW HERE ###
	spec = [
        Selector, [
            [Sequence,
                [HunterFoundDaemon,
                [Selector,
                    [(HitpointDaemon, 0.4),
                    [Sequence,
                        ChaseHero,
                        KillHero
                    ]],
                    Retreat
                ]]
            ],
            EvadeHunter
        ]
    ]
	# spec = [
	# 	(Selector),
	# 	[
	# 		(Sequence),
	# 		(HunterFoundDaemon),
	# 		(EvadeHunter)
	# 	],
	# 	[
	# 		(HitpointDaemon, 0.4),
	# 		[
	# 			(Sequence),
	# 			(ChaseHero),
	# 			(KillHero)
	# 		]
	# 	],
	# 	(Retreat)
	# ]
 
	### YOUR CODE GOES ABOVE HERE ###
	return spec

def myBuildTree(agent):
	myid = str(agent.getTeam())
	root = None
	### YOUR CODE GOES BELOW HERE ###
 
	### YOUR CODE GOES ABOVE HERE ###
	return root

### Helper function for making BTNodes (and sub-classes of BTNodes).
### type: class type (BTNode or a sub-class)
### agent: reference to the agent to be controlled
### This function takes any number of additional arguments that will be passed to the BTNode and parsed using BTNode.parseArgs()
def makeNode(type, agent, *args):
	node = type(agent, args)
	return node

###############################
### BEHAVIOR CLASSES:


##################
### Taunt
###
### Print disparaging comment, addressed to a given NPC
### Parameters:
###   0: reference to an NPC
###   1: node ID string (optional)

class Taunt(BTNode):

	### target: the enemy agent to taunt

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		# First argument is the target
		if len(args) > 0:
			self.target = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target is not None:
			print("Hey", self.target, "I don't like you!")
		return ret

##################
### MoveToTarget
###
### Move the agent to a given (x, y)
### Parameters:
###   0: a point (x, y)
###   1: node ID string (optional)

class MoveToTarget(BTNode):
	
	### target: a point (x, y)
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		# First argument is the target
		if len(args) > 0:
			self.target = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def enter(self):
		BTNode.enter(self)
		self.agent.navigateTo(self.target)

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None:
			# failed executability conditions
			# #print("exec", self.id, "false")
			return False
		elif distance(self.agent.getLocation(), self.target) < self.agent.getRadius():
			# Execution succeeds
			# #print("exec", self.id, "true")
			return True
		else:
			# executing
			return None
		return ret

##################
### Retreat
###
### Move the agent back to the base to be healed
### Parameters:
###   0: percentage of hitpoints that must have been lost to retreat
###   1: node ID string (optional)


class Retreat(BTNode):
	
	### percentage: Percentage of hitpoints that must have been lost
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.percentage = 0.5
		# First argument is the factor
		if len(args) > 0:
			self.percentage = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def enter(self):
		BTNode.enter(self)
		base = self.agent.world.getBaseForTeam(self.agent.getTeam())
		if base:
			self.agent.navigateTo(base.getLocation())
			enemyHero = self.agent.world.getEnemyNPCs(self.agent.getTeam())
			for enemy in enemyHero:
				if isinstance(enemy, Hero):
					self.agent.turnToFace(enemy.getLocation())
					self.agent.shoot()
				elif isinstance(enemy, Minion):
					self.agent.turnToFace(enemy.getLocation())
					self.agent.shoot()
	
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.getHitpoints() > self.agent.getMaxHitpoints() * self.percentage:
			# fail executability conditions
			# #print("exec", self.id, "false")
			return False
		elif self.agent.getHitpoints() == self.agent.getMaxHitpoints():
			# Exection succeeds
			# #print("exec", self.id, "true")
			return True
		else:
			# executing
			return None
		return ret

##################
### ChaseMinion
###
### Find the closest minion and move to intercept it.
### Parameters:
###   0: node ID string (optional)


class ChaseMinion(BTNode):

	### target: the minion to chase
	### timer: how often to replan

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		self.timer = 50
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)
		self.timer = 50
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if len(enemies) > 0:
			best = None
			dist = 0
			for e in enemies:
				if isinstance(e, Minion):
					d = distance(self.agent.getLocation(), e.getLocation())
					if best == None or d < dist:
						best = e
						dist = d
			self.target = best
		if self.target is not None:
			navTarget = self.chooseNavigationTarget()
			if navTarget is not None:
				self.agent.navigateTo(navTarget)


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None or self.target.isAlive() == False:
			# failed execution conditions
			# #print("exec", self.id, "false")
			return False
		elif self.target is not None and distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
			# succeeded
			# #print("exec", self.id, "true")
			return True
		else:
			# executing
			self.timer = self.timer - 1
			if self.timer <= 0:
				self.timer = 50
				navTarget = self.chooseNavigationTarget()
				if navTarget is not None:
					self.agent.navigateTo(navTarget)
			return None
		return ret

	def chooseNavigationTarget(self):
		if self.target is not None:
			return self.target.getLocation()
		else:
			return None

##################
### KillMinion
###
### Kill the closest minion. Assumes it is already in range.
### Parameters:
###   0: node ID string (optional)


class KillMinion(BTNode):

	### target: the minion to shoot

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)
		self.agent.stopMoving()
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if len(enemies) > 0:
			best = None
			dist = 0
			for e in enemies:
				if isinstance(e, Minion):
					d = distance(self.agent.getLocation(), e.getLocation())
					if best == None or d < dist:
						best = e
						dist = d
			self.target = best


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
			# failed executability conditions
			# #print("exec", self.id, "false")
			return False
		elif self.target.isAlive() == False:
			# succeeded
			# #print("exec", self.id, "true")
			return True
		else:
			# executing
			if self.agent.canDodge:
				self.agent.dodge()
				# Check if agent is outside the world dimensions
				world = self.agent.world
				location = self.agent.getLocation()
				if location[0] < 0:
					location = (0, location[1])
				elif location[0] > world.dimensions[0]:
					location = (world.dimensions[0], location[1])
				if location[1] < 0:
					location = (location[0], 0)
				elif location[1] > world.dimensions[1]:
					location = (location[0], world.dimensions[1])
				self.agent.navigateTo(location)
			self.shootAtTarget()
			return None
		return ret

	def shootAtTarget(self):
		if self.agent is not None and self.target is not None:
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()


##################
### ChaseHero
###
### Move to intercept the enemy Hero.
### Parameters:
###   0: node ID string (optional)

class ChaseHero(BTNode):

	### target: the hero to chase
	### timer: how often to replan

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		self.timer = 50
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)
		self.timer = 50
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		for e in enemies:
			if isinstance(e, Hero):
				self.target = e
				navTarget = self.chooseNavigationTarget()
				if navTarget is not None:
					self.agent.navigateTo(navTarget)
				return None


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None or self.target.isAlive() == False:
			# fails executability conditions
			#print("exec", self.id, "false")
			return False
		elif distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
			# succeeded
			#print("exec", self.id, "true")
			return True
		else:
			# executing
			self.timer = self.timer - 1
			if self.timer <= 0:
				navTarget = self.chooseNavigationTarget()
				if navTarget is not None:
					self.agent.navigateTo(navTarget)
			return None
		return ret

	def chooseNavigationTarget(self):
		if self.target is not None:
			return self.target.getLocation()
		else:
			return None

##################
### KillHero
###
### Kill the enemy hero. Assumes it is already in range.
### Parameters:
###   0: node ID string (optional)


class KillHero(BTNode):

	### target: the minion to shoot

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)
		self.agent.stopMoving()
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		for e in enemies:
			if isinstance(e, Hero):
				self.target = e
				return None

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
			# failed executability conditions
			if self.target == None:
				print("foo none")
			else:
				print("foo dist", distance(self.agent.getLocation(), self.target.getLocation()))
			#print("exec", self.id, "false")
			return False
		elif self.target.isAlive() == False:
			# succeeded
			#print("exec", self.id, "true")
			return True
		else:
			#executing
			if self.agent.canDodge:
				self.agent.dodge()
				# Check if agent is outside the world dimensions
				world = self.agent.world
				location = self.agent.getLocation()
				if location[0] < 0:
					location = (0, location[1])
				elif location[0] > world.dimensions[0]:
					location = (world.dimensions[0], location[1])
				if location[1] < 0:
					location = (location[0], 0)
				elif location[1] > world.dimensions[1]:
					location = (location[0], world.dimensions[1])
				self.agent.navigateTo(location)
			if self.agent.canareaeffect:
				self.agent.areaEffect()
			self.shootAtTarget()
			return None
		return ret

	def shootAtTarget(self):
		if self.agent is not None and self.target is not None:
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()


##################
### HitpointDaemon
###
### Only execute children if hitpoints are above a certain threshold.
### Parameters:
###   0: percentage of hitpoints that must be remaining to pass the daemon check
###   1: node ID string (optional)


class HitpointDaemon(BTNode):
	
	### percentage: percentage of hitpoints that must be remaining to pass the daemon check
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.percentage = 0.5
		# First argument is the factor
		if len(args) > 0:
			self.percentage = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if(self.agent == None):
			return False
		if self.agent.getHitpoints() < self.agent.getMaxHitpoints() * self.percentage:
			# Check failed
			print("exec", self.id, "fail")
			return False
		else:
			# Check didn't fail, return child's status
			return self.getChild(0).execute(delta)
		return ret

##################
### BuffDaemon
###
### Only execute children if agent's level is significantly above enemy hero's level.
### Parameters:
###   0: Number of levels above enemy level necessary to not fail the check
###   1: node ID string (optional)

class BuffDaemon(BTNode):

	### advantage: Number of levels above enemy level necessary to not fail the check

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.advantage = 0
		# First argument is the advantage
		if len(args) > 0:
			self.advantage = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		hero = None
		# Get a reference to the enemy hero
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		for e in enemies:
			if isinstance(e, Hero):
				hero = e
				break
		if hero == None or self.agent.level <= hero.level + self.advantage:
			# fail check
			print("exec", self.id, "fail")
			return False
		else:
			# Check didn't fail, return child's status
			return self.getChild(0).execute(delta)
		return ret





#################################
### MY CUSTOM BEHAVIOR CLASSES


class HunterFoundDaemon(BTNode):
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		if len(args) > 0:
			self.id = args[0]
		
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		hunter = None
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		for e in enemies:
			if isinstance(e, Hunter2):
				hunter = e
				break
		if hunter is not None:
			return True
		else:
			return self.getChild(0).execute(delta)
		return ret

class EvadeHunter(BTNode):
    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        if len(args) > 0:
            self.id = args[0]
   
    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        self.chooseEvadeTarget()
        
    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        hunter = None
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hunter2):
                hunter = e
                break
                
        if hunter:
            self.timer -= 1
            if self.timer <= 0:
                self.timer = 50
                self.chooseEvadeTarget()

            for enemy in enemies:
                if not isinstance(enemy, Hunter2) and distance(self.agent.getLocation(), enemy.getLocation()) < BIGBULLETRANGE:
                    self.agent.turnToFace(enemy.getLocation())
                    self.agent.shoot()
            
            return None 
        return False
        
    def chooseEvadeTarget(self):
        hunter = None
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hunter2):
                hunter = e
                break
                
        if hunter:
            dx = self.agent.getLocation()[0] - hunter.getLocation()[0]
            dy = self.agent.getLocation()[1] - hunter.getLocation()[1]
            scale = 200
            target_x = self.agent.getLocation()[0] + (dx * scale / math.sqrt(dx*dx + dy*dy))
            target_y = self.agent.getLocation()[1] + (dy * scale / math.sqrt(dx*dx + dy*dy))
            target_x = max(0, min(self.agent.world.dimensions[0], target_x))
            target_y = max(0, min(self.agent.world.dimensions[1], target_y))   
            self.target = (target_x, target_y)
            self.agent.navigateTo(self.target)