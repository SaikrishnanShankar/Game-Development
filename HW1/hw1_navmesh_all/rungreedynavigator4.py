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
from greedynavigator import *
			
			
			
			
nav = GreedyNavigator()
	
			
world = GameWorld(SEED, (1000, 1000), (1000, 1000))
agent = Agent(AGENT, (200, 100), 0, SPEED, world)

world.initializeTerrain([[(320, 110), (480, 200), (370, 400), (100, 435), (180, 250)],
                         [(740, 160), (940, 450), (800, 540), (600, 410)],
                         [(285, 550), (400, 755), (150, 745)],
                         [(590, 750), (910, 720), (925, 870), (580, 870)]]) 
world.setPlayerAgent(agent)
agent.setNavigator(nav)
nav.setWorld(world)
world.initializeRandomResources(NUMRESOURCES)
world.debugging = True
world.run()
