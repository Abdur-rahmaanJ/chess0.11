## Simple Chess Engine

## Tkinter rewrite (was originally pygame)

import sys
import time
import random
import Image
#import threading
#from threading import Timer
import Tkinter
import PIL
import tkMessageBox
global tkFrame
from Tkinter import *
from PIL import ImageTk, Image
from piecesquaretables import *
from GUI import *
import GUI

class TkFrame(Frame):
    # main Tk frame

    def __init__(self, parent):
        Frame.__init__(self, parent, relief=RAISED)
        self.parent = parent
        self.img = {}
        self.initUI()

    def initUI(self):
        self.parent.title("Raven Chess Engine 0.11")
        self.parent.minsize(687,505)
        self.pack(fill=BOTH, expand=YES)

class NewGameDialog:

    def __init__(self, parent):

        global AIOption
        global flippedVar

        flippedVar = False
        
        top = self.top = Toplevel(parent)
        top.title("")
        top.iconbitmap(r'icon.ico')
        lbl = Label(top, text="New Game")
        lbl.config(font=('calibri',(15)))
        lbl.grid(row=0,column=0,columnspan=2)
        #lbl.pack()

        '''
        self.e = Entry(top)
        self.e.pack(padx=5)
        self.e.focus_set()
        '''
        master = top

        lblBlack = Label(top, text="Black")
        lblBlack.config(font=('calibri',(12)))
        lblBlack.grid(row=1,column=0)
        
        master.blackPlayerOption = StringVar()
        master.blackPlayerOption.set("Raven 0.1") # default value

        self.blackPlayer = OptionMenu(master, master.blackPlayerOption, "Raven 0.1", "Human")
        self.blackPlayer.config(width=15, font=('calibri',(9)),bg='white')
        self.blackPlayer.grid(row=1,column=1)

        lblWhite = Label(top, text="White")
        lblWhite.config(font=('calibri',(12)))
        lblWhite.grid(row=2,column=0)
        
        master.whitePlayerOption = StringVar()
        master.whitePlayerOption.set("Human") # default value

        self.whitePlayer = OptionMenu(master, master.whitePlayerOption, "Raven 0.1", "Human")
        self.whitePlayer.config(width=15, font=('calibri',(9)),bg='white')
        self.whitePlayer.grid(row=2,column=1)
        #w.pack()

        self.var = BooleanVar()
        chkFlipped = Checkbutton(master, command=self.setflipped, variable=self.var, text="Black plays from bottom")
        chkFlipped.grid(row=3,column=0, columnspan=3)

        b = Button(top, text="Start Game", command=self.ok)
        b.grid(row=4,column=0, columnspan=3, ipadx=50)
        #b.pack(pady=5)

    def setflipped(self):
        global flippedVar

        flippedVar = self.var.get()

    def ok(self):

        global AIDepth
        global flipped, flippedVar

        #print "value is", self.top.AIOption.get()
        blackPlayer = None
        if self.top.blackPlayerOption.get() == "Human": blackPlayer = "Human"
        if self.top.blackPlayerOption.get() == "Raven 0.1": blackPlayer = "AI"
        whitePlayer = None
        if self.top.whitePlayerOption.get() == "Human": whitePlayer = "Human"
        if self.top.whitePlayerOption.get() == "Raven 0.1": whitePlayer = "AI"
        #print blackPlayer, whitePlayer
        #print parent.AIOption.get()
        #AIDepth = (int(self.e.get()) - 1)
        flipped = flippedVar
        initNewGame(whitePlayer, blackPlayer)
        drawBoard()
        drawPieces()

        self.top.destroy()

class PromoteDialog:
    
    def __init__(self, parent):
        global game
        global promPiece
        global promTkRoot
        
        #print game['tomove']
        top = self.top = Toplevel(parent)
        #print top
        top.title("Promote")
        top.iconbitmap(r'icon.ico')
        photoQ=ImageTk.PhotoImage(file='pieces\BQ.png')
        photoR=ImageTk.PhotoImage(file='pieces\BR.png')
        photoB=ImageTk.PhotoImage(file='pieces\BB.png')
        photoN=ImageTk.PhotoImage(file='pieces\BN.png')
        if game['tomove'] == "White":
            photoQ=ImageTk.PhotoImage(file='pieces\WQ.png')
            photoR=ImageTk.PhotoImage(file='pieces\WR.png')
            photoB=ImageTk.PhotoImage(file='pieces\WB.png')
            photoN=ImageTk.PhotoImage(file='pieces\WN.png')
        btnQ = Button(top, command=self.selPieceQ,image=photoQ)
        btnR = Button(top, command=self.selPieceR,image=photoR)
        btnB = Button(top, command=self.selPieceB,image=photoB)
        btnN = Button(top, command=self.selPieceN,image=photoN)
        btnQ.image = photoQ
        btnR.image = photoR
        btnB.image = photoB
        btnN.image = photoN
        btnQ.grid(row=0,column=0, columnspan=1, ipadx=0)
        btnR.grid(row=0,column=1, columnspan=1, ipadx=0)
        btnB.grid(row=0,column=2, columnspan=1, ipadx=0)
        btnN.grid(row=0,column=3, columnspan=1, ipadx=0)
        
    def selPieceQ(self):
        global promPiece
        promPiece = 'Q'
        self.top.destroy()
    def selPieceR(self):
        global promPiece
        promPiece = 'R'
        self.top.destroy()
    def selPieceB(self):
        global promPiece
        promPiece = 'B'
        self.top.destroy()
    def selPieceN(self):
        global promPiece
        promPiece = 'N'
        self.top.destroy()

class moveNode:
    def __init__(self, move, children, parent) :
        self.move = move
        self.children = children
        self.parent = parent
        score = None
        depth = 1


def main():
    global app
    global board
    global boardCanvas
    global movesText
    global movesTextScr
    global evalLabel
    global evalLabelText
    global thinkingLabel
    global thinkingLabelText
    global topLabel,bottomLabel
    global freePlay
    global tkRoot
    global clickDragging
    global AIDepth
    global knightVal, rookVal, gameStage, pawnCount
    global flipped, flippedVar
    global boardHistory, boardHistoryPos
    global oldappheight, oldappwidth
    global boardImg

    global topLabel, bottomLabel, movesText, movesTextScr, btnFirst, btnPrev, btnNext, btnLast

    boardHistory = []
    boardHistoryPos = 0

    board = []

    flipped = False

    knightVal = 2.5
    rookVal = 5
    gameStage = 'Opening'
    pawnCount = 16
    AIDepth = 1

    clickDragging = False
    freePlay = False

    initGame()

    tkRoot = Tk()
    tkRoot.iconbitmap(r'icon.ico')
    # position/dimensions for main tk frame
    x = 100
    y = 100
    if "tv" == "tv1":
        x = 1420
        y = 100
    w = 687
    h = 505
    oldappheight = h
    oldappwidth = w
    geostring = "%dx%d+%d+%d" % (w, h, x, y)

    tkRoot.geometry(geostring)
    app = TkFrame(tkRoot)

    app.bind("<Configure>", appresize)
    boardCanvas = Canvas(app, width=480, height=480)
    boardCanvas.bind("<Button-1>", canvasClick)
    boardCanvas.bind("<ButtonRelease-1>", canvasRelease)
    boardCanvas.bind("<B1-Motion>", canvasMotion)
    #boardCanvas.config(bg="black")
    boardCanvas.pack(expand=YES)
    boardCanvas.place(x=0, y=25)

    topLabel = Label(tkRoot, bg="#000000", fg="white", bd=2, relief=GROOVE, font=('calibri',(12),'bold'), text="")
    topLabel.place(x=495,y=28,w=180,h=40)
    bottomLabel = Label(tkRoot, bg="white", fg="black", bd=2, relief=GROOVE, font=('calibri',(12),'bold'), text="")
    bottomLabel.place(x=495,y=460,w=180,h=40)
    #topLabel.pack()
    #movesLbl = Label(tkRoot, text="Moves")
    #movesLbl.pack()
    #movesLbl.place(x=500, y=205)

    movesText = Text(tkRoot, width=22, height=8, background="#555555", foreground="#FFFFFF")


    movesTextScr = Scrollbar(tkRoot)
    movesTextScr.config(command=movesText.yview)
    #movesTextScr.grid(row=0, column=1, sticky='nsew')
    movesText.config(yscrollcommand=movesTextScr.set)

    movesTextScr.pack(side="right",fill="y", expand=False)
    movesText.pack(side="left", fill="both", expand=True)

    #movesText.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    movesText.place(x=500,y=180)
    movesTextScr.place(x=669,y=180,w=10,h=132)
    movesTextScr.activate(tkRoot)

    btnFirst = Button(tkRoot, text="<<", command=skipFirst)
    btnFirst.place(x=500,y=312,w=45,h=25)

    btnPrev = Button(tkRoot, text="<", command=skipPrev)
    btnPrev.place(x=545,y=312,w=45,h=25)

    btnNext = Button(tkRoot, text=">",command=skipNext)
    btnNext.place(x=590,y=312,w=45,h=25)

    btnLast = Button(tkRoot, text=">>", command=skipLast)
    btnLast.place(x=635,y=312,w=45,h=25)

    evalLabelText = StringVar()
    thinkingLabelText = StringVar()

    evalLabel= Label(tkRoot, text="Eval: 0",  textvariable=evalLabelText)
    evalLabel.pack()
    evalLabel.place(x=500, y=190)
    evalLabel.place(x=50000, y=19000)    

    thinkingLabel= Label(tkRoot, text="Thinking: 0%",  textvariable=thinkingLabelText)
    thinkingLabel.pack()
    thinkingLabel.place(x=500, y=210)
    thinkingLabel.place(x=50000, y=21000)
    evalLabelText.set("Eval: 0")
    thinkingLabelText.set("Thinking: 0%")

    app.menubar = Menu
    # Game menu
    Menubar = Menubutton(app, text="Game", bd=0)
    Menubar.grid()
    Menubar.menu = Menu(Menubar, tearoff=0)
    Menubar["menu"] = Menubar.menu
    Menubar.menu.add_command(label="New Game", command=newgamedlg)
    Menubar.menu.add_command(label="Resign", command=resign)
    #Menubar.menu.add_command(label="New Game(ava)", command=newgameava)
    #Menubar.menu.add_command(label="New Game(hva)", command=newgamehva)
    #Menubar.menu.add_command(label="New Game(hvh)", command=newgamehvh)
    #Menubar.menu.add_command(label="Analysis", command=analysis)
    Menubar.menu.add_command(label="Exit", command=tkRoot.destroy)

    # Practice menu
    MenuPrac = Menubutton(app, text="Practice", bd=0)
    MenuPrac.grid()
    MenuPrac.menu = Menu(MenuPrac, tearoff=0)
    MenuPrac["menu"] = MenuPrac.menu
    MenuPrac.place(x=60, y=0)
    MenuPrac.menu.add_command(label="Queen and Rook Mate", command=pracQueenRookMate)
    MenuPrac.menu.add_command(label="One Queen Mate", command=pracOneQueenMate)
    MenuPrac.menu.add_command(label="One Rook Mate", command=pracOneRookMate)
    MenuPrac.menu.add_command(label="Two Bishops Mate", command=pracTwoBishopsMate)
    MenuPrac.menu.add_command(label="Bishop and Knight Mate", command=pracBishopKnightMate)
    tkRoot.config(menu=Menubar)
    tkRoot.update()
    initNewGame("Human", "AI")
    #game['ended'] = True
    drawBoard()
    drawPieces()
    #drawCover()
    tkRoot.after(1, gameloop)
    tkRoot.mainloop()
    #print "!!!!"

