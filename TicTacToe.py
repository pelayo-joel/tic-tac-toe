from IA import EasyIA, DrawIA
from pick import pick
import json
import os

"""This is the whole code for the Tic-Tac-Toe game, you might need to install pip and the library 'pick' for it to work properly,
    other than that the game should work flawlessly, it handles almost everything from AI difficulty, saving scores and users with rankings, replaying... """

"""GLOBAL VARIABLES"""
#emplacement is the board itself
emplacement = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
#playersName stores both active player, needed for how i builded the game
playersName = ["", ""]
#Are you playing with the computer ?
IAMode = False
#Data from the json file that contains all registered users:scores and stores it in 'scores'
with open("PlayerScores.json") as ps:
    scores = json.load(ps)

"""Displays an introduction to the game as well as the rules and how to play"""
def Intro():
    print(f"___________.__               ___________                       ___________            ")
    print(f"\__    ___/|__| ____         \__    ___/____      ____         \__    ___/___   ____  ")
    print(f"  |    |   |  |/ ___\   ______ |    |  \__  \   _/ ___\   ______ |    | /  _ \_/ __ \ ")
    print(f"  |    |   |  \  \___  /_____/ |    |   / __ \  \  \___  /_____/ |    |(  <_> )  ___/ ")
    print(f"  |____|   |__|\___  >         |____|  (____  /  \___  >         |____| \____/ \___  >")
    print(f"                   \/                       \/       \/                            \/ \n")
    try:
        input("\nPress enter to continue...")
        ClearScreen()
        print("\nRules and how to play :")
        input("\nPress enter to continue...")
        print("\n   -  If you've already played Tic-Tac-Toe, you already know the rules\n       align your signs vertically, horizontaly, or diagonaly on the board to win")
        input("\nPress enter to continue...")
        print("\n   -  Choose any boxes by pressing their coordinates (example : B2)")
        input("\nPress enter to continue...")
        print("\n   -  You can play either with a friend or the computer")
        input("\nPress enter to continue...")
    except KeyboardInterrupt or EOFError:     
        print("\nGame exit")
        exit()

"""Sets up the game, this is basically the main menu where you'll check the rules, the ranking, or if you want to play (pvp or against the AI)"""
def GameSetup():
    global playersName
    global IAMode
    while True:
        try:
            title = 'Game mode : '
            options = ['Solo', 'Multiplayer', 'Score Ranking', 'Rules']
            option, index = pick(options, title)
            if option == "Multiplayer":
                ClearScreen()
                IAMode = False
                for i in range(0, 2):
                    playersName[i] = str(input(f"Player {i+1} username (' ' are prohibited): "))
                    if " " in playersName[i] or playersName[i] == "":
                        playersName[i] = f"Guest{i+1}"
                    if playersName[i].lower() in scores:
                        print(f"Welcome back {playersName[i]}")
                    else:
                        print(f"Your name has been registered, greetings to {playersName[i]}")
                        scores.update({playersName[i].lower():0})
                        SaveJSON_Updates()
                ScoredBoard()
                input("\nPress enter to continue...")
                break
            elif option == "Solo":
                ClearScreen()
                IAMode = True
                titleIA = 'Choose your difficulty : '
                optionsIA = ['EasyIA', 'DrawIA']
                optionIA, index = pick(optionsIA, titleIA)
                if optionIA == "EasyIA":
                    playersName[0] = str(input(f"Player username : "))
                    playersName[1] = "EasyIA"
                    if playersName[0] == "":
                        playersName[0] = f"Guest1"
                    if playersName[0].lower() in scores:
                        print(f"Welcome back {playersName[0]}")
                    else:
                        print(f"Your name has been registered, greetings to {playersName[0]}")
                        scores.update({playersName[0].lower():0})
                        SaveJSON_Updates()
                    print(f"You'll play against {playersName[1]}")
                    input("\nPress enter to continue...")
                    break
                else:
                    playersName[0] = str(input(f"Player username : "))
                    playersName[1] = "DrawIA"
                    if playersName[0] == "":
                        playersName[0] = f"Guest1"
                    if playersName[0].lower() in scores:
                        print(f"Welcome back {playersName[0]}")
                    else:
                        print(f"Your name has been registered, greetings to {playersName[0]}")
                        scores.update({playersName[0].lower():0})
                        SaveJSON_Updates()
                    print(f"You'll play against {playersName[1]}")
                    input("\nPress enter to continue...")
                    break
            elif option == "Score Ranking":
                ClearScreen()
                ScoreRanking()
                input("\nPress enter to continue...")
            elif option == "Rules":
                ClearScreen()
                Intro()
        except KeyboardInterrupt or EOFError:
            ClearScreen()
            exit("Game exit")

           
