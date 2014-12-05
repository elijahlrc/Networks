import random
import pygame
import sys
pygame.init()
ids = 0
brain = []
Clock = pygame.time.Clock()
#========TO DO======
#load config file
#better hebbian learning
#better conection initialization
numb_of_nerons = 8000
THRESHHOLD = .25
STARTING_FATIGUE = 20
#Conection vars
CONECTION_WEIGHT_MEAN = 1.25
CONECTION_WEIGHT_VARIANCE = 1.5
CONECTION_DISTANCE_ROOT_MEAN = 3.25
CONECTION_DISTANCE_ROOT_VARIANCE = 1
CONNECTION_STRENGTH_INCREASE = .07
CONECTION_STRENGTH_DECAY = 1.0/2000.0

#flip vars
FATIGUE_RESTORATION = .15
FATIGUE_RESTORATION_MIN = 1.0/700.0
CONECTION_RANDOMNESS = .008

class neron:
    def __init__(self, ids):
        self.threshhold = THRESHHOLD
        self.sum_input = 0#random.random()*1.5
        self.id = ids
        self.conections = []
        x,y = round(((random.random()+.25*random.random())/1.25)*1920),round(((random.random()+.25*random.random())/1.25)*1080)
        self.position = (int(x), int(y))
        self.fatigue = STARTING_FATIGUE
##        if x<1000 and x>800 and y<1000 and y>800:
##            self.sum_input = 2
##        else:
##            self.sum_input = 0
    def conect(self):
        distances = []
        for count in range(0,numb_of_nerons):
            dist = (((self.position[0]-brain[count].position[0])**2)+((self.position[1]-brain[count].position[1])**2))**.5
            if dist <= ((random.gauss(CONECTION_DISTANCE_ROOT_MEAN,CONECTION_DISTANCE_ROOT_VARIANCE)**2)) and count !=self.id:
                weight = random.gauss(CONECTION_WEIGHT_MEAN,CONECTION_WEIGHT_VARIANCE)#center, standard dev
                self.conections.append([count,weight])
    def check_fire(self):
        if self.sum_input >= self.threshhold+self.fatigue:
            self.sum_input = 0
            self.fatigue = 1+self.fatigue*1.1
            return True
        else:
            self.sum_input = 0

            return False
    
    def flip(self):
        for conection in self.conections:
            conection[1] += random.gauss(0,CONECTION_RANDOMNESS) #randomness factor in conection strenth, alllows nerons to go from positive to negative
            if conection[1] > 0:
                conection[1] -= (conection[1]**1.4)*CONECTION_STRENGTH_DECAY#need exponent?
            else:
                conection[1] -= conection[1] *CONECTION_STRENGTH_DECAY
        #Eddit Weights:
        

        #End Weight ajustment.
        
        if self.fatigue >= 0:
            self.fatigue -= random.random()*FATIGUE_RESTORATION
        self.fatigue -= random.random()*FATIGUE_RESTORATION*FATIGUE_RESTORATION_MIN
        #print (self.sum_input)
        circle_size = int(abs(self.fatigue*3)**(.85))  #int(abs(self.fatigue))
        if self.sum_input>=self.threshhold:
            #screen.set_at(self.position,(255,0,0))

            pygame.draw.circle(screen, (0,0,150,normalize_range(255-self.fatigue*20)),self.position,circle_size)
        else:
            pygame.draw.circle(screen, (150,0,0,0),self.position,circle_size)

            screen.set_at(self.position,(255,0,0))
            #screen.set_at(self.position,(0,0,255))

for count in range(0,numb_of_nerons):
    brain.append(neron(ids))
    ids+=1
print ("loading")
print("["),
def normalize_range(val):
    if val>255:
        return 255
    elif val< 0:
        return 0
    else:
        return val
for count in range(0,numb_of_nerons):
    brain[count].conect()
    percent = 50*(float(count)/numb_of_nerons)
    if round(percent)==percent:
        print("="),
print("]")

screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
pygame.display.toggle_fullscreen()
mainloop = True
pause = False


    
while mainloop == True:
    screen.fill((0,0,0))
    fireing = []
    for neron in brain:
        neron.flip()
        if neron.check_fire():
            for conection in neron.conections:
                if conection[1]>0:
                    conection[1] += CONNECTION_STRENGTH_INCREASE
                elif conection[1]<=0:
                    conection[1] -= CONNECTION_STRENGTH_INCREASE
                brain[conection[0]].sum_input += conection[1] #add input to comections curent value

                #display fireing:
                if conection[1]<-1:
                    color = (255,30,0)
                elif conection[1]>5:
                    color = (0,30,255)
                    
                else:
                    blue = max(0, (conection[1])*51)
                    red = 255-blue
                    color = (red,0,blue)
                pygame.draw.aaline(screen,color,neron.position,brain[conection[0]].position)
                #End display fireing
                
                
        else:
            pass
        
    #print ("tick")

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause == False:
                pause = True
            else:
                pause =False

        elif event.type is pygame.MOUSEBUTTONUP:
            pass
            
    while pause == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause == False:
                    pause = True
                else:
                    pause =False

            elif event.type is pygame.MOUSEBUTTONUP:
                pass
    pygame.display.flip()
    #Clock.tick(60)
        

