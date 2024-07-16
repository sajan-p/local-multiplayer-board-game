from Utility import drawBackground
from Constants import BOARD_LAYOUT

class Player:
    def __init__(self, primaryKey, secondaryKey, playerNumber, tile = 0):
        self.primaryKey = primaryKey
        self.secondaryKey = secondaryKey
        self.playerNumber = playerNumber
        self.tile = 0
        
    def __str__(self):
        return "Player " + str(self.playerNumber) + " at " + str(self.tile) + " (" + str(self.primaryKey) + "/" + str(self.secondaryKey) + ")"

class Tile:
    def __init__(self, num, x, y, type, isOn):
        self.num = num
        self.x = x
        self.y = y
        self.type = type # "N" = Normal, "G" = Good, "B" = Bad
        self.isOn = isOn
        
        # Images
        self.normalTileImage = loadImage("img/game/tile/normal.png")
        self.goodTileImage = loadImage("img/game/tile/good.png")
        self.badTileImage = loadImage("img/game/tile/bad.png")
        
    def __str__(self):
        return str(self.type) + " " + "Tile " + str(self.num)
        
    def draw(self):
       
        if self.type == "N":
            image(self.normalTileImage, self.x, self.y)
        elif self.type == "B":
            image(self.badTileImage, self.x, self.y)
        elif self.type == "G":
            image(self.goodTileImage, self.x, self.y)       
                
                            

    