"""Prints the board"""
def Board():
    print(f"         1       2       3    ")
    print("     " + "_"*25)
    print(f"     |       |       |       |\n  A  |   {emplacement[0][0]}   |   {emplacement[0][1]}   |   {emplacement[0][2]}   |")
    print(f"     |_______|_______|_______|")
    print(f"     |       |       |       |\n  B  |   {emplacement[1][0]}   |   {emplacement[1][1]}   |   {emplacement[1][2]}   |")
    print(f"     |_______|_______|_______|")
    print(f"     |       |       |       |\n  C  |   {emplacement[2][0]}   |   {emplacement[2][1]}   |   {emplacement[2][2]}   |")
    print(f"     |_______|_______|_______|\n")

"""Prints the Scores board between the two active players"""
def ScoredBoard():
    global playersName
    width = max(len(playersName[0]), len(playersName[1])) + 6

    print(5*" ",(width+5)*"_")
    print(5*" ", "|", (width+1)*" ", "|")
    print(5*" ", "|", 2*" ", playersName[0], scores[playersName[0].lower()], (width-5-len(playersName[0]))*" ", "|")
    print(5*" ", "|", 2*" ", playersName[1], scores[playersName[1].lower()], (width-5-len(playersName[1]))*" ", "|")
    print(5*" ", "|", (width+1)*"_", "|\n")

"""Displays the ranking between all registered players"""
def ScoreRanking():
    width = 0
    longestName = 0
    rank = 1
    storedName = []
    margin = 5*f" "
    padding = 2*f" "
    firstLabel = f"Rank"
    secondLabel = f"Name"
    thirdLabel = f"Scores"

    for keys in scores:
        if longestName < len(keys):
            longestName = len(keys)
    rankedScores = sorted(list(scores.values()), key=None, reverse=True)
    width = len(padding)+len(firstLabel)+1+len(secondLabel)+(longestName-3)+1+len(thirdLabel)+8

    print(margin,(width+3)*f"_")
    print(margin, f"|", width*f" ", f"|")
    print(margin, f"|", padding, firstLabel, f" ", secondLabel, (longestName-3)*f" ", f" ", thirdLabel, f" ", f"|")
    print(margin, f"|", width*f" ", f"|")
    for i in range(len(rankedScores)-1):
        if i > 0 and rankedScores[i] != rankedScores[i-1]:
            rank += 1
        name = ""
        for key, value in scores.items():
            if rankedScores[i] == value and (key not in storedName) :
                name = key
                storedName.append(name)
                break
        print(margin, f"|", padding+f" ", rank, 3*f" ", name, ((longestName-len(name)+4))*f" ", rankedScores[i], (len(thirdLabel)-1)*f" ", f"|")
    print(margin, f"|", (width)*f"_", f"|\n")

"""Clears the board if you're replaying"""
def ClearBoard(): 
    global emplacement
    emplacement = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

"""The input system, it works with coordinates"""
def InputSystem(playerSign, posInput):
    x = ["A", "B", "C"]
    posY = int(posInput[1]) - 1
    posX = posInput[0].upper()

    if (posX not in x and (0 > posY and 2 < posY)):
        return False
    elif emplacement[x.index(posX)][posY] != " ":
        print("Choose among the remaining boxes")
        return False
    else:
        emplacement[x.index(posX)][posY] = playerSign
        return True

