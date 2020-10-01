#!/usr/bin/env python3

import random
import pathlib

def getWordList() -> list:
    # Load words for hangman and return them as a list.
    
    wordListFilename = 'sowpods.txt'
    wordListPath = pathlib.Path(__file__).parent / wordListFilename
    wordListFile = open(wordListPath, 'r')

    rawWordList = wordListFile.readlines()

    # Need to process the raw word list and strip leading and trailing whitespaces
    wordList = list()
    for word in rawWordList:
        wordList.append(word.strip())

    return wordList

def getWord() -> str:
    # Load in the word list to choose from
    wordList = getWordList()

    # Check that the list is not empty
    if len(wordList) == 0:
        return ''

    # Make sure all words in the list are strings
    if all(isinstance(item, str) for item in wordList):
        pass
    else:
        return ''

    # select a random number between 1st and last index of word list
    newWord = wordList[random.randint(0, len(wordList) - 1)]

    # return that word
    return newWord


def getPersonString(wrongGuesses=0):
    # Generate the hanging person string based on the number of incorrect guesses.
    # TODO: Should probably move this into the HangpersonGame class for cleanliness

    # 1.    |
    # 2.    0
    # 3.   /|\
    # 4.   / \
    # 5.
    resultLines = list()
    
    # Initialize a counter for the lines
    numLines = 0

    # Set the total number of lines needed for the presentation
    maxLines = 5

    # wrongGuesses = 0
    if wrongGuesses >= 1:
        resultLines.append('   |   ')
        resultLines.append('\n')
        numLines+=1
        resultLines.append('   0   ')
        resultLines.append('\n')
        numLines+=1

    # wrongGuesses = 2
    if wrongGuesses >= 2:
        resultLines.append('  /')

    # wrongGuesses = 3
    if wrongGuesses >= 3:
        resultLines.append('|')

    # wrongGuesses = 4
    if wrongGuesses >= 4:    
        resultLines.append('\  ')
        resultLines.append('\n')
        numLines+=1

    # wrongGuesses = 5
    if wrongGuesses >= 5:
        resultLines.append('  /')

    # wrongGuesses = 6
    if wrongGuesses >= 6:
        resultLines.append(' \  ')
        resultLines.append('\n')
        numLines+=1
    
    for i in range(numLines, maxLines):
        resultLines.append('\n')

    return ''.join(resultLines)


def getWordProgressString(wordToGuess, guesses):
    # iterate through the characters of the word to guess and
    # check if that character is in the list of guesses.
    # If the character is present in the list of guesses, then
    # fill it in, otherwise leave a blank.

    wordProgress = list()

    for char in wordToGuess:
        if char in guesses:
            wordProgress.append(char)
        else:
            wordProgress.append('_')

    return ' '.join(wordProgress)

class HangpersonGameState(object):
    def __init__(self, gameWord):
        self.gameWord = gameWord
        self.numTurns = 0
        self.guesses = list()
        self.remainingTries = 6

    def isGuessValid(self, guess):
        # Valid guesses are a single character string that is a-z
        if isinstance(guess, str) and guess.isalpha() and len(guess) == 1:
            return True
        
        return False

    def isGuessNew(self, guess):
        # Return True if the supplied guess has already been made?
        if guess in self.guesses:
            return False

        return True

    def hasWon(self):
        # Initializing win state to True, because we are going to determine by process of
        # elimination. If all characters are present in the guesses, then the game has
        # been won. Any characters that are not present in the guesses means the game
        # has not yet been won.
        winState = True
        for i, char in enumerate(self.gameWord):
            if char not in self.guesses:
                winState = False
        
        return winState

    def makeGuess(self, guess):
        result = []
        
        # Check that the guess is valid first
        if not self.isGuessValid(guess):
            result.append(f'"{guess}" is not valid. Your guess must be a single alphabetical character. Try again...')
            return result

        # if the guess is valid and new, add it to the list and increment the turn
        if not self.isGuessNew(guess):
            result.append(f'Hrmmm. You already guessed "{guess}", try again...')
            return result

        # Add the guess and increment the turn counter
        self.guesses.append(guess)
        self.numTurns += 1
        
        # Reduce the number of remaining tries if the guess is incorrect
        if guess in self.gameWord:
            result.append(f'Nice work! You got one!')
        else:
            self.remainingTries -= 1

            if self.remainingTries == 0:
                result.append(f'Oh no! You ran out of tries. The word was "{self.gameWord}" Better luck next time!')
            else:
                result.append(f'Uh oh! There is no "{guess}" in this word! You have {self.remainingTries} left!')
            
        result.append('\n')

        progress = 6 - self.remainingTries
        personProgress = getPersonString(progress)
        wordProgress = getWordProgressString(self.gameWord, self.guesses)
        result.append(personProgress)
        result.append('\n')
        result.append(wordProgress)
        result.append('\n')
        
        if self.hasWon():
            result.append(f'Congrats, you won!!')

        result.append('\n')
        return ''.join(result)

def newGame():
    # initate a game of hangperson
    print('Welcome to hangperson, an outdated game to test your word guessing skills. Prepare yourself!')

    # Begin initializing game state
    gameState = HangpersonGameState(getWord().casefold())
    
    while gameState.remainingTries > 0 and not gameState.hasWon():
        currentGuess = input('Guess a letter: ').casefold()
        print(gameState.makeGuess(currentGuess))

    playAgainResult = input('Play again? (Y or N): ')
    if playAgainResult.casefold() == 'y':
        newGame()

newGame()