class Page_Game:
    def __init__(self):
        self.players = []
        self.turn = None
        self.board = []
        
        # Images
        self.scoreBackground0 = loadImage("img/game/scoreboard/0.png")
        self.scoreBackground1 = loadImage("img/game/scoreboard/1.png")
        self.scoreBackground2 = loadImage("img/game/scoreboard/2.png")
        self.scoreBackground3 = loadImage("img/game/scoreboard/3.png")
        
        # Pieces
        self.piece0 = loadImage("img/game/piece/0.png")
        self.piece1 = loadImage("img/game/piece/1.png")
        self.piece2 = loadImage("img/game/piece/2.png")
        self.piece3 = loadImage("img/game/piece/3.png")
        
        # Spinner
        self.goodSpinner = loadImage("img/game/spinner/good.png")
        self.badSpinner = loadImage("img/game/spinner/bad.png")
        self.pointer = loadImage("img/game/spinner/pointer.png")
        
        self.state = "R" # "R" = Roll, "P" = Pause, "C" = Choose
        self.gameText = "Insert Text Here"
        
        self.resetGame = False
         
        self.timeoutFunctions = [] # [[startTime, totalTime, function]...] # time in millis()
        self.drawGoodSpinner = False
        self.drawBadSpinner = False
        self.pointerX = 0
        
        self.isOtherMoving = False
        self.otherMovingPlayer = None
        
        self.questions = [["sin0", "0"], ["sin30", "1/2"], ["sin45", "sqrt2/2"], ["sin60", "sqrt3/2"], ["sin90", "1"], ["cos0", "1"], ["cos30", "sqrt3/2"], ["cos45", "sqrt2/2"], ["cos60", "1/2"], ["cos90", "0"], ["tan0", "0"], ["tan30", "sqrt3/3"], ["tan45", "1"], ["tan60", "sqrt3"], ["tan90", "undefined"]] 
        self.currQuestion  = []
        self.answerPrimary = None
        
        
    def draw(self):
        drawBackground()
        
        self.drawScoreBoard()
        self.drawTiles()
        self.drawPieces()
        self.drawText()
        self.manageTimeout()
        self.drawSpinners()
    
    def mouseClicked(self):      
        pass
    
    def keyTyped(self):
        if self.state == "R":
            if key.upper() == self.turn.primaryKey or key.upper() == self.turn.secondaryKey:
                if (key.upper() == self.turn.primaryKey and self.answerPrimary) or (key.upper() == self.turn.secondaryKey and not self.answerPrimary):
                    self.recieveRoll()
                else:
                   self.swapTurns() 
        if self.state == "C":
            if key.upper() == self.turn.primaryKey:
                self.confirmOtherMove(False)
            elif key.upper() == self.turn.secondaryKey:
                self.confirmOtherMove(True)
    
    def mouseMoved(self):
        pass
        
    def mouseReleased(self):
        pass
        
    def mousePressed(self):
        pass
    
    def getPlayers(self, players):
        self.players = []
        self.turn = None
        self.board = []
        self.state = "R" # "R" = Roll, "P" = Pause
        self.gameText = "Insert Text Here"
        
        self.resetGame = False
         
        self.timeoutFunctions = [] # [[startTime, totalTime, function]...] # time in millis()
        
        self.drawGoodSpinner = False
        self.drawBadSpinner = False  
        self.pointerX = 0      
        
        self.players = players        
        self.turn = players[0]
        
        self.createBoard()
        self.setupQuestion()
        
        self.isOtherMoving = False
        self.otherMovingPlayer = None
        
    def setupQuestion(self):
        self.currQuestion = self.questions[floor(random(len(self.questions)))]
        self.otherAnswer = self.questions[floor(random(len(self.questions)))]
        
        while self.otherAnswer[1] == self.currQuestion[1]:
            self.otherAnswer = self.questions[floor(random(len(self.questions)))]
            
        if floor(random(2)) == 0:
            self.gameText = self.currQuestion[0] + " = " + self.currQuestion[1] + " -> " + self.turn.primaryKey + "  /  " + self.otherAnswer[1] + " -> " + self.turn.secondaryKey
            self.answerPrimary = True
        else:
            self.gameText = self.currQuestion[0] + " = " + self.otherAnswer[1] + " -> " + self.turn.primaryKey + "  /  " + self.currQuestion[1] + " -> " + self.turn.secondaryKey
            self.answerPrimary = False
        
    def drawScoreBoard(self):
        imageMode(CORNER)
        
        # Draws Scoreboard Background
        if self.turn.playerNumber == 0:
            image(self.scoreBackground0, 0, 0)
        elif self.turn.playerNumber == 1:
            image(self.scoreBackground1, 0, 0)
        elif self.turn.playerNumber == 2:
            image(self.scoreBackground2, 0, 0)
        elif self.turn.playerNumber == 3:
            image(self.scoreBackground3, 0, 0)
            
    def drawTiles(self):
        for tile in self.board:
            tile.draw()
            
    def drawPieces(self):
        sharedTiles = [] # list full of lists of pieces on same tile
        foundMatchingTile = False
        
        for player in self.players:
            foundMatchingTile = False
            
            for sharedTile in sharedTiles:
                if player.tile == sharedTile[0].tile:
                    foundMatchingTile = True
                    sharedTile.append(player)
            if not foundMatchingTile:
                sharedTiles.append([player])
                
        for sharedTile in sharedTiles:
            if len(sharedTile) == 4:
                x = self.findTilePosition(sharedTile[0].tile)[0] + 17
                y = self.findTilePosition(sharedTile[0].tile)[1] + 5
                self.drawPiece(0, x-10, y-10)
                self.drawPiece(1, x+10, y-10)
                self.drawPiece(2, x-10, y+10)
                self.drawPiece(3, x+10, y+10)
            elif len(sharedTile) == 3:
                x = self.findTilePosition(sharedTile[0].tile)[0] + 17
                y = self.findTilePosition(sharedTile[0].tile)[1] + 5
                self.drawPiece(sharedTile[0].playerNumber, x-10, y-10)
                self.drawPiece(sharedTile[1].playerNumber, x+10, y-10)
                self.drawPiece(sharedTile[2].playerNumber, x, y+10)
            elif len(sharedTile) == 2:
                x = self.findTilePosition(sharedTile[0].tile)[0] + 17
                y = self.findTilePosition(sharedTile[0].tile)[1] + 5
                self.drawPiece(sharedTile[0].playerNumber, x-10, y)
                self.drawPiece(sharedTile[1].playerNumber, x+10, y)
            else:
                x = self.findTilePosition(sharedTile[0].tile)[0] + 17
                y = self.findTilePosition(sharedTile[0].tile)[1] + 5
                self.drawPiece(sharedTile[0].playerNumber, x, y)
        
    def drawPiece(self, num, x, y):
        imageMode(CORNER)
        if num == 0:
            image(self.piece0, x, y)    
        elif num == 1:
            image(self.piece1, x, y)   
        elif num == 2:
            image(self.piece2, x, y)   
        elif num == 3:
            image(self.piece3, x, y)       
            

    def drawText(self):
        textAlign(LEFT)
        fill(0)
        textSize(20)
        text(self.gameText, 220, 60)
        textSize(24)

    def createBoard(self):
        imageMode(CORNER)
        x = 70
        y = 500
        gap = 70
        changeBuffer = 0
        movingRight = True
        
        
        for i in range(len(BOARD_LAYOUT)):
            boardTile = BOARD_LAYOUT[i]
            
            if changeBuffer == 6:
                y -= gap
                changeBuffer += 1
            elif changeBuffer == 7:
                y -= gap
                changeBuffer = 1
                movingRight = not movingRight
            else:
                if movingRight:
                    x += gap
                else:
                    x -= gap
                changeBuffer += 1
            
            self.board.append(Tile(i, x, y, boardTile, False))
            
    def findTilePosition(self, tileNum):
        for tile in self.board:
            if tile.num == tileNum:
                return [tile.x, tile.y]
            
    def getPlayerFromNumber(self, num):
        for player in self.players:
            if player.playerNumber == num:
                return player
            
            
    def recieveRoll(self):
        self.gameText = "Rolling Dice..."
        self.state = "P"
        self.timeoutFunctions.append([millis(), 1000, self.rollDice, []])
        
    def rollDice(self):
        diceValue = self.dice()
        self.gameText = "Player " + str(self.turn.playerNumber + 1) + " rolled a " + str(diceValue) + "!"     
        self.timeoutFunctions.append([millis(), 1000, self.updateBoard, [diceValue, 0]])
        
    
    def updateBoard(self, params):
        
        if self.isOtherMoving:
            if params[0] <= -1:
                if params[1] <= params[0]:
                    self.checkBoard()
                    return
                if self.otherMovingPlayer.tile - 1 == -1:
                    self.checkBoard()
                    return
                
                self.otherMovingPlayer.tile -= 1        
                self.timeoutFunctions.append([millis(), 500, self.updateBoard, [params[0], params[1]-1]])
            else:
                if params[1] >= params[0]:
                    self.checkBoard()
                    return
                
                if self.otherMovingPlayer.tile + 1 == len(BOARD_LAYOUT):
                    self.timeoutFunctions.append([millis(), 500, self.setWinner, []])
                    return
        
                self.otherMovingPlayer.tile += 1        
                self.timeoutFunctions.append([millis(), 500, self.updateBoard, [params[0], params[1]+1]])
        
        elif params[0] <= -1:
            if params[1] <= params[0]:
                self.checkBoard()
                return
            if self.turn.tile - 1 == -1:
                self.checkBoard()
                return
            
            self.turn.tile -= 1        
            self.timeoutFunctions.append([millis(), 500, self.updateBoard, [params[0], params[1]-1]])
            
        else:
            if params[1] >= params[0]:
                self.checkBoard()
                return
            
            if self.turn.tile + 1 == len(BOARD_LAYOUT):
                self.timeoutFunctions.append([millis(), 500, self.setWinner, []])
                return
    
            self.turn.tile += 1        
            self.timeoutFunctions.append([millis(), 500, self.updateBoard, [params[0], params[1]+1]])
        
    def checkBoard(self):
        landedTile = BOARD_LAYOUT[self.turn.tile]
        other = self.checkIfOnOther()
        
        if self.isOtherMoving:
            theirLandedTile = BOARD_LAYOUT[self.otherMovingPlayer.tile]
            
            if theirLandedTile == "B":
                self.gameText = "Player " + str(self.otherMovingPlayer.playerNumber + 1) + " landed on a bad tile!"
                self.timeoutFunctions.append([millis(), 1000, self.badTile, []])
            elif theirLandedTile == "G":
                self.gameText = "Player " + str(self.otherMovingPlayer.playerNumber + 1) + " landed on a good tile!"
                self.timeoutFunctions.append([millis(), 1000, self.goodTile, []])
                
            elif landedTile == "N":
                self.drawGoodSpinner = False
                self.drawBadSpinner = False
                self.pointerX = 0
                
                self.otherMovingPlayer = None
                self.isOtherMoving = False            
                
                self.timeoutFunctions.append([millis(), 500, self.swapTurns, []])
            
            
        elif other != None:
            self.gameText = str(self.turn.secondaryKey) + " - Move Player " + str(other.playerNumber + 1) + "/" + str(self.turn.primaryKey) + " - Move Self"
            
            self.otherMovingPlayer = other
            self.isOtherMoving = True
            self.state = "C"
        
        elif landedTile == "N":
            self.drawGoodSpinner = False
            self.drawBadSpinner = False
            self.pointerX = 0
            
            self.otherMovingPlayer = None
            self.isOtherMoving = False            
            
            self.timeoutFunctions.append([millis(), 500, self.swapTurns, []])
        elif landedTile == "G":
            self.gameText = "Player " + str(self.turn.playerNumber + 1) + " landed on a good tile!"
            self.timeoutFunctions.append([millis(), 1000, self.goodTile, []])
        elif landedTile == "B":
            self.gameText = "Player " + str(self.turn.playerNumber + 1) + " landed on a bad tile!"
            self.timeoutFunctions.append([millis(), 1000, self.badTile, []])
    
    def goodTile(self):
        self.drawGoodSpinner = True
        self.pointerX = 0
        
        self.timeoutFunctions.append([millis(), 500, self.animateSpinner, [floor(random(421))]])
        
    def badTile(self):
        self.drawBadSpinner = True
        self.pointerX = 0
        
        self.timeoutFunctions.append([millis(), 500, self.animateSpinner, [floor(random(421))]])
        
    def swapTurns(self):
        self.turn = self.getPlayerFromNumber((self.turn.playerNumber + 1) % len(self.players))
        self.setupQuestion()
        self.state = "R"
    
    def dice(self):
        return ceil(random(6))
    
    def manageTimeout(self):
        for timeout in self.timeoutFunctions:
            startTime = timeout[0]
            totalTime = timeout[1]
            cb = timeout[2]
            params = timeout[3]
            
            if millis() - startTime >= totalTime:
                self.timeoutFunctions.remove(timeout)      
                if params == []:      
                    cb()
                else:
                    cb(params)
                    
    def setWinner(self):
        if self.isOtherMoving:
            self.gameText = "The winner is Player " + str(self.otherMovingPlayer.playerNumber + 1) + "!"
            self.timeoutFunctions.append([millis(), 5000, self.closeGame, []])
        else:            
            self.gameText = "The winner is Player " + str(self.turn.playerNumber + 1) + "!"
            self.timeoutFunctions.append([millis(), 5000, self.closeGame, []])
        
    def closeGame(self):
        self.resetGame = True
        
    def drawSpinners(self):
        if self.drawGoodSpinner:
            image(self.goodSpinner, 125, 200)
            image(self.pointer, self.pointerX + 125, 200)
        if self.drawBadSpinner:
            image(self.badSpinner, 125, 200)
            image(self.pointer, self.pointerX + 125, 200)
        
    def animateSpinner(self, params):
        finalValue = params[0]
        
        if self.pointerX >= finalValue:
            self.timeoutFunctions.append([millis(), 500, self.evaluateSpinner, []])
            return
        
        self.pointerX += 10.5
        
        self.timeoutFunctions.append([millis(), 1, self.animateSpinner, [finalValue]])
        
    def evaluateSpinner(self):
        spaces = 0
        if self.pointerX <= 21 * 2:
            spaces = 1
        elif self.pointerX <= 21 * 10:
            spaces = 2
        elif self.pointerX <= 21 * 16:
            spaces = 3
        elif self.pointerX <= 21 * 19:
            spaces = 4
        else:
            spaces = 10
            
        if self.isOtherMoving:   
            if self.drawGoodSpinner:
                self.gameText = "Player " + str(self.otherMovingPlayer.playerNumber + 1) + " moves " + str(spaces) + " forward!"
                self.timeoutFunctions.append([millis(), 100, self.removeSpinner, []])      
                self.timeoutFunctions.append([millis(), 1000, self.updateBoard, [spaces, 0]])
            if self.drawBadSpinner:            
                self.gameText = "Player " + str(self.otherMovingPlayer.playerNumber + 1) + " moves " + str(spaces) + " backward!"
                self.timeoutFunctions.append([millis(), 100, self.removeSpinner, []])      
                self.timeoutFunctions.append([millis(), 1000, self.updateBoard, [-spaces, 0]])
        else:
            if self.drawGoodSpinner:
                self.gameText = "Player " + str(self.turn.playerNumber + 1) + " moves " + str(spaces) + " forward!"
                self.timeoutFunctions.append([millis(), 100, self.removeSpinner, []])      
                self.timeoutFunctions.append([millis(), 1000, self.updateBoard, [spaces, 0]])   
                
            if self.drawBadSpinner:
                self.gameText = "Player " + str(self.turn.playerNumber + 1) + " moves " + str(spaces) + " backward!"
                self.timeoutFunctions.append([millis(), 100, self.removeSpinner, []])      
                self.timeoutFunctions.append([millis(), 1000, self.updateBoard, [-spaces, 0]])
            
    def removeSpinner(self):
        self.drawGoodSpinner = False
        self.drawBadSpinner = False
        self.pointerX = 0
            
            
    def checkIfOnOther(self):
        tile = self.turn.tile
        sameTilePlayers = []
        
        for player in self.players:
            if player.playerNumber != self.turn.playerNumber and player.tile == tile:
                sameTilePlayers.append(player)
                
        
        if len(sameTilePlayers) == 0:
            return None
        elif len(sameTilePlayers) == 1:
            return sameTilePlayers[0]
        else:
            return sameTilePlayers[floor(random(len(sameTilePlayers)))]
                
        
    def confirmOtherMove(self, isMovingOther):
        self.state = "P"
        
        if isMovingOther:
            self.gameText = "Player " + str(self.otherMovingPlayer.playerNumber + 1) + " is moving back!"
            self.drawBadSpinner = True
            self.timeoutFunctions.append([millis(), 1000, self.badTile, []])
        else:
            self.gameText = "Player " + str(self.turn.playerNumber + 1) + " is moving forward!"
            self.drawGoodSpinner = True
            self.otherMovingPlayer = None
            self.isOtherMoving = False
            self.timeoutFunctions.append([millis(), 1000, self.goodTile, []])
            
        
        
            
    
        
        
    
    
    
        
