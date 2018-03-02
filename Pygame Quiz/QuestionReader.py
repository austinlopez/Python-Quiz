
import pygame, sys, os, csv





def getQuestionAndAnswers(source,fileName):
    questions = {}
    answerFinal = []
    with open(source+fileName,newline='') as csvfile:
        seperateQuestions = csv.reader(csvfile,delimiter=':',quotechar='"')
        for row in seperateQuestions:
            questions[row[0]] = row[1]
    for question in questions:
        answerTemp = []
        seperateAnswers = csv.reader(question,delimiter=',',quotechar='"')
        #print(seperateAnswers[0])
        for answer in seperateAnswers:
            print(answer)
        #    answerTemp.append(answer)
        #    print(answerTemp)
        #print(question)
    print()


getQuestionAndAnswers('.\data','\questions.txt')