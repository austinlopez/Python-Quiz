
import pygame, sys, random, time
from pygame.locals import *
from threading import Timer


windowSize = [800,600]

BG_COLOR = [211,211,255]

pygame.init()


class Block():

    def __init__(self, name, color, x, y, width, height, outlineColor=[0]):
        self.name = name
        self.color = color
        #self.pos = pos
        self.x1 = x
        self.y1 = y
        self.width = width
        self.height = height
        self.outlineColor = outlineColor

    def draw(self, screen):
        if self.outlineColor == [0]:
            self.piece1 = pygame.draw.rect(screen, self.color,[self.x1,self.y1, self.width, self.height])
        else: 
            self.piece1 = pygame.draw.rect(screen,self.outlineColor,[self.x1,self.y1,self.width,self.height],3)
            self.piece2 = pygame.draw.rect(screen,self.color,[self.x1,self.y1,50,50])
            #self.outline = pygame.draw.lines(screen,[0,0,0],True,self.points,OUTLINE_WIDTH)

    def pointInBlock(self, x, y):
        if ((self.x1 < x < (self.x1 + self.width)) & (self.y1 < y < (self.y1 + self.height))):
            print("That is in: Block ",self.name)
            return True

class Answers(pygame.sprite.Sprite):

    def __init__(self,screen, name, x, y, width, height, color):
        self.answerName = name
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.screen = screen

        self.rect = Block(self.answerName, color,x,y, 300, 300)#, [255,0,0])

    def draw(self):
        self.rect.draw(self.screen)


class Question():

    def __init__(self, topic, question, answers, correctAnswer):
        self.topic = topic
        self.question = question
        self.answers = answers
        self.correctAnswer = correctAnswer
        




def main():
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("pygame Quiz")

    screen.fill(BG_COLOR)

    answer1 = Answers(screen,"lol idk",100,200,150,50,[0,255,255])
    answer1.draw()

    while True:
        #screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                answer1.rect.pointInBlock(pos[0],pos[1])

            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        pygame.display.flip()



main()