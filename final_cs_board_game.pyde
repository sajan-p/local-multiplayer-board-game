from Page_Menu import Page_Menu
from Page_Setup import Page_Setup
from Page_Game import Page_Game

def setup():
    global state, pageMenu, pageSetup, pageGame, players 
    
    # General styling setup
    size(600, 600)
    noStroke()
    
    # Font setup
    f = createFont("BaiJamjuree-Bold.ttf", 100)
    textFont(f)
    frameRate(60)
    
    state = "M" # M = Menu, S = Setup, G = Game
    
    # Creates objects for pages
    pageMenu = Page_Menu()
    pageSetup = Page_Setup()
    pageGame = Page_Game()
    
    players = []
    
def draw():
    global state
    clear()
    
    if state == "M":
        pageMenu.draw()
        
        if pageMenu.openPlayButton:
            state = "S"
 

    if state == "S":
        pageSetup.draw()    
        
        if pageSetup.onFinishSetup() != None:
            players = pageSetup.onFinishSetup()
            pageGame.getPlayers(players)
            state = "G"        
            
    if state == "G":
        pageGame.draw()   
        
        if pageGame.resetGame:
            state = "M"
            pageMenu.openPlayButton = False
            pageSetup.didClickGo = False


def mouseClicked():
    if state == "M":
        pageMenu.mouseClicked()
    elif state == "S":
        pageSetup.mouseClicked()
    elif state == "G":
        pageGame.mouseClicked()
        
def mouseReleased():
    if state == "M":
        pageMenu.mouseReleased()
    elif state == "S":
        pageSetup.mouseReleased()
    elif state == "G":
        pageGame.mouseReleased()
        
def mousePressed():
    if state == "M":
        pageMenu.mousePressed()
    elif state == "S":
        pageSetup.mousePressed()
    elif state == "G":
        pageGame.mousePressed()
        
def mouseMoved():
    if state == "M":
        pageMenu.mouseMoved()
    elif state == "S":
        pageSetup.mouseMoved()
    elif state == "G":
        pageGame.mouseMoved()
        
def keyTyped():
    if state == "M":
        pageMenu.keyTyped()
    elif state == "S":
        pageSetup.keyTyped()
    elif state == "G":
        pageGame.keyTyped()
