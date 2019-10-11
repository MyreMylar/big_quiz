import os
os.environ['PYGAME_FREETYPE'] = "TRUE"

import pygame
from pygame.locals import *


def lerp( A, B, C):
    return (C * B) + ((1.0-C) * A)

def render_word_wrapped_text(screen, textBoxRect, textToWrap, font, boldFont, timeDelta, textColour):
    textPrintingFinished = False
    textLines = textToWrap.split('\n')
    lineNum = 0
    currentScreenYPos = textBoxRect[1]
   
    lineLenAcc = 0
    while not textPrintingFinished:
        boldLine = False
        currentScreenYPos = textBoxRect[1] + lineNum * font.get_linesize()
        textLine = textLines[lineNum]

        if "[b]" in textLine:
            textLine = textLine.replace("[b]", "")
            boldLine = True
             
        if font.size(textLine)[0] >= textBoxRect[2]:
            lineWords = textLine.split(' ')
            lineLength = 0
            wordNum = 0
            foundWordWrapPoint = False
            for word in lineWords:
                lineLength += font.size(word)[0]
                lineLength += font.size(" ")[0]
                if lineLength >= textBoxRect[2] and not foundWordWrapPoint:
                    foundWordWrapPoint = True
                    textLine = ""
                    for wordIndex in range(0, wordNum):
                        textLine += lineWords[wordIndex] + " "

                    nextTextLine = ""
                    for newLineWordIndex in range(wordNum, len(lineWords)):
                        nextTextLine += lineWords[newLineWordIndex] + " "

                    textLines.insert(lineNum+1,nextTextLine)
                    
                wordNum += 1

        lineEnd = len(textLine)


        if boldLine:
            adventureOutputTextRender = boldFont.render(textLine, True, textColour)
            adventureOutputTextRenderRect = adventureOutputTextRender.get_rect(x=textBoxRect[0], y=currentScreenYPos)

        else:
            adventureOutputTextRender = font.render(textLine, True, textColour)
            adventureOutputTextRenderRect = adventureOutputTextRender.get_rect(x=textBoxRect[0], y=currentScreenYPos)

        screen.blit(adventureOutputTextRender, adventureOutputTextRenderRect)
                    
            

        lineNum += 1
        lineLenAcc += len(textLine)
        if lineNum == len(textLines):
            textPrintingFinished = True