"""As the name implies, checks if the board has a winning combination"""
def WinCheck(board):
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return True
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            return True
    if ((board[0][0] == board[1][1] == board[2][2] != " ") or
        (board[2][0] == board[1][1] == board[0][2] != " ")):
        return True
    return False

"""Utility function to clean up the code, as its name implies it updates the json file if there are any changes between scores and the json"""
def SaveJSON_Updates():
    with open("PlayerScores.json", "w") as ps:
        json.dump(scores, ps, indent=4, separators=(",",": "))

"""Utility function, clears the terminal screen for clarity"""
def ClearScreen():
    osName = os.name
    if osName == "posix":
        os.system("clear")
    elif osName == "nt":
        os.system("cls")



"""The game itself"""
def main():
    global emplacement
    global playersName
    global IAMode
    playerName = ""
    player = ""
    playerTurn = 0
    turn = 1

    Intro()
    while True:

        GameSetup()

        while True:
            try:
                ClearScreen()
                starter = str(input(f"Who's starting ? (1 : {playersName[0]}, 2 : {playersName[1]})\n"))
                if starter == "2": 
                    tmp = playersName[0]
                    playersName[0] = playersName[1]
                    playersName[1] = tmp
                if ("DrawIA" in playersName or "EasyIA" in playersName) and starter == "2":
                    charSel = input("\nChoose your sign (X or O) : ")
                    if charSel == "X" or charSel =="x":
                        playerTurn = -1
                        break
                    elif charSel == "O" or charSel == "o": 
                        playerTurn = 1
                        break
                    else:
                        print("X or O")
                else:
                    charSel = input(f"\n{playersName[0]}, choose between X or O : ")
                    if charSel == "X" or charSel =="x":
                        playerTurn = 1
                        break
                    elif charSel == "O" or charSel == "o": 
                        playerTurn = -1
                        break
                    else:
                        print("X or O")
            except KeyboardInterrupt or EOFError:
                print("\nGame exit")
                exit()

        while True:
            print(f"\nTurn {turn}\n")
            if turn % 2 != 0:
                playerName = playersName[0]
            else:
                playerName = playersName[1]
            if playerTurn == 1:
                player = "X"
            else:
                player = "O"

            Board()

            print(f"     {playerName} : {player}\n")
            position = 0
            while True:
                try:
                    if IAMode and playerName == "EasyIA":
                        input(f"{playerName}'s turn...\n")
                        position = str(EasyIA(emplacement))
                    elif IAMode and playerName == "DrawIA":
                        input(f"{playerName}'s turn...\n")
                        position = str(DrawIA(emplacement, player))
                    else:
                        position = input(f"{playerName}, enter a position (coordinates like B2): ")

                    if InputSystem(player, position):
                        break
                except KeyboardInterrupt or EOFError:
                    print("\nGame exit")
                    exit()
                except:
                    ClearScreen()
                    Board()
                    print("Invalid number or input, try again")

            if turn > 8 and not WinCheck(emplacement):
                ClearScreen()
                Board()
                print("GGs to both players, it is a draw")
                input("\nPress enter to continue...")
                SaveJSON_Updates()
                ScoredBoard()
                replay = input("Would you like to play again ? (Y/n) : ")
                if replay.upper() == "YES" or replay.upper() == "Y":
                    turn = 1
                    ClearBoard()
                    break
                ClearScreen()
                exit("\nThanks for playing !")
            elif WinCheck(emplacement):
                ClearScreen()
                Board()
                print(f"Congratulations, {playerName} wins")
                scores.update({playerName.lower():(scores[playerName.lower()]+1)})
                SaveJSON_Updates()
                ScoredBoard()
                input("\nPress enter to continue...")
                replay = input("Would you like to play again ? (Y/n) : ")
                if replay.upper() == "YES" or replay.upper() == "Y":
                    turn = 1
                    ClearBoard()
                    break
                ClearScreen()
                exit("\nThanks for playing !")
            
            ClearScreen()
            playerTurn *= -1
            turn += 1

        


if __name__ == "__main__":
    main()