
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          #print self.target
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.prev_state = self.state
    self.target = None
    self.no_target = False
    self.has_resource = False
    self.body.set_alarm(0.5)

  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  appropriate.)
    
    #find yourself
    you = self.body.find_nearest('Slug')
    
    #if low health, start fleeing
    if you.amount < 0.5:
        self.set_state('flee')
        
    #If player give out order to slug:
    if message == 'order':
        if details == 'i':
            #Idle
            self.set_state('idle')

        elif details == 'a':
            #Attack
            self.set_state('attack')

        elif details == 'h':
            #Harvest:
            self.set_state('harvest')

        elif details == 'b':
            #Build
            self.set_state('build')

        else:
            #Move command
            self.set_state('moving')
            self.body.go_to(details)

    if self.state == 'idle':
        self.body.stop()
        
        if message == 'timer':
            self.reset_timer()
            
    if self.state == 'moving':
        if message == 'timer':
            self.reset_timer()
        #should probably reset to idle once the destination is reached here
    
    #Attack case
    if self.state == 'attack':
        if message == 'timer':
            self.target = self.body.find_nearest('Mantis')
            self.reset_timer()
            
            if self.target:
                self.body.follow(self.target)
            elif self.no_target:
                self.state_finished()
        if message == 'collide' and details['what'] == 'Mantis':
            mantis = details['who']
            mantis.amount -= 0.05 # take a tiny little bite

    #Flee case
    if self.state == 'flee':
        self.target = self.body.find_nearest('Nest')
        
        if message == 'timer':
            self.reset_timer()
        
        self.body.go_to(self.target)

        if message == 'collide' and details['what'] == 'Nest':
            you.amount += 0.5
        
        if you.amount > 0.75:
            self.state = self.prev_state
    
    #Harvest
    if self.state == 'harvest':
        if message == 'collide':
            if details['what'] == 'Nest':
                nest = details['who']
                if self.has_resource:
                    self.has_resource = False
            elif details['what'] == 'Resource':
                resource = details['who']
                if not self.has_resource:
                    self.has_resource = True
                    resource.amount -= 0.25
                
        if message == 'timer':
            if self.has_resource:
                self.target = self.body.find_nearest('Nest')
            else:
                self.target = self.body.find_nearest('Resource')
                
            self.reset_timer()
        
            if self.target:
                self.body.go_to(self.target)
            elif self.no_target:
                self.state_finished()
        
    #Build
    if self.state == 'build':
        if message == 'collide':
            if details['what'] == 'Nest':
                nest = details['who']
                nest.amount += 0.01
                
        if message == 'timer':
            self.target = self.body.find_nearest('Nest')
            self.reset_timer()
        
            if self.target:
                self.body.go_to(self.target)
            elif self.no_target:
                self.state_finished()

  def reset_timer(self):
    self.body.set_alarm(0.5)
    
    if self.target:
        self.no_target = False
    else:
        self.no_target = True
        
  def set_state(self, state):
    if self.prev_state is not self.state:
        self.prev_state = self.state
    self.state = state
    
  def state_finished(self):
    self.no_target = False
    if self.state == self.prev_state:
        self.state = 'idle'
    else:
        self.state = self.prev_state

world_specification = {
  'worldgen_seed': 13, # comment-out to randomize
  'nests': 4,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
