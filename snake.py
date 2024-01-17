import pygame, sys
from pygame.locals import *
from random import randint
import json



# initialisation des elements de pygame
pygame.init()
# -----------------------------------------------------
# fonction technique
def get_(file:str, key:str=None):
    with open(file, "r") as f:
        dts=json.load(f)
    
    return dts[key] if key!=None else dts

def insert_(file:str, value, key:str=None):
    dts=get_(file)
    dts[key]=value
    with open(file, "w") as f:
        json.dump(dts,f)
    
    return dts[key] if key!=None else dts
# -----------------------------------------------------

# 
class FOOD(pygame.sprite.Sprite):
    def __init__(self, rect:tuple) -> None:
        self.food_rect=pygame.Rect(rect[0],rect[1],rect[2],rect[3])
    
    def move(self, all_tiles:list):
        tile=all_tiles[randint(0,len(all_tiles)-1)] # on selectionne la prochaine position dans la liste des position
        # on positionne 
        self.food_rect.x=tile["x"]
        self.food_rect.y=tile["y"]
    
    def draw(self, surface:pygame.Surface,color:tuple=(255,0,0)):
        # on affiche le repas sur la surface
        pygame.draw.circle(surface, color, (self.food_rect.x+self.food_rect.w/2,self.food_rect.y+self.food_rect.h/2), self.food_rect.w/2)  # (surface, color, center, radius)

# 
class CUBE(pygame.sprite.Sprite):
    def __init__(self, rect:tuple, color:tuple,eyes:bool=False) -> None:
        super().__init__()
        self.x,self.y=rect[0],rect[1] # position initiale
        self.w,self.h=rect[2],rect[3] # dimansion du cube
        self.eyes=eyes                # est ce que c'est la cube actuel est la tete?
        self.color=color              # couleur du cube
    
    def move(self,x:int,y:int):
        self.x,self.y=x,y # mise a jour de la nouvelle position du cube
    
    def draw(self, surface:pygame.Surface):
        # affichage du cube
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.w,self.h))
        if self.eyes:
            # affichage des yeux si le cube represente la tete
            pygame.draw.circle(surface,(0,0,0),(self.x+4,self.y+8),4)
            pygame.draw.circle(surface,(0,0,0),(self.x+self.w-4,self.y+8),4)

    def rect(self):
        # on recupere le rectangle correspondant au cube (c'est un truc de pygame) :')
        return pygame.Rect(self.x,self.y,self.w,self.h)

