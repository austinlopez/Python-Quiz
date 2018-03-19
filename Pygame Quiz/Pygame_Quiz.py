
import pygame, sys, random, time, csv, pygame.color, smtplib
from pygame.locals import *
from threading import Timer
from email.mime.text import MIMEText

import QuestionReader

pygame.init()

"""
    Constants
"""

WINDOW_SIZE = [800,600]
SOUND_PATH = '.\Sounds'
IMAGE_DIR = '.\images'
DATA_DIR = '.\data'
FONT_DIR = '.\Fonts'
BACKGROUND_COLOR = [211,211,255]#pygame.color.THECOLORS["grey"]
ANSWER1_COLOR = []
ANSWER2_COLOR = []
ANSWER3_COLOR = []
ANSWER4_COLOR = []

BG_COLOR = [211,211,255]

OSWALD_FONT = ".\Fonts\Oswald\Oswald-Regular.ttf"
SANS_FONT = FONT_DIR+"\Open_Sans_Condensed\OpenSansCondensed-Light.ttf"


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

def text_to_screen(screen, text, x, y, size = 50, font_type = None, color = (50, 50, 50)):
    """
        Draws Text to the screen above
        everything else.
    """
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        sizeTaken = font.size(text)
        text = font.render(text, True, color)
        
        screen.blit(text, ((x - (sizeTaken[0]/2)), (y - (sizeTaken[1]/2)))) #y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e

def startTimer(length,functionAfter):
    t = Timer(length,functionAfter)
    t.start()

"""
    Classes
"""

class Block():
    """
        The actual block of the answer.
        Consists of the function to draw the rectangle.

    """

    def __init__(self, name, x, y, width, height, color, outlineColor=[0],text=None,textColor=[0,0,0],textFont=OSWALD_FONT,textSize=20):
        self.name = name
        self.color = color
        #self.pos = pos
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outlineColor = outlineColor
        self.text = text; self.textColor = textColor;self.textFont = textFont;self.textSize = textSize

    def draw(self, screen):
        if self.outlineColor == [0]:
            self.piece1 = pygame.draw.rect(screen, self.color, [self.x,self.y,self.width,self.height])
            text_to_screen(screen,self.text,((self.width/2)+self.x),((self.height/2)+self.y),self.textSize,self.textFont,self.textColor)
        else: 
            self.piece1 = pygame.draw.rect(screen,self.outlineColor,[self.x-2,self.y-2,self.width+4,self.height+4])
            self.piece2 = pygame.draw.rect(screen,self.color,[self.x,self.y,self.width,self.height])
            text_to_screen(screen,self.text,((self.width/2)+self.x),((self.height/2)+self.y),self.textSize,self.textFont,self.textColor)

    def pointInBlock(self, x, y):
        if ((self.x < x < (self.x + self.width)) & (self.y < y < (self.y + self.height))):
            print("That is in: Block ",self.name)
            return self.name

class Answers(pygame.sprite.Sprite):
    """
        The Object for each answer
        Takes in:
            the screen
            the question (name)
            the x, y, width, and height of the box for the question
            the color and outline color of the box
        Functions:
            create the Block
    """
    def __init__(self,screen,id, name, x, y, width, height, color,bgColor=[0]):
        self.answerName = name
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.x = x; self.y = y; self.width = width; self.height = height
        self.image.fill(color)
        self.color = color
        self.bgColor = bgColor
        self.screen = screen

        self.createAnswerBlock(self.answerName)

        #self.rect = Block(self.answerName, x,y, self.width, self.height,color,bgColor)#, [255,0,0])

    def createAnswerBlock(self,answers):
        #Need to implement the text that goes into the block. 
        self.rect = Block(self.answerName, self.x,self.y, self.width, self.height,self.color,self.bgColor,self.answerName,[15,15,15],OSWALD_FONT)#, [255,0,0])
        pass

    def draw(self, screen):
        self.rect.draw(screen)


