from Constants import BUTTON_PRESS_SHRINK

class Button:
    def __init__(self, x, y, w, h, onPress, colour="white"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.onPress = onPress
        self.colour = colour
        
        self.hover = False
        self.pressed = False
        
    def draw(self):
        if self.hover:
            cursor(HAND)
            tint(240, 240, 240)
            self.render()
            tint(255, 255, 255)
        else:
            cursor(ARROW)
            tint(255, 255, 255)
            self.render()
        
    # Draws Raw Component
    def render(self):
        fill(self.colour)
        rect(self.x, self.y, self.w, self.h)
        
    def checkBounds(self, mx, my):
        return mx > self.x and mx < self.x + self.w and my > self.y and my < self.y + self.h
        
    def mouseClicked(self):
        if self.checkBounds(mouseX, mouseY):
            self.onPress()
    
    def mouseMoved(self):
        if self.checkBounds(mouseX, mouseY):
            self.hover = True
        else:
            self.hover = False
            
    def mouseReleased(self):
        self.pressed = False
        
    def mousePressed(self):
        if self.checkBounds(mouseX, mouseY):
            self.pressed = True
            
            
class ButtonImage(Button):
    def __init__(self, img, x, y, onPress):
        # TODO: Change to match super
        self.w = img.width
        self.h = img.height
        self.x = x-self.w/2
        self.y = y-self.h/2
        self.img = img
        self.onPress = onPress
        
        self.hover = False
        self.pressed = False
        
    def draw(self):
        if self.pressed:
            self.w = self.img.width - self.img.width/BUTTON_PRESS_SHRINK
            self.h = self.img.height - self.img.height/BUTTON_PRESS_SHRINK
            self.x += self.img.width/2
            self.y += self.img.height/2
            
            imageMode(CENTER)
            
            tint(230, 230, 230)
            image(self.img, self.x, self.y, self.w, self.h)
            tint(255, 255, 255)
            
            self.w = self.img.width
            self.h = self.img.height
            self.x -= self.img.width/2
            self.y -= self.img.height/2
            
        else: 
            # TODO: Change to match super
            if self.hover:
                tint(240, 240, 240)
                self.render()
                tint(255, 255, 255)
            else:
                tint(255, 255, 255)
                self.render()
    
    def render(self):
        imageMode(CORNER)
        image(self.img, self.x, self.y)
        imageMode(CENTER)
        