# 
class SNAKE:
    def __init__(self,rect:tuple):
        self.body=[] # la liste des cubes qui forme le corps
        self.x_init,self.y_init=rect[0],rect[1] # on initialise la position du snake(ici on fait reference a la tete, le reste du corps sera aligne selon la tete)
        self.w,self.h=rect[2],rect[3]           # dimension des cube
        self.moving={"x":1,"y":0}               # la direction de la tete
        self.pas={"x":rect[2],"y":rect[3]}      # marge de deplacement en x et en y
        self.eating=False                       # est ce que le snake se mange lui meme?
        
        # formation du corps
        self.add(True,(0,155,0))                # ajout de la tete
        self.add()                              # part 1
        self.add()                              # part 2
        
    def add(self,eyes:bool=False, color:tuple=(0,255,0)):
        if len(self.body)>=1:
            last_cube_rect=self.body[-1].rect()                  # on recupere le rectangle du dernier cube 
            # on ajoute le prochain cube en fonction du send de la tete et de la position du dernier cube
            if self.moving=={"x":1,"y":0}:
                x=last_cube_rect.x-self.pas["x"]
                y=last_cube_rect.y
            elif self.moving=={"x":-1,"y":0}:
                x=last_cube_rect.x+self.pas["x"]
                y=last_cube_rect.y
            elif self.moving=={"x":0,"y":1}:
                x=last_cube_rect.x
                y=last_cube_rect.y-self.pas["y"]
            elif self.moving=={"x":0,"y":-1}:
                x=last_cube_rect.x
                y=last_cube_rect.y+self.pas["y"]
        else:
            x,y=self.x_init,self.y_init                          # position de la tete
        self.body.append(CUBE((x,y,self.w,self.h),color,eyes))
       
    def move(self):
        if not self.eating:                                         # s'il ne se mange pas
            for i,cube in enumerate(self.body):
                    if(i==0):                                           # si le cube actuel represente la tete
                        self.x_init+=self.moving["x"]*self.pas["x"]
                        self.y_init+=self.moving["y"]*self.pas["y"]
                        x=self.x_init
                        y=self.y_init
                    else:                                               # si le cube actuel represente une partie du corps
                        x=last_cube.x
                        y=last_cube.y
                        if self.moving=={"x":0,"y":0}:
                            last_cube=self.body[i].rect()
                            x=last_cube.x
                            y=last_cube.y
                    
                    last_cube=self.body[i].rect()                       # on sauvegarde les coordonnees du cube actuelle pour les attribuer au cube prochain
                    cube.move(x,y)                                      # on deplace le cube actuel
                   
    def snake_collide_surface(self, surface:pygame.Surface) -> bool:
        head_rect=self.body[0].rect()
        if head_rect.collidepoint(surface.get_rect().w,head_rect.y) and self.moving["x"]==1:            # est ce le snake croise croise le mur droit?
            return True
        elif head_rect.collidepoint(-self.pas["x"],head_rect.y) and self.moving["x"]==-1:               # est ce le snake croise croise le mur gauche?
            return True
        if head_rect.collidepoint(head_rect.x,surface.get_rect().h) and self.moving["y"]==1:            # est ce le snake croise croise le mur du haut?
            return True
        elif head_rect.collidepoint(head_rect.x,-self.pas["y"]) and self.moving["y"]==-1:               # est ce le snake croise croise le mur du bas?
            return True
        return False
    
    def draw(self,surface:pygame.surface):
        for cube in self.body:
            cube.draw(surface)                    # on affiche les cube de la liste
    
    def eating_myself(self):
        head_rect=self.body[0].rect()
        self.eating=[True for i,cube in enumerate(self.body) if head_rect.colliderect(cube.rect()) and i>0]
        self.eating=True if len(self.eating)>0 else False

    def directions(self):
        key_press=pygame.key.get_pressed()                                            # on recupere la liste des bouttons qui ont ete presses
        # on definit les prochaines direction x et y
        if key_press[K_DOWN]:
            self.moving={"x":0,"y":1} if self.moving["y"]!=-1 else self.moving
        elif key_press[K_UP]:
            self.moving={"x":0,"y":-1} if self.moving["y"]!=1 else self.moving
        elif key_press[K_LEFT]:
            self.moving={"x":-1,"y":0} if self.moving["x"]!=1 else self.moving
        elif key_press[K_RIGHT]:
            self.moving={"x":1,"y":0} if self.moving["x"]!=-1 else self.moving