class Question():
    """
        Start a question for the quiz
        Takes in:
            the screen being displayed to
            the topic
            the question
            the answer choices
            the correct answer
        Functions:
            create the aswer objects and store in a dictionary
            check if the one clicked is correct
    """
    def __init__(self, screen, topic, question, answers, correctAnswer):
        self.screen = screen
        self.topic = topic
        self.question = question
        self.answers = answers
        self.correctAnswer = correctAnswer

        self.timeTaken = 0
        self.answerBlocks = {}

        #print(topic,question,answers,correctAnswer)

    def createAnswers(self):
        answerNum = 1
        for answer in self.answers:
            if answerNum == 1:
                self.answerBlocks[answerNum] = Answers(self.screen, answerNum, answer, 10,300,380,130, [255,128,64], [0,0,0])
            if answerNum == 2:
                self.answerBlocks[answerNum] = Answers(self.screen, answerNum, answer, 410,300,380,130, [255,128,0], [0,0,0])
            if answerNum == 3:
                self.answerBlocks[answerNum] = Answers(self.screen, answerNum, answer, 10,450,380,130, [128,64,64], [0,0,0])
            if answerNum == 4:
                self.answerBlocks[answerNum] = Answers(self.screen, answerNum, answer, 410,450,380,130,[128,0,255], [0,0,0])
            #self.answerBlocks[answerNum] = Answers(self.screen, answer, 100,100,100,100,[0,0,0],[0,0,0])
            #self.answerBlocks[answerNum].createAnswerBlock(self.answers)
            #self.answerBlocks[answerNum].draw()
            answerNum += 1

    def drawAll(self):
        text_to_screen(self.screen,self.question,(WINDOW_SIZE[0]/2),100)
        for answers in self.answerBlocks:
            self.answerBlocks[answers].draw(self.screen)

    def whichOneClicked(self,x,y):
        for answer in self.answerBlocks:
            if self.answerBlocks[answer].rect.pointInBlock(x,y):
                self.thisQTimer.cancel()
                return answer

    def addSec(self):
        self.timeTaken += 1
        self.time()

    def getT(self):
        return self.timeTaken

    def time(self):
        self.thisQTimer = Timer(1,self.addSec)
        self.thisQTimer.start()


        

class Quiz():
    """
        Start a quiz
        Takes in:
            the screen it is being displayed to
            the file source for the questions
        Functions:
            select a random question from the ones remaining
            remove a question from the ones left
            initialize a question object, and set as the current question
            keep track of the score

    """
    def __init__(self, screen, source):
        self.screen = screen
         #questions, answers = QuestionReader.getQuestionAndAnswers('.\data','\questions.txt')
        questions = QuestionReader.getQuestionAndAnswers('.\data','\questions.txt')
        self.questions = questions[0]
        self.answerKey = questions[1]
        #print(self.questions)
        #print(self.answerKey)
        self.answerNum = {}
        questionNum = 0
        for questionName in self.questions:
            self.answerNum[questionNum] = questionName
            questionNum += 1
        #print(self.answerNum)

        self.answeredCorrect = []
        self.correctNum = 0
        self.answeredWrong = []
        self.wrongNum = 0
        self.whatQ = 0
        self.score = 0

        self.totalQuestions = len(self.questions)
        #print(self.totalQuestions)
        self.currentStateOfQuiz = "mainMenu"
        self.mainMenuOnce()

    def mainMenuOnce(self):
        #playSound("") #Possible Menu Music
        print("Function mainMenuOnce")

    def mainMenu(self):
        text_to_screen(self.screen, "PyGame Quiz", (WINDOW_SIZE[0]/2), 90, 100,SANS_FONT,[30,100,180])
        startQuizButton = Block("Start Quiz",(WINDOW_SIZE[0]/2 - 200),(WINDOW_SIZE[1]/2-100),400,100,[0,200,0],[0,0,0],"Start Quiz",[15,15,15],OSWALD_FONT,40)
        startQuizButton.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if startQuizButton.pointInBlock(pos[0],pos[1]):
                    print("Start Quiz")
                    self.currentStateOfQuiz = "startingQuiz"
                    playSound("\Menu Select.mp3")
                    #self.selectRandomQuestion()
                    #self.initializeQuestion()
                    self.beforeFirstQ()
                    pass
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        #pass

    def beforeFirstQ(self):
        #text_to_screen(self.screen, "Get Ready For the Quiz!", (WINDOW_SIZE[0]/2),150,85,SANS_FONT,[30,30,30])
        startTimer(3,self.selectRandomQuestion)
        self.whatQ = 1
        #self.selectRandomQuestion()
        #self.initializeQuestion()
        #self.currentStateOfQuiz = "question"

    def selectRandomQuestion(self):
        if len(self.answerNum.keys()) != 0:
            self.currentChoice = random.choice(list(self.answerNum.keys()))
            self.currentQuestion = self.answerNum[self.currentChoice]
            self.initializeQuestion()
            self.currentStateOfQuiz = "question"
        else:
            print("Quiz Over!")
            self.currentStateOfQuiz = 'finished'
        #print(self.currentQuestion)
        #print(choice)
        #print(self.answerNum[choice])
        #return self.currentQuestion

    def initializeQuestion(self):
        self.currentQuestion = Question(self.screen, 'Something', self.currentQuestion, self.questions[self.currentQuestion],self.answerKey[self.currentQuestion])
        self.currentQuestion.createAnswers()
        self.currentQuestion.drawAll()
        self.currentQuestion.time()
        text_to_screen(self.screen,self.currentQuestion.question,(WINDOW_SIZE[0]/2),100)

    def checkIfCorrect(self,answered):
        """
            If correct, add dictionary object to quiz.correct -- self.answeredCorrect
            If wrong, add dictionary object to quiz.wrong -- self.answeredWrong
            Then Either way take it out of the choices
        """
        print("The answer was:",self.currentQuestion.correctAnswer)
        print(answered)
        if answered == None:
            return
        if int(answered) == int(self.currentQuestion.correctAnswer):
            #print("You answered it correctly")
            self.answeredCorrect.append(self.answerKey[self.currentQuestion.question])
            self.answerNum.pop(self.currentChoice)
            self.correctNum += 1
            thisScore = 100 - (self.currentQuestion.getT()*5)
            self.score += thisScore
            playSound("\correctPing.mp3")
        if int(answered) != int(self.currentQuestion.correctAnswer):
            #print("You answered it wrong")
            self.answeredWrong.append(self.answerKey[self.currentQuestion.question])
            self.answerNum.pop(self.currentChoice)
            self.wrongNum += 1
            playSound("\wrongPing.mp3")
        self.selectRandomQuestion()

    def quizOver(self):
        pass


