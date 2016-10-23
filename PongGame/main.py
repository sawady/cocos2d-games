import cocos
from cocos.director import director
import cocos.actions as actions
from cocos.layer import Layer, ColorLayer
from cocos.sprite import Sprite
from cocos.rect import Rect
from cocos.draw import Line
# from pyglet.window.key import KeyStateHandler
from pyglet.window import key
# from pyglet.window import Screen

# from cocos.actions import *

class Table(ColorLayer):
    def __init__(self):
        # blueish color
        super(Table, self).__init__(239, 228, 176, 255)
        
        middle_line = Line((320, 0), (320, 480), (255, 255, 255, 255), stroke_width=4)
        self.add(middle_line, z=2)
        
class KeyDisplay(Layer):
    
    is_event_handler = True

    def __init__(self):
        super(KeyDisplay, self).__init__()

        "Called every time just before the node enters the stage."
        super(KeyDisplay, self).on_enter()

        self.points1 = cocos.text.Label("0", font_name='Times New Roman', font_size=32,
                                        anchor_x='center', anchor_y='center', x=280, y=440)
        self.points2 = cocos.text.Label("0", font_name='Times New Roman', font_size=32,
                                        anchor_x='center', anchor_y='center', x=360, y=440)
        self.add(self.points1)
        self.add(self.points2)
        
        self.player_velocity = 200
        
        self.player1 = Sprite('assets/images/paleta.png')
        self.player1.position = 20, 240
        self.player1.velocity = (0, 0)
        
        self.player2 = Sprite('assets/images/paleta.png')
        self.player2.position = 620, 240
        self.player2.velocity = (0, 0)
        
        self.add(self.player1)
        self.add(self.player2)

        self.player1.do(actions.BoundedMove(640, 480))
        self.player2.do(actions.BoundedMove(640, 480))
        
        self.ball = Sprite('assets/images/bola.png', position=(320, 240))
        self.ball_velocity = 200
        self.ball.velocity = (self.ball_velocity, self.ball_velocity)
        self.add(self.ball)

        self.ball.do(BallMove(self.player1, self.player2, 640, 480))
        
    def on_key_press(self, k, modifiers):
        if k is key.UP:
            self.player1.velocity = (0, self.player_velocity)
        if k is key.DOWN:
            self.player1.velocity = (0, -self.player_velocity)
        if k is key.W:
            self.player2.velocity = (0, self.player_velocity)
        if k is key.S:
            self.player2.velocity = (0, -self.player_velocity)

    def on_key_release(self, k, modifiers):
        if k is key.UP or k is key.DOWN:
            self.player1.do(actions.Twirl(amplitude=0.1, duration=0.5))
            self.player1.velocity = (0, 0)
        if k is key.W or k is key.S:
            self.player2.do(actions.Twirl(amplitude=0.1, duration=0.5))
            self.player2.velocity = (0, 0)
            
    def on_exit(self):
        "Called every time just before the node exits the stage."
        super(KeyDisplay, self).on_exit()
        director.window.remove_handlers(self.keys)
        
    def update_text(self, text, s):
        text.element.text = s

class BallMove(actions.Move):
    def init(self, p1, p2, width, height):
        self.width, self.height = width, height
        self.p1, self.p2 = p1, p2

    def step(self, dt):
        super(BallMove, self).step(dt)
        x, y = self.target.position
        w, h = self.target.width, self.target.height
        
        target_rect = self.target.get_rect()
        
        if x > self.width - w / 2:
            x = self.width - w / 2
            self.target.velocity = (self.target.velocity[0] * -1, self.target.velocity[1])
        elif x < w / 2:
            x = w / 2
            self.target.velocity = (self.target.velocity[0] * -1, self.target.velocity[1])
            
        if y > self.height - h / 2:
            y = self.height - h / 2
            self.target.velocity = (self.target.velocity[0], self.target.velocity[1] * -1)
        elif y < h / 2:
            y = h / 2
            self.target.velocity = (self.target.velocity[0], self.target.velocity[1] * -1)
        self.target.position = (x, y)

# TODO: DO MANU SCENE

director.init(resizable=True)
director.run(cocos.scene.Scene(Table(), KeyDisplay()))
