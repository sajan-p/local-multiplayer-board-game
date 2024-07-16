from Utility import drawBackground, hover
from Button import ButtonImage
from Page_Game import Player

class PlayerKeybindsTextbox:
    def __init__(self, x, y, playerNumber, isPrimary, content):
        self.textboxImage = loadImage("img/setup/textbox.png")
        self.x = x - self.textboxImage.width / 2
        self.y = y - self.textboxImage.height / 2
        self.w = self.textboxImage.width
        self.h = self.textboxImage.height
        self.playerNumber = playerNumber
        self.isPrimary = isPrimary
        self.content = content
        
        self.hover = False
        self.active = False
    
    def draw(self, content):
        self.content = content
        imageMode(CORNER)
        
        if self.active:
            tint(220, 220, 220)
            self.render(content)
            tint(255, 255, 255)
        elif self.hover:
            tint(240, 240, 240)
            self.render(content)
            tint(255, 255, 255)
        else:
            tint(255, 255, 255)
            self.render(content)
        
        imageMode(CENTER)
        
    def render(self, content):
        image(self.textboxImage, self.x, self.y)
                
        fill(0)
        textAlign(CENTER)
        textSize(24)
        text(content, self.x+2 + self.textboxImage.width/2, self.y+8 + self.textboxImage.height / 2)
        fill(255)
        
        
    def checkBounds(self, mx, my):
        self.x += 45
        self.y += 26
        self.w -= 90
        self.h -= 52
        
        isTrue = mx > self.x and mx < self.x + self.w and my > self.y and my < self.y + self.h
        
        self.x -= 45
        self.y -= 26
        self.w += 90
        self.h += 52
        
        return isTrue
        
    def mouseClicked(self):
        if self.checkBounds(mouseX, mouseY):
            self.active = True
        else:
            self.active = False
            
        return self.active
    
    def mouseMoved(self):
        if self.checkBounds(mouseX, mouseY):
            self.hover = True
        else:
            self.hover = False
        return self.hover
    
        
class PlayerSetup:
    def __init__(self, x, y, setupImage, playerNumber, primaryKey, secondaryKey, isPlaying, onPlayerPress, onPlayerAdd):
        self.x = x
        self.y = y
        self.setupImage = setupImage
        self.playerNumber = playerNumber
        self.primaryKey = primaryKey
        self.secondaryKey = secondaryKey
        self.isPlaying = isPlaying
        self.onPlayerPress = onPlayerPress
        self.onPlayerAdd = onPlayerAdd
        
        self.playerAddImage = loadImage("img/setup/player_add.png")
        self.playerAddButton = ButtonImage(self.playerAddImage, self.x, self.y, onPlayerAdd)   

        self.backImage = loadImage("img/setup/back_button.png")
        self.backButton = ButtonImage(self.backImage, self.x + 50, self.y - 70, onPlayerPress)        
        
        self.primaryKeybindsTextbox = PlayerKeybindsTextbox(self.x, self.y-12, self.playerNumber, True, self.primaryKey)
        self.secondaryKeybindsTextbox = PlayerKeybindsTextbox(self.x, self.y+60, self.playerNumber, False, self.secondaryKey)
        
    def draw(self):
        if self.isPlaying:
            image(self.setupImage, self.x, self.y)
            self.primaryKeybindsTextbox.draw(self.primaryKey)
            self.secondaryKeybindsTextbox.draw(self.secondaryKey)
        else:
            self.playerAddButton.draw()
        
    def drawButton(self):
        self.backButton.draw()

