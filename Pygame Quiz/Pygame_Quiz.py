
import pygame, sys, random, time, csv, pygame.color
from pygame.locals import *
from threading import Timer

import QuestionReader

pygame.init()

"""
    Constants
"""

WINDOW_SIZE = [800,600]
SOUND_PATH = ''
IMAGE_DIR = '.\images'
DATA_DIR = '.\data'
BACKGROUND_COLOR = [211,211,255]#pygame.color.THECOLORS["grey"]

BG_COLOR = [211,211,255]

#answerfont = pygame.font.Font('freesansbold.ttf',64) # set font and size
#scorefont = pygame.font.Font('freesansbold.ttf',30)

"""
    Functions
"""

def playSound(name, times=0):
    """
        Plays a sound from the path determined
        in the constants. 
    """
    path = SOUND_PATH
    try:
        pygame.mixer.music.load(path+name)
        pygame.mixer.music.play(times)
    except pygame.error:
        print('There is no file with this name')

def text_to_screen(screen, text, x, y, size = 50, color = (50, 50, 50), font_type = None):
    """
        Draws Text to the screen above
        everything else.
    """
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e

"""
    Classes
"""

class Block():

    def __init__(self, name, color, x, y, width, height, outlineColor=[0]):
        self.name = name
        self.color = color
        #self.pos = pos
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outlineColor = outlineColor

    def draw(self, screen):
        if self.outlineColor == [0]:
            self.piece1 = pygame.draw.rect(screen, self.color, [self.x,self.y,self.width,self.height])
        else: 
            self.piece1 = pygame.draw.rect(screen,self.outlineColor,[self.x-2,self.y-2,self.width+4,self.height+4])
            self.piece2 = pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])

    def pointInBlock(self, x, y):
        if ((self.x < x < (self.x + self.width)) & (self.y < y < (self.y + self.height))):
            print("That is in: Block ",self.name)
            return True

class Answers(pygame.sprite.Sprite):

    def __init__(self,screen, name, x, y, width, height, color,bgColor=[0]):
        self.answerName = name
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.screen = screen

        self.rect = Block(self.answerName, color,x,y, 300, 300,bgColor)#, [255,0,0])

    def createAnswerBlock(self,answers):
        answer1 = Block('answer1',[255,128,64],10,300,250,100,[0,0,0])
        answer2 = Block('answer1',[255,128,0],270,300,250,100,[0,0,0])
        answer3 = Block('answer1',[128,64,64],10,410,250,100,[0,0,0])
        answer4 = Block('answer1',[128,0,255],270,410,250,100,[0,0,0])
        answer1.draw(self.screen)
        answer2.draw(self.screen)
        answer3.draw(self.screen)
        answer4.draw(self.screen)

    def draw(self):
        self.rect.draw(self.screen)


class Question():

    def __init__(self, screen, topic, question, answers, correctAnswer):
        self.screen = screen
        self.topic = topic
        self.question = question
        self.answers = answers
        self.correctAnswer = correctAnswer

        self.answerBlocks = {}

        #print(topic,question,answers,correctAnswer)

    def createAnswers(self):
        answerNum = 0
        for answer in self.answers:
            if answerNum == 0:
                self.answerBlocks[answerNum] = Answers(self.screen, answer, 10,300,250,100, [255,128,64], [0,0,0])
            if answerNum == 1:
                self.answerBlocks[answerNum] = Answers(self.screen, answer, 270,300,250,100, [255,128,0], [0,0,0])
            if answerNum == 2:
                self.answerBlocks[answerNum] = Answers(self.screen, answer, 10,410,250,100, [128,64,64], [0,0,0])
            if answerNum == 3:
                self.answerBlocks[answerNum] = Answers(self.screen, answer, 270,410,250,100,[128,0,255], [0,0,0])
            #self.answerBlocks[answerNum] = Answers(self.screen, answer, 100,100,100,100,[0,0,0],[0,0,0])
            #self.answerBlocks[answerNum].createAnswerBlock(self.answers)
            self.answerBlocks[answerNum].draw()
            answerNum += 1
        

class Quiz():

    def __init__(self, screen, source):
        self.screen = screen
        quiz = QuestionReader.getQuestionAndAnswers('.\data','\questions.txt')
        self.questions = quiz[0]
        self.answerKey = quiz[1]
        #print(self.questions)
        #print(self.answerKey)
        self.answerNum = {}
        questionNum = 0
        for questionName in self.questions:
            self.answerNum[questionNum] = questionName
            questionNum += 1

    def selectRandomQuestion(self):
        self.currentQuestion = self.answerNum[random.randint(0,len(self.answerNum))]
        print(self.currentQuestion)
        #return self.currentQuestion

    def initializeQuestion(self):
        self.currentQuestion = Question(self.screen, 'Something', self.currentQuestion, self.questions[self.currentQuestion],self.answerKey[self.currentQuestion])
        self.currentQuestion.createAnswers()

"""
    Main Game Code
"""

def main():

    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("pygame Quiz")

    screen.fill(BG_COLOR)

    currentQuiz = Quiz(screen, 'Question.txt')
    currentQuiz.selectRandomQuestion()
    currentQuiz.initializeQuestion()

    #answer1 = Answers(screen,"lol idk",100,200,150,50,[0,255,255])
    #answer1.draw()
    #answer2 = Answers(screen,"another one",400,200,150,50,[0,200,200],[100,50,0])
    #answer2.draw()

    while True:
        #screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                #answer1.rect.pointInBlock(pos[0],pos[1])
                #answer2.rect.pointInBlock(pos[0],pos[1])

            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        pygame.display.flip()



main()