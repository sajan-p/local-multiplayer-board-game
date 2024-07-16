from Utility import drawBackground, hover
from Button import ButtonImage

class Page_Menu:
    def __init__(self):
        self.titleTextImage = loadImage("img/text/title.png")  
        self.playButtonImage = loadImage("img/buttons/play.png")  
        self.rulesButtonImage = loadImage("img/buttons/rules.png")
        
        self.playButton = ButtonImage(self.playButtonImage, 300, 250, self.onPlayButtonPress)
        
        self.openPlayButton = False
    
    def draw(self):
        drawBackground()
        hover(self.titleTextImage, 300, 100)
        self.drawButtons()
    
    def mouseClicked(self):      
        self.playButton.mouseClicked()
    
    def keyTyped(self):
        pass
    
    def mouseMoved(self):
        self.playButton.mouseMoved()
        
    def mouseReleased(self):
        self.playButton.mouseReleased()
        
    def mousePressed(self):
        self.playButton.mousePressed()
        
    def drawButtons(self):
        self.playButton.draw()
        
    def onPlayButtonPress(self):
        self.openPlayButton = True

        
    
    
    
        
