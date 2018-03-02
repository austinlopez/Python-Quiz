
import sys, os, csv

def getQuestionAndAnswers(source,fileName):
    questions = {}
    answers = {}
    answerFinal = []
    with open(source+fileName,newline='') as csvfile:
        seperateQuestions = csv.reader(csvfile,delimiter=':',quotechar='"')
        for row in seperateQuestions:
            questions[row[0]] = row[1]
            answers[row[0]] = row[2]
    for question in questions:
        answerForQuestion = questions[question].split(',')
        answerFinal.append(answerForQuestion)
        questions[question] = answerForQuestion
        #print('answerTemp:',answerTemp)
        #seperateAnswers = csv.reader(questions[question],delimiter=',',quotechar='"')
        #print(seperateAnswers)
        #for answer in seperateAnswers:
        #    print(answer)
        #    answerTemp.append(answer)
        #    print(answerTemp)
    #print(questions)
    #print(answers)
    return (questions, answers)

#something = getQuestionAndAnswers('.\data','\questions.txt')
#print(something)