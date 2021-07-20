import pygame
from math import sqrt, atan2, sin, cos, pi,floor
import serial
# --- constants --- (UPPER_CASE names)

def padding(number):
    number=str(int(floor(number)))
    while len(number)<3:
        number='0'+number
    return number

SCREEN_WIDTH = 600
SCREEN_HEIGHT =350
d = 100
#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE   = (0,   0,   125)
BLACK = (0,0,0)
GREY = (125,125,125)
CLEAR_GREY = (200,200,200)
VERY_CLEAR_GREY = (230,230,230)
FPS = 30

arduino = '/dev/ttyUSB0'
TOUT = 100
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Robot Arm Manual Control Interface")

rectangle = pygame.rect.Rect(300, 180, 30, 30)
rectangle_draging = False
rectangle2 = pygame.rect.Rect(400, 180, 30, 30)
rectangle2_draging = False
rectangle3 = pygame.rect.Rect(300, 300, 30, 30)
rectangle4 = pygame.rect.Rect(85, 85, 30, 30)
rectangle5 = pygame.rect.Rect(85, 5, 30, 30)
rectangle5_draging = False
rectangle6 = pygame.rect.Rect(550, 30, 30, 30)
rectangle6_draging = False
rectangle7 = pygame.rect.Rect(255, 10, 120, 35)
rectangle7_draging = False
rectangle8 = pygame.rect.Rect(18,100, 200, 85)
rectangle9 = pygame.rect.Rect(10,180, 200, 150)


font=pygame.font.Font(None,30)
base=font.render("Base", 1,(0,0,0))
skelleton=font.render("Arm Joints", 1,(0,0,0))
manipulator=font.render("Manipulator", 1,(0,0,0))
closed=font.render("Closed -", 1,(0,0,0))
open=font.render("Open -", 1,(0,0,0))
send=font.render("SEND", 1,(255,255,255))

theta0 = 90
theta1 = 90
theta2 = 18
theta3 = 45

texServos=font.render("Servo Command: ", 1,(0,0,0))
texTheta0=font.render("Theta 0: "+str(theta0), 1,(0,0,0))
texTheta1=font.render("Theta 1: "+str(theta1), 1,(0,0,0))
texTheta2=font.render("Theta 2: "+str(theta2), 1,(0,0,0))
texTheta3=font.render("Theta 3: "+str(theta3), 1,(0,0,0))

device = False

try:
    Port = serial.Serial(arduino, 9600, timeout = TOUT)
    print("Arduino Connected")
    device = True
except:
    print("Couldn't connect to Arduino")
    Port = None

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

                elif rectangle2.collidepoint(event.pos):
                    rectangle2_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle2.x - mouse_x
                    offset_y = rectangle2.y - mouse_y

                elif rectangle5.collidepoint(event.pos):
                    rectangle5_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle5.x - mouse_x
                    offset_y = rectangle5.y - mouse_y

                elif rectangle6.collidepoint(event.pos):
                    rectangle6_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle6.x - mouse_x
                    offset_y = rectangle6.y - mouse_y

                elif rectangle7.collidepoint(event.pos):
                    rectangle7_draging = True

                    if not device:
                        try:
                            Port = serial.Serial(arduino, 9600, timeout = TOUT)
                            print("Arduino Connected")
                            device = True
                        except:
                            print("No Arduino Device")
                            device = False
                    else:
                        try:
                            command = padding(int(theta0))+','+padding(int(theta1))+','+padding(int(theta2))+','+padding(theta3)+'a'
                            print("Data sent: "+command[:-1])
                            #Port.write(command.encode()) #para python 3
                            Port.write(command) #para python 2.7
                            message = Port.readline()
                            print(message)
                        except:
                            print("Couldn't send data")


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False
                rectangle2_draging = False
                rectangle5_draging = False
                rectangle6_draging = False
                rectangle7_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                nextX = mouse_x + offset_x
                nextY = mouse_y + offset_y
                dAngle = atan2(nextX-rectangle3.x,nextY-rectangle3.y)
                nextY = rectangle3.y+ 1.2*d*cos(dAngle)
                nextX = rectangle3.x+ 1.2*d*sin(dAngle)
                dY = nextY-rectangle.y
                dX = nextX-rectangle.x
                if rectangle3.y >= rectangle2.y+dY and rectangle3.y >= nextY:
                    rectangle.y = nextY
                    rectangle.x = nextX
                    rectangle2.y = rectangle2.y+dY
                    rectangle2.x = rectangle2.x+dX
                    theta1 = int(floor(dAngle*180/pi))
                    if theta1>=0:
                        theta1-=90
                    else:
                        theta1+=270
                    texTheta1=font.render("Theta 1: "+str(theta1), 1,(0,0,0))
            elif rectangle2_draging:
                mouse_x, mouse_y = event.pos
                nextX = mouse_x + offset_x
                nextY = mouse_y + offset_y
                dAngle = atan2(nextX-rectangle.x,nextY-rectangle.y)

                nextY = rectangle.y+ d*cos(dAngle)
                nextX = rectangle.x+ d*sin(dAngle)
                dY = nextY-rectangle2.y
                dX = nextX-rectangle2.x

                if rectangle3.y >= rectangle2.y+dY:
                    theta2 = int(floor(dAngle*180.0/pi))
                    theta2 = int(floor(90.0/114.0*theta2+90.0))
                    if theta2>=90 and theta2<=180:
                        rectangle2.y = nextY
                        rectangle2.x = nextX
                    #if theta2>180:
                    #    theta2=180
                    #    nextY = rectangle.y+ d
                    #    nextX = rectangle.x+ d
                    #    rectangle2.y = nextY
                    #    rectangle2.x = nextX
                    #elif theta2<90:
                    #    theta2=90
                    #    if rectangle.y+100 <= rectangle3.y:
                    #        rectangle2.y = rectangle.y+100
                    #        rectangle2.x = rectangle.x
                    else:
                        if theta2<90:
                            theta2 =90
                        else:
                            theta2 = 180
