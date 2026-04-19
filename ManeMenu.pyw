#Better Menu using PY??#

import pygame,subprocess,os,webbrowser,sys,time,csv

##Quick File Loader
def FileLoader(FileDir,BackupFileDir):
    try:
        scoreFile = open(FileDir,"r")
    except:
        backupFile = open(BackupFileDir,"r")
        backupData = backupFile.read()
        scoreFile =  open(FileDir,"x")
        scoreFile.write(backupData)
        backupFile.close()
    scoreFile = open(FileDir,"r")
    scoreData = scoreFile.read()
    scoreFile.close()
    scoreData= scoreData.split(",")
    return (scoreData)

##Save to File Function
def FileSaver(content,fileDir,method="w"):
    '''What you want to save, Where, "x" or "w" '''
    saveFile= open(fileDir,method)
    saveFile.write(content)
    saveFile.close()
    return()

##Reconstruct the data through ScoreList and TitleList
def UpdateScores(scores,titles):
    '''Scores and Titles MUST BE THE SAME LENGTH'''
    product = list([])
    for i in range (0,len(scores)):
        product.append(f"{titles[i]}")
        product.append(f"{scores[i]}")
    product = tuple(product)
    return(product)

def SaveScores(content,FileDir):
    fileToClear =open(FileDir,"w")
    fileToClear.close()
    for i in range (0,len(content)):
        if i != (len(content)-1):
            FileSaver(f"{content[i]},",FileDir,"a")
        else:
            FileSaver(f"{content[i]}",FileDir,"a")

##Download,0,\nMusic,0,Game,0,\nWork,0,

##Loading the File
scoreData=FileLoader(r"Documents\Scores.txt",r"Documents\Backups\BackupScores.txt")

##Making variables to hold individual datasets
titleList = (scoreData[::2])
global scoreList
scoreList= (scoreData[1::2])
screenWidthMultiplier= len(scoreList)

##Get variables
maxScreenSizes = (1920,1080)
screenSizes = (220*(screenWidthMultiplier),210)

##Draw variables
xGap= 10
yGap= 100

##Creating the OPEN PROCESS for the links
def OpenProcess(args):
    print(args)
    if args[-3::] != "exe":
        webbrowser.open(rf"{args}")
    else:
        subprocess.Popen([rf"{args}"])

def OpenLinks(args):
    print(len(args))
    for i in range (0,len(args)):
        OpenProcess(args[i])

##Making the incrementation per opening of the thingymajigga
def Increment(i,nList,step=1):
    '''Used To Increment the Score Values'''
    print(f"skibidi, nList{i},{i},{step}")
    n = int(nList[i]) 
    n +=step
    nList[i] = str(n)
    return (nList)
    
##Boot Pygame
pygame.init()
global clicked
clicked = False

##Make the Icon
icon = pygame.image.load("Images\menu.png")
pygame.display.set_icon(icon)

##Text Variables
titleFont = pygame.font.SysFont("Calibri",36)
scoreFont = pygame.font.SysFont("Calibri",20)
menuTitleString=("Your Menu")

def StringPrinter(string,x,y,font):
    '''This is to be used within an iteravite thing so that it repeats the same thing with exponential values'''
    stringTexture = font.render(string,True,(255,255,200))
    screen.blit(stringTexture,(x,y))

##Making Button Classes For The exponential amount of buttons
class ClassButtons:
    
    def __init__(self,x,y,w,h):
        '''X,Y, width,height
            To be used to create each button'''
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        clicked = False
        
    def draw(self,clicked,scoreList):
        #getmouseposition
        pos = pygame.mouse.get_pos()
        #check the mouse is over the click conditions       
        if pos[0] >= self.x and pos[1] >=self.y and pos[0] <= self.x+self.w and pos[1] <= self.y+self.h:
            if pygame.mouse.get_pressed()[0] ==1 and clicked == True:
                print(f"Button{i} Clicked")
                clicked=False
                time.sleep(1)
                selectedLink=FileLoader(rf"Documents\Backups\Links\{titleList[i]}.txt","")
                print(selectedLink)
                OpenLinks(selectedLink)
                scoreList = Increment(i,scoreList)
                
        pygame.draw.rect(screen,(30,30,30),(self.x,self.y,self.w,self.h))
        StringPrinter(titleList[i],xGap+(i*220)+10,yGap+30,titleFont)

class ScoreButtons:
    
    def __init__(self,x,y,w,h):
        '''X,Y, width,height
            To be used to create each button'''
        self.x=x
        self.y=y
        self.w=w
        self.h=h
    def draw(self):
        
        pygame.draw.rect(screen,(30,30,30),(self.x,self.y,self.w,self.h))
        StringPrinter(scoreList[i],60+(i*(220))+10,yGap/1.5+5,scoreFont)

screen = pygame.display.set_mode(screenSizes)

while True:
    pygame.display.set_caption("Menu")
    run = True
    while run:

        ##Get ingame events e.g keypresses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SaveScores(UpdateScores(scoreList,titleList),"Documents\Scores.txt")
                pygame.quit()
                sys.exit()
            
            if event.type ==pygame.MOUSEBUTTONDOWN:
                print("clicked")
                clicked = True
            if event.type ==pygame.MOUSEBUTTONUP:
                print("UNCLICKED")
                clicked = False
                
            if event.type ==pygame.KEYDOWN:

                ##All KeyPresses go here
                if event.key ==pygame.K_ESCAPE:
                    SaveScores(UpdateScores(scoreList,titleList),"Documents\Scores.txt")
                    pygame.quit()
                    sys.exit()
     
            ##Draw on pygame
            screen.fill((90,90,200))

            ##Creating the indivudal buttons For Score and for the Titles
            titleButtons = ([])
            scoreButtons =([])
            for i in range (0,screenWidthMultiplier):
                titleButtons.append(ClassButtons(xGap+(i*220),yGap,200,100))
                scoreButtons.append(ScoreButtons(60+(i*(220)),yGap/1.5,100,25))

            ##Creating the title Background
            pygame.draw.rect(screen,(30,30,30),(xGap,10,(screenWidthMultiplier*220)-20,50))
            StringPrinter(menuTitleString,(screenWidthMultiplier/2*220)-80,20,titleFont)


            ##Draw all the buttons
            for i in range (0,len(scoreButtons)):
                scoreButtons[i].draw()
                titleButtons[i].draw(clicked,scoreList)

            
                
            pygame.display.flip()

pygame.quit()
                


