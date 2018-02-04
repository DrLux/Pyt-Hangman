__author__ = 'Sorrentino Luca'

#####################################
# Autore: Sorrentino Luca
# Matricola: 797180
#####################################

import os
import getpass
import random
from os import listdir
from os.path import isfile, join


HANGMANPICS = ['''

    +---+
    |   |
        |
        |
        |
        |
   ========       ''', '''

    +---+
    |   |
    O   |
        |
        |
        |
   ========''', '''

    +---+
    |   |
    O   |
    |   |
        |
        |
   ========''', '''

    +---+
    |   |
   \O   |
    |   |
        |
        |
   ========''', '''

    +---+
    |   |
   \O/  |
    |   |
        |
        |
   ========''', '''

    +---+
    |   |
   \O/  |
    |   |
   /    |
        |
   ========''', '''

    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
   ========''']

YOUWIN = 1
YOULOSE = 2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Riceve e verifica la parola inserita dall' utente
def userInput():
    bool = True
    while bool:
        print("Insert the secret word: ")
        word = getpass.getpass("> ") #getpass non mostra l' input a schermo
        if word.isalpha(): #controlla che ci siano solo lettere (no space, no numeri o altro)
            bool = False
        else:
            print("Problem with input. The special characters are not allowed (Enter only letters)")
    return word.lower() #restituisco la parola in caratteri minuscoli

# Lancia una ricerca automatica del file nella directory attuale e in tutte le sottocartelle
def visit(mypath):
    for f in listdir(mypath):  #funzione di libreria che lista una cartella
        complete = join(mypath, f)  #concatena path folder e filename
        if isfile(complete):  #è un file?
            yield complete  #fine ricorsione
        else:  #se non è un file è una cartello, quindi lancio qui la ricorsione
            for t in visit(complete):  #continua ricorsione
                yield t

# Restituisce il path del file "impiccato.txt"
def findFile():
    bool_path = True
    mypath = os.getcwd() #stabilisce la tua posizione attuale nel filesystem
    scandir = visit(mypath)
    for file in scandir:
        if "hangman.txt" in file:  # se trova almeno 1 path che contiene "hangman.txt", anche se in una sottocartella
            return file
    print(" File non Found")
    while bool_path:
      filepath = input(" Insert a valid file path: ")
      if isfile(filepath): # Controlla se l'input utente punta davvero ad un file
        bool_path = False  
    return (filepath)

# Pesca una parola a caso dal file
def readData(path):
    if (input("Do you want to play in Single Player Mode? (yes or no) ").lower().startswith('y')):
        return userInput()
    else:
        infile = open(path, 'r')
        lines = infile.readlines() #legge il file riga per riga
        infile.close()
        max_lines = len(lines) #il numero massimo di righe
        choosed = random.randint(1, max_lines-1) #genero il numero random per scegliere la parola
        secretWord = lines[choosed]
        return secretWord.strip() #elimino l' ultimo carattere balnk

#Gli elementi da stampare a schermo
def displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord, endGame = 0):
    os.system('cls')
    print(bcolors.BOLD + bcolors.HEADER + " " + bcolors.UNDERLINE  + " H A N G M A N " + bcolors.ENDC)
    if endGame == 1:
        print(bcolors.OKGREEN +"\n YOU WIN!" + bcolors.ENDC)
    if endGame == 2:
        print (bcolors.FAIL + "\n GAME OVER!" + bcolors.ENDC)
    print(HANGMANPICS[len(missedLetters)])
    print("\n")

    print(' Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ') #sostituisco il newline con uno space, cosi ho tutte le lettere su una linea e non a capo
    print("\n")

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:] #sostituisci l' i-esimo * con la lettera giusta corrispondete

    for letter in blanks:
        print(" " + letter, end=' ')
    print("\n")

# Raccoglie e verifica le lettere inserite dall' utente
def getGuess(alreadyGuessed):
    while True:
        guess = input(" Guess a letter: ")
        guess = guess.lower()
        if len(guess) != 1: # Deve essere una unica lettera
            print(' Please enter only a single letter.')
        elif guess in alreadyGuessed: #Non deve essere già stata inserita
            print(' You have already entered that letter. Please choose another one.')
        elif guess.isalpha():
            return guess
        else:
            print(' Please enter a LETTER.')

# Torna true se il giocatore vuole giocare ancora, false altrimenti.
def playAgain():
    return input("\n\n Do you want to play again? (yes or no)  ").lower().startswith('y')


filePath = findFile()
missedLetters = ''
correctLetters = ''
secretWord = readData(filePath)
gameIsDone = False

while True:
    displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord)
    guess = getGuess(missedLetters + correctLetters) #Il giocatore non può inserire lettere già inserite, sia corrette che errate
    if guess in secretWord: #Se il giocatore indovina
        correctLetters = correctLetters + guess
        #Controllo se il giocatore ha vinto
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters: #Se c'è almeno una lettera della parola che non è nella lista di lettere indovinate
                foundAllLetters = False
                break
        if foundAllLetters: #se invece a questo punto foundAllLetters è rimasto true
            displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord, YOUWIN)
            print(' Yes! The secret word is "' + secretWord)
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess
        #Controllo se il giocatore ha perso
        if len(missedLetters) == len(HANGMANPICS) - 1: #Se il numero di lettere errate è quello di pezzi di omino
            displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord, YOULOSE)
            print(' You have run out of guesses!\n After ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            gameIsDone = True
    # Se gameIsDone è True, chiedo all' utente se vuole fare una nuova partita.
    if gameIsDone:
        if playAgain():
            os.system('cls')
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord = readData(filePath)
        else:
            break