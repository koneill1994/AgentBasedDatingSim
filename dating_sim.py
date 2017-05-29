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

height=1012
width=1012
field_dim = (height,width)

max_radius = 30

# i suppose would be indicative of introversion?
mean_interaction_radius = 10
sd_interaction_radius = 3

mean_expected_utility = 5
sd_expected_utility = 2

marriage_wait_time_distribution = (50,10) # mean, sd

render_pygame_window=True



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
    self.significant_other = None
    self.taken = False
    self.acquaintances=[]
    self.interacted_counter=0
    self.ID = agent_counter
    self.marriage_wait_time=max(random.gauss(marriage_wait_time_distribution[0],marriage_wait_time_distribution[1]),0)
    self.married = False
    self.relationship_start_time = None
  
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
    self.interacted_counter+=1
    e_u = self.EstimatedUtility(other)
    self.UpdateExpectedUtility(e_u,sim_time)
    if other not in self.acquaintances:
      self.interacted.append((other,e_u))
      self.acquaintances.append(other)

  # if this is true for both, they will date
  def CheckInterested(self,other):
     if self.EstimatedUtility(other) > self.expected_utility:
       return True
  
  def EnterRelationship(self,other):
    self.taken = True
    self.significant_other = other
    self.relationship_start_time = sim_time
    
  def EstimatedUtility(self,other):
    return other.attractiveness # more complex formula later
  
  def UpdateExpectedUtility(self,new_utility,t):
    # recompute the average
    self.expected_utility = ((self.expected_utility*(self.interacted_counter-1))+new_utility)/self.interacted_counter
    #self.expected_utility *= 1-(t+1)/10
    
  def CheckForIntersectingCircles(self,agent_list):
    for agent in agent_list:
      if agent is not self:
        if SqrDistance(self.location,agent.location) < (self.radius + agent.radius)**2:
          self.interaction_list.append(agent)
  
  def CheckIfReadyToMarry(self):
    if sim_time-self.relationship_start_time > self.marriage_wait_time:
      return True
    else:
      return False
  
  # this assumes they are already in a relationship with someone
  def Marry(self):
    self.married=True

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
  

def RemoveFromCouples(agent_a,agent_b):
  for c in range(len(couples)):
    if agent_a in couples[c] or agent_b in couples[c]:
      couples.pop(c)
      break # to speed it up, it /shouldn't/ be necessary to keep looking
  
def CheckIfDate(agent_a,agent_b):
  if agent_a.CheckInterested(agent_b) and agent_b.CheckInterested(agent_a):
    # free the agents from their previous romantic obligations
    RemoveFromCouples(agent_a,agent_b)
    
    agent_a.EnterRelationship(agent_b)
    agent_b.EnterRelationship(agent_a)
    couples.append((agent_a,agent_b))
  
def GeneratePossibleInteractions(agents):
  for a in agents:
    a.CheckForIntersectingCircles(agents)
  
def AverageExpectedUtility(agents):
  total=0
  for a in agents:
    total+=a.expected_utility
  return 1.0*total/len(agents)
  
def AverageSocialCircle(agents):
  total=0
  for a in agents:
    total+=len(a.interacted)
  return 1.0*total/len(agents)

def AverageInteractionRadius(agents):
  total=0
  for a in agents:
    total+=a.interaction_radius
  return 1.0*total/len(agents)

def render_text(text):
  if pygame.font:
    font = pygame.font.Font(None, 24)
    text = font.render(text, 1, (0,0,0))
    textpos = text.get_rect(right=width-20, top=20)
    screen.blit(text, textpos)

def WriteHeader(logfile):
  c = ','
  s = 'agentID' + c
  s+='attractiveness'+c
  s+='expected_utility'+c
  s+='no_of_interactions'+c
  s+='x_pos'+c
  s+='y_pos'+c
  s+='center_x'+c
  s+='center_y'+c
  s+='radius'+c
  s+='interaction_radius'+c
  s+='partner'+c
  s+='married'
  logfile.write(s+'\n')
  
def WriteLine(logfile,agent):
  c = ','
  s = str(agent.ID) + c
  s+=str(agent.attractiveness)+c
  s+=str(agent.expected_utility)+c
  s+=str(agent.interacted_counter)+c
  s+=str(agent.location[0])+c
  s+=str(agent.location[1])+c
  s+=str(agent.center[0])+c
  s+=str(agent.center[1])+c
  s+=str(agent.radius)+c
  s+=str(agent.interaction_radius)+c
  if agent.significant_other == None:
    s+='NA'+c
  else:
    s+=str(agent.significant_other.ID)+c
  s+=str(agent.married)
  logfile.write(s+'\n')

def LogAgents(agents):  
  f = open('./logs/logfile_' + str(sim_time) + '.csv','w')
  WriteHeader(f)
  for a in agents:
    WriteLine(f,a)
  f.close()

## start of main code here

no_of_agents = 500

agents=[]

couples=[]

agent_counter = 0
for n in range(no_of_agents):
  agents.append(Agent())
  agent_counter+=1

GeneratePossibleInteractions(agents)

sim_time = 0

display_text=''
text_timer=0

# pygame initialization

if(render_pygame_window):
  pygame.init()
  screen = pygame.display.set_mode(field_dim)

  black = 0,0,0,255
  white = 255,255,255,255
  red = 255,0,0,255
  blue = 0,0,255,255
  green = 0,255,0,255
  yellow = 255,255,0,255










while(True): # i like to live dangerously
  
  
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if keys[pygame.K_SPACE]: 
      LogAgents(agents)
      text_timer=20
      display_text = 'logged'
  
  
  print('\n')
  print("epoch = " + str(sim_time))
  print("couples:" + str(len(couples)))
  print("average expected utility: "+str(AverageExpectedUtility(agents)))
  #print AverageInteractionRadius(agents)
  #print agents[0].expected_utility
  
  if(render_pygame_window):
    screen.fill(white)
  
  for person in agents:
    person.Move()
    if(render_pygame_window):
      screen.blit(person.icon,person.location)
    
    
  # check and see which agents are close enough to meet
  for person in agents:
    if not person.married:
      for other in person.interaction_list:
        if not other.married:
          if SqrDistance(person.location,other.location) < (person.interaction_radius + other.interaction_radius)**2:
            person.Interact(other)
            other.Interact(person)
            CheckIfDate(person,other)
            
  # check for marriages
  for c in couples:
    if c[0].CheckIfReadyToMarry() and c[1].CheckIfReadyToMarry():
      c[0].Marry()
      c[1].Marry()
        
  if(render_pygame_window):
    render_text(display_text)
    if text_timer==0: display_text=''
    else: text_timer-=1
    
    #draw the couples linkages
    for c in couples:
      if c[0].married and c[1].married:
        pygame.draw.line(screen,black,c[0].location,c[1].location,3)
      else:
        pygame.draw.line(screen,black,c[0].location,c[1].location,1)
    pygame.display.flip()
    
  
  
  
  
  
  
  sim_time+=1
