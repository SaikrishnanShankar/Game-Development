
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
from moba import *
from Hunter import *

class MyMinion(Minion):
    
    def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
        Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
        ### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
        self.states = [Idle, NavigateToTower, NavigateToBase, AssaultTower, AssaultBase, SiegeTower, SiegeBase, EvadeHunterNearBase, EvadeHunterNearTower, GatherReinforcements]
        self.is_engaging = False
        self.tactical_distance = 60
        ### YOUR CODE GOES ABOVE HERE ###
        # if not hasattr(MyMinion, 'minion_count'):
        #     MyMinion.minion_count = {0: 0, 1: 0}
        # MyMinion.minion_count[self.team] = MyMinion.minion_count.get(self.team, 0) + 1
        # print(f"Team {self.team} Minion Count: {MyMinion.minion_count[self.team]}")
    def start(self):
        Minion.start(self)
        self.changeState(Idle)

class Idle(State):
    
    def enter(self, oldstate):
        State.enter(self, oldstate)
        self.agent.stopMoving()
    
    def execute(self, delta = 0):
        State.execute(self, delta)
        team = self.agent.team
        enemy_towers = self.agent.world.getEnemyTowers(myteam = team)
        
        if enemy_towers:
            if len(enemy_towers) == 2:
                tower1_dist = distance(enemy_towers[0].position, self.agent.position)
                tower2_dist = distance(enemy_towers[1].position, self.agent.position)
                target_tower = enemy_towers[0] if tower1_dist < tower2_dist else enemy_towers[1]
                self.agent.changeState(NavigateToTower, target_tower.position)
            else:
                self.agent.changeState(NavigateToTower, enemy_towers[0].position)
        else:
            enemy_bases = self.agent.world.getEnemyBases(myteam = team)
            if enemy_bases:
                self.agent.changeState(NavigateToBase, enemy_bases[0].position)

class NavigateToTower(State):
   
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        if self.target_pos:
            self.agent.navigateTo(self.target_pos)
        self.agent.changeState(AssaultTower, self.target_pos)

class NavigateToBase(State):
   
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        if self.target_pos:
            self.agent.navigateTo(self.target_pos)
        self.agent.changeState(AssaultBase, self.target_pos)

class AssaultTower(State):
    
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        towers = self.agent.world.getEnemyTowers(myteam = self.agent.team)
        

        if not towers or (len(towers) == 1 and towers[0].position != self.target_pos):
            self.agent.changeState(Idle)

        if not self.agent.isMoving():
            self.agent.changeState(Idle)

        enemy_hunters = [npc for npc in self.agent.world.getEnemyNPCs(myteam = self.agent.team) 
                        if isinstance(npc, Hunter)]
        
        for hunter in enemy_hunters:
            hunter_distance = distance(hunter.position, self.agent.position)
            if (1.5*BASEBULLETRANGE < hunter_distance < 2.5*BASEBULLETRANGE and 
                len(self.agent.world.getNPCsForTeam(team = self.agent.team)) <= 15):
                if not any(distance(self.agent.position, t.position) <= BASEBULLETRANGE for t in towers):
                    self.agent.stopMoving()
                    self.agent.changeState(EvadeHunterNearTower, self.target_pos)

        visible_towers = self.agent.getVisibleType(Tower)
        for tower in visible_towers:
            if tower.position == self.target_pos:
                dist_to_tower = distance(self.target_pos, self.agent.position)
                if dist_to_tower <= BASEBULLETRANGE/2:
                    self.agent.changeState(SiegeTower, self.target_pos)
                    self.agent.stopMoving()
                elif dist_to_tower <= BASEBULLETRANGE:
                    self.agent.turnToFace(self.target_pos)
                    self.agent.shoot()
                elif (dist_to_tower >= 1.5*BASEBULLETRANGE and 
                      dist_to_tower <= 4*BASEBULLETRANGE and 
                      not self.agent.is_engaging):
                    nearby_allies = sum(1 for ally in self.agent.world.getNPCsForTeam(team = self.agent.team)
                                     if distance(ally.position, self.agent.position) <= 300)
                    if nearby_allies <= 3:
                        self.agent.stopMoving()
                        self.agent.changeState(GatherReinforcements, self.target_pos)

class AssaultBase(State):
    
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        if not self.agent.isMoving():
            self.agent.changeState(Idle)

        enemy_hunters = [npc for npc in self.agent.world.getEnemyNPCs(myteam = self.agent.team) 
                        if isinstance(npc, Hunter)]
        
        for hunter in enemy_hunters:
            if (1.5*BASEBULLETRANGE < distance(hunter.position, self.agent.position) < 2.5*BASEBULLETRANGE and 
                len(self.agent.world.getNPCsForTeam(team = self.agent.team)) <= 15):
                self.agent.stopMoving()
                self.agent.changeState(EvadeHunterNearBase, self.target_pos)

        for base in self.agent.getVisibleType(Base):
            if base.team != self.agent.team:
                dist_to_base = distance(self.target_pos, self.agent.position)
                if dist_to_base <= BASEBULLETRANGE/2:
                    self.agent.changeState(SiegeBase, self.target_pos)
                    self.agent.stopMoving()
                elif dist_to_base <= BASEBULLETRANGE:
                    self.agent.turnToFace(self.target_pos)
                    self.agent.shoot()

        for enemy in self.agent.getVisibleType(Minion):
            if enemy.team != self.agent.team:
                self.agent.turnToFace(enemy.position)
                self.agent.shoot()

