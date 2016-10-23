import cocos
from cocos.director import director
import cocos.actions as actions
from cocos.layer import Layer, ColorLayer
# from cocos.rect import Rect
from cocos.draw import Line
from pyglet.window.key import KeyStateHandler
from pyglet.window import key
from pyglet.window import Screen

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
        
        self.player1 = cocos.sprite.Sprite('paleta.png')
        self.player1.position = 20, 240
        self.player1.velocity = (0, 0)
        
        self.player2 = cocos.sprite.Sprite('paleta.png')
        self.player2.position = 620, 240
        self.player2.velocity = (0, 0)
        
        self.add(self.player1)
        self.add(self.player2)

        self.player1.do(actions.BoundedMove(640, 480))
        self.player2.do(actions.BoundedMove(640, 480))
        
        self.ball = cocos.sprite.Sprite('bola.png', position=(320, 240))
        self.ball_velocity = 10
        self.add(self.ball)

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
            self.player1.velocity = (0, 0)
        if k is key.W or k is key.S:
            self.player2.velocity = (0, 0)
        
    def on_exit(self):
        "Called every time just before the node exits the stage."
        super(KeyDisplay, self).on_exit()
        director.window.remove_handlers(self.keys)
        
    def update_text(self, text, s):
        text.element.text = s

# TODO: DO MANU SCENE

director.init(resizable=True)
director.run(cocos.scene.Scene(Table(), KeyDisplay()))