class Page_Setup:
    def __init__(self):
        self.setupTextImage = loadImage("img/text/setup.png") 
        
        self.playerOneSetupTileImage = loadImage("img/setup/p1_background.png")
        self.playerTwoSetupTileImage = loadImage("img/setup/p2_background.png")
        self.playerThreeSetupTileImage = loadImage("img/setup/p3_background.png")
        self.playerFourSetupTileImage = loadImage("img/setup/p4_background.png")
        
        self.playerOneSetup = PlayerSetup(220, 190, self.playerOneSetupTileImage, 0, "Z", "X", True, self.onPlayerPress, self.onPlayerAdd)
        self.playerTwoSetup = PlayerSetup(375, 190, self.playerTwoSetupTileImage, 1, "N", "M", True, self.onPlayerPress, self.onPlayerAdd)
        self.playerThreeSetup = PlayerSetup(220, 390, self.playerThreeSetupTileImage, 2, "T", "Y", True, self.onPlayerPress, self.onPlayerAdd)
        self.playerFourSetup = PlayerSetup(375, 390, self.playerFourSetupTileImage, 3, "U", "I", True, self.onPlayerPress, self.onPlayerAdd)
        
        self.playerSetups = [self.playerOneSetup, self.playerTwoSetup, self.playerThreeSetup, self.playerFourSetup]
        self.playerKeybinds = [self.playerOneSetup.primaryKeybindsTextbox, self.playerOneSetup.secondaryKeybindsTextbox, self.playerTwoSetup.primaryKeybindsTextbox, self.playerTwoSetup.secondaryKeybindsTextbox, self.playerThreeSetup.primaryKeybindsTextbox, self.playerThreeSetup.secondaryKeybindsTextbox, self.playerFourSetup.primaryKeybindsTextbox, self.playerFourSetup.secondaryKeybindsTextbox]
        
        self.lastClicked = -1
        self.backButtonToDisplay = 3
        
        self.playerAddImage = loadImage("img/setup/player_add.png")
        
        self.goImage = loadImage("img/setup/go_button.png")
        self.goButton = ButtonImage(self.goImage, 300, 540, self.onGoButtonPress)
        
        self.didClickGo = False
    
    def draw(self):
        drawBackground()
        hover(self.setupTextImage, 300, 50, 3, 7)
        self.drawPlayerSetupTiles()
        self.drawBackButton()
        self.goButton.draw()
    
    def mouseClicked(self):
            
        if self.backButtonToDisplay == 2:
            self.playerSetups[3].playerAddButton.mouseClicked()
            self.playerSetups[2].backButton.mouseClicked()
            
        elif self.backButtonToDisplay == -1:
            self.playerSetups[3].playerAddButton.mouseClicked()
            self.playerSetups[2].playerAddButton.mouseClicked()
    
        elif self.backButtonToDisplay != 1:    
            self.playerSetups[self.backButtonToDisplay].backButton.mouseClicked()
            
        self.goButton.mouseClicked()
            
    def keyTyped(self):
        if self.lastClicked == -1: return
        if key.upper() not in "1234567890-=QWERTYUIOP[]\ASDFGHJKL;'ZXCVBNM,./": return
        
        playerNumber = self.playerKeybinds[self.lastClicked].playerNumber
        isPrimary = self.playerKeybinds[self.lastClicked].isPrimary
        
        otherKey = self.checkKeyExists(key)
        
        savedKey = ""
                
        if isPrimary:
            savedKey = self.playerSetups[playerNumber].primaryKey
            self.playerSetups[playerNumber].primaryKey = key.upper()
        else:
            savedKey = self.playerSetups[playerNumber].secondaryKey
            self.playerSetups[playerNumber].secondaryKey = key.upper()
            
        if otherKey != -1:
            otherPlayerNumber = self.playerKeybinds[otherKey].playerNumber
            otherIsPrimary = self.playerKeybinds[otherKey].isPrimary
            
            if otherIsPrimary:
                self.playerSetups[otherPlayerNumber].primaryKey = savedKey
            else:
                self.playerSetups[otherPlayerNumber].secondaryKey = savedKey
            
    
    def mouseMoved(self):
        onTextbox = False
        
        for textbox in self.playerKeybinds:
            if not self.toCheck(textbox): continue
            
            if textbox.mouseMoved():
                onTextbox = True
        
        if onTextbox:
            cursor(POINT)
        else:
            cursor(ARROW)
            
        if self.backButtonToDisplay != -1:    
            self.playerSetups[self.backButtonToDisplay].backButton.mouseMoved()
            
        if self.backButtonToDisplay == 2:
            self.playerSetups[3].playerAddButton.mouseMoved()
            
        if self.backButtonToDisplay == -1:
            self.playerSetups[3].playerAddButton.mouseMoved()
            self.playerSetups[2].playerAddButton.mouseMoved()
            
        self.goButton.mouseMoved()
        
        
    def mouseReleased(self):
        if self.backButtonToDisplay != -1:    
            self.playerSetups[self.backButtonToDisplay].backButton.mouseReleased()
        
        if self.backButtonToDisplay == 2:
            self.playerSetups[3].playerAddButton.mouseReleased()
            
        if self.backButtonToDisplay == -1:
            self.playerSetups[3].playerAddButton.mouseReleased()
            self.playerSetups[2].playerAddButton.mouseReleased()
        
        self.goButton.mouseReleased()
        
    def mousePressed(self):
        foundButton = False
        
        for i in range(len(self.playerKeybinds)):
            if not self.toCheck(self.playerKeybinds[i]): pass
            
            if self.playerKeybinds[i].mouseClicked():
                foundButton = True
                if i != self.lastClicked:
                    self.playerKeybinds[self.lastClicked].active = False
                    self.lastClicked = i
                break
        
        if not foundButton:
            self.lastClicked = -1
            
        if self.backButtonToDisplay != -1:    
            self.playerSetups[self.backButtonToDisplay].backButton.mousePressed()
        
        if self.backButtonToDisplay == 2:
            self.playerSetups[3].playerAddButton.mousePressed()
            
        if self.backButtonToDisplay == -1:
            self.playerSetups[3].playerAddButton.mousePressed()
            self.playerSetups[2].playerAddButton.mousePressed()
            
        self.goButton.mousePressed()
                
        
    def drawPlayerSetupTiles(self):
        self.playerOneSetup.draw()
        self.playerTwoSetup.draw()
        self.playerThreeSetup.draw()
        self.playerFourSetup.draw()
        return
        
    def checkKeyExists(self, k):
        for i in range(len(self.playerKeybinds)):
            if self.playerKeybinds[i].content == k.upper():
                return i
        
        return -1
    
    def findBackButtonToDisplay(self):
        if self.playerThreeSetup.isPlaying == True and self.playerFourSetup.isPlaying == False:
            return 2
        elif self.playerThreeSetup.isPlaying == True and self.playerFourSetup.isPlaying == True:
            return 3
        else:
            return -1
    
    def drawBackButton(self):
        if self.backButtonToDisplay == -1: return
        self.playerSetups[self.backButtonToDisplay].drawButton()
    
    def onPlayerPress(self):
        if self.backButtonToDisplay == 3:
            self.playerSetups[3].isPlaying = False
            self.backButtonToDisplay = 2
        elif self.backButtonToDisplay == 2:
            self.playerSetups[2].isPlaying = False
            self.backButtonToDisplay = -1
            
    def onPlayerAdd(self):
        if self.backButtonToDisplay == -1:
            self.playerSetups[2].isPlaying = True
            self.backButtonToDisplay = 2
        elif self.backButtonToDisplay == 2:
            self.backButtonToDisplay = 3
            self.playerSetups[3].isPlaying = True
        
    def toCheck(self, textbox):
        if self.backButtonToDisplay == 3 or textbox.playerNumber < self.backButtonToDisplay:
            return True
        return False
    
    def onGoButtonPress(self):
        self.didClickGo = True
        
    def onFinishSetup(self):
        if self.didClickGo:
            players = []
            
            for playerSetup in self.playerSetups:
                if playerSetup.isPlaying:
                    players.append(Player(playerSetup.primaryKey, playerSetup.secondaryKey, playerSetup.playerNumber))
                    
            return players
                
        else:
            return None
    
    
        