class SiegeTower(State):
    
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        self.agent.turnToFace(self.target_pos)
        self.agent.shoot()

        tower_visible = False
        for tower in self.agent.getVisibleType(Tower):
            if tower.position == self.target_pos:
                tower_visible = True
                if delta % 7 == 0:
                    self._perform_tactical_movement()
                self.agent.turnToFace(self.target_pos)
                self.agent.shoot()
                break

        if not tower_visible:
            self.agent.changeState(Idle)

    def _perform_tactical_movement(self):
        x, y = self.agent.position
        angle = math.atan2(y - self.target_pos[1], x - self.target_pos[0])
        
        if len(self.agent.world.getNPCsForTeam(team = self.agent.team)) % 2 == 1:
            self.agent.tactical_distance = -self.agent.tactical_distance
            
        new_pos = (x + self.agent.tactical_distance * math.sin(angle),
                  y - self.agent.tactical_distance * math.cos(angle))

        if self._is_valid_position(new_pos):
            self.agent.moveToTarget(new_pos)
            self.agent.tactical_distance = -self.agent.tactical_distance

    def _is_valid_position(self, position):
        for obstacle in self.agent.world.obstacles:
            if pointInsidePolygonPoints(self.agent.position, obstacle.getPoints()):
                return False
            if any(minimumDistance(line, position) < 2.5 * self.agent.maxradius 
                  for line in obstacle.getLines()):
                return False
        return True

class SiegeBase(State):
    
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        self.agent.turnToFace(self.target_pos)
        self.agent.shoot()

        for base in self.agent.getVisibleType(Base):
            if base.team != self.agent.team:
                if delta % 7 == 0:
                    self._perform_tactical_movement()
                self.agent.turnToFace(self.target_pos)
                self.agent.shoot()
                break

    def _perform_tactical_movement(self):
        x, y = self.agent.position
        angle = math.atan2(y - self.target_pos[1], x - self.target_pos[0])
        new_pos = (x + self.agent.tactical_distance * math.sin(angle),
                  y - self.agent.tactical_distance * math.cos(angle))

        if self._is_valid_position(new_pos):
            self.agent.moveToTarget(new_pos)
            self.agent.tactical_distance = -self.agent.tactical_distance

    def _is_valid_position(self, position):
        for obstacle in self.agent.world.obstacles:
            if pointInsidePolygonPoints(self.agent.position, obstacle.getPoints()):
                return False
            if any(minimumDistance(line, position) < self.agent.maxradius 
                  for line in obstacle.getLines()):
                return False
        return True

class EvadeHunterNearTower(State):
   
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        enemy_hunters = [npc for npc in self.agent.world.getEnemyNPCs(myteam = self.agent.team)
                        if isinstance(npc, Hunter)]
        
        if not enemy_hunters or len(self.agent.world.getNPCsForTeam(team = self.agent.team)) > 15:
            self.agent.changeState(Idle)

        for tower in self.agent.getVisibleType(Tower):
            if distance(tower.position, self.agent.position) <= SMALLBULLETRANGE:
                self.agent.turnToFace(self.target_pos)
                self.agent.shoot()
                return

        for enemy in self.agent.getVisibleType(Minion):
            if enemy.team != self.agent.team:
                self.agent.turnToFace(enemy.position)
                self.agent.shoot()

class EvadeHunterNearBase(State):
    
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        enemy_hunters = [npc for npc in self.agent.world.getEnemyNPCs(myteam = self.agent.team)
                        if isinstance(npc, Hunter)]
        
        if not enemy_hunters or len(self.agent.world.getNPCsForTeam(team = self.agent.team)) > 15:
            self.agent.changeState(NavigateToBase, self.target_pos)

        for base in self.agent.getVisibleType(Base):
            if (base.team != self.agent.team and 
                distance(base.position, self.agent.position) <= SMALLBULLETRANGE):
                self.agent.turnToFace(self.target_pos)
                self.agent.shoot()
                return

        for enemy in self.agent.getVisibleType(Minion):
            if enemy.team != self.agent.team:
                self.agent.turnToFace(enemy.position)
                self.agent.shoot()

class GatherReinforcements(State):
    
    def parseArgs(self, args):
        self.target_pos = args[0]

    def execute(self, delta = 0):
        allies = self.agent.world.getNPCsForTeam(team = self.agent.team)        
        nearby_allies = sum(1 for ally in allies 
                          if distance(ally.position, self.agent.position) <= 300)
        
       
        should_attack = (
            any(isinstance(ally.state, SiegeTower) for ally in allies) or
            nearby_allies > 3 or
            len(self.agent.world.getEnemyTowers(myteam = self.agent.team)) < 2 or
            len(allies) > 15
        )
        
        if should_attack:
            self.agent.is_engaging = True
            self.agent.changeState(AssaultTower, self.target_pos)
            
        else:
            enemy_minions = self.agent.getVisibleType(Minion)
            for enemy in enemy_minions:
                if enemy.team != self.agent.team:
                    self.agent.turnToFace(enemy.position)
                    self.agent.shoot()
            
            visible_towers = self.agent.getVisibleType(Tower)
            for tower in visible_towers:
                if tower.position == self.target_pos:
                    if distance(tower.position, self.agent.position) <= BASEBULLETRANGE:
                        self.agent.turnToFace(self.target_pos)
                        self.agent.shoot()
                    break