#                    rectangle2.y = nextY
#                    rectangle2.x = nextX
                    texTheta2=font.render("Theta 2: "+str(theta2), 1,(0,0,0))
            elif rectangle5_draging:
                mouse_x, mouse_y = event.pos
                nextX = mouse_x + offset_x
                nextY = mouse_y + offset_y
                dAngle = atan2(nextX-rectangle4.x,nextY-rectangle4.y)
                nextY = rectangle4.y+ 80*cos(dAngle)
                nextX = rectangle4.x+ 80*sin(dAngle)
                if nextY <= rectangle4.y:
                    theta0 = floor(dAngle*180/pi)
                    if theta0<0:
                        theta0+=270
                    else:
                        theta0-=90
                    rectangle5.y = nextY
                    rectangle5.x = nextX
                texTheta0=font.render("Theta 0: "+str(theta0), 1,(0,0,0))
            elif rectangle6_draging:
                mouse_x, mouse_y = event.pos
                nextY = mouse_y + offset_y
                if nextY>=31 and nextY<=181:
                    rectangle6.y = nextY
                    #theta3 = rectangle6.y*45/150+36 #0 a 180
                    theta3 = int(floor(rectangle6.y*180/150-37)) #0 a 180
                    texTheta3=font.render("Theta 3: "+str(theta3), 1,(0,0,0))
    # - updates (without draws) -

    # empty

    # - draws (without updates) -




    screen.fill(VERY_CLEAR_GREY)

    pygame.draw.circle(screen, RED, (100,100), 80,5)

    pygame.draw.rect(screen, VERY_CLEAR_GREY, rectangle8)
    pygame.draw.line(screen, RED, (20,100), (180,100), 5)

    pygame.draw.line(screen, BLACK, (rectangle.x+15,rectangle.y+15), (rectangle2.x+15,rectangle2.y+15), 5)
    pygame.draw.line(screen, BLACK, (rectangle.x+15,rectangle.y+15), (rectangle3.x+15,rectangle3.y+15), 5)
    pygame.draw.line(screen, BLACK, (rectangle4.x+15,rectangle4.y+15), (rectangle5.x+15,rectangle5.y+15), 5)
    pygame.draw.line(screen, BLACK, (565,30), (565,212), 5)

    if (rectangle_draging):
        pygame.draw.rect(screen, RED, rectangle)
    else:
        pygame.draw.rect(screen, BLUE, rectangle)

    if (rectangle2_draging):
        pygame.draw.rect(screen, RED, rectangle2)
    else:
        pygame.draw.rect(screen, BLUE, rectangle2)

    pygame.draw.rect(screen, BLUE, rectangle3)
    pygame.draw.rect(screen, BLUE, rectangle4)

    if (rectangle5_draging):
        pygame.draw.rect(screen, RED, rectangle5)
    else:
        pygame.draw.rect(screen, BLUE, rectangle5)

    if (rectangle6_draging):
        pygame.draw.rect(screen, CLEAR_GREY, rectangle6)
    else:
        pygame.draw.rect(screen, GREY, rectangle6)

    if (rectangle7_draging):
        pygame.draw.rect(screen, GREY, rectangle7)
    else:
        pygame.draw.rect(screen, CLEAR_GREY, rectangle7)

    pygame.draw.rect(screen, WHITE, rectangle9)

    screen.blit(base, (75, 120))
    screen.blit(skelleton, (260, 330))
    screen.blit(manipulator, (480, 5))
    screen.blit(closed, (460, 35))
    screen.blit(open, (470, 185))
    screen.blit(send,(290, 18))
    screen.blit(texServos, (20, 190))
    screen.blit(texTheta0, (40, 220))
    screen.blit(texTheta1, (40, 250))
    screen.blit(texTheta2, (40, 280))
    screen.blit(texTheta3, (40, 310))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
