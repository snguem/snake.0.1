import pygame, sys
from pygame.locals import *
from random import randint


pygame.init()

class FOOD:
    def __init__(self, size:dict, x:int, y:int, eyes:bool=False) -> None:
        self.x=x
        self.y=y
        self.w=size["w"]
        self.h=size["h"]
        self.eyes=eyes
        self.move()
        self.get_rect()
    
    def move(self):
        global all_tiles
        while True:
            tile=all_tiles[randint(0,len(all_tiles)-1)]
            if tile["x"]%self.w==0 or tile["y"]%self.h==0:
                self.x=tile["x"]
                self.y=tile["y"]
                break
    
    def draw(self, surface:pygame.Surface,color:tuple=(0,255,0)):
        self.get_rect()
        pygame.draw.rect(surface,color,(self.x,self.y,self.w,self.h))
    
    def get_rect(self):
        self.food_rect=pygame.Rect(self.x,self.y,self.w,self.h)
        
        

class CUBE:
    def __init__(self, size:dict, x:int, y:int, color:tuple,eyes:bool=False) -> None:
        self.x=x
        self.y=y
        self.w=size["w"]
        self.h=size["h"]
        self.eyes=eyes
        self.color=color
    
    def move(self,x,y):
        self.x=x
        self.y=y
    
    def draw(self, surface:pygame.Surface):
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.w,self.h))
        if self.eyes:
            pygame.draw.circle(surface,(0,0,0),(self.x+4,self.y+8),4)
            pygame.draw.circle(surface,(0,0,0),(self.x+16,self.y+8),4)

    def rect(self):
        return {"w":self.w,"h":self.h,"x":self.x,"y":self.y}

class SNAKE:
    def __init__(self,w:int,h:int,x,y) -> None:
        # global snake_surface
        self.body=[]
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        # self.speed=2
        self.moving={"x":1,"y":0}
        self.pas={"x":w,"y":h}
        self.add(True)
        self.add()
        self.add()
        
    def add(self,eyes:bool=False):
        if len(self.body)>=1:
            pos=self.body[-1].rect()
            if self.moving=={"x":1,"y":0}:
                x=pos["x"]-self.pas["x"]
                y=pos["y"]
            elif self.moving=={"x":-1,"y":0}:
                x=pos["x"]+self.pas["x"]
                y=pos["y"]
            elif self.moving=={"x":0,"y":1}:
                x=pos["x"]
                y=pos["y"]-self.pas["y"]
            elif self.moving=={"x":0,"y":-1}:
                x=pos["x"]
                y=pos["y"]+self.pas["y"]
        else:
            x=self.x
            y=self.y
        self.body.append(CUBE({"w":self.w,"h":self.h},x,y,(randint(0,255),randint(0,255),randint(0,255)),eyes))
        
    def move(self):
        global snake_surface
        last_cube=None
        for i,cube in enumerate(self.body):
            if(i==0):
                self.x+=self.moving["x"]*self.pas["x"]
                self.y+=self.moving["y"]*self.pas["y"]
                x=self.x
                y=self.y
            else:
                if self.moving=={"x":1,"y":0}:
                    x=last_cube["x"]
                    y=last_cube["y"]
                elif self.moving=={"x":-1,"y":0}:
                    x=last_cube["x"]
                    y=last_cube["y"]
                elif self.moving=={"x":0,"y":1}:
                    x=last_cube["x"]
                    y=last_cube["y"]
                elif self.moving=={"x":0,"y":-1}:
                    x=last_cube["x"]
                    y=last_cube["y"]
                
            last_cube=self.body[i].rect()
                
            cube.move(x,y)
            
    def collide(self, surface:pygame.Surface) -> bool:
        head=self.body[0]
        head_rect=pygame.Rect(head.x,head.y,head.w,head.h)
        if head_rect.collidepoint(surface.get_rect().w,head_rect.y) and self.moving["x"]==1:
            return False
        elif head_rect.collidepoint(-self.pas["x"],head_rect.y) and self.moving["x"]==-1:
            return False
        if head_rect.collidepoint(head_rect.x,surface.get_rect().h) and self.moving["y"]==1:
            return False
        elif head_rect.collidepoint(head_rect.x,-self.pas["y"]) and self.moving["y"]==-1:
            return False
        return True
    
    def eat(self, food:FOOD):
        head=self.body[0]
        head_rect=pygame.Rect(head.x,head.y,head.w,head.h)
        if head_rect.colliderect(food.food_rect):
            # self.moving={"x":0,"y":0}
            food.move()
            self.add()
    
    def draw(self):
        global snake_surface
        for cube in self.body:
            cube.draw(snake_surface)
    
def make_snake_are(surface:pygame.Surface):
    global width, height, all_tiles
    # print(surface.get_rect().width, height)
    x,y=0,0
    for i in range(height):
        for j in range(width):
            pygame.draw.rect(surface,(255,255,0),(x,y,width,height),1)
            all_tiles.append({"x":x,"y":y})
            x+=width
        x=0
        y+=height

# clock=pygame
screen=pygame.display.set_mode((600,500)) # initialisation de l'ecran principale

snake_surface=pygame.Surface((400,400))
# 
all_tiles=[]
# 
carreaux_w=20
carreaux_h=20
width=snake_surface.get_rect().width//carreaux_w
height=snake_surface.get_rect().height//carreaux_h
make_snake_are(snake_surface)
# 
snake=SNAKE(width,height,0,0)
food=FOOD({"w":width,"h":height},40,40)
food.move()

running=True # initialisation de la cle du jeu, c'est cette variable qui permet de maintenir le jeu
tick=8
increase=False
while running:
    # clock
    # print("test")
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
        elif event.type == KEYDOWN:
            # print("ok",event,K_DOWN,event.type == K_DOWN)
            if event.key == K_DOWN:
                snake.moving={"x":0,"y":1}
            elif event.key == K_UP:
                snake.moving={"x":0,"y":-1}
            elif event.key == K_LEFT:
                snake.moving={"x":-1,"y":0}
            elif event.key == K_RIGHT:
                snake.moving={"x":1,"y":0}
    screen.fill("gray")
    # pygame.draw.rect(screen, (0,0,0), (100 ,150 ,70 ,30) , 0)
    snake_surface.fill((0,0,0))
    snake.draw()
    food.draw(snake_surface,(0,255,0))
    snake.move()
    snake.eat(food)
    running=snake.collide(snake_surface)
    screen.blit(snake_surface,(100,50))
    police = pygame . font . SysFont ('Arial', 20 , bold = True ) 
    texte = police . render (f"Score: {len(snake.body)-3}", True , (0 ,128 ,0) )
    screen.blit (texte , (200 ,0))
    
    # if((len(snake.body)-1)%10==0 and not increase and len(snake.body)-1>0):
    #     tick+=5
    #     increase=True
    # elif(len(snake.body)%10!=0 and increase):
    #     increase=False
        
    pygame.display.flip()
    pygame.time.Clock().tick(tick)

pygame.quit()

