# agent based expected utility dating simulation

import random
import math
import numpy

import sys, os, pygame, PIL, time
from PIL import Image
from pygame import gfxdraw


# agent properties
# gender
# orientation 
# location (x,y)
# attractiveness
# list of known agents, and expected utilities

# put all of these on bell curves


# necessary stuff for first model
# random center
# random radius
# (interaction radius)
# random expected utility
# movement rule
# list of known people and estimated utilities


# polynomial dropoff function for determining movement
# probabilities of all possibile moves are evaluated

# math says 37 % (1/e)

# expected utility based 



# starting requirements
  # movement rule
  # utility weights
  # dating rule
  # marriage rule


# simplified for first model
gender_list=['m','f']

field_dim = (1012,1012)

max_radius = 30

# i suppose would be indicative of introversion?
mean_interaction_radius = 10
sd_interaction_radius = 3

mean_expected_utility = 5
sd_expected_utility = 2


class Agent:
  
  def __init__(self):
    self.GenerateRandomStats()
    
  def GenerateAttractiveness(self):
    n=random.gauss(5,2)
    self.attractiveness = numpy.clip(n,0,10)
    
  def GenerateRandomStats(self):
    self.GenerateAttractiveness()
    self.gender=gender_list[random.randrange(0,1)]
    self.center=(random.randrange(0,field_dim[0]),random.randrange(0,field_dim[1]))
    self.location = self.center
    self.radius = random.randrange(0,max_radius)
    self.interaction_radius = max(random.gauss(mean_interaction_radius,sd_interaction_radius),0)
    self.expected_utility = max(random.gauss(mean_expected_utility,sd_expected_utility),0)
    self.interacted = []
    self.icon = self.GenerateIcon()
    self.interaction_list = []
  
  def GenerateIcon(self):
    icon_dim = (5,5)
    col=self.ColorFromAttractiveness()
    im=Image.new( 'RGB', icon_dim, col)
    PIL_bytes = im.tobytes("raw")
    pygame_img = pygame.image.fromstring(PIL_bytes,icon_dim,"RGB")
    return pygame_img
    
  def ColorFromAttractiveness(self):
    r=0
    b=0
    g=0
    # attractiveness is from 0 to 10
    # 0 is blue
    # 2.5 is bluegreen
    # 5 is green
    # 7.5 is greenred
    # 10 is red
    if self.attractiveness < 5:
      b= int(max(1-self.attractiveness/5.0,0)*255)
    if self.attractiveness > 5:
      r =  -int(min(1-self.attractiveness/5.0,1)*255)
    g = int(255*(1-abs((self.attractiveness-5)/5.0)))
    return (r,g,b)
    
  def Move(self):
    points = AdjacentPoints(self.location)
    points_new = []
    # probability_distribution = GenerateProbabilityDistribution(points) # save for later
    # make sure they don't leave their radius
    for p in points:
      if SqrDistance(self.center,p) < max_radius**2:
        points_new.append(p)
    self.location = points[random.randrange(0,len(points))]
    
  def Interact(self,other):
    e_u = self.EstimatedUtility(other)
    self.interacted.append((other,e_u))
    
  def EstimatedUtility(self,other):
    return other.attractiveness # more complex formula later
  
  def UpdateExpectedUtility(self):
    total_utility=0
    for person in self.interacted:
      total_utility+=person[0]
    self.expected_utility = total_utility/len(self.interacted) #average of all seen utilities
    
  def CheckForIntersectingCircles(self,agent_list):
    for agent in agent_list():
      if SqrDistance(self.location,agent.location) < (self.radius + agent.radius)**2:
        self.interaction_list.append(agent)
  

def AdjacentPoints((x,y)):
  return [(x+1,y),
          (x+1,y+1),
          (x+1,y-1),
          (x,y),
          (x,y+1),
          (x,y-1),
          (x-1,y),
          (x-1,y+1),
          (x-1,y-1)]
  
  
def SqrDistance((x,y),(a,b)):
  return (x-a)**2 + (y-b)**2
  
  
  

## start of main code here

no_of_agents = 500

agents=[]


for n in range(no_of_agents):
  agents.append(Agent())

sim_time = 0

# pygame initialization


pygame.init()
screen = pygame.display.set_mode(field_dim)

black = 0,0,0,255
white = 255,255,255,255
red = 255,0,0,255
blue = 0,0,255,255
green = 0,255,0,255
yellow = 255,255,0,255











while(True): # i like to live dangerously
  
  screen.fill(white)
  
  print sim_time
  for person in agents:
    person.Move()
    person.interaction_done = False
    screen.blit(person.icon,person.location)
    
    
  # check and see which agents are close enough to meet
  for person in agents:
    for other in person.interaction_list:
      if SqrDistance(person.location,other.location) < (person.interaction_radius + other.interaction_radius)**2:
        person.Interact(other)
        other.Interact(person)
    
  pygame.display.flip()
  sim_time+=1
