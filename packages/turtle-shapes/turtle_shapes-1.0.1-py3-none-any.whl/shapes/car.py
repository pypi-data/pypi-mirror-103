from shapes import circle, rectangle
import turtle
class Car:
    def __init__(self,hoodLength, hoodWidth, bodyLength, bodyWidth, bodyPenColor, bodyFillColor, hoodPenColor, hoodFillColor, wheelPenColor, wheelFillColor,wheelRadius):
        self.body = rectangle.Rectangle(bodyLength, bodyWidth, bodyPenColor, bodyFillColor)
        self.hood = rectangle.Rectangle(hoodLength, hoodWidth, hoodPenColor, hoodFillColor)
        self.wheel1 = circle.Circle(wheelPenColor, wheelFillColor)
        self.wheel2 = circle.Circle(wheelPenColor, wheelFillColor)
        self.wheelRadius = wheelRadius

    def draw(self, x, y):
        self.body.draw(x, y)
        # t.penup()
        # t.left(90)
        # t.forward(self.body.length)
        # t.left(90)
        # t.forward(self.body.width/2)
        # t.pendown()
        self.hood.draw(x-(self.body.width/2)+(self.hood.width/2), y+self.body.length)
        self.wheel1.draw(x,y-self.wheelRadius,self.wheelRadius)
        self.wheel2.draw(x-(self.body.width-2*self.wheelRadius), y-self.wheelRadius, self.wheelRadius)

if __name__ == "__main__":
    car = Car(20,50,30,100,(1,0,0),(1,0,0), (0,1,0), (0,0,1),(0,0,0), (0,0,0),10)
    car.draw(40,40)
    car.draw(-80, -10)
    turtle.mainloop()