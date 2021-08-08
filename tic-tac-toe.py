"""
Set task: Creating a tic-tac-toe game with a GUI.
Method:
* On __init__(), self.board (list) is generated with 9 empty cells in 3 rows and 3 columns and self.turn (in) is set to 0. self.gameover (dict) is also reset.
* game() randomly sets self.turn to 0 or 1. Even turns are considered player turns, odd turns are computer turns and the respective method is called.
* __playerTurn__() asks the player for input in form "x-y" and updates the corresponding cell in self.board.
* __computerTurn__() calls on __simulate()__ to do the heavy lifting. Here Greg Surma's "Unbeatable AI" algorithm is implemented, check https://gsurma.medium.com/tic-tac-toe-creating-unbeatable-ai-with-minimax-algorithm-8af9e52c1e7d#14e6 for the details.
* __gameOver__() checks all possible win conditions and updates self.gameover accordingly.
"""

from random import randint
from re import fullmatch
from copy import deepcopy
from time import sleep
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

class TicTacToe:

    def __init__(self):
        self.board = [
            ["","",""],
            ["","",""],
            ["","",""]
            ]
        self.turn = 0
        self.gameover = {"Gameover": False, "Winner": None}

        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.root.title("Tic-Tac-Toe")

        self.font = Font(family="Verdana", size=48)
        self.textLabel = tk.Label(self.root,font="Verdana 12",width=20,height=2,text="")
        self.textLabel.grid(row=0,column=0,columnspan=3)

        self.button11 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((1,1)))
        self.button11.grid(row=1,column=0)
        self.button12 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((1,2)))
        self.button12.grid(row=1,column=1)
        self.button13 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((1,3)))
        self.button13.grid(row=1,column=2)

        self.button21 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((2,1)))
        self.button21.grid(row=2,column=0)
        self.button22 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((2,2)))
        self.button22.grid(row=2,column=1)
        self.button23 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((2,3)))
        self.button23.grid(row=2,column=2)

        self.button31 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((3,1)))
        self.button31.grid(row=3,column=0)
        self.button32 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((3,2)))
        self.button32.grid(row=3,column=1)
        self.button33 = tk.Button(self.root,height=1,width=3,font=self.font,state="disabled",command=lambda: self.__playerTurn__((3,3)))
        self.button33.grid(row=3,column=2)

        self.buttonStart = tk.Button(self.root,height=1,width=15,font="Verdana 12",text="Start",command=self.__gameStart__)
        self.buttonStart.grid(row=4,column=1,columnspan=2)

        self.buttons=[
            [self.button11,self.button12,self.button13],
            [self.button21,self.button22,self.button23],
            [self.button31,self.button32,self.button33]
        ]

        self.root.mainloop()

    def __repr__(self):
        gameboard = list()
        for row in self.board:
            for cell in row:
                if not cell:
                    gameboard.append(" ")
                else:
                    gameboard.append(cell)
        
        return f"-------------\n| {gameboard[0]} | {gameboard[1]} | {gameboard[2]} |\n| {gameboard[3]} | {gameboard[4]} | {gameboard[5]} |\n| {gameboard[6]} | {gameboard[7]} | {gameboard[8]} |\n-------------"

    def __gameStart__(self):
        self.board = [
            ["","",""],
            ["","",""],
            ["","",""]
            ]
        self.turn = 0
        self.gameover = {"Gameover": False, "Winner": None}
        self.buttonStart.configure(text="Restart",foreground="red")
        for row in self.buttons:
            for column in row:
                column.configure(state="normal",text="")
        self.turn = randint(0,1)
        if self.turn == 0:
            self.textLabel.configure(text="Computer turn.")
            self.textLabel.update()
            self.__computerTurn__()
        self.textLabel.configure(text="Player turn.")

    def __computerTurn__(self):
        sleep(randint(0,3))
        result = self.__simulate__(self.board,self.turn)
        self.board[result[0]][result[1]] = "O"
        self.buttons[result[0]][result[1]].configure(text="O",state="disabled")
        self.__gameOver__(self.board)
        if self.gameover["Gameover"]:
            self.textLabel.configure(text="Game Over.")
            for row in self.buttons:
                for column in row:
                    column.configure(state="disabled")
            if self.gameover["Winner"] == None:
                messagebox.showinfo(title="Game Over.",message="You managed to draw!")
            else:
                messagebox.showinfo(title="Game Over.",message=f"{self.gameover['Winner']} victory")
        else:
            self.textLabel.configure(text="Player turn.")
            self.turn += 1

    def __playerTurn__(self,val):
        self.board[int(val[0])-1][int(val[1])-1] = "X"
        self.buttons[int(val[0])-1][int(val[1])-1].configure(text="X",state="disabled")
        self.__gameOver__(self.board)
        if self.gameover["Gameover"]:
            self.textLabel.configure(text="Game Over.")
            for row in self.buttons:
                for column in row:
                    column.configure(state="disabled")
            if self.gameover["Winner"] == None:
                messagebox.showinfo(title="Game Over.",message="You managed to draw!")
            else:
                messagebox.showinfo(title="Game Over.",message=f"{self.gameover['Winner']} victory")
        else:
            self.textLabel.configure(text="Computer turn.")
            self.textLabel.update()
            self.turn += 1
            self.__computerTurn__()

    def __simulate__(self,board,turn):
        boardClone = deepcopy(board)
        goodResults = []
        drawResults = []
        badResults = []
        result = list()
        #print(f"goodResults={goodResults}\ndrawResults={drawResults}\nbadResults={badResults}")
        for i in range(3):
            for j in range(3):
                #boardClone2 = deepcopy(board)
                #print(f"i,j={i,j}, board[i][j]={boardClone[i][j]}\nTurn={turn}\nResults={result}\nGoodResults={goodResults}\nDrawResults={drawResults}\nBadResults={badResults}")
                if not boardClone[i][j]:
                    if turn%2:
                        boardClone[i][j] = "X"
                    else:
                        boardClone[i][j] = "O"
                    gameover = self.__gameOver__(boardClone)
                    if gameover["Gameover"] and gameover["Winner"] == "PC":
                        result.append(1)
                    elif gameover["Gameover"] and gameover["Winner"] == "Player":
                        result.append(-1)
                    elif gameover["Gameover"]:
                        result.append(0)
                    else:
                        #print("calling simulate again",boardClone)
                        result.append(self.__simulate__(boardClone,turn+1))
                    if turn == self.turn and result[-1] == 1:
                        goodResults.append((i,j))
                    elif turn == self.turn and result[-1] == 0:
                        drawResults.append((i,j))
                    elif turn == self.turn and result[-1] == -1:
                        badResults.append((i,j))
                    boardClone[i][j] = ""
        #print(f"Turn={turn}\nResults={result}\nGoodResults={goodResults}\nDrawResults={drawResults}\nBadResults={badResults}")
        if len(goodResults) > 0:
            return goodResults[randint(0,len(goodResults)-1)]
        elif len(drawResults) > 0:
            return drawResults[randint(0,len(drawResults)-1)]
        elif len(badResults) > 0:
            return badResults[randint(0,len(badResults)-1)]
        elif turn % 2:
            return min(result)
        return max(result)

    def __gameOver__(self,board):
        gameover = False
        winner = None
        if ["X","X","X"] in board:
            gameover = True
            winner = "Player"
        elif ["O","O","O"] in board:
            gameover = True
            winner = "PC"
        else:
            for i in range(3):
                if [board[0][i],board[1][i],board[2][i]] == ["X","X","X"]:
                    gameover = True
                    winner = "Player"
                    break
                elif [board[0][i],board[1][i],board[2][i]] == ["O","O","O"]:
                    gameover = True
                    winner = "PC"
                    break
            if [board[0][0],board[1][1],board[2][2]] == ["X","X","X"] or [board[0][2],board[1][1],board[2][0]] == ["X","X","X"]:
                gameover = True
                winner = "Player"
            elif [board[0][0],board[1][1],board[2][2]] == ["O","O","O"] or [board[0][2],board[1][1],board[2][0]] == ["O","O","O"]:
                gameover = True
                winner = "PC"
            elif "" not in board[0] and "" not in board[1] and "" not in board[2]:
                gameover = True
        
        self.gameover = {"Gameover": gameover, "Winner": winner}
        return self.gameover

    def __reset__(self):
        pass

T = TicTacToe()