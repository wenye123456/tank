import pygame
import time
import random
from pygame.sprite import Sprite

SCREEN_HEIGHT=512
SCREEN_WIDTH=800
TANK_HEIGHT=16
TANK_WIDTH=16

BG_COLOR=pygame.Color(0,0,0)

class BaseItem(Sprite):
  def __init__(self,color,width,height):
    pygame.sprite.Sprite.__init__(self)
  

class MainGame():
  window=None
  font=None
  my_tank=None
  def __init__(self):
    MainGame.Width=50
    MainGame.Height=32
    MainGame.enemycount=5
    MainGame.gamemap=[]
    MainGame.enemytanklist=[]
    MainGame.mybulletlist=[]
    MainGame.enemybulletlist=[]
    MainGame.explodelist=[]
    MainGame.walllist=[]
    MainGame.Music=Music()
    pass
  def StartGame(self):
    pygame.display.init()
    MainGame.window=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("坦克大战")
    
    
    self.TextInit()
    MainGame.Music.PlayExplode()
    MainGame.gamemap=self.createMap()
    MainGame.my_tank=MyTank(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    self.createEnemyTank()
    self.createWall()
    
    while True:
      starttime=time.time()
      MainGame.window.fill(BG_COLOR)
      
      self.EventHandle()
      
      MainGame.my_tank.Move()
      self.blitEnemyTank()
      self.blitBullet()
      self.blitEnemyBullet()
      self.blitExplode()
      self.blitWall()
      MainGame.my_tank.Display()
      MainGame.window.blit(self.GetTextSurface("point:"),(0,0))
      MainGame.window.blit(self.GetTextSurface("heath:{0}".format(MainGame.my_tank.heath)),(0,20))
      pygame.display.update()
      

      
      endtime=time.time()
      flashtime=endtime-starttime
      #print(flashtime)
      if flashtime<1/60:
        time.sleep(1/60-flashtime)
        
      
      
  def EndGame(self):
    pygame.quit()
    print("退出")
    exit()

  def EventHandle(self):
    eventlist=pygame.event.get()
    for event in eventlist:
      if event.type==pygame.QUIT:
        self.EndGame()
      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_a:
          MainGame.my_tank.direction='L'


          pass
        elif event.key==pygame.K_w:
          MainGame.my_tank.direction='U'


          pass
        elif event.key==pygame.K_s:
          MainGame.my_tank.direction='D'


          pass
        elif event.key==pygame.K_d:
          MainGame.my_tank.direction='R'

          pass
        if event.key==pygame.K_0:
          MainGame.my_tank.Revive()
          pass
        if event.key==pygame.K_1:
          MainGame.my_tank.heath-=1
          pass
        if event.key==pygame.K_SPACE:
          if len(MainGame.mybulletlist)<4:
            MainGame.mybulletlist.append(Bullet(MainGame.my_tank))
          
          pass
      if event.type==pygame.KEYUP:
        if event.key==pygame.K_a:
          MainGame.my_tank.direction='L'
          MainGame.my_tank.stop=True

          pass
        elif event.key==pygame.K_w:
          MainGame.my_tank.direction='U'
          MainGame.my_tank.stop=True

          pass
        elif event.key==pygame.K_s:
          MainGame.my_tank.direction='D'
          MainGame.my_tank.stop=True

          pass
        elif event.key==pygame.K_d:
          MainGame.my_tank.direction='R'
          MainGame.my_tank.stop=True

          pass
  def TextInit(self):
    pygame.font.init()
    #print(pygame.font.get_fonts())
    self.font=pygame.font.SysFont('dengxian',18)
    
  def GetTextSurface(self,Text):
    text_surface=self.font.render(Text,True,pygame.Color(255,255,255))
    return text_surface
    pass
  def createEnemyTank(self):
    top=100
    for i in range(MainGame.enemycount):
      left=random.randint(0,SCREEN_WIDTH)
      speed=random.randint(1,3)
      MainGame.enemytanklist.append(EnemyTank(left,top,speed))
  def createMap(self):

    gamemap=[[0]*MainGame.Height for i in range(MainGame.Width)]
    
    for i in range(MainGame.Width):
      for j in range(MainGame.Height):
        if i==0 or j==0 or i==MainGame.Width-1 or j==MainGame.Height-1:
          gamemap[i][j]=1
        if j==10:
          gamemap[i][j]=1
    gamemap[25][10]=0
    gamemap[24][10]=0
    gamemap[26][10]=0




    return gamemap
  def createWall(self):
    #50*32 16
    for i in range(MainGame.Width):
      for j in range(MainGame.Height):
        if MainGame.gamemap[i][j]==1:
          wall=Wall(i*16,j*16)
          MainGame.walllist.append(wall)
          
      

      
  def blitEnemyTank(self):
    for tank in self.enemytanklist:
      if tank.live==False:
        self.enemytanklist.remove(tank)
        continue
      tank.Move()
      tank.Display()
      bullet_temp=tank.Shot()
      if bullet_temp!=None:
        MainGame.enemybulletlist.append(bullet_temp)
  def blitBullet(self):
    for bullet in MainGame.mybulletlist:
      if bullet.live==True:
        bullet.DisplayBullet()
        bullet.HitEnemy()
        bullet.HitWall()
      else:
        MainGame.mybulletlist.remove(bullet)
  def blitEnemyBullet(self):
    for bullet in MainGame.enemybulletlist:
      if bullet.live==True:
        bullet.DisplayBullet()
        bullet.HitMyTank()
        bullet.HitWall()
      else:
        MainGame.enemybulletlist.remove(bullet)
  def blitExplode(self):
    for explode in MainGame.explodelist:
      if explode.live==True:
        explode.DisplayExplode()
      else:
        MainGame.explodelist.remove(explode)
  def blitWall(self):
    for wall in MainGame.walllist:
      wall.Display()
      

  
    
  
class Tank(BaseItem):
  def __init__(self,left,top):

    self.images={'U':pygame.image.load(R"src\red\up1.png"),
                 'L':pygame.image.load(R"src\red\left1.png"),
                 'R':pygame.image.load(R"src\red\right1.png"),
                 'D':pygame.image.load(R"src\red\down1.png"),
                 }
    self.direction='U'
    self.speed=3
    self.rect=self.images[self.direction].get_rect()
    self.rect.left=left
    self.rect.top=top
    self.oldrect=self.rect.copy()

    self.live=True

    
    pass
  def Move(self): 
    self.oldrect=self.rect.copy()
    if self.direction=='L':
      if self.rect.left>0:
       self.rect.left-=self.speed
    elif self.direction=='R':
      if self.rect.left<SCREEN_WIDTH-TANK_WIDTH:
       self.rect.left+=self.speed
    if self.direction=='U':
      if self.rect.top>0:
        self.rect.top-=self.speed
    elif self.direction=='D':
      if self.rect.top<SCREEN_HEIGHT-TANK_HEIGHT:
       self.rect.top+=self.speed
    self.HitWall()
    self.HitTank()
    pass
  
  def Shot(self):
    return Bullet(self)
    pass
  def Display(self):
    self.image=self.images[self.direction]
    MainGame.window.blit(self.image,self.rect)
    pass
  def HitWall(self):
    for wall in MainGame.walllist:
      if pygame.sprite.collide_rect(wall,self):
        self.rect=self.oldrect
  def HitTank(self):
    for tank in MainGame.enemytanklist:
      if tank==self:
        continue
      if pygame.sprite.collide_rect(tank,self):
        self.rect=self.oldrect
    if MainGame.my_tank==self:
      return 
    if pygame.sprite.collide_rect(MainGame.my_tank,self):
      self.rect=self.oldrect
  
class MyTank(Tank):
  
  def __init__(self,left=0,top=0):
    super(MyTank,self).__init__(left,top)
    self.heath=3
    
  def Move(self):
    self.oldrect=self.rect.copy()
    key_pressed=pygame.key.get_pressed()
    if(key_pressed[pygame.K_a] and self.rect.left>0):
      self.rect.left-=self.speed
    elif(key_pressed[pygame.K_d] and self.rect.left<SCREEN_WIDTH-TANK_WIDTH):
      self.rect.left+=self.speed
    if(key_pressed[pygame.K_w] and self.rect.top>0):
      self.rect.top-=self.speed
    elif(key_pressed[pygame.K_s] and self.rect.top<SCREEN_HEIGHT-TANK_HEIGHT):
      self.rect.top+=self.speed
    self.HitWall()
    self.HitTank()
  def Display(self):
    if self.heath<=0:
      return 
    self.image=self.images[self.direction]
    MainGame.window.blit(self.image,self.rect)
    pass
  def Revive(self):
    if self.heath>0:
      return 
    self.rect.left=SCREEN_WIDTH/2
    self.rect.top=SCREEN_HEIGHT/2
    self.heath=3
    
  
class EnemyTank(Tank):
  def __init__(self,left=0,top=0,speed=3):
    super(EnemyTank,self).__init__(left,top)
    self.images={
      'U':pygame.image.load(R"src\blue\up1.png"),
      'L':pygame.image.load(R"src\blue\left1.png"),
      'R':pygame.image.load(R"src\blue\right1.png"),
      'D':pygame.image.load(R"src\blue\down1.png"),
    }
    self.direction=self.RandomDirection()
    self.rect=self.images[self.direction].get_rect()
    #self.image=self.images[self.direction]
    self.rect.left=left
    self.rect.top=top
    self.step=100
    self.speed=speed
    self.shotcount=0
    
  def RandomDirection(self):
    directions=['U','D','L','R']
    return directions[random.randint(0,3)]

  def Move(self): 
    self.oldrect=self.rect.copy()
    self.step-=1
    if self.step<=0:
      self.step=100
      self.direction=self.RandomDirection()
      return 
    if self.direction=='L':
      if self.rect.left>0:
       self.rect.left-=self.speed
      else:
        self.direction=self.RandomDirection()
    elif self.direction=='R':
      if self.rect.left<SCREEN_WIDTH-TANK_WIDTH:
       self.rect.left+=self.speed
      else:
        self.direction=self.RandomDirection()
    if self.direction=='U':
      if self.rect.top>0:
        self.rect.top-=self.speed
      else:
        self.direction=self.RandomDirection()
    elif self.direction=='D':
      if self.rect.top<SCREEN_HEIGHT-TANK_HEIGHT:
       self.rect.top+=self.speed
      else:
        self.direction=self.RandomDirection()
    self.HitWall()
    self.HitTank()
  def Shot(self):
    self.shotcount+=1
    if self.shotcount<60:
      return None
    self.shotcount=0
    if random.randint(1,100)<30:
      return Bullet(self)
    else:
      return None
  
    

class Bullet(BaseItem):
  def __init__(self,tank):
    self.images={
      'U':pygame.image.load(R"src\explotions\shot\down.png"),
      'L':pygame.image.load(R"src\explotions\shot\right.png"),
      'R':pygame.image.load(R"src\explotions\shot\left.png"),
      'D':pygame.image.load(R"src\explotions\shot\up.png"),
    }
    Bullet.width=6
    Bullet.height=8
    self.rect=self.images['U'].get_rect()
    self.direction=tank.direction
    self.image=self.images[self.direction]
    if self.direction=='U':
      self.rect.left=tank.rect.left+TANK_WIDTH/2-Bullet.width/2
      self.rect.top=tank.rect.top-Bullet.height/2
    if self.direction=='D':
      self.rect.left=tank.rect.left+TANK_WIDTH/2-Bullet.width/2
      self.rect.top=tank.rect.top-Bullet.height/2+TANK_HEIGHT
    if self.direction=='L':
      self.rect.left=tank.rect.left-Bullet.width/2
      self.rect.top=tank.rect.top-Bullet.height/2+TANK_HEIGHT/2
    if self.direction=='R':
      self.rect.left=tank.rect.left-Bullet.width/2+TANK_WIDTH
      self.rect.top=tank.rect.top-Bullet.height/2+TANK_HEIGHT/2
    self.speed=5
    self.live=True
    
    
    
    
    pass
  def DisplayBullet(self):
    MainGame.window.blit(self.image,self.rect)
    self.Move()
    pass
  def Move(self):
    if self.direction=='L':
      if self.rect.left>0:
       self.rect.left-=self.speed
      else:
        self.live=False
    elif self.direction=='R':
      if self.rect.left<SCREEN_WIDTH-self.width:
       self.rect.left+=self.speed
      else:
        self.live=False
    if self.direction=='U':
      if self.rect.top>0:
        self.rect.top-=self.speed
      else:
        self.live=False
    elif self.direction=='D':
      if self.rect.top<SCREEN_HEIGHT-self.height:
       self.rect.top+=self.speed
      else:
        self.live=False
  def HitEnemy(self):
    for enemyTank in MainGame.enemytanklist:
      if pygame.sprite.collide_rect(enemyTank,self):
        enemyTank.live=False
        self.live=False
        explode=Explode(enemyTank)
        MainGame.explodelist.append(explode)
  def HitMyTank(self):
    if pygame.sprite.collide_rect(MainGame.my_tank,self):
      self.live=False
      MainGame.my_tank.heath-=1
      explode=Explode(MainGame.my_tank)
      MainGame.explodelist.append(explode)
      
  def HitWall(self):
    for wall in MainGame.walllist:
      if pygame.sprite.collide_rect(wall,self):
        self.live=False
    
  
class Wall(BaseItem):
  def __init__(self,left,top):
    self.image=pygame.image.load(R"src\other\steel01.png")
    self.image=pygame.transform.scale(self.image,(16,16))
    self.rect=self.image.get_rect()
    self.rect.left=left
    self.rect.top=top
    self.exist=True
    
    pass
  def Display(self):
    MainGame.window.blit(self.image,self.rect)
    pass
  

class Explode():
  def __init__(self,tank):
    self.rect=tank.rect 
    self.images=[
      pygame.image.load(R"src\explotions\explotion\1.png"),
      pygame.image.load(R"src\explotions\explotion\2.png"),
      pygame.image.load(R"src\explotions\explotion\3.png"),
      pygame.image.load(R"src\explotions\explotion\4.png"),
      pygame.image.load(R"src\explotions\explotion\5.png")
    ]
    self.step=0
    self.image=self.images[self.step]
    self.live=True
    
    pass
  def DisplayExplode(self):
    if self.live==False:
      return 
    self.image=self.images[self.step]
    if self.step<4:
      self.step+=1
    else:
      self.live=False
    MainGame.window.blit(self.image,self.rect)
    pass
class Music():
  def __init__(self) -> None:
    pygame.mixer.init()
    self.explodemusic=pygame.mixer.music.load(R"src\music\explode.mp3")
    pass
  def PlayExplode(self):
    pygame.mixer.music.play()
  
if __name__=='__main__':
  MainGame().StartGame()
  print("退出")
  