# 
class GAME:
    def __init__(self) -> None:
        self.ecran=pygame.display.set_mode((700,500))                       # initialisation de l'ecran principale
        self.surface=pygame.Surface((400,400))                              # initialisation de la surface de jeu
        self.all_tiles=[]                                                   # initialisation de la liste des positions
        self.carreaux_w,self.carreaux_h=25,25                               # dimension des carreux et pas du snake
        self.run_game=True                                                  # est ce le jeu doit etre actif?
    
    def dessiner_terrain(self):
        self.all_tiles=[]                                                   # initialisation de la liste des positions
        for i in range(self.surface.get_rect().height//self.carreaux_h):
            for j in range(self.surface.get_rect().width//self.carreaux_w):
                pygame.draw.rect(self.surface,(0,255,0),(self.carreaux_w*j,self.carreaux_h*i,self.carreaux_w,self.carreaux_h),1)
                self.all_tiles.append({"x":self.carreaux_w*j,"y":self.carreaux_h*i})    # on rempli la liste des position
    
    def initialisation(self):
        # initialisation du snake et food
        self.snake=SNAKE((self.carreaux_w*2,0,self.carreaux_w,self.carreaux_h))
        self.food=FOOD((self.carreaux_w,self.carreaux_h,self.carreaux_w,self.carreaux_h))
    
    def is_snake_eat_food(self):
        snake_head=self.snake.body[0].rect()
        if snake_head.colliderect(self.food.food_rect):
            self.snake.add()
            while True:
                self.food.move(self.all_tiles)
                if len([1 for body in self.snake.body if body.rect().colliderect(self.food.food_rect)])==0:      # on verifie si la position de food est celle de l'un des cubes de snake
                    break
    
    def game_over(self):
        police = pygame.font.SysFont ('Arial', 40 , bold = True ) 
        texte = police.render("Game Over", True , (255 ,255 ,255) )
        
        pygame.draw.rect(self.surface, (255 ,0 ,0),(0,(self.surface.get_rect().h/2)-50,self.surface.get_rect().w,60))
        self.surface.blit (texte , (115 ,(self.surface.get_rect().h/2)-45))
    
    def options(self):
        police = pygame.font.SysFont ('Arial', 20 , bold = True ) 
        # textes
        texte_start = police.render(f"Reset", True , (255 ,255 ,255) )
        texte_pause = police.render(f"Pause", True , (255 ,255 ,255) )
        texte_play = police.render(f"Play", True , (255 ,255 ,255) )
        
        # rects
        pygame.draw.rect(self.ecran, (255 ,0 ,0),self.button_start)
        pygame.draw.rect(self.ecran, (255 ,0 ,0),self.button_pause)
        pygame.draw.rect(self.ecran, (255 ,0 ,0),self.button_play)
        
        # affichages des textes
        self.ecran.blit (texte_start , (105 ,100))
        self.ecran.blit (texte_pause , (100 ,150))
        self.ecran.blit (texte_play , (110 ,200))
    
    def compte_a_rebours(self):
        police = pygame.font.SysFont ('Arial', 40 , bold = True ) 
        texte = police.render(f"{self.compteur}", True , (255 ,255 ,255) )
        if self.compteur>0 and self.play:
            pygame.draw.rect(self.surface, (255 ,0 ,0),(0,(self.surface.get_rect().h/2)-50,self.surface.get_rect().w,60))
            self.surface.blit (texte , (185 ,(self.surface.get_rect().h/2)-40))
            self.compteur-=1
    
    def gaming(self):
        self.food.move(self.all_tiles)
        tick=8                                                      # vitesse du jeu
        self.compteur=3                                             # compte a rebours
        score_last=get_("score.json","score")                       # on recupere le meilleur score
        # rectangles des different boutton
        self.button_start = pygame.Rect(50, 100, 150, 30)
        self.button_pause = pygame.Rect(50, 150, 150, 30)
        self.button_play = pygame.Rect(50, 200, 150, 30)
        # 
        self.is_game_over=False                                      # est ce qu'il a perdu?
        self.play=False                                             # est ce que le jeu est en pause?
        while self.run_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run_game=False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_pause.collidepoint(event.pos):
                        self.play=False
                        self.compteur=3
                    elif self.button_play.collidepoint(event.pos):
                        if not self.is_game_over:
                            self.play=True
                            tick=2
                    elif self.button_start.collidepoint(event.pos):
                        self.initialisation()
                        self.food.move(self.all_tiles)
                        self.play=False
                        self.compteur=3

            # mise a jour de l'arriere plan
            self.ecran.fill("black")
            self.surface.fill("black")
            # affichage du terrin
            self.dessiner_terrain()
            # 
            
            self.is_game_over=self.snake.snake_collide_surface(self.surface)
            # 
            if not self.is_game_over and not self.snake.eating:
                if self.compteur>0 and self.play:
                    self.compte_a_rebours()
                    self.snake.draw(self.surface)
                    self.food.draw(self.surface)
                else:
                    tick=8
                    self.snake.eating_myself()
                    if not self.snake.eating and self.play:
                        self.snake.directions()
                        self.snake.move()
                        
                        self.is_snake_eat_food()
                
                    self.snake.draw(self.surface)
                    self.food.draw(self.surface)
                    
            else:
                if get_("score.json","score")<len(self.snake.body)-3:
                    insert_("score.json",len(self.snake.body)-3,"score")
                    score_last=get_("score.json","score")
                self.play=False
                self.game_over()
                tick=1
                
            
            # 
            self.options()
            # 
            police = pygame.font.SysFont ('Arial', 20 , bold = True ) 
            texte = police.render(f"Best score: {score_last}", True , (0 ,128 ,0) )
            self.ecran.blit (texte , (250 ,20))
            
            texte = police.render(f"Score: {len(self.snake.body)-3}", True , (0 ,128 ,0) )
            self.ecran.blit (texte , (170+self.surface.get_rect().w ,20))
            self.ecran.blit(self.surface,(250,50))
            
            pygame.display.flip()
            pygame.time.Clock().tick(tick)

        pygame.quit()

    
# 

if __name__=="__main__":
    game=GAME()
    game.dessiner_terrain()
    game.initialisation()
    game.gaming()
    