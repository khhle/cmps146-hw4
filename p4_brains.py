
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
    self.state = None
    self.target = None

  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)

    #find yourself
    you = self.body.find_nearest('Slug')
    #if low health, start fleeing
    if you.amount < 0.5:
        self.state = 'flee'


    #If player give out order to slug:
    if message == 'order':
        if details == 'i':
            #Implement idle
            self.state = 'idle'
            self.body.stop()


        elif details == 'a':
            #Implement attack
            self.state = 'attack'

        elif details == 'h':
            #Implement harvest:
            self.body.stop()

        elif details == 'b':
            #implement build
            self.body.stop()

        else:
            #Implement move command
            self.body.go_to(details)
            self.state = 'moving'

    #Attack case
    if self.state == 'attack' :
        self.target = self.body.find_nearest('Mantis')
        self.body.follow(self.target)
        self.body.set_alarm(1)

        if message == 'collide' and details['what'] == 'Mantis':
            mantis = details['who']
            mantis.amount -= 0.05 # take a tiny little bite

    #Flee case
    if self.state == 'flee':
        self.target = self.body.find_nearest('Nest')
        self.body.follow(self.target)

        if message == 'collide' and details['what'] == 'Nest':
            you.amount += 0.5

    pass    

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
