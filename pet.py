import sys
from random import choice, randint

import pyglet
import pymunk
import pymunk.pyglet_util

options = pymunk.pyglet_util.DrawOptions()
toplevel = sys.modules["__main__"]




class Config:
    def __init__(self):
        self.WINDOW_WIDTH = 800 if not hasattr(toplevel, "WINDOW_WIDTH") else toplevel.WINDOW_WIDTH 
        self.WINDOW_HEIGHT = 600 if not hasattr(toplevel, "WINDOW_HEIGHT") else toplevel.WINDOW_HEIGHT  
        self.GRAVITY = (0, 0) if not hasattr(toplevel, "GRAVITY") else toplevel.GRAVITY  
        self.DENSITY = 10 if not hasattr(toplevel, "DENSITY") else toplevel.DENSITY 
        self.FRICTION = 0.5 if not hasattr(toplevel, "FRICTION") else toplevel.FRICTION 
        self.ELASTICITY = 0.8 if not hasattr(toplevel, "ELASTICITY") else toplevel.ELASTICITY 
        self.DT = 0.02 if not hasattr(toplevel, "DT") else toplevel.DT
        self.RANDOM_RADIUS_RANGE = (10,20) if not hasattr(toplevel, "RANDOM_RADIUS_RANGE") else toplevel.RANDOM_RADIUS_RANGE
        self.RANDOM_VELOCITY_RANGE = (-300, 300)  if not hasattr(toplevel, "RANDOM_VELOCITY_RANGE") else toplevel.RANDOM_VELOCITY_RANGE
        self.RANDOM_X_RANGE = (int(self.WINDOW_WIDTH*0.4), int(self.WINDOW_WIDTH*0.6)) if not hasattr(toplevel, "RANDOM_X_RANGE") else toplevel.RANDOM_X_RANGE 
        self.RANDOM_Y_RANGE = (int(self.WINDOW_HEIGHT*0.4), int(self.WINDOW_HEIGHT*0.6)) if not hasattr(toplevel, "RANDOM_Y_RANGE") else toplevel.RANDOM_Y_RANGE 
        self.RANDOM_COLOR_DICT = {
            "red" : (255,0,0,255),
            "orange" : (255,165,0,255),
            "yellow" : (255,255,0,255),
            "green" : (0,255,0,255),
            "blue" : (0,0,255,255),
            "cyan" : (0,255,255,255),
            "purple" : (255,0,255,255),
            "white" : (255,255,255,255),
        }  if not hasattr(toplevel, "RANDOM_COLOR_DICT") else toplevel.RANDOM_COLOR_DICT
        self.WALL_THICKNESS = 16 if not hasattr(toplevel, "WALL_THICKNESS") else toplevel.WALL_THICKNESS 




class Engine:
    " pymunk physics engine wrapper with pyglet support"

    def __init__(self):
        self.config = Config()

        self.window = pyglet.window.Window(self.config.WINDOW_WIDTH, 
                                            self.config.WINDOW_HEIGHT, 
                                            resizable=False)
        self.space = pymunk.Space()
        self.space.gravity = self.config.GRAVITY


    def add_circle(self,x=None,
                        y=None, 
                        radius=None,
                        density=None,
                        friction=None,
                        elasticity=None,
                        color=None,
                        static=False,
                        kinematic=False,
                        velocity=None,
                        ):
        if static:
            circle_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        elif kinematic:
            circle_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        else:
            circle_body = pymunk.Body(body_type=pymunk.Body.DYNAMIC) 

        if radius:
            circle_shape = pymunk.Circle(circle_body, radius)
        else:
            circle_shape = pymunk.Circle(circle_body, randint(*self.config.RANDOM_RADIUS_RANGE))

        circle_shape.density = density if density else self.config.DENSITY
        circle_shape.friction = friction if friction else self.config.FRICTION
        circle_shape.elasticity = elasticity if elasticity else self.config.ELASTICITY
        
        if color :
            if type(color) is str:
                circle_shape.color = self.config.RANDOM_COLOR_DICT[color]     
            else:
                circle_shape.color = color
        else:
            circle_shape.color = choice(list(self.config.RANDOM_COLOR_DICT.values()))

        temp_x = x if x else randint(*self.config.RANDOM_X_RANGE)
        temp_y = y if y else randint(*self.config.RANDOM_Y_RANGE)
        circle_body.position = (temp_x, temp_y)

        if velocity :
            circle_body.velocity = velocity
        elif circle_body.body_type is pymunk.Body.DYNAMIC:
            circle_body.velocity = (randint(*self.config.RANDOM_VELOCITY_RANGE),
                                    randint(*self.config.RANDOM_VELOCITY_RANGE)
                                    )

        self.space.add(circle_body, circle_shape)
        return  circle_shape

    def make_bottom_wall(self):
        self.make_wall( (0,0), (self.window.width,0))

    def make_4_walls(self):
        self.make_wall( (0,0), (self.window.width,0))
        self.make_wall( (0,self.window.height), (self.window.width,self.window.height))
        self.make_wall( (0,0), (0,self.window.height))
        self.make_wall( (self.window.width,0), (self.window.width,self.window.height))

    def make_wall(self, a, b):
        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape = pymunk.Segment(wall_body, a,b,self.config.WALL_THICKNESS)
        wall_shape.friction = self.config.FRICTION
        wall_shape.elasticity = self.config.ELASTICITY
        wall_body.position = 0, 0
        self.space.add(wall_shape)

    
    def on_draw(self):
        self.window.clear()
        self.space.debug_draw(options)



    def default_update(self, dt):
        self.space.step(dt)

    def run(self):
        
        
        self.on_draw = self.window.event(self.on_draw)

        if hasattr(toplevel, "on_mouse_press"):
            toplevel.on_mouse_press = self.window.event(toplevel.on_mouse_press)

        if hasattr(toplevel, "on_mouse_drag"):
            toplevel.on_mouse_drag = self.window.event(toplevel.on_mouse_drag)

        if hasattr(toplevel, "on_key_press"):
            toplevel.on_key_press = self.window.event(toplevel.on_key_press)

        if hasattr(toplevel,"update"):
            pyglet.clock.schedule_interval(toplevel.update, self.config.DT)
        else:
            pyglet.clock.schedule_interval(self.default_update, self.config.DT)
        pyglet.app.run()