def appresize(event):
    global boardCanvas
    global canvasSize
    global board
    global app
    global tkRoot
    global boardImg
    global topLabel, bottomLabel, movesText, movesTextScr, btnFirst, btnPrev, btnNext, btnLast

    boardCanvas.pack(expand=YES)
    boardCanvas.config(width=30, height=30,bg="black")
    boardCanvas.pack(expand=NO)
    #print app.winfo_height()
    appheight = app.winfo_height()
    appwidth = app.winfo_width()
    biggestDim = "height"
    canvasSize = appwidth - 202
    if appwidth > appheight:
        biggestDim = "width"
        canvasSize = appheight - 25
    if appwidth < (canvasSize + 202):
        canvasSize = appwidth - 202
    #scaleh = appheight / oldappheight
    #scalew = appwidth / oldappwidth
    #print appwidth, appheight, canvasSize
    canvasSize = (int(canvasSize / 8) * 8)
    h = canvasSize
    w = canvasSize
    #boardImg.zoom(scalew, scaleh)
    boardCanvas.place(x=00,y=25,w=w,h=h)
    topLabel.place(x=(canvasSize + 10))
    bottomLabel.place(x=(canvasSize + 10),y=(canvasSize-20))
    movesText.place(x=(canvasSize + 10),y=((canvasSize / 2) - 60))
    movesTextScr.place(x=(canvasSize + 10 + 160),w=20,y=((canvasSize / 2) - 60))
    btnFirst.place(x=(canvasSize + 10),y=((canvasSize / 2) + 73))
    btnPrev.place(x=(canvasSize + 10 + 45),y=((canvasSize / 2) + 73))
    btnNext.place(x=(canvasSize + 10 + 90),y=((canvasSize / 2) + 73))
    btnLast.place(x=(canvasSize + 10 + 135),y=((canvasSize / 2) + 73))

    drawBoard()
    drawPieces()
    tkRoot.update()

def skipFirst():
    global boardHistory, boardHistoryPos
    boardHistoryPos = 0
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()

def skipPrev():
    global boardHistory, boardHistoryPos
    boardHistoryPos -= 1
    if boardHistoryPos < 0: boardHistoryPos = 0
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()
    pass

def skipNext():
    global boardHistory, boardHistoryPos
    boardHistoryPos += 1
    if boardHistoryPos > (len(boardHistory) - 1): boardHistoryPos = len(boardHistory) - 1
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()
    pass

def skipLast():
    global boardHistory, boardHistoryPos
    boardHistoryPos = (len(boardHistory) - 1)
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()
    pass

def gameloop():
    global game, player, board
    if game['ended'] == False:
        playerType = player[game['tomove']]
        #playerType = "AI"
        if playerType == 'AI':
            tkRoot.update()
            makeAIMove()

        #tkRoot.update()
        # tkRoot.mainloop()
    tkRoot.after(1, gameloop)


def initGame():
    # Initialize when program runs

    global game  # main game dict
    global kingPos  # positions of white/black king
    global player  # defines player for each side (Human or AI)
    global board  # 64-byte array
    global pieceList
    global pieceCol
    global legalMoves
    global moveSet
    global player  # whether player White/Black is human or AI
    global legalMovesEP
    global legalMovesCastling
    global allowCastlingQS, allowcastlingKS
    global isSearching
    global AILevel
    global pieceVal
    global evalMobilityCheck
    global moveList
    global pieceSquareTable, pieceSquareTableEndgame, pieceSquareTableOpening
    global logFile

    logFile = open("ai_log.txt","w")

    evalMobilityCheck = True

    pieceVal = {'P': 1.00, 'B': 3.20, 'N': 3.00, 'R': 5.00, 'Q': 9.00, 'K': 1000.00}
    AILevel = 2
    player = {}
    game = {}
    game['delay'] = 0
    pieceList = {}
    pieceCol = {}
    legalMoves = []
    kingPos = {}
    moveSet = {}
    legalMovesEP = []
    legalMovesCastling = []
    allowCastlingQS = {'White': True, 'Black': True}
    allowCastlingKS = {'White': True, 'Black': True}
    isSearching = False
    moveList = []

    moveSet['N'] = [(-2, -1), (-2, +1), (-1, -2), (-1, +2), (+1, -2), (+1, +2), (+2, -1), (+2, +1)]
    moveSet['B'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]  # four diagonal directions
    moveSet['R'] = [(+0, -1), (+0, +1), (-1, +0), (+1, +0)]  # four lateral directions
    moveSet['Q'] = moveSet['R'] + moveSet['B']
    moveSet['K'] = moveSet['Q']
    pieceList['White'] = 'P', 'R', 'N', 'B', 'Q', 'K'
    pieceList['Black'] = 'p', 'r', 'n', 'b', 'q', 'k'
    pieceCol = {'P': 'White', 'R': 'White', 'N': 'White', 'B': 'White', 'Q': 'White', 'K': 'White',
                'p': 'Black', 'r': 'Black', 'n': 'Black', 'b': 'Black', 'q': 'Black', 'k': 'Black',
                '0': '0'}

def initNewGame(player1, player2):
    #print "new game:", player1, player2
    global board
    global allowCastlingQS, allowCastlingKS
    global moveList
    global moveNum
    global movesText
    global movesTextScr
    global topLabel, bottomLabel
    global tkRoot
    global flipped
    global boardHistory, boardHistoryPos

    #top player is black

    #print "!!!!!"
    whiteText = player1
    blackText = player2
    if whiteText == "AI": whiteText = "Raven"
    if blackText == "AI": blackText = "Raven"
    topLabel.config(bg="black",fg="white")
    bottomLabel.config(bg="white",fg="black")
    topLabel.config(text=blackText)
    bottomLabel.config(text=whiteText)

    if flipped:
        topLabel.config(bg="white",fg="black")
        bottomLabel.config(bg="black",fg="white")
        topLabel.config(text=whiteText)
        bottomLabel.config(text=blackText)
    tkRoot.update()

    moveList = []
    movesText.delete(1.0, Tkinter.END)
    moveNum = 1
    player['White'] = player1
    player['Black'] = player2
    game['tomove'] = 'White'
    game['nottomove'] = 'Black'
    game['3fold-draw'] = False
    game['50-move-count'] = 0
    game['50-move-draw'] = False
    game['check'] = False
    kingPos['White'] = (4, 7)
    kingPos['Black'] = (4, 0)
    game['movelist'] = []
    legalMovesEP = []
    legalMovesCastling = []
    allowCastlingQS = {'White': True, 'Black': True}
    allowCastlingKS = {'White': True, 'Black': True}
    game['ended'] = False
    board = [
        'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
        'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
        'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
    ]
    '''
    board = [
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', 'P', 'P', 'P', '0',
        '0', 'K', '0', '0', '0', '0', '0', 'P',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', 'R',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', 'k', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
    ]
    '''
    #print len(board)
    # if player[game['tomove']] == 'AI':
    #makeAIMove()
    boardHistory = []
    boardHistory.append(list(board))
    boardHistoryPos = 0
    genLegalMoves()


def initPracGame(gameType):
    global board, kingPos, allowCastlingKS, allowCastlingQS, tkRoot, game
    global boardHistory, boardHistoryPos
    initNewGame("Human", "AI")
    board = [
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
    ]
    game['tomove'] = 'White'
    game['nottomove'] = 'Black'
    # add white king
    # generate random square on board
    generating = True
    while generating:
        randpos = (random.randint(0, 7), random.randint(0, 7))
        if board[convertSquaretoPos(randpos)] == '0': generating = False  # make sure square is empty
        kingPos['White'] = randpos
        board[convertSquaretoPos(randpos)] = 'K'

    if gameType == "One Rook Mate":
        # add white rook
        # generate random square on board
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            if board[convertSquaretoPos(randpos)] == '0':
                board[convertSquaretoPos(randpos)] = 'R'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'R'

    if gameType == "One Queen Mate":
        # add white queen
        # generate random square on board
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            if board[convertSquaretoPos(randpos)] == '0':
                board[convertSquaretoPos(randpos)] = 'Q'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'Q'

    if gameType == "Queen and Rook Mate":
        # add white queen
        # generate random square on board
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            if board[convertSquaretoPos(randpos)] == '0':
                board[convertSquaretoPos(randpos)] = 'Q'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'Q'

        # add white rook
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            if board[convertSquaretoPos(randpos)] == '0':
                board[convertSquaretoPos(randpos)] = 'R'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'R'
    
    if gameType == "Two Bishops Mate":
        #print "!"
        # add white light square bishop
        # generate random square on board
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            i = randpos[0]
            j = randpos[1]
            col = 'light'
            if ( ( (i + j) % 2 ) == 0 ): col = 'dark'
            if board[convertSquaretoPos(randpos)] == '0' and col == 'light':
                board[convertSquaretoPos(randpos)] = 'B'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'B'
        
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            i = randpos[0]
            j = randpos[1]
            col = 'light'
            #print (i,j), col
            if ( ( (i + j) % 2 ) == 0 ): col = 'dark'
            if board[convertSquaretoPos(randpos)] == '0' and col == 'dark':
                board[convertSquaretoPos(randpos)] = 'B'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'B'

    if gameType == "Bishop and Knight Mate":
        # add white queen
        # generate random square on board
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            if board[convertSquaretoPos(randpos)] == '0':
                board[convertSquaretoPos(randpos)] = 'B'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'B'
        
        generating = True
        while generating:
            randpos = (random.randint(0, 7), random.randint(0, 7))
            origPiece = board[convertSquaretoPos(randpos)]
            if board[convertSquaretoPos(randpos)] == '0':
                board[convertSquaretoPos(randpos)] = 'N'
                #print isInCheck(board, kingPos['Black'], 'Black')
                generating = False  # make sure square is empty
            board[convertSquaretoPos(randpos)] = origPiece
        board[convertSquaretoPos(randpos)] = 'N'

    # add black king
    # generate random square on board
    generating = True
    while generating:
        randpos = (random.randint(0, 7), random.randint(0, 7))
        origPiece = board[convertSquaretoPos(randpos)]
        board[convertSquaretoPos(randpos)] = 'k'
        origKingPos = kingPos['Black']
        kingPos['Black'] = randpos
        if origPiece == '0' and isInCheck(board, randpos,
                                                                   'Black') == False: generating = False  # make sure square is empty
        board[convertSquaretoPos(randpos)] = origPiece
        kingPos['Black'] = origKingPos
        genLegalMoves()
        if len(legalMoves) == 0: generating = True
    kingPos['Black'] = randpos
    board[convertSquaretoPos(randpos)] = 'k'

    #kingPos['White'] = (4, 5)
    #kingPos['Black'] = (0, 3)
    allowCastlingQS = {'White': False, 'Black': False}
    allowCastlingKS = {'White': False, 'Black': False}

    boardHistory = []
    boardHistoryPos = 0
    boardHistory.append(list(board))

    genLegalMoves()
    drawBoard()
    drawPieces()

def analysis():
    print "Analysis"
    bestMove = alphabeta(1)
    capPiece = board[convertSquaretoPos(bestMove[1])]
    isCapture = False
    if capPiece != '0': isCapture = True
    makeTempMove(bestMove)
    moveScore = evalBoard()
    piece = board[convertSquaretoPos(bestMove[1])]
    bestMoveNot = convertMovetoNot(piece,isCapture,bestMove[0],bestMove[1])
    takebackTempMove(bestMove)
    print "best move", bestMove, bestMoveNot

def pracOneRookMate():
    initPracGame("One Rook Mate")

def pracOneQueenMate():
    initPracGame("One Queen Mate")

def pracQueenRookMate():
    initPracGame("Queen and Rook Mate")

def pracTwoBishopsMate():
    initPracGame("Two Bishops Mate")

def pracBishopKnightMate():
    initPracGame("Bishop and Knight Mate")

def setevalnomob():
    global evalMobilityCheck
    evalMobilityCheck = False
    tkMessageBox.showinfo("Game over", "Eval mobility check disabled.")


def setevalmob():
    global evalMobilityCheck
    evalMobilityCheck = True
    tkMessageBox.showinfo("Game over", "Eval mobility check enabled.")

def promdlg():
    global tkRoot
    global promDlg
    global app

    promDlg = PromoteDialog(app)
    d = promDlg
    #x = mouse.x
    #y = mouse.y
    x = 500
    y = 200
    w = 260
    h = 70
    geostring = "%dx%d+%d+%d" % (w, h, x, y)
    d.top.geometry(geostring)
    promTkRoot = tkRoot.wait_window(d.top)
    #promTkRoot.wait_window(d.top)

def resign():
    global game, player
    global movesText
    updatemovesText()
    outString = ""
    halfMoveNum = 0
    fullMoveNum = 1
    #print game['ended']
    if game['ended'] == False:
        if game['tomove'] == "White": outString += "\nWhite resigns."
        if game['tomove'] == "Black": outString += "\nBlack resigns."
        movesText.insert(INSERT, outString)
        movesText.see(Tkinter.END)
        game['tomove'] = None
        game['ended'] = True
    #movesText.delete(1.0, Tkinter.END)
    #drawCover()

def newgamedlg():
    global AIOption
    global tkRoot
    d = NewGameDialog(tkRoot)
    x = 300
    y = 300
    w = 180
    h = 150
    AIOption = StringVar()
    geostring = "%dx%d+%d+%d" % (w, h, x, y)
    d.top.geometry(geostring)
    #d.top.w.grid(row=1,column=1)
   # d.top.w.pack()
    tkRoot.wait_window(d.top)

