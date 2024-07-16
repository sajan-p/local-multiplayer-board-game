# Renders the background
def drawBackground():
    imageMode(CORNER)
    
    backgroundImage = loadImage("img/background.png")   
    image(backgroundImage, -(frameCount % 600), -(frameCount % 600))
    
# Creates hover effect on images
def hover(img, x, y, hoverDist = 5, hoverSpeed = 10, centered = True):
    if centered:
        imageMode(CENTER)
    else:
        imageMode(CORNER)
    image(img, x, y + hoverDist*sin(millis()/(10*hoverSpeed)))