"""
    Main Game Code
"""

def main():

    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("pygame Quiz")

    screen.fill(BG_COLOR)

    currentQuiz = Quiz(screen, 'Question.txt')
    #currentQuiz.selectRandomQuestion()
    #currentQuiz.initializeQuestion()

    #answer1 = Answers(screen,"lol idk",100,200,150,50,[0,255,255])
    #answer1.draw()
    #answer2 = Answers(screen,"another one",400,200,150,50,[0,200,200],[100,50,0])
    #answer2.draw()

    while True:
        screen.fill(BG_COLOR)
        #for event in pygame.event.get():
        #    if event.type == pygame.MOUSEBUTTONDOWN:
        #        pos = pygame.mouse.get_pos()
        #        print(pos)
        #        #answer1.rect.pointInBlock(pos[0],pos[1])
        #        #answer2.rect.pointInBlock(pos[0],pos[1])
        #        #currentQuiz.currentQuestion.whichOneClicked(pos[0],pos[1])
        #
        #    if event.type == pygame.QUIT:
        #        pygame.quit(); sys.exit()

        if currentQuiz.currentStateOfQuiz == "mainMenu":
            currentQuiz.mainMenu()
        if currentQuiz.currentStateOfQuiz == "startingQuiz":
            text_to_screen(currentQuiz.screen, "Get Ready For the Quiz!", (WINDOW_SIZE[0]/2),150,85,SANS_FONT,[30,30,30])
            text_to_screen(currentQuiz.screen,"Number of Questions: {0}".format(currentQuiz.totalQuestions),(WINDOW_SIZE[0]/2), 350,65,SANS_FONT,[30,30,30])
        if currentQuiz.currentStateOfQuiz == "question":
            text_to_screen(currentQuiz.screen,"Time Taken: {0} seconds".format(currentQuiz.currentQuestion.timeTaken),600,15,20,OSWALD_FONT, [30,30,30])
            text_to_screen(currentQuiz.screen,"Answered Correctly: {0}  Answered Wrong: {1}".format(currentQuiz.correctNum,currentQuiz.wrongNum), 200,15,20,OSWALD_FONT,[30,30,30])
            text_to_screen(currentQuiz.screen,"Score: {0}.".format(currentQuiz.score), 100,35,20,OSWALD_FONT,[30,30,30])
            currentQuiz.currentQuestion.drawAll()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #playSound("\Menu Select.mp3")
                    pos = pygame.mouse.get_pos()
                    #print(pos)
                    #answer1.rect.pointInBlock(pos[0],pos[1])
                    #answer2.rect.pointInBlock(pos[0],pos[1])
                    oneClicked = currentQuiz.currentQuestion.whichOneClicked(pos[0],pos[1])
                    currentQuiz.checkIfCorrect(oneClicked)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            pass
        if currentQuiz.currentStateOfQuiz == "finished":
            text_to_screen(currentQuiz.screen,"Congrats!", WINDOW_SIZE[0]/2,100,50,SANS_FONT,[30,30,30])
            text_to_screen(currentQuiz.screen,"You Answered {0} Correct".format(currentQuiz.correctNum), WINDOW_SIZE[0]/2,200,50,SANS_FONT,[30,30,30])
            text_to_screen(currentQuiz.screen,"You Got {0} Wrong".format(currentQuiz.wrongNum), WINDOW_SIZE[0]/2,300,50,SANS_FONT,[30,30,30])
            text_to_screen(currentQuiz.screen,"You Got a Total Score of: {0}.".format(currentQuiz.score), WINDOW_SIZE[0]/2,400,50,SANS_FONT,[30,30,30])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #playSound("\Menu Select.mp3")
                    pos = pygame.mouse.get_pos()
                    #print(pos)
                    #answer1.rect.pointInBlock(pos[0],pos[1])
                    #answer2.rect.pointInBlock(pos[0],pos[1])
                    #oneClicked = currentQuiz.currentQuestion.whichOneClicked(pos[0],pos[1])
                    #currentQuiz.checkIfCorrect(oneClicked)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
        pygame.display.flip()



main()