def newgamehva():
    initNewGame("Human", "AI")
    drawBoard()
    drawPieces()


def newgamehvh():
    initNewGame("Human", "Human")
    drawBoard()
    drawPieces()


def newgameava():
    initNewGame("AI", "AI")
    drawBoard()
    drawPieces()


def setAI0():
    global AILevel
    AILevel = 0


def setAI1():
    global AILevel
    AILevel = 1


def setAI2():
    global AILevel
    AILevel = 2


def gameexit():
    tkRoot.destroy()
    sys.exit()


# conversion functions


def convertMovetoNot(pieceMoved, isCapture, startSquare, endSquare):
    # make proper notation for output
    # To Add: detect when two pieces of same type can move to/capture on same square (e.g. Rexf5)

    global board
    global game
    global legalMoves
    global promPiece

    toMove = game['tomove']

    startSquareIndex = startSquare[1] * 8 + startSquare[0]  #start square board[] position
    endSquareIndex = endSquare[1] * 8 + endSquare[0]  #end square board[] position
    notStartSquare = convertPostoNot(startSquareIndex)
    notEndSquare = convertPostoNot(endSquareIndex)
    notCapture = ''
    outputCapture = ' moves to '
    outputCheck = ''
    promString = ''
    if isCapture:
        outputCapture = ' captures on '
        notCapture = 'x'
    notSign = ''
    notPiece = pieceMoved.upper()
    if notPiece == 'P':
        notPiece = ''
        if notCapture: notPiece = notStartSquare[0]
        if endSquare[1] == 0 or endSquare[1] == 7: promString = '=' + promPiece

    # ambiguity check
    numAmbigs = 0
    notAmbig = ''
    ambigFile = False
    ambigRank = False
    ambigMoves = []
    for lMove in legalMoves:
        lPiece = board[convertSquaretoPos(lMove[0])]
        #print lMove, lPiece
        if lMove[1] == endSquare and lPiece == pieceMoved and lMove != (startSquare, endSquare): # chosen move and this move both move to same square and are same piece, ambiguity
            numAmbigs+=1
            #print lMove, (startSquare, endSquare), lPiece, pieceMoved
            if lMove[0][0] != startSquare[0]: #files are different
                notAmbig = convertPostoNot(startSquareIndex)[0] # set notAmbig to the file
                ambigFile = True
            if lMove[0][0] == startSquare[0]: # files are same
                notAmbig = convertPostoNot(startSquareIndex)[1] # set notAmbig to the rank
                ambigRank = True
            ambigMoves.append(lMove)
    #if numAmbigs > 2: notAmbig = convertPostoNot(startSquareIndex)
    '''
    numAmbigs = 0
    for ambigMove in ambigMoves:
        ambigPiece = board[convertSquaretoPos(ambigMove[0])]
        ambigMoveSQIndex = ambigMove[0][1] * 8 + ambigMove[0][0]
        ambigMoveEQIndex = ambigMove[1][1] * 8 + ambigMove[1][0]
        if (ambigMove[1] == endSquare and ambigPiece == pieceMoved and (notAmbig == convertPostoNot(ambigMoveEQIndex)[0]) or notAmbig == convertPostoNot(ambigMoveEQIndex)[1]):
            numAmbigs+=1
    '''
    if (ambigRank and ambigFile): notAmbig = convertPostoNot(startSquareIndex)
    game['check'] = False
    inCheck = isInCheck(board, kingPos[toMove], toMove)
   # print inCheck, kingPos[toMove], toMove
    origLegalMoves = list(legalMoves)
    genLegalMoves()
    if inCheck:
        game['check'] = True
        outputCheck = '[check]'
        notSign += '+'
        if len(legalMoves) == 0: notSign = '#'
    #output move
    #print promString
    outstring = notPiece + notAmbig + notCapture + notEndSquare + promString + notSign
    if (pieceMoved.upper() == 'K'):
        #print (startSquare,endSquare)
        if ((startSquare,endSquare) == ((4,7),(2,7))): outstring = "0-0-0"
        if ((startSquare,endSquare) == ((4,0),(2,0))): outstring = "0-0-0"
        if ((startSquare,endSquare) == ((4,7),(6,7))): outstring = "0-0"
        if ((startSquare,endSquare) == ((4,0),(6,0))): outstring = "0-0"
    legalMoves = list(origLegalMoves)
    return outstring
    #origToMove + " " + pieceMoved.upper() + " on " + notStartSquare + outputCapture + notEndSquare + " " + outputCheck


