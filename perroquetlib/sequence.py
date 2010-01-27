# -*- coding: utf-8 -*-

# Copyright (C) 2009-2010 Frédéric Bertolus.
#
# This file is part of Perroquet.
#
# Perroquet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Perroquet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Perroquet.  If not, see <http://www.gnu.org/licenses/>.


import re

class CompleteSequenceError(Exception):
    pass

class Sequence(object):
    def __init__(self):
        
        #self.symbolList = what is between words (or "")
        #self.wordList = words that we want to find
        #self.workList = words that was writen (or "")
        #self.workValidityList = 1 if the word if good, 0 else
        #
        #self.activeWordIndex = the word that is currently being edited
        #self.activeWordPos = the position in that word
        #
        #self.helpChar = the char printed when you want a hint
        #
        #Note: self.symbolList, self.word, Listself.workList 
        #and self.workValidityList have always the same length
        
        self.symbolList = []
        self.wordList = []
        self.workList = []
        self.workValidityList = []
        
        self.activeWordIndex = 0
        self.activeWordPos = 0
        
        self.helpChar = '~'
    
    def Load(self, text):
        textToParse = text
        while len(textToParse) > 0:
            # ?
            if re.match('^([0-9\'a-zA-Z]+)[^0-9\'a-zA-Z]', textToParse):
                m = re.search('^([0-9\'a-zA-Z]+)[^0-9\'a-zA-Z]', textToParse)
                word = m.group(1)
                sizeToCut =  len(word)
                textToParse = textToParse[sizeToCut:]
                if len(self.wordList) == len(self.symbolList) :
                    self.symbolList.append('')
                self.wordList.append(word)
                self.workList.append("")
                self.workValidityList.append(0)
            # ?
            elif re.match('^([^0-9\'a-zA-Z]+)[0-9\'a-zA-Z]', textToParse):
                m = re.search('^([^0-9\'a-zA-Z]+)[0-9\'a-zA-Z]', textToParse)
                symbol = m.group(1)
                sizeToCut = len(symbol)
                textToParse = textToParse[sizeToCut:]
                self.symbolList.append(symbol)
            # ?
            else:
                # ?
                if re.match('^([0-9\'a-zA-Z]+)', textToParse):
                    if len(self.wordList) == len(self.symbolList) :
                        self.symbolList.append('')
                    self.wordList.append(textToParse)
                    self.workList.append("")
                    self.workValidityList.append(0)
                # ?
                else:
                    self.symbolList.append(textToParse)
                break

    def GetSymbolList(self):
        return self.symbolList

    def GetWordList(self):
        return self.wordList

    def GetWorkList(self):
        return self.workList

    def GetWordCount(self):
        return len(self.wordList)

    def GetActiveWordIndex(self):
        return self.activeWordIndex

    def SetActiveWordIndex(self, index):
        self.activeWordIndex = index
        print index

    def GetActiveWordPos(self):
        return self.activeWordPos

    def SetActiveWordPos(self, index):
        self.activeWordPos = index

    def SelectSequenceWord(self, wordIndex,wordIndexPos):
        self.activeWordPos = wordIndexPos
        self.activeWordIndex = wordIndex

        if self.IsValidWord():
            self.NextWord()

    def WriteCharacter(self, character):
        if self.IsValidWord():
            if self.NextWord():
                self.WriteCharacter(character)
            else:
                raise CompleteSequenceError
        else:
            #if replacing an helpChar
            if self.activeWordPos < len(self.workList[self.activeWordIndex]) and self.workList[self.activeWordIndex][self.activeWordPos] == self.helpChar:
                self.workList[self.activeWordIndex] = self.workList[self.activeWordIndex][:self.activeWordPos] + character + self.workList[self.activeWordIndex][self.activeWordPos+1:]
            else:
                self.workList[self.activeWordIndex] = self.workList[self.activeWordIndex][:self.activeWordPos] + character + self.workList[self.activeWordIndex][self.activeWordPos:]
            self.activeWordPos += 1
            self.WorkChange()


    def DeletePreviousCharacter(self):
        if self.IsValidWord():
            if self.PreviousWord():
                self.DeletePreviousCharacter()
        elif len(self.workList[self.activeWordIndex]) == 0:
            if self.PreviousWord():
                self.DeletePreviousCharacter()
        elif self.activeWordPos == 0:
            if self.PreviousWord():
                self.DeletePreviousCharacter()
        else:
            self.workList[self.activeWordIndex] = self.workList[self.activeWordIndex][:self.activeWordPos-1]  + self.workList[self.activeWordIndex][self.activeWordPos:]
            self.activeWordPos -= 1
            self.WorkChange()

    def DeleteNextCharacter(self):
        if self.IsValidWord():
            if self.NextWord(False):
                self.DeleteNextCharacter()
        elif len(self.workList[self.activeWordIndex]) == 0:
            if self.NextWord(False):
                self.DeleteNextCharacter()
        elif self.activeWordPos == len(self.workList[self.activeWordIndex]) :
            if self.NextWord(False):
                self.DeleteNextCharacter()
        else:
            self.workList[self.activeWordIndex] = self.workList[self.activeWordIndex][:self.activeWordPos]  + self.workList[self.activeWordIndex][self.activeWordPos+1:]
            self.WorkChange()

    def NextWord(self, end = True):
        if self.activeWordIndex < len(self.workList) - 1:
            self.activeWordIndex +=1
            if end:
                self.activeWordPos = len(self.workList[self.activeWordIndex])
            else:
                self.activeWordPos = 0
            if self.IsValidWord():
                return self.NextWord(end)
            else:
                return True
        else:
            if end:
                self.activeWordPos = len(self.workList[self.activeWordIndex])
            else:
                self.activeWordPos = 0
            return False

    def PreviousWord(self, end = True):
        if self.activeWordIndex > 0:
            self.activeWordIndex -=1
            if end:
                self.activeWordPos = len(self.workList[self.activeWordIndex])
            else:
                self.activeWordPos = 0
            if self.IsValidWord():
                return self.PreviousWord()
            else:
                return True
        else:
            if end:
                self.activeWordPos = len(self.workList[self.activeWordIndex])
            else:
                self.activeWordPos = 0
            return False


    def FirstWord(self):
        self.activeWordIndex = 0
        self.activeWordPos = 0
        while self.IsValidWord():
            if not self.NextWord(False):
                break


    def LastWord(self):
        self.activeWordIndex = len(self.workList) -1
        self.activeWordPos = len(self.workList[self.activeWordIndex])
        while self.IsValidWord():
            if not self.PreviousWord(True):
                break

    def NextCharacter(self):
        if self.activeWordPos >= len(self.workList[self.activeWordIndex]):
            self.NextWord(False)
        else:
            self.activeWordPos += 1

    def PreviousCharacter(self):
        if self.activeWordPos == 0:
            self.PreviousWord()
        else:
            self.activeWordPos -= 1

    def IsValidWord(self):

        if self.workValidityList[self.activeWordIndex] == 1:
            return True
        else:
            return False

    def GetValidity(self, index):
        return self.workValidityList[index]

    def IsValid(self):
        valid = True
        id = 0
        for word in self.workList:
            if word.lower() != self.wordList[id].lower():
                valid = False
                break
            id += 1
        return valid

    def GetWordFound(self):
        found = 0
        id = 0
        for word in self.workList:
            if word.lower() == self.wordList[id].lower():
                found += 1
            id += 1
        return found

    def IsEmpty(self):
        empty = True
        for word in self.workList:
            if word != "":
                empty = False
                break
        return empty

    def CompleteWord(self):
        """Reveal correction for word at cursor in current sequence"""
        if self.IsValidWord():
            if self.NextWord(False):
                self.CompleteWord()
            return

        currentWord = self.workList[self.activeWordIndex]
        goodWord = self.wordList[self.activeWordIndex]

        outWord = ""
        first_error = -1
        for i in range(0, len(goodWord)):
            if i < len(currentWord) and currentWord[i].lower() == goodWord[i].lower():
                outWord += goodWord[i]
            else:
                outWord += self.helpChar
                if first_error == -1:
                    first_error = i

        if len(currentWord) == len(goodWord) and first_error != -1:
            outWord = outWord[:first_error] + goodWord[first_error] + outWord[first_error+1:]
            self.activeWordPos = first_error+1
        elif first_error != -1:
            self.activeWordPos = first_error
        else:
            self.activeWordPos = 0

        self.workList[self.activeWordIndex] = outWord
        self.WorkChange()

    def CompleteAll(self):
        """Reveal all words"""
        id = 0
        for word in self.wordList:
            self.workList[id] = word
            self.ComputeValidity(id)
            id += 1

    def WorkChange(self):
        """Update the validity of the current word"""
        self.ComputeValidity(self.activeWordIndex)
        if self.workValidityList[self.activeWordIndex] < 0:
            location = self.CheckLocation(self.activeWordIndex)
            if location != -1:
                self.workList[location] = self.workList[self.activeWordIndex]
                self.workList[self.activeWordIndex] = ""
                self.ComputeValidity(self.activeWordIndex)
                self.ComputeValidity(location)
                self.activeWordPos = 0

    def ComputeValidity(self, index):
        # ?

        validity = 0
        #Global check
        if self.workList[index].lower() == self.wordList[index].lower():
            validity = float(1)
        else:
            currentLength = len(self.workList[index])
            targetLength = len(self.wordList[index])


            #Length validity
            lengthWeight = 0.2
            lengthValidity = lengthWeight * (1 - abs(1-float(currentLength)/float(targetLength)))

            if lengthValidity > lengthWeight:
                lengthValidity = lengthWeight

            #Character validity
            charWeight = 0.8
            weightPerChar = float(charWeight) / float(targetLength)
            current = self.workList[index].lower()
            target = self.wordList[index].lower()

            charValidity = 0

            for i in range(0, currentLength):
                if i >= targetLength:
                    charValidity -= weightPerChar
                elif current[i] == target[i]:
                    charValidity += weightPerChar
                else:
                    charValidity -= weightPerChar

            if charValidity > charWeight:
                charValidity = charWeight

            validity = lengthValidity + charValidity

        self.workValidityList[index] = validity

    def CheckLocation(self, index):
        # ?
        for i in range(1,4):
            if index+i < len(self.wordList) and self.GetValidity(index+i) != 1 and self.workList[index].lower() == self.wordList[index+i].lower():
                return index + i
            if index-i >= 0 and self.GetValidity(index-i) != 1 and self.workList[index].lower() == self.wordList[index-i].lower():
                return index - i

        return -1

    def GetTimeBegin(self):
        return self.beginTime

    def GetTimeEnd(self):
        return self.endTime

    def SetTimeBegin(self, time):
        self.beginTime = time

    def SetTimeEnd(self, time):
        self.endTime = time
