import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))
sceneImg = pygame.image.load("scene\scene1.jpg")

pygame.display.set_caption("Lenin Sanchez's Game")
icon = pygame.image.load("LENIN.jpg")
pygame.display.set_icon(icon)

#****Player Setup***********
playerImg = pygame.image.load("navePlayer\\navemain32.png")
playerX = 350
playerY = 490
playerX_change = 0

def player(x,y):
    screen.blit(playerImg,(x, y))

#*********Enemy Setup********************

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
enemyImg1 = pygame.image.load("enemy\enemy5.png")

for i in range(num_enemies):
    enemyImg.append(enemyImg1)
    enemyX.append(random.randint(0,700))
    enemyY.append(random.randint(10,150) +10)
    enemyX_change.append(1)
    enemyY_change.append(30)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#***********Power Setup*****************
powerImg = pygame.image.load("power1.png")
powerX = 0
powerY = 490
powerX_change = 0
powerY_change = 5
power_state = "ready"

def fire_power(x,y):
    global power_state
    power_state = "fire"
    screen.blit(powerImg,(x + 35,y + 1))

#***********Collision*************

def isCollision(enemyX,enemyY,powerX,powerY):
    distance = math.sqrt((math.pow((enemyX-powerX),2)) + (math.pow((enemyY-powerY),2)))
    if distance < 30:
        return True
    else:
        return False

#********Score Setup*************

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX =10
textY=10

def show_score(x,y):
    score = font.render(f"Your score is: {score_value}",True,(255,0,0))
    screen.blit(score,(x,y))

#**************Game Over***************

over_font = pygame.font.Font('freesansbold.ttf',64)
def game_over():
    over_text =over_font.render("GAME OVER", True,(255,255,255))
    screen.blit(over_text,(250,250))

#*************Program************************

running = True
while running:

    screen.blit(sceneImg,(0,0))
    # pygame.display.flip()
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
                
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            
            if event.key == pygame.K_SPACE:
                if power_state is "ready":
                    powerX = playerX
                    fire_power(powerX,powerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

#***********Movement mechanism of Player****************
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 700:
        playerX = 700

#***********Movement mechanism of enemies**************
    for i in range(num_enemies):
        
        #game over
        if enemyY[i] > 250:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            break
    
        enemyX[i] += enemyX_change[i]
    
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 700:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],powerX,powerY)
        if collision:
            powerY = 490
            power_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,700)
            enemyY[i] = random.randint(10,150)
        enemy(enemyX[i], enemyY[i],i)


#***********Movement mechanism of Power************  
#       
    if powerY <= 0:
        powerY = 490
        power_state = "ready"
    if power_state is "fire":
        fire_power(powerX, powerY)
        powerY-= powerY_change

    player(playerX,playerY)
    show_score(textX,textY)    
    pygame.display.update()