def convertXYtoBoardIndex(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts cursor X, Y position to board array X, Y position
    returnX = int(x / squareSize)
    returnY = int(y / squareSize)
    if flipped:
        returnX = int((canvasSize - x) / squareSize)
        returnY = int((canvasSize - y) / squareSize)
    return (returnX, returnY)


def convertBoardIndextoXY(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts board index X, Y to tile draw position X, Y
    returnX = x * squareSize
    returnY = y * squareSize
    if flipped:
        returnX = int((7 - x) * squareSize)
        returnY = int((7 - y) * squareSize)
    return (returnX, returnY)


def convertPostoNot(pos):
    # Converts a board array position to board square (e.g. 1 = a8)
    # TODO: Make more readable

    posFile = (pos % 8)  # every 8th byte is a new row
    posRank = int(round(((63 - pos) / 8),
                        0))  # each column is the nth byte in a row # use (63 - pos) to orient board as a8 = top left
    squareFile = chr((97 + posFile))
    squareRank = str((1 + posRank))
    return squareFile + squareRank


def convertSquaretoPos(square):
    # Converts a board square (e.g. (0,0)) to the board array position (e.g. 0)
    posIndex = square[0] + 8 * square[1]
    return posIndex


def genLegalMoves():
    # Generate list of legal moves for side to move
    global board
    global legalMoves
    global game
    global allowCastlingQS, allowCastlingKS
    global legalMovesCastling

    legalMoves = []
    legalMovesCastling = []
    a = 0
    for i in board:
        # i  is board[] value: (eg 'p', 'w', '0')
        if ( (i != '0') and  # not an empty square
                 (pieceCol[i] == game['tomove']) ):  # is side to move
            #pieces on board (e.g. p, k, P, R, K)
            p = int(a)
            tileYindex = int(a / 8)
            tileXindex = a - int(tileYindex * 8)
            genPieceLegalMove(i, (tileXindex, tileYindex))
            #debug: print "%s %s on: (%d, %d)" % (game['tomove'], i, tileXindex, tileYindex)
            #debug: print i
        # increase counter a (board[a])
        a += 1

    # generate castling moves
    canCastleQS = allowCastlingQS[game['tomove']]
    canCastleKS = allowCastlingKS[game['tomove']]

    # check if player is in check
    kPos = kingPos[game['tomove']]

    if (isInCheck(board, kPos, game['tomove'])):
        canCastleQS = False
        canCastleKS = False

    # check inbetween squares for occupied
    if game['tomove'] == 'Black':
        if canCastleQS == True:
            if board[convertSquaretoPos((1, 0))] != '0': canCastleQS = False  # QS N square
            if board[convertSquaretoPos((2, 0))] != '0': canCastleQS = False  # QS B square
            if board[convertSquaretoPos((3, 0))] != '0': canCastleQS = False  # QS Q square
        if canCastleKS == True:
            if board[convertSquaretoPos((6, 0))] != '0': canCastleKS = False  # QS N square
            if board[convertSquaretoPos((5, 0))] != '0': canCastleKS = False  # QS B square
    if game['tomove'] == 'White':
        if canCastleQS == True:
            if board[convertSquaretoPos((1, 7))] != '0': canCastleQS = False  # QS N square
            if board[convertSquaretoPos((2, 7))] != '0': canCastleQS = False  # QS B square
            if board[convertSquaretoPos((3, 7))] != '0': canCastleQS = False  # QS Q square
        if canCastleKS == True:
            if board[convertSquaretoPos((6, 7))] != '0': canCastleKS = False  # QS N square
            if board[convertSquaretoPos((5, 7))] != '0': canCastleKS = False  # QS B square

    # check inbetween squares for check, for castling
    if game['tomove'] == 'Black':
        if canCastleQS == True:  # king and QS rook haven't moved
            #if isInCheck(board, (1,0), 'Black') == True: canCastleQS = False # QS N square
            if isInCheck(board, (2, 0), 'Black') == True: canCastleQS = False  # QS B square
            if isInCheck(board, (3, 0), 'Black') == True: canCastleQS = False  # QS Q square
        if canCastleKS == True:  # king and KS rook haven't moved
            if isInCheck(board, (6, 0), 'Black') == True: canCastleKS = False  # KS N square
            if isInCheck(board, (5, 0), 'Black') == True: canCastleKS = False  # KS B square
    if game['tomove'] == 'White':
        if canCastleQS == True:  # king and QS rook haven't moved
            #if isInCheck(board, (1,7), 'White') == True: canCastleQS = False # QS N square
            if isInCheck(board, (2, 7), 'White') == True: canCastleQS = False  # QS B square
            if isInCheck(board, (3, 7), 'White') == True: canCastleQS = False  # QS Q square
        if canCastleKS == True:  # king and KS rook haven't moved
            if isInCheck(board, (6, 7), 'White') == True: canCastleKS = False  # KS N square
            if isInCheck(board, (5, 7), 'White') == True: canCastleKS = False  # KS B square
    if canCastleQS == True: legalMovesCastling += [( kPos, ((kPos[0] - 2), kPos[1]) )]
    if canCastleKS == True: legalMovesCastling += [( kPos, ((kPos[0] + 2), kPos[1]) )]
    #toMove = game['tomove']
    #game['check'] = isInCheck(board, kingPos[toMove], toMove)

def checkGameOver():

    global board
    global game
    global legalMoves
    global boardHistory, boardHistoryPos

    # draw by stalemate
    if len(legalMoves) == 0:  # no legal moves available
       # print game['check']
        game['ended'] = True
        if game['check']:
            outstring = game['nottomove'] + " wins by checkmate."
            tkMessageBox.showinfo("Game over", outstring)
        if game['check'] == False:
            tkMessageBox.showinfo("Game over", "Game drawn by stalemate.")
            # print "Game over: Game drawn by stalemate."
        return

    #draw by insufficient material
    piecesLeft = []
    for piece in board:
        if piece != '0':
            piecesLeft += piece
            piecesLeft.sort()
    if (
                                (piecesLeft == ['K', 'k']) or
                                (piecesLeft == ['K', 'b', 'k']) or
                            (piecesLeft == ['B', 'K', 'k']) or
                        (piecesLeft == ['K', 'N', 'k']) or
                    (piecesLeft == ['K', 'k', 'n']) or
                (piecesLeft == ['B', 'K', 'b', 'k']) or
            (piecesLeft == ['K', 'N', 'k', 'n'])
    ):
        outstring = "Draw by insufficient material."
        tkMessageBox.showinfo("Game over", outstring)
        game['ended'] = True

    #draw by three-fold repetition
    curPos = boardHistoryPos
    numReps = 0
    while curPos >= 0:
        boardState = list(boardHistory[curPos])
        #print boardState[0], board[0]
        if (list(boardState) == list(board)): numReps+=1
        if numReps >= 3: #numReps == 2 (repeated twice) means that current position has occured for third time
            game['ended'] = True
            outstring = "Draw by three-fold repetition."
            tkMessageBox.showinfo("Game over", outstring)
            return
        curPos -= 2

    #draw by 50-move rule
    if game['50-move-count'] >= 100:
        game['ended'] = True
        outstring = "Draw by 50-move rule."
        tkMessageBox.showinfo("Game over", outstring)
        return





def genPieceLegalMove(piece, pos):
    # Find legal moves for a given piece.

    # piece = piece type (eg 'r', 'k', P')
    #pos = piece position (eg (0,0), (2,4), (4,6), (7,7))
    global legalMoves
    global game

    color = game['tomove']
    piece = piece.upper()
    pieceFile = pos[0]
    pieceRank = pos[1]
    toPosIndex = 0
    toPosPiece = '0'
    toAdd = []
    pieceIndex = convertSquaretoPos((pieceFile, pieceRank))
    if piece == 'P':
        #find moves for pawn
        pawnDir = -1  # for white (-1 goes up the board array)
        if color == 'Black': pawnDir = 1  # for black (+1 goes down the board array)

        # Check for one move forward
        toPosIsOpen = True
        toPosInRange = True
        pawnOneForwardOpen = True  #used for checking the two forward special move
        toPos = (pos[0], (pos[1] + pawnDir * 1))
        if (toPos[0] < 0 or toPos[0] > 7 or
                    toPos[1] < 0 or toPos[1] > 7): toPosInRange = False
        if toPosInRange:
            toPosIndex = convertSquaretoPos(toPos)
            toPosPiece = board[toPosIndex]
        #print toPosInRange
        if toPosPiece != '0':
            # one square forward is blocked by pawn/piece
            toPosIsOpen = False
            pawnOneForwardOpen = False
        if ((toPosIsOpen) and (toPosInRange)):
            toAdd += [(pos, toPos)]  # pawn can move 1 forward

        # Check for special move pawn 2 forward
        toPosIsOpen = True
        toPosInRange = True  # no range check, will always be in board range (2 forward from starting pos)
        toPos = (pos[0], (pos[1] + pawnDir * 2))
        if ((color == 'White') and (pieceRank == 6) or
                    (color == 'Black') and (pieceRank == 1)):  # On starting position (allow 2 moves forward)
            toPosIndex = convertSquaretoPos(toPos)
            toPosPiece = board[toPosIndex]
            if toPosPiece != '0':
                # 2 squares forward is blocked by a piece/pawn
                toPosIsOpen = False
            if ((toPosIsOpen) and (pawnOneForwardOpen)):
                toAdd += [(pos, toPos)]  # pawn can move 1 forward


        #check for capture up/left
        toPosCanCapture = True
        toPosIsOpen = True
        toPosInRange = True
        toPos = (pos[0] + pawnDir * 1, (pos[1] + pawnDir * 1))
        if (toPos[0] < 0 or toPos[0] > 7 or
                    toPos[1] < 0 or toPos[1] > 7): toPosInRange = False
        if toPosInRange:
            toPosIndex = convertSquaretoPos(toPos)
            toPosPiece = board[toPosIndex]
            if toPosPiece == '0':
                toPosCanCapture = False
            if pieceCol[toPosPiece] == color:  #blocked by same color piece
                toPosCanCapture = False
            if (toPosCanCapture):
                toAdd += [(pos, toPos)]  # can capture forward and left

        #check for capture up/right
        toPosCanCapture = True
        toPosInRange = True
        toPos = (pos[0] - pawnDir * 1, (pos[1] + pawnDir * 1))
        if (toPos[0] < 0 or toPos[0] > 7 or
                    toPos[1] < 0 or toPos[1] > 7): toPosInRange = False
        if toPosInRange:
            toPosIndex = convertSquaretoPos(toPos)
            toPosPiece = board[toPosIndex]
            if toPosPiece == '0':
                toPosCanCapture = False
            if pieceCol[toPosPiece] == color:  #blocked by same color piece
                toPosCanCapture = False
            if (toPosCanCapture):
                toAdd += [(pos, toPos)]  # can capture forward and right
                #check for en-passant
                #check for promotion

    if piece == 'N' or piece == 'K':
        # knights and kings can only move to their moveSet elements
        moveDirs = moveSet[piece]
        for moveDir in moveDirs:
            toPosInRange = True
            posX = pos[0]
            posY = pos[1]
            moveXDir = moveDir[0]
            moveYDir = moveDir[1]
            posX = posX + moveXDir
            posY = posY + moveYDir
            toPos = (posX, posY)
            if (toPos[0] < 0 or toPos[0] > 7 or
                        toPos[1] < 0 or toPos[1] > 7):
                toPosInRange = False  # Out of board range
            toPosIndex = convertSquaretoPos(toPos)
            if toPosInRange:
                toPosPiece = board[toPosIndex]
                if toPosPiece == '0':  #empty square
                    toAdd += [(pos, toPos)]
                elif toPosPiece != '0':  #square is occupied
                    if (pieceCol[toPosPiece] != game['tomove']):  #piece is opponent's - capture move
                        toAdd += [(pos, toPos)]

    if ((piece == 'B') or (piece == 'Q') or (piece == 'R')):
        # bishops, queens and rooks can move infinitely along their moveSet element directions
        moveDirs = moveSet[piece]
        for moveDir in moveDirs:
            posX = pos[0]
            posY = pos[1]
            moveXDir = moveDir[0]
            moveYDir = moveDir[1]
            while True:  # Loop until break
                posX = posX + moveXDir
                posY = posY + moveYDir
                toPos = (posX, posY)
                if (toPos[0] < 0 or toPos[0] > 7 or
                            toPos[1] < 0 or toPos[1] > 7):
                    break  # Out of board range
                toPosIndex = convertSquaretoPos(toPos)
                toPosPiece = board[toPosIndex]
                if toPosPiece == '0':  #empty square
                    toAdd += [(pos, toPos)]
                elif toPosPiece != '0':  #square is occupied
                    if (pieceCol[toPosPiece] != game['tomove']):  #piece is opponent's - capture move
                        toAdd += [(pos, toPos)]
                        break  # break on capture square
                    elif (pieceCol[toPosPiece] == game['tomove']):  #piece belongs to side to move
                        break  # move direction is blocked by own piece

    for move in toAdd:
        addLegalMove(move)


def addLegalMove((pos, toPos)):
    # Adds a move (from square, to square) to the legalMoves list

    global legalMoves
    global board
    # print "adding legal move", pos, toPos
    exposesCheck = False
    makeTempMove((pos, toPos))
    tomove = game['tomove']
    if (isInCheck(board, kingPos[tomove], tomove)):
        exposesCheck = True
    takebackTempMove((pos, toPos))
    if exposesCheck == False:
        legalMoves += [(pos, toPos)]


def isInCheck(inBoard, pos, col):
    # pos is position of king to find check for
    # or position of square to check if attacked by opponent (checking if king can move there)
    # define col and Oppcol to check for
    if (pos[0] < 0 or pos[0] > 7 or
                pos[1] < 0 or pos[1] > 7):  #check is out of range
        return False
    boardIndex = convertSquaretoPos(pos)
    piece = inBoard[boardIndex]
    if piece == 'K':
        col = 'White'
        oppCol = 'Black'
    elif piece == 'k':
        col = 'Black'
        oppCol = 'White'
    if col == 'White':
        oppCol = 'Black'
    elif col == 'Black':
        oppCol = 'White'
    #check for checks with pawns
    pawnDir = 1  # for white (1 goes down the board array - see attacks coming from down direction [white attack])
    if oppCol == 'Black': pawnDir = -1  # for black (-1 goes up the board array [black attack])

    #check for attack from pawn diagonal left
    fromPos = ((pos[0] - 1), (pos[1] + 1 * pawnDir))
    fromPosInRange = True
    fromPosIndex = convertSquaretoPos(fromPos)
    if (fromPos[0] < 0 or fromPos[0] > 7 or
                fromPos[1] < 0 or fromPos[1] > 7):
        fromPosInRange = False  # Out of board range
    if fromPosInRange:
        fromPosPiece = inBoard[fromPosIndex]
        if pieceCol[fromPosPiece] == oppCol and fromPosPiece.upper() == 'P':
            #piece is opponent's colour and right piece type
            #in check by pawn diagonal and left
            return True

    #check for attack from pawn diagonal right
    fromPos = ((pos[0] + 1), (pos[1] + 1 * pawnDir))
    fromPosInRange = True
    fromPosIndex = convertSquaretoPos(fromPos)
    if (fromPos[0] < 0 or fromPos[0] > 7 or
                fromPos[1] < 0 or fromPos[1] > 7):
        fromPosInRange = False  # Out of board range
    if fromPosInRange:
        fromPosPiece = inBoard[fromPosIndex]
        if pieceCol[fromPosPiece] == oppCol and fromPosPiece.upper() == 'P':
            #piece is opponent's colour and right piece type
            #in check by pawn diagonal and right
            return True


    #check for checks with kings and knights
    #same kind of check: check if piece is directly attacking
    moveSetList = ['K', 'N']
    for piece in moveSetList:
        moveDirs = moveSet[piece]
        for moveDir in moveDirs:
            #fromPos: square from which the attack originates
            fromPosInRange = True
            posX = pos[0]
            posY = pos[1]
            moveX = moveDir[0]
            moveY = moveDir[1]
            posX = posX + moveX
            posY = posY + moveY
            fromPos = (posX, posY)
            fromPosIndex = convertSquaretoPos(fromPos)
            if (fromPos[0] < 0 or fromPos[0] > 7 or
                        fromPos[1] < 0 or fromPos[1] > 7):
                fromPosInRange = False  # Out of board range
            if fromPosInRange:
                fromPosPiece = inBoard[fromPosIndex]
                if pieceCol[fromPosPiece] == oppCol and fromPosPiece.upper() == piece:
                    #piece is opponent's colour and right piece type
                    return True

    #print "didnt get here"

    moveSetList = ['Q', 'B', 'R']
    for piece in moveSetList:
        moveDirs = moveSet[piece]
        for moveDir in moveDirs:
            #check each square leading from king outwards in moveDir direction
            posX = pos[0]
            posY = pos[1]
            moveX = moveDir[0]
            moveY = moveDir[1]
            while True:  # loop until break
                posX = posX + moveX
                posY = posY + moveY
                fromPos = (posX, posY)
                if (fromPos[0] < 0 or fromPos[0] > 7 or
                            fromPos[1] < 0 or fromPos[1] > 7):
                    break  # moved out of range of board
                fromPosIndex = convertSquaretoPos(fromPos)
                fromPosPiece = inBoard[fromPosIndex]
                if fromPosPiece != '0':  # piece occupies square
                    if fromPosPiece.upper() == piece and pieceCol[fromPosPiece] == oppCol:  #piece attacking king is right piece type and belongs to opponent
                        #print "check is from", fromPosPiece, "at", fromPos
                        #print "to move:", game['tomove']
                        return True
                    else:
                        break
                    break  # end of check line

    return False


def makeTempMove((startSquare, endSquare)):
    # makes a temporary move to the board
    #use takebackTempMove() to take back
    global board
    global lastPieceMoved, lastPieceCaptured
    global kingPos

    #time.sleep(3)
    move = (startSquare, endSquare)
    startSquareIndex = startSquare[1] * 8 + startSquare[0]  #start square board[] position
    endSquareIndex = endSquare[1] * 8 + endSquare[0]  #end square board[] position

    #print len(board), endSquareIndex,  "!!!!!!!"
    pieceCaptured = board[endSquareIndex]
    pieceMoved = board[startSquareIndex]


    #makes move by updating board[]
    board[endSquareIndex] = pieceMoved
    board[startSquareIndex] = '0'

    if game['tomove'] == 'Black': pawnDir = +1
    if game['tomove'] == 'White': pawnDir = -1

    # check if move is en passant
    if (move in legalMovesEP):
        # move is en passant
        # remove captured pawn
        squareX = endSquare[0]
        squareY = endSquare[1] - pawnDir
        squareIndex = convertSquaretoPos((squareX, squareY))
        board[squareIndex] = '0'

    # check if move is castling
    #print "in maketempMove", move, legalMovesCastling
    if (move in legalMovesCastling):
        # move is castling
        # move rook to other side of king
        if (endSquare == (6, 0)):  # black KS castle
            board[convertSquaretoPos((7, 0))] = '0'  # remove black KS rook
            board[convertSquaretoPos((5, 0))] = 'r'  # move black KS rook to other side of king
        if (endSquare == (2, 0)):  # black QS castle
            board[convertSquaretoPos((0, 0))] = '0'  # remove black QS rook
            board[convertSquaretoPos((3, 0))] = 'r'  # move black QS rook to other side of king

        if (endSquare == (6, 7)):  # white KS castle
            board[convertSquaretoPos((7, 7))] = '0'  # remove white KS rook
            board[convertSquaretoPos((5, 7))] = 'R'  # move white KS rook to other side of king
        if (endSquare == (2, 7)):  # white QS castle
            board[convertSquaretoPos((0, 7))] = '0'  # remove white QS rook
            board[convertSquaretoPos((3, 7))] = 'R'  # move white QS rook to other side of king


    #update kingPos{} king position after king move
    if pieceMoved == 'k':
        kingPos['Black'] = endSquare
    if pieceMoved == 'K':
        kingPos['White'] = endSquare

    lastPieceMoved = pieceMoved
    lastPieceCaptured = pieceCaptured


def takebackTempMove((startSquare, endSquare)):
    global board
    global lastEndSquarePiece
    global kingPos

    move = (startSquare, endSquare)
    startSquareIndex = startSquare[1] * 8 + startSquare[0]  # start square board[] position
    endSquareIndex = endSquare[1] * 8 + endSquare[0]  # end square board[] position
    pieceMoved = board[endSquareIndex]

    if game['tomove'] == 'Black': pawnDir = +1
    if game['tomove'] == 'White': pawnDir = -1

    toMove = game['tomove']
    # update kingPos{} king position after king move
    if pieceMoved == 'k':
        kingPos['Black'] = startSquare
    if pieceMoved == 'K':
        kingPos['White'] = startSquare

    # check if move is en passant
    if (move in legalMovesEP):
        # move is en passant
        # remove captured pawn
        squareX = endSquare[0]
        squareY = endSquare[1] - pawnDir
        squareIndex = convertSquaretoPos((squareX, squareY))
        board[squareIndex] = 'P'

    # check if move is castling
    if (move in legalMovesCastling):
        # move is castling
        # move rook to other side of king
        if (endSquare == (6, 0)):  # black KS castle
            board[convertSquaretoPos((7, 0))] = 'r'  # remove black KS rook
            board[convertSquaretoPos((5, 0))] = '0'  # move black KS rook to other side of king
        if (endSquare == (2, 0)):  # black QS castle
            board[convertSquaretoPos((0, 0))] = 'r'  # remove black QS rook
            board[convertSquaretoPos((3, 0))] = '0'  # move black QS rook to other side of king

        if (endSquare == (6, 7)):  # white KS castle
            board[convertSquaretoPos((7, 7))] = 'R'  # remove white KS rook
            board[convertSquaretoPos((5, 7))] = '0'  # move white KS rook to other side of king
        if (endSquare == (2, 7)):  # white QS castle
            board[convertSquaretoPos((0, 7))] = 'R'  # remove white QS rook
            board[convertSquaretoPos((3, 7))] = '0'  # move white QS rook to other side of king


    #makes move by updating board[]
    board[endSquareIndex] = lastPieceCaptured
    board[startSquareIndex] = lastPieceMoved


def updatemovesText():
    global movesText
    global movesList
    global moveList
    global boardHistoryPos

    outString = ""
    halfMoveNum = 0
    fullMoveNum = 1
    outPos = 0
    for move in moveList:
        halfMoveNum += 1
        if ((halfMoveNum % 2) == 1): outString += str(fullMoveNum) + ". "
        if halfMoveNum == boardHistoryPos:
            outString += "[" + move + "] "
            outPos = len(outString)
        if halfMoveNum != boardHistoryPos: outString += move + " "
        if ((halfMoveNum % 2) == 0):
            fullMoveNum += 1
            outString += "\n"

    #print outString
    movesText.delete(1.0, Tkinter.END)
    movesText.insert(INSERT, outString)
    movesText.see(Tkinter.END)
    #movesText.see(Tkinter.END)


def makeMove((startSquare, endSquare)):
    global moveList
    global board
    global game
    global kingPos
    global legalMovesEP
    global legalMovesCastling
    global allowCastlingKS, allowCastlingQS
    global moveNum
    global movesText
    global movesTextScr
    global promPiece
    global tkRoot
    global knightVal, rookVal, gameStage, pawnCount
    global boardHistoryPos
    global promPiece

    if game['ended'] == True:
        return
    if game['tomove'] == 'Black': moveNum += 1

    # set pawnDir -- used for en passant checks
    if game['tomove'] == 'Black': pawnDir = +1
    if game['tomove'] == 'White': pawnDir = -1
    kPos = kingPos[game['tomove']]

    move = (startSquare, endSquare)
    startSquareIndex = startSquare[1] * 8 + startSquare[0]  # start square board[] position
    endSquareIndex = endSquare[1] * 8 + endSquare[0]  # end square board[] position
    endSquarePiece = board[endSquareIndex]
    pieceMoved = board[startSquareIndex]

    # makes move by updating board[]
    board[endSquareIndex] = pieceMoved
    board[startSquareIndex] = '0'
    isCapture = False
    if (endSquarePiece != '0'): isCapture = True

    # check if move is en passant
    if (move in legalMovesEP):
        # move is en passant
        # remove captured pawn
        squareX = endSquare[0]
        squareY = endSquare[1] - pawnDir
        squareIndex = convertSquaretoPos((squareX, squareY))
        board[squareIndex] = '0'

    # check if move is castling
    #print "in makeMove", move, legalMovesCastling
    if (move in legalMovesCastling):
        # move is castling
        # move rook to other side of king
        if (endSquare == (6, 0)):  # black KS castle
            board[convertSquaretoPos((7, 0))] = '0'  # remove black KS rook
            board[convertSquaretoPos((5, 0))] = 'r'  # move black KS rook to other side of king
        if (endSquare == (2, 0)):  # black QS castle
            board[convertSquaretoPos((0, 0))] = '0'  # remove black QS rook
            board[convertSquaretoPos((3, 0))] = 'r'  # move black QS rook to other side of king

        if (endSquare == (6, 7)):  # white KS castle
            board[convertSquaretoPos((7, 7))] = '0'  # remove white KS rook
            board[convertSquaretoPos((5, 7))] = 'R'  # move white KS rook to other side of king
        if (endSquare == (2, 7)):  # white QS castle
            board[convertSquaretoPos((0, 7))] = '0'  # remove white QS rook
            board[convertSquaretoPos((3, 7))] = 'R'  # move white QS rook to other side of king

    # promotion

    if pieceMoved == 'P' and endSquare[1] == 0:  # white pawn promotes
        promPiece = 'Q'
        if player[game['tomove']] == 'Human':
            #print "white promotes"
            promdlg()
        board[endSquareIndex] = promPiece
        #board[endSquareIndex] = 'Q'  # give white queen
    if pieceMoved == 'p' and endSquare[1] == 7:  #black pawn promotes
        promPiece = 'q'
        if player[game['tomove']] == 'Human':
            #print "black promotes"
            promdlg()
        board[endSquareIndex] = promPiece.lower()
        #board[endSquareIndex] = 'q'  # give black queen

    # en passant

    legalMovesEP = []

    if (pieceMoved.upper() == 'P' and abs((endSquare[1] - startSquare[1])) == 2):
        # checks if pawn moved 2 spaces forward
        # for en-passant

        #if a piece is to the right of the endsquare
        outOfRange = False
        rightX = endSquare[0] + 1
        leftX = endSquare[0] - 1

        if pieceMoved == 'P':
            oppPawn = 'p'
            pawnDir = -1
        if pieceMoved == 'p':
            oppPawn = 'P'
            pawnDir = +1

        if rightX < 0 or rightX > 7: outOfRange = True
        if leftX < 0 or leftX > 7: outOfRange = True
        epSquare = (startSquare[0], (startSquare[1] + pawnDir))
        if outOfRange == False:
            checkIndex = convertSquaretoPos((leftX, endSquare[1]))
            if board[checkIndex] == oppPawn:  #opposing pawn is directly to left of pawn
                # en passant is available from the left
                legalMovesEP += [( (leftX, endSquare[1]), epSquare)]
            checkIndex = convertSquaretoPos((rightX, endSquare[1]))
            if board[checkIndex] == oppPawn:  #opposing pawn is directly to right of pawn
                # en passant is available from the right
                legalMovesEP += [( (rightX, endSquare[1]), epSquare)]
        pass

    # castling
    legalMovesCastling = []

    if pieceMoved == 'r':
        if startSquare == (0, 0):  # black QS rook moved
            allowCastlingQS['Black'] = False
        if startSquare == (7, 0):  # black KS rook moved
            allowCastlingKS['Black'] = False
    if pieceMoved == 'R':
        if startSquare == (0, 7):  # white QS rook moved
            allowCastlingQS['White'] = False
        if startSquare == (7, 7):  # white KS rook moved
            allowCastlingKS['White'] = False

    if pieceMoved == 'k':  # black king moved
        allowCastlingKS['Black'] = False
        allowCastlingQS['Black'] = False
    if pieceMoved == 'K':  # white king moved
        allowCastlingKS['White'] = False
        allowCastlingQS['White'] = False

    #update kingPos{} king position after king move
    if pieceMoved == 'k':
        kingPos['Black'] = endSquare
    if pieceMoved == 'K':
        kingPos['White'] = endSquare

    if player[game['tomove']] == "Human":
        drawBoard()
        drawPieces()
        tkRoot.update()

    newNotToMove = game['tomove']
    # Set side to move (alternate white/black)
    newToMove = game['tomove']

    boardHistory.append(list(board))
    boardHistoryPos = (len(boardHistory) - 1)

    #toMove = game['tomove']
    #game['check'] = isInCheck(board, kingPos[newNotToMove], newNotToMove)
    moveList.append(convertMovetoNot(pieceMoved, isCapture, startSquare, endSquare))
    updatemovesText()
    tkRoot.update()
    queenCount = board.count('Q') + board.count('q')
    gameStage = 'Midgame'
    if ((allowCastlingQS["White"] or allowCastlingKS["White"]) or (allowCastlingQS["Black"] or allowCastlingKS["Black"])):
        # someone can still castle
        gameStage = 'Opening'
    if queenCount == 0: gameStage = 'Endgame'
    pawnCount = board.count('p') + board.count('P')
    knightVal = pieceVal['N'] - ((16 - pawnCount) * .025) # N loses 0.05 for each missing pawn
    rookVal = pieceVal['R'] + ((16 - pawnCount) * .025)
    #time.sleep(10)

    updatemovesText()

    drawBoard()
    drawPieces()
    tkRoot.update()

    #gen legal moves, set side to move, redraw board
    game['50-move-count'] += 1
    if (isCapture) or (pieceMoved.upper() == 'P'):
        game['50-move-count'] = 0
    tkRoot.update()
    toMove = newToMove
    notToMove = newNotToMove
    origToMove = toMove
    if toMove == 'White':
        game['tomove'] = 'Black'
    elif toMove == 'Black':
        game['tomove'] = 'White'
    toMove = game['tomove']
    if toMove == 'White': game['nottomove'] = 'Black'
    if toMove == 'Black': game['nottomove'] = 'White'
    genLegalMoves()
    game['check'] = isInCheck(board, kingPos[toMove], toMove)
    if game['ended'] == False: checkGameOver()


def canvasClick(event):
    global clickDragging
    global ClickStartScrPos
    global clickStartPiece
    global clickStartBoardIndex
    global lastTileXIndex, lastTileYIndex
    global clickStartSquare
    global board
    global game
    global flipped
    global boardHistory, boardHistoryPos
    global canvasSize
    global player

    squareSize = canvasSize / 8

    if boardHistoryPos != (len(boardHistory) - 1): return

    if game['ended'] == False and (player[game['tomove']] == 'Human'):
        # User Clicks Down within board square
        mouseX = event.x
        mouseY = event.y
        # convert mouseX, mouseY to board array indices
        (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
        #convert board indices to screen X Y position of tiles
        (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)
        #calculate boardIndex = board[] square index
        boardIndex = tileYIndex * 8 + tileXIndex
        piece = board[boardIndex]
        if (piece == '0'):  #user tries to drag empty square
            return
        if (pieceCol[piece] != game['tomove']):
            return
        #draw green square over tile
        #boardCanvas.draw.rect(pygScreen, (0,255,0), (tileScrX + 2, tileScrY + 2, 57, 57), 4)
        boardCanvas.create_rectangle(tileScrX +3, tileScrY +3, (tileScrX + squareSize - 2), (tileScrY + squareSize - 2), outline="#00FF00",
                                     width=6)
        clickDragging = True
        clickStartScrPos = (tileScrX, tileScrY)  # store top left screen X, Y for tile position
        clickStartBoardIndex = (tileXIndex, tileYIndex)
        clickStartPiece = piece
        lastTileXIndex = tileXIndex
        lastTileYIndex = tileYIndex
        clickStartSquare = clickStartBoardIndex
    if game['ended'] == True:
        newgamedlg()

def canvasMotion(event):
    global lastTileScrX
    global lastTileScrY
    global lastTileXIndex
    global lastTileYIndex
    global canvasSize
    global clickStartBoardIndex

    if not clickDragging: return
    squareSize = canvasSize / 8
    mouseX = event.x
    mouseY = event.y
    # convert mouseX, mouseY to board array indices
    (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
    #convert board indices to screen X Y position of tiles
    (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)

    #clickStartBoardIndex = (tileXIndex, tileYIndex)
    #calculate boardIndex = board[] square index
    boardIndex = tileYIndex * 8 + tileXIndex
    move = (clickStartBoardIndex, (tileXIndex, tileYIndex))
    if clickDragging:
        if (move in legalMoves) or (move in legalMovesEP) or (move in legalMovesCastling):
            #draw green square over moused over square
            boardCanvas.create_rectangle(tileScrX +3, tileScrY +3, (tileScrX + (squareSize - 2)), (tileScrY + (squareSize - 2)),
                                         outline="#00FF00", width=6)
        if ((lastTileXIndex != tileXIndex) or (lastTileYIndex != tileYIndex)):  # user mouses to a new square
            if (clickStartSquare != (lastTileXIndex, lastTileYIndex)):  # don't redraw if it's the start square
                redrawTile(lastTileXIndex, lastTileYIndex)  # redraw over last square (to remove green rect)
            lastTileXIndex = tileXIndex
            lastTileYIndex = tileYIndex
    pass


def redrawTile(x, y):
    global count
    global board
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # redraws a tile with its piece
    boardIndex = y * 8 + x
    i = x
    j = y
    xpos = (i * squareSize) - 3
    ypos = (j * squareSize) - 3 # each tile is 60x60 px
    if flipped:
        xpos = ((7 - i) * squareSize)
        ypos = ((7 - j) * squareSize)
    col = colLight
    if ( ( (i + j) % 2 ) == 0 ): col = colDark  # alternate tiles are dark
    # redraw tile
    drawEndX = (xpos + squareSize)
    drawEndY = (ypos + squareSize)
    if flipped:
        drawEndX = ((7 - xpos) + squareSize)
        drawEndY = ((7 - ypos) + squareSize)

    tempDrawDir = 1
    if (game['tomove'] == "Black") and (flipped == True): tempDrawDir = 0
    if (game['tomove'] == "White") and (flipped == True): tempDrawDir = 0
    boardCanvas.create_rectangle(xpos + 3 * tempDrawDir, ypos + 3 * tempDrawDir, (xpos + squareSize + 3 * tempDrawDir), (ypos + squareSize + 3 * tempDrawDir), fill=col, outline=col)
    #redraw piece
    piece = board[boardIndex]
    pieceFile = ''

    if (piece == 'R'): pieceFile = 'pieces\WR.png'  #white rook
    if (piece == 'N'): pieceFile = 'pieces\WN.png'  #white knight
    if (piece == 'B'): pieceFile = 'pieces\WB.png'  #white bishop
    if (piece == 'Q'): pieceFile = 'pieces\WQ.png'  #white queen
    if (piece == 'K'): pieceFile = 'pieces\WK.png'  #white king
    if (piece == 'P'): pieceFile = 'pieces\WP.png'  #white pawn

    if (piece == 'r'): pieceFile = 'pieces\BR.png'  #black rook
    if (piece == 'n'): pieceFile = 'pieces\BN.png'  #black knight
    if (piece == 'b'): pieceFile = 'pieces\BB.png'  #black bishop
    if (piece == 'q'): pieceFile = 'pieces\BQ.png'  #black queen
    if (piece == 'k'): pieceFile = 'pieces\BK.png'  #black king
    if (piece == 'p'): pieceFile = 'pieces\BP.png'  #black pawn
    count += 1
    if (pieceFile != ''):
        #app.img[count] = ImageTk.PhotoImage(file=pieceFile)
        #boardCanvas.create_image((xpos), (ypos), image=app.img[count], anchor=NW)

        img = Image.open(pieceFile)
        img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
        app.img[count] = ImageTk.PhotoImage(img)
        boardCanvas.create_image(xpos+3*tempDrawDir, ypos+3*tempDrawDir, image=app.img[count], anchor=NW)
    pass


def canvasRelease(event):
    global clickDragging
    global board, tkRoot
    global boardHistory, boardHistoryPos
    if (clickDragging == False):
        return
    if boardHistoryPos != (len(boardHistory) - 1): return
    #tkRoot.update()
    mouseX = event.x
    mouseY = event.y

    # convert mouseX, mouseY to board array indices
    (tileXindex, tileYindex) = convertXYtoBoardIndex(mouseX, mouseY)
    #convert board indices to X Y position of tiles
    #(tileScrX, tileScrY) = convertBoardIndextoXY(tileXindex, tileYindex)
    startSquare = (clickStartBoardIndex[0], clickStartBoardIndex[1])
    endSquare = (tileXindex, tileYindex)
    pieceMoved = clickStartPiece
    move = (startSquare, endSquare)
    moveIsValid = False
    # Check if move is valid
    if ( (clickStartBoardIndex != (tileXindex, tileYindex)) and  #not dragging onto start square
             (pieceMoved != '0') ):  #not dragging from an empty square
        # Check whether move is in legalMoves[] (is legal move)
        if (move in legalMoves) or (move in legalMovesEP) or (move in legalMovesCastling): moveIsValid = True
        if freePlay:  #if freePlay: allow non-legal moves
            moveIsValid = True
        if moveIsValid:
            # Valid move
            # Move on board[] endsquare and zero starting square
            #makeMove((startSquare, endSquare))
            #drawBoard()
            #drawPieces()
            #tkRoot.update()
            redrawTile(tileXindex,tileYindex)
            makeMove((startSquare, endSquare))
    if clickDragging == True:
        clickDragging = False
        drawBoard()
        drawPieces()
        tkRoot.update()



def evalBoard():
    global evalMobilityCheck
    global legalMoves
    global pieceSquareTable, pieceSquareTableEndgame, pieceSquareTableOpening
    global knightVal, rookVal, gameStage, pawnCount

    score = 0
    scoreBlack = 0
    scoreWhite = 0
    a = 0
    #print gameStage
    #print queensLeft
    for piece in board:
        if piece != '0':
            p = int(a)
            tileYindex = int(a / 8)
            tileXindex = a - int(tileYindex * 8)
            pos = (tileXindex, tileYindex)
           # if piece == 'k': kingPos['Black'] = pos
            #if piece == 'K': kingPos['Black'] = pos
            # add piece values
            if piece.islower():
                # piece belongs to Black
                val = pieceVal[piece.upper()]
                if piece.upper() == 'N':
                    val = knightVal
                if piece.upper() == 'R':
                    val = rookVal
                    if tileYindex == 6:
                        #black rook on white's 7th rank
                        val -= 0.2
                score -= val
            if piece.isupper():
                val = pieceVal[piece.upper()]
                if piece.upper() == 'N':
                    val = knightVal
                if piece.upper() == 'R':
                    val = rookVal
                    if tileYindex == 1:
                        #white rook on blacks 7th rank
                        val += 0.2
                score += val
            # add value from piece square table
            PSTVal = pieceSquareTable[piece][p]
            if piece.upper() == 'K' and gameStage == 'Endgame': PSTVal = pieceSquareTableEndgame[piece][p]
            if piece.upper() == 'Q' and gameStage == 'Opening': PSTVal = pieceSquareTableOpening[piece][p]
            score = score + (float(PSTVal) / 100)
            evalMobilityCheck = False
            if evalMobilityCheck:
                for (startPos, endPos) in legalMoves:
                    if startPos == pos:
                        amount = 0.02
                        if pos in [(3, 3), (4, 3), (3, 4), (4, 4)]: amount = 0.1
                        if piece.islower():
                            score -= amount
                        if piece.isupper():
                            score += amount
        a += 1
    #score = scoreWhite - scoreBlack
    #print piece, score
    #if piece.lower() != 'r' and piece.lower() != 'q' and piece != '0':
    #    print piece, pieceSquareTable[piece]
    #    score = score + (pieceSquareTable[piece] / 100)
    #print score
    return score


def alphabeta(depth):
    global game
    global board
    global legalMoves
    global bestMove
    global gameStage

    startTime = time.time()

    startCol = game['tomove']
    notStartCol = game['nottomove']
    moveTree = []
    genLegalMoves()
    legalMoves = (legalMoves + legalMovesEP + legalMovesCastling)

    alpha = -9999
    beta = 9999
    # Add all legal moves to first level of move tree
    for move in legalMoves :
        node = moveNode((move), [], None)
        node.score = None
        moveTree.append(node)
        isCheckMate = False
        oppInCheck = False
        oppInCheckmate = False
        meInCheckmate = False
        origBoard = list(board)
        makeTempMove(node.move)
        origLegalMoves = list(legalMoves)


        tomove = game['tomove']
        nottomove = game['nottomove']
        if game['tomove'] == 'White': tomove = 'Black'
        if game['tomove'] == 'Black': tomove = 'White'
        game['tomove'] = tomove
        if game['tomove'] == 'White': game['nottomove'] = 'Black'
        if game['tomove'] == 'Black': game['nottomove'] = 'White'

        genLegalMoves()
        legalMoves = (legalMoves + legalMovesEP + legalMovesCastling)
        if len(legalMoves) == 0:
            meInCheck = isInCheck(board, kingPos[startCol], startCol)
            if meInCheck: #loses to checkmate
                meInCheckmate = True
            oppInCheck = isInCheck(board, kingPos[notStartCol], notStartCol)
            if oppInCheck: #wins with checkmate
                oppInCheckmate = True
                bestMoves = [node.move]
                bestMove = node.move
                bestMoveNode = node
        if oppInCheckmate:
            bestMoveNode = node
            bestMove = node.move
            if startCol == 'Black':
                score = -9999
            if startCol == 'White':
                score = 9999
            node.score = score
            bestScore = node.score
            cmScore = score
            bestMoveIsMate = True
            board = list(origBoard)
            legalMoves = list(origLegalMoves)
            tomove = game['tomove']
            nottomove = game['nottomove']
            if game['tomove'] == 'White': tomove = 'Black'
            if game['tomove'] == 'Black': tomove = 'White'
            game['tomove'] = tomove
            if game['tomove'] == 'White': game['nottomove'] = 'Black'
            if game['tomove'] == 'Black': game['nottomove'] = 'White'

            return (node.move)
        board = list(origBoard)
        legalMoves = list(origLegalMoves)
    # moveTree complete for depth 0
    origKingPos = {}
    origKingPos['Black'] = kingPos['Black']
    origKingPos['White'] = kingPos['White']
    origBoard = list(board)
    newTree = []
    currentTree = []
    nextChildren = list(moveTree)
    aboveNodes = []
    finalNodes = []
    bestMoveIsMate = False
    if depth == 0:
        aboveNodes = moveTree # moveTree will only be populated with the depth-1 nodes i.e. nodes of legalMoves
        for node in aboveNodes:
            makeTempMove(node.move)
            score = evalBoard()
            #score = round(score,2)
            tomove = game['tomove']
            nottomove = game['nottomove']
            if game['tomove'] == 'White': tomove = 'Black'
            if game['tomove'] == 'Black': tomove = 'White'
            game['tomove'] = tomove
            if game['tomove'] == 'White': game['nottomove'] = 'Black'
            if game['tomove'] == 'Black': game['nottomove'] = 'White'

            origLegalMoves = list(legalMoves)
            genLegalMoves()
            if len(legalMoves) == 0:
                if isInCheck(board, kingPos[game['tomove']],game['tomove']):
                    if game['tomove'] == startCol:
                        #if AI is the one getting mated
                        #give it worst score possible
                        if startCol == 'Black': score = 9999
                        if startCol == 'White': score = -9999
                    if game['tomove'] != startCol:
                        #AI has given checkmate
                        #give best score possible
                        if startCol == 'Black': score = -9999
                        if startCol == 'White': score = 9999
            legalMoves = list(origLegalMoves)

            tomove = game['tomove']
            nottomove = game['nottomove']
            if game['tomove'] == 'White': tomove = 'Black'
            if game['tomove'] == 'Black': tomove = 'White'
            game['tomove'] = tomove
            if game['tomove'] == 'White': game['nottomove'] = 'Black'
            if game['tomove'] == 'Black': game['nottomove'] = 'White'

            board = list(origBoard)
            node.score = score
    if depth > 0:
        curDepth = 0
        while curDepth < depth:
            curDepth += 1
            #print curDepth
            tomove = game['tomove']
            nottomove = game['nottomove']
            if game['tomove'] == 'White': tomove = 'Black'
            if game['tomove'] == 'Black': tomove = 'White'
            game['tomove'] = tomove
            if game['tomove'] == 'White': game['nottomove'] = 'Black'
            if game['tomove'] == 'Black': game['nottomove'] = 'White'

            currentTree = list(nextChildren)
            nextChildren = []

            # generate children for next depth
            #beforeBoard = list(board)
            moveList = []
            board = list(origBoard)
            kingPos['Black'] = origKingPos['Black']
            kingPos['White'] = origKingPos['White']
            if startCol == "Black": bestScore = 9999
            if startCol == "White": bestScore = -9999
            i = 0
            currentStartTime = time.time()
            currentTreeLen = len(currentTree)
            for node in currentTree:
                i+=1
                moveList = [node.move]
                aboveNode = node.parent
                while aboveNode != None:
                    moveList.append(aboveNode.move)
                    aboveNode = aboveNode.parent
                #print moveList
                moveList = list(reversed(moveList))
                game['tomove'] = startCol
                game['nottomove'] = notStartCol
                for move in moveList:
                    makeTempMove(move)
                    tomove = game['tomove']
                    nottomove = game['nottomove']
                    if game['tomove'] == 'White': tomove = 'Black'
                    if game['tomove'] == 'Black': tomove = 'White'
                    game['tomove'] = tomove
                    if game['tomove'] == 'White': game['nottomove'] = 'Black'
                    if game['tomove'] == 'Black': game['nottomove'] = 'White'
                isCheckMate = False
                oppInCheckmate = False
                meInCheckmate = False
                genLegalMoves()
                legalMoves = (legalMoves + legalMovesEP + legalMovesCastling)
                if len(legalMoves) == 0:
                    meInCheck = isInCheck(board, kingPos[startCol], startCol)
                    if meInCheck: #loses to checkmate
                        meInCheckmate = True
                    oppInCheck = isInCheck(board, kingPos[notStartCol], notStartCol)
                    if oppInCheck: #wins with checkmate
                        oppInCheckmate = True
                        bestMoves = [node.move]
                        bestMove = node.move
                bestMove = moveList[0]
                if startCol == 'Black': bestScore = 9999
                if startCol == 'White': bestScore = -9999
                #genLegalMoves()
                origMoveList = list(moveList)
                iscutoff = False
                finished = False
                #if isCheckMate: time.sleep(3)
                bestMoveNode = ()
                if oppInCheckmate:
                    bestMoveNode = node
                    bestMove = node.move
                    if startCol == 'Black':
                        score = -9999
                    if startCol == 'White':
                        score = 9999
                    node.score = score
                    bestScore = node.score
                    cmScore = score
                    bestMoveIsMate = True
                while finished == False and not (oppInCheckmate or meInCheckmate):
                    for nextMove in legalMoves:
                        moveList = list(origMoveList)
                        nextMoveNode = moveNode(nextMove,[], node)
                        nextMoveNode.score = None
                        moveList.append(nextMove)
                        if curDepth == depth:
                            # terminal node
                            beforeBoard = list(board)
                            tomove = game['tomove']
                            nottomove = game['nottomove']
                            capPiece = board[convertSquaretoPos(nextMove[1])]
                            makeTempMove(nextMove)
                            if game['tomove'] == 'White': tomove = 'Black'
                            if game['tomove'] == 'Black': tomove = 'White'
                            game['tomove'] = tomove
                            if game['tomove'] == 'White': game['nottomove'] = 'Black'
                            if game['tomove'] == 'Black': game['nottomove'] = 'White'
                            tomove = game['tomove']
                            nottomove = game['nottomove']
                            score = evalBoard()
                            #print score
                            if isInCheck(board, kingPos[game['tomove']],game['tomove']):
                                origLegalMoves = list(legalMoves)
                                genLegalMoves()
                                if len(legalMoves) == 0:
                                    if game['tomove'] == startCol:
                                        #if AI is the one getting mated
                                        #give it worst score possible
                                        if startCol == 'Black': score = 9999
                                        if startCol == 'White': score = -9999
                                    if game['tomove'] != startCol:
                                        #AI has given checkmate
                                        #give best score possible
                                        if startCol == 'Black': score = -9999
                                        if startCol == 'White': score = 9999
                                legalMoves = list(origLegalMoves)
                            '''
                            #check for checkmate, stalemate, draw by repetition and 50 move rule
                            origLegalMoves = list(legalMoves)
                            genLegalMoves()
                            if len(legalMoves) == 0:
                                if isInCheck(board, kingPos[game['tomove']],game['tomove']):
                                    #game is checkmate
                                    if game['tomove'] == startCol:
                                        #if AI is the one getting mated
                                        #give it worst score possible
                                        if startCol == 'Black': score = 9999
                                        if startCol == 'White': score = -9999
                                    if game['tomove'] != startCol:
                                        #AI has given checkmate
                                        #give best score possible
                                        if startCol == 'Black': score = -9999
                                        if startCol == 'White': score = 9999
                                if not isInCheck(board, kingPos[game['tomove']],game['tomove']):
                                    #game is stalemate
                                    score = 0
                            legalMoves = list(origLegalMoves)
                            curPos = boardHistoryPos
                            numReps = 0
                            curPos = -1
                            while curPos >= 0:
                                boardState = list(boardHistory[curPos])
                                #print boardState[0], board[0]
                                if (list(boardState) == list(board)): numReps+=1
                                if numReps >= 3: #numReps == 2 (repeated twice) means that current position has occured for third time
                                    score = 0
                                    return
                                curPos -= 2
                            '''
                            '''
                            if capPiece != '0':
                                QSScore = QSSearch(score)
                                score = QSScore
                                node.score = score
                            '''
                            #print moveList, capPiece

                            tomove = game['tomove']
                            nottomove = game['nottomove']
                            if game['tomove'] == 'White': tomove = 'Black'
                            if game['tomove'] == 'Black': tomove = 'White'
                            game['tomove'] = tomove
                            if game['tomove'] == 'White': game['nottomove'] = 'Black'
                            if game['tomove'] == 'Black': game['nottomove'] = 'White'

                            board = list(origBoard)
                            aboveNode = nextMoveNode.parent
                            aboveScore = nextMoveNode.parent.score
                            if aboveScore == None:
                                nextMoveNode.parent.score = score
                                aboveScore = score
                            if aboveNode != None:
                                if game['tomove'] == 'Black': #minimize score for black
                                    if score < aboveScore:
                                        aboveScore = score
                                        nextMoveNode.parent.score = score
                                        if score <= bestScore:
                                            pass
                                            #bestScore = score
                                if game['tomove'] == 'White': #maximize score for white
                                    if score > aboveScore:
                                        aboveScore = score
                                        nextMoveNode.parent.score = score
                                aboveNodeParent = aboveNode.parent
                                if game['tomove'] == 'White': # maximize score for white
                                    if score >= alpha:
                                        #prune this nude
                                        pass
                                if game['tomove'] == 'Black': #minimize score for black
                                    if score <= beta:
                                        pass
                            if score >= alpha:
                                alpha = score
                            if score <= beta:
                                beta = score
                            board = list(beforeBoard)
                        nextChildren.append(nextMoveNode)
                        node.children.append(nextMoveNode)
                        moveTree.append(nextMoveNode)
                    finished = True
                if curDepth == depth:
                    aboveNodes.append(node)
                if ((i%500)==0):
                    thinkingPercent = (i * float(100.00 / currentTreeLen))
                    thinkingTimeDone = (time.time() - currentStartTime)
                    thinkingRate = float(float(i) / float(thinkingTimeDone)) #nodes/sec
                    thinkingTimeLeft = float(float(currentTreeLen - i) / float(thinkingRate))
                    thinkingRate = round(thinkingRate,2)
                    thinkingTimeLeft = round(thinkingTimeLeft,2)
                    #thinkingLabelText.set("Thinking: " + str(int(round(thinkingPercent,0))) + "%")
                    #tkRoot.update()
                    #if ((i%500)==0): print str(i),"/", len(currentTree)
                    print "Depth: " + str(curDepth) + " Thinking: " + str(int(round(thinkingPercent,0))) + "% " + "Time left: " + str(thinkingTimeLeft) + "s Rate: " + str(thinkingRate) + "nodes/sec"
                board = list(origBoard)
                kingPos['Black'] = origKingPos['Black']
                kingPos['White'] = origKingPos['White']
    tomove = game['tomove']
    nottomove = game['nottomove']
    if game['tomove'] == 'White': tomove = 'Black'
    if game['tomove'] == 'Black': tomove = 'White'
    game['tomove'] = tomove
    if game['tomove'] == 'White': game['nottomove'] = 'Black'
    if game['tomove'] == 'Black': game['nottomove'] = 'White'
    while aboveNodes != []:
        newAboveNodes = []
        for node in aboveNodes:
            score = node.score
            aboveNode = node.parent
            if aboveNode != None:
                if aboveNode not in newAboveNodes: newAboveNodes.append(aboveNode)
                aboveScore = aboveNode.score
                aboveMove = aboveNode.move
                if aboveScore == None:
                    node.parent.score = score
                    aboveScore = score
                if game['tomove'] == 'Black': #minimize score for black
                    if score < aboveScore:
                        aboveScore = score
                        node.parent.score = score
                if game['tomove'] == 'White': #maximize score for white
                    if score > aboveScore:
                        aboveScore = score
                        node.parent.score = score
        if newAboveNodes == []:
            # at top level of tree
            finalNodes = aboveNodes
        aboveNodes = newAboveNodes
        tomove = game['tomove']
        nottomove = game['nottomove']
        if game['tomove'] == 'White': tomove = 'Black'
        if game['tomove'] == 'Black': tomove = 'White'
        game['tomove'] = tomove
        if game['tomove'] == 'White': game['nottomove'] = 'Black'
        if game['tomove'] == 'Black': game['nottomove'] = 'White'
    # at this point the top level of the tree has scores assigned for all of its moves
    # simply pick the one with the best score
    game['tomove'] = startCol
    if game['tomove'] == 'Black':
        bestScore = 9999
    if game['tomove'] == 'White':
        bestScore = -9999
    worstScore = bestScore
    bestMoves = []
    #print "aaaa1", len(finalNodes)
    for node in finalNodes:
        score = node.score
        move = node.move
        #print score
        if score == None: score = worstScore
        #print score, round(score,3)
        #score = round(score,3)
        #print move, score
        #print "Final:", move, score, bestScore
        #print move
        if game['tomove'] == 'Black':
            if score == bestScore:
                bestScore = score
                bestMoves += [move]
            if score < bestScore:
                bestScore = score
                bestMoves = [move]
                #print [move], score
        if game['tomove'] == 'White':
            if score == bestScore:
                bestScore = score
                bestMoves += [move]
            if score > bestScore:
                bestScore = score
                bestMoves = [move]
                #print [move], score
        #bestScore = round(bestScore,3)
    if len(bestMoves) == 0:
        #print legalMoves
        #print "no final moves found"
        bestMoves = legalMoves
    #print bestMoves
    if len(bestMoves) == 0: bestMoves = ['None']
    moveIndex = random.randint(0, (len(bestMoves) - 1))
    bestMove = bestMoves[int(moveIndex)]
    #print bestMove, bestScore
    #print len(moveTree)
    endTime = time.time()
    if bestMoveIsMate:
        bestScore = cmScore
    debugInfo = True
    if debugInfo:
        print "---"
        print "Think time: " + str(round(endTime - startTime,1)) + " seconds"
        print "Depth: " + str(depth + 1)
        print "Stage: " + gameStage
        print "Nodes: " + str(len(moveTree))
        print "Chosen move: " + str(bestMove)
        print "Eval: " + str(bestScore)
        if ((endTime - startTime) != 0): print "Nodes/sec: " + str( int(round((len(moveTree) / (endTime - startTime)),0)) )
        print "---"

    game['tomove'] = startCol
    if game['tomove'] == 'White': game['nottomove'] = 'Black'
    if game['tomove'] == 'Black': game['nottomove'] = 'White'
    genLegalMoves()
    #print bestScore
    #evalLabelText.set("Eval: " + str(round(float(bestScore),2)))

    return bestMove

def SEE(move):
    # static exchange evaluation

    global game, legalMoves, moveSet, board, tkRoot, pieceCol
    drawBoard()
    drawPieces()
    tkRoot.update()
    time.sleep(.93)
    makeTempMove(move)
    tomove = game['tomove']
    nottomove = game['nottomove']
    print tomove
    startCol = tomove
    notStartCol = nottomove
    attackedPiece = board[convertSquaretoPos(move[1])]
    attackedSquare = move[1]
    seeScore = pieceVal[attackedPiece.upper()]
    if tomove == 'Black': seeScore *= -1
    print "SEE:", move, attackedPiece
    print game['tomove']
    origLegalMoves = list(legalMoves)
    genLegalMoves()
    origBoard = list(board)
    cheapestReplyScore = 100
    cheapestReply = legalMoves[0]
    capMoves = len(legalMoves)
    while capMoves > 0:
        capMoves = 0
        for reply in legalMoves:
            capPiece = board[convertSquaretoPos(reply[0])]
            cappedPiece = board[convertSquaretoPos(reply[1])]
            if cappedPiece != '0': print cappedPiece, pieceCol[cappedPiece], tomove, reply[1], attackedSquare
            if cappedPiece != '0' and pieceCol[cappedPiece] != tomove and reply[1] == attackedSquare:
                capMoves += 1
                print capMoves,"@!!@!@!@!"
                if pieceVal[capPiece.upper()] < cheapestReplyScore:
                    cheapestReplyScore = pieceVal[capPiece.upper()]
                    cheapestReply = reply
        cappedPiece = board[convertSquaretoPos(cheapestReply[1])]
        makeTempMove(cheapestReply)
        if pieceCol[cappedPiece.upper()] == 'White':
            #white piece captured
            seeScore -= pieceVal[cappedPiece.upper()]
        if pieceCol[cappedPiece.upper()] == 'Black':
            #black piece captured
            seeScore += pieceVal[cappedPiece.upper()]            
        print cheapestReply, "!"
        tomove = game['tomove']
        nottomove = game['nottomove']
        if game['tomove'] == 'White': tomove = 'Black'
        if game['tomove'] == 'Black': tomove = 'White'
        game['tomove'] = tomove
        if game['tomove'] == 'White': game['nottomove'] = 'Black'
        if game['tomove'] == 'Black': game['nottomove'] = 'White'
        tomove = game['tomove']
        nottomove = game['nottomove']
        #print tomove,capMoves
        genLegalMoves()
        cheapestReplyScore = 100
    game['tomove'] = startCol
    game['nottomove'] = notStartCol
    tomove = game['tomove']
    nottomove = game['nottomove']
    drawBoard()
    drawPieces()
    tkRoot.update()
    time.sleep(.9)
    board = list(origBoard)
    # find all direct attackers

    
    
    '''
    currentSquare = attackedSquare
    moveDirs = ['Q','R','B','N','K']
    whiteAttacks = []
    blackAttacks = []
    for piece in moveDirs:
        moveDirs = moveSet[piece]
        for moveDir in moveDirs:
            inRange = True
            #print moveDir
            if piece == 'N' or piece == 'K':
                currentSquare = (attackedSquare[0] + moveDir[0], attackedSquare[1] + moveDir[1])
                if currentSquare[0] < 0 or currentSquare[0] > 7 or currentSquare[1] < 0 or currentSquare[1] > 7:
                    # out of range
                    inRange = False
                if inRange:
                    print currentSquare
                    attackingPiece = board[convertSquaretoPos(currentSquare)]
                    if attackingPiece.upper() == piece and pieceCol[attackedPiece] != pieceCol[attackingPiece]:
                        attackMove = (currentSquare,attackedSquare)
                        if attackMove != move:
                            if attackingPiece.upper() == attackingPiece: whiteAttacks.append(attackMove)
                            if attackingPiece.upper() != attackingPiece: blackAttacks.append(attackMove)
            if piece == 'Q' or piece == 'R' or piece == 'B':
                currentSquare = (attackedSquare[0] + moveDir[0], attackedSquare[1] + moveDir[1])
                if currentSquare[0] < 0 or currentSquare[0] > 7 or currentSquare[1] < 0 or currentSquare[1] > 7:
                    # out of range
                    inRange = False
                if inRange:
                    print currentSquare
    print whiteAttacks, blackAttacks
    '''
    pass
    
def QSSearch(origScore):

    # don't use this
    # it's garbage

    global board
    global game

    startCol = game['tomove']
    notStartCol = game['nottomove']
    tomove = game['tomove']
    nottomove = game['nottomove']
    beforeBoard = list(board)
    QSTree = []
    genLegalMoves()
    allMoves = legalMoves + legalMovesCastling + legalMovesEP
    capMoves = []
    # generate all capture moves
    for move in allMoves:
        capPiece = board[convertSquaretoPos(move[1])]
        if capPiece != '0':
            capMoves.append(move)
            node = moveNode(move, [], None)
            QSTree.append(node)
    #top level of QS tree is made
    lastQSTree = []
    while QSTree != []:
        for node in QSTree:
            lastQSTree = list(QSTree)
            capNodes = []
            moveList = [node.move]
            aboveNode = node.parent
            while aboveNode != None:
                moveList.append(aboveNode.move)
                aboveNode = aboveNode.parent
            moveList = list(reversed(moveList))
            #print "!", moveList
            game['tomove'] = startCol
            game['nottomove'] = notStartCol
            for move in moveList:
                print moveList
                makeTempMove(move)
                drawBoard()
                drawPieces()
                tkRoot.update()
                time.sleep(2)
                tomove = game['tomove']
                nottomove = game['nottomove']
                if game['tomove'] == 'White': tomove = 'Black'
                if game['tomove'] == 'Black': tomove = 'White'
                game['tomove'] = tomove
                if game['tomove'] == 'White': game['nottomove'] = 'Black'
                if game['tomove'] == 'Black': game['nottomove'] = 'White'

            node.score = evalBoard()
            genLegalMoves()
            allMoves = legalMoves + legalMovesCastling + legalMovesEP
            for move in allMoves:
                capPiece = board[convertSquaretoPos(move[1])]
                #print capPiece
                if capPiece != '0':
                    newNode = moveNode(move,[],node)
                    node.children.append(newNode)
                    capNodes.append(newNode)
                    node.score = None
                    #print "aaa", moveList, capPiece
        board = list(beforeBoard)
        QSTree = list(capNodes)
    aboveNodes = list(lastQSTree)
    #score all nodes
    finalNodes = []
    while aboveNodes != []:
        newAboveNodes = []
        for node in aboveNodes:
            score = node.score
            aboveNode = node.parent
            if aboveNode != None:
                if aboveNode not in newAboveNodes: newAboveNodes.append(aboveNode)
                aboveScore = aboveNode.score
                aboveMove = aboveNode.move
                if aboveScore == None:
                    node.parent.score = score
                    aboveScore = score
                if game['tomove'] == 'Black': #minimize score for black
                    if score < aboveScore:
                        aboveScore = score
                        node.parent.score = score
                if game['tomove'] == 'White': #maximize score for white
                    if score > aboveScore:
                        aboveScore = score
                        node.parent.score = score
        if newAboveNodes == []:
            # at top level of tree
            finalNodes = aboveNodes
        aboveNodes = newAboveNodes
    game['tomove'] = startCol
    game['nottomove'] = notStartCol
    bestScore = origScore
    if finalNodes:
        if game['tomove'] == 'Black':
            bestScore = 9999
        if game['tomove'] == 'White':
            bestScore = -9999
    bestMoves = []
    bestMove = None
    for node in finalNodes:
        score = node.score
        move = node.move
        print "QS Final:",move, score
        '''
        drawBoard()
        drawPieces()
        tkRoot.update()
        time.sleep(2)
        '''
        #print move, score
        #print "QS Final:", move, score, bestScore
        #print move
        if game['tomove'] == 'Black':
            if score == bestScore:
                bestScore = score
            if score < bestScore:
                bestScore = score
                #print [move]
        if game['tomove'] == 'White':
            if score == bestScore:
                bestScore = score
            if score > bestScore:
                bestScore = score
                #print [move]
    #if len(lastQSTree) > 0: print "aa", lastQSTree[0].move
    game['tomove'] = startCol
    game['nottomove'] = notStartCol
    board = list(beforeBoard)
    if bestScore == None: return origScore
    return bestScore

def searchMoves_L2():
    global origBoard
    global board
    global bestMove
    global AIDepth
    bestMove = None

    origBoard = list(board)
    AIDepth = 1
    toreturn = alphabeta(AIDepth)
    #print "return", toreturn
    return toreturn

def makeAIMove():
    AILevel = 2
    allMoves = legalMoves + legalMovesEP + legalMovesCastling
    totalAllowedMoves = len(allMoves)
    if AILevel == 0:
        if totalAllowedMoves > 0:
            moveIndex = random.randint(0, (totalAllowedMoves - 1))
            move = allMoves[moveIndex]
            makeMove((move[0], move[1]))
    if AILevel == 1:
        move = searchMoves_L1()
        makeMove(move)
    if AILevel == 2:
        move = searchMoves_L2()
        #print "ai move:", move
        if move != 'None': makeMove(move)
    if AILevel == 3:
        move = searchMoves_L3()
        makeMove(move)
    if totalAllowedMoves == 0:
        pass
        #game['ended'] = True

def drawCover():
    boardCanvas.delete("all")
    app.cover = ImageTk.PhotoImage(file='cover_simple.PNG')
    boardCanvas.create_image(-120, 3, image=app.cover, anchor=NW)
    
def drawBoard():
    global boardCanvas
    global canvasSize
    global colLight, colDark
    global app
    global boardImg
    global scalw, scaleh
    board = ''
    #img = Image.Open(file='board.PNG')
    img = Image.open("board.PNG")
    img = img.resize((canvasSize, canvasSize),Image.ANTIALIAS)
    boardImg = ImageTk.PhotoImage(img)
    #boardImg.config(file='board.PNG')
    #boardImg = PhotoImage(file='board.PNG').zoom(320,320)
    #boardImg.width = scalew
    #boardImg.height = scaleh
    #print dir(boardImg)
    boardCanvas.delete("all")
    boardCanvas.create_image(3, 3, image=boardImg, anchor=NW)
    colLight = (128, 128, 128)
    colDark = (196, 196, 196)
    colLight = '#%02x%02x%02x' % colLight
    colDark = '#%02x%02x%02x' % colDark
    return
    # Draw tiles
    boardsize = 60
    for i in range(0, 8):
        for j in range(0, 8):
            xpos = (i * 60)
            ypos = (j * 60)  # each tile is 60x60 px
            col = colLight
            if ( ( (i + j) % 2 ) == 0 ): col = colDark  # alternate tiles are dark
            # pygame.draw.rect(pygScreen, col, (xpos, ypos, 60, 60))
            boardCanvas.create_rectangle(xpos, ypos, (xpos + 65), (ypos + 65), fill=col, outline=col)


def drawPieces():
    global board
    global boardCanvas
    global canvasSize
    global app
    global count
    global flipped
    global boardHistory, boardHistoryPos

    app.img = {}
    count = 0
    dspboard = list(board)
    if flipped: dspboard = reversed(board)
    if boardHistoryPos != (len(boardHistory) - 1) and boardHistory != []:
        dspboard = list(boardHistory[boardHistoryPos])
        if flipped: dspboard = reversed(dspboard)
    for i in dspboard:
        # xTile goes from 0 to 7 (files)
        # yTile goes from 0 to 7 (ranks)
        xTile = (count % 8)  # every 8th byte is a new row
        yTile = int(round((count / 8), 0))  # each column is the nth byte in a row
        squareSize = int(canvasSize / 8)
        xDrawPos = (xTile * squareSize) - 3
        yDrawPos = (yTile * squareSize) - 3
        piece = i
        # debug# print count, piece, xTile, yTile
        pieceFile = ''

        if (piece == 'R'): pieceFile = 'pieces\WR.png'  #white rook
        if (piece == 'N'): pieceFile = 'pieces\WN.png'  #white knight
        if (piece == 'B'): pieceFile = 'pieces\WB.png'  #white bishop
        if (piece == 'Q'): pieceFile = 'pieces\WQ.png'  #white queen
        if (piece == 'K'): pieceFile = 'pieces\WK.png'  #white king
        if (piece == 'P'): pieceFile = 'pieces\WP.png'  #white pawn

        if (piece == 'r'): pieceFile = 'pieces\BR.png'  #black rook
        if (piece == 'n'): pieceFile = 'pieces\BN.png'  #black knight
        if (piece == 'b'): pieceFile = 'pieces\BB.png'  #black bishop
        if (piece == 'q'): pieceFile = 'pieces\BQ.png'  #black queen
        if (piece == 'k'): pieceFile = 'pieces\BK.png'  #black king
        if (piece == 'p'): pieceFile = 'pieces\BP.png'  #black pawn

        if (pieceFile != ''):
            img = Image.open(pieceFile)
            img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
            app.img[count] = ImageTk.PhotoImage(img)
            boardCanvas.create_image(xDrawPos + 3, yDrawPos + 3, image=app.img[count], anchor=NW)
        count += 1

main()
