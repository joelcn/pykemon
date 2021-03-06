
import pygame, os, sys, time, random
from pygame.locals import *

           #R    G    B
BLUE =     (0,   0,   255)
GREEN =    (0,   128, 0)
PURPLE =   (128, 0,   128)
RED =      (255, 0,   0)
YELLOW =   (255, 255, 0)
NAVYBLUE = (0,   0,   128)
WHITE =    (255, 255, 255)
BLACK =    (0,   0,   0)
ALPHA =    (255, 0,   255)

################################################################################
#Utility Functions
################################################################################
def MoveStrip(pokemonList, moveNumber):
  moveName = pokemonList[moveNumber+3].lower() + '.txt' 
  with open(moveName, 'r') as f:
    fileString = f.read()
    fileList = fileString.split('\n')
    i = 0
    moveList = []
    while i<6:
      moveList.append(fileList[i])
      i += 1
    f.close()
  return moveList
  
def PokemonStrip(targetFile):
  with open(targetFile, 'r') as f:
    fileString = f.read()
    fileList = fileString.split('\n')
    i = 0
    targetList = []
    while i<11:
      targetList.append(fileList[i])
      i += 1
    f.close()
  return targetList
  
def PrintMoves(moveList):
  for x in moveList:
    print x[5]
  print ""

def PrintChoices(choices):
  for x in choices:
    print x
  print ""

def ClearTerminal():
  os.system('cls' if os.name=='nt' else 'clear')
  
def drawMoveText(text, font, surface, x, y, color):
  textobj = font.render(text,1,color)
  textrect = textobj.get_rect()
  textrect.center = (x,y)
  surface.blit(textobj,textrect)
  pygame.display.update()

def drawText(text, font, surface, x, y, color):
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  
  textobj1 = font.render(textLine1,1,color)
  textrect1 = textobj1.get_rect()
  textrect1.topleft = (x,y)
  surface.blit(textobj1,textrect1)
  pygame.display.update()
  
  textobj2 = font.render(textLine2,1,color)
  textrect2 = textobj2.get_rect()
  textrect2.topleft = (x,y+10)
  surface.blit(textobj2,textrect2)
  pygame.display.update()
    
def animateText(text, font, surface, x, y, color):
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  i = 0
  for letter in textLine1:
    realLine1 = textLine1[:i]
    textobj1 = font.render(realLine1,1,color)
    textrect1 = textobj1.get_rect()
    textrect1.topleft = (x,y)
    surface.blit(textobj1,textrect1)
    pygame.display.update()
    fpsClock.tick(FPS)
    i += 1
  j = 0
  for letter in textLine2:
    realLine2 = textLine2[:j]
    textobj2 = font.render(textLine2,1,color)
    textrect2 = textobj2.get_rect()
    textrect2.topleft = (x,y+10)
    surface.blit(textobj2,textrect2)
    pygame.display.update()
    j += 1
  
class Button():
  def assignImage(self, picture):
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
    self.rect.topleft = x,y
  def drawButton(self, picture):
    DISPLAYSURF.blit(picture, self.rect)
  def pressed(self,mouse):
    if self.rect.collidepoint(mouse) == True:
      return True

class HealthBar():
  def init(self,x,y):
    self.position = x,y
    self.negDimensions = (150,5)
    self.posDimensions = [150,5]
  def drawRects(self):
    #(x,y,width,height)
    pygame.draw.rect(DISPLAYSURF, RED, (self.position, self.negDimensions))
    pygame.draw.rect(DISPLAYSURF, GREEN, (self.position, self.posDimensions))
    pygame.display.update()
  def updateBar(self, pokemonList):
    maxHealth = pokemonList[8]
    currentHealth = pokemonList[1]
    healthProportion = int(currentHealth)/float(maxHealth)
    newDimension = healthProportion*self.negDimensions[0]
    self.posDimensions[0] = newDimension

################################################################################
#Battle Logic Functions
################################################################################

def PlayerChoice(targetFile):
  pPokemon = []
  pPokemon = PokemonStrip(targetFile)
  moveNumber = 1
  pAttackList = []
  while moveNumber<5:
    pAttackList.append(MoveStrip(pPokemon, moveNumber))
    moveNumber += 1
  return [pPokemon, pAttackList]

def ComputerChoice(choices):
  choice = random.randint(0,1)
  if choices[choice] == "Charmander":
    computerImgList = charImages
  elif choices[choice] == "Bulbasaur":
    computerImgList = bulbImages
  elif choices[choice] == "Squirtle":
    computerImgList = squirtImages
  targetFile = choices[choice].lower() + '.txt'
  cPokemon = []
  cPokemon = PokemonStrip(targetFile)
  moveNumber = 1
  cAttackList = []
  while moveNumber<5:
    cAttackList.append(MoveStrip(cPokemon, moveNumber))
    moveNumber += 1
  return [cPokemon, cAttackList, computerImgList]
  
def redraw():
  DISPLAYSURF.blit(playerImgList[1], (0,195))
  drawText(pPokemon[0], font, DISPLAYSURF, 200, 315, BLACK)
  playerBar.updateBar(pPokemon)
  playerBar.drawRects()
  DISPLAYSURF.blit(computerImgList[0], (200, 0))
  drawText(cPokemon[0], font, DISPLAYSURF, 10, 45, BLACK)
  computerBar.updateBar(cPokemon)
  computerBar.drawRects()
  pygame.display.update()

def displayMessage(message):
  drawText(message, font, DISPLAYSURF, 10,400, BLACK)
  redraw()
  time.sleep(1)
  DISPLAYSURF.blit(background, (0,0))


def pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats):
  DISPLAYSURF.blit(background, (0,0))
  displayMessage(pPokemon[0] + " used " + pMove[5])
  time.sleep(1)
  #print pPokemon[0] + " used " + pMove[5] + "."
  mode = pMove[0]
  if mode == "1":
    cPokemon = DamageMod(pPokemon, pMove, cPokemon, pStats, cStats)
  elif mode == "21":
    pStats = StatMod(pMove, pStats, pStats, pPokemon[0])
  elif mode == "22":
    cStats = StatMod(pMove, pStats, cStats, cPokemon[0])

def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats):
  displayMessage(cPokemon[0] + " used " + cMove[5] + ".")
  print ""
  mode = cMove[0]
  if mode == "1":
    pPokemon = DamageMod(cPokemon, cMove, pPokemon, cStats, pStats)
  elif mode == "21":
    cStats = StatMod(cMove, cStats, cStats, cPokemon[0])
  elif mode == "22":
    pStats = StatMod(cMove, cStats, pStats, pPokemon[0])
    
def DamageMod(attacker, attack, target, attackerStats, targetStats):
  typeAdvantage = AdvantageCalc(attack, target)
  DMG = int(attack[2])
  aATK = StatIndex(attackerStats, "A")
  tDEF = StatIndex(targetStats, "D")
  effect = DMG*(aATK/tDEF)*typeAdvantage
  target[1] = int(target[1]) - effect
  print attacker[0] + " dealt", effect, "damage!"
  print ""
  return target
  
def StatMod(move, attackerStats, targetStats, defenderName):
  targetStat = move[4]
  effect = move[3]
  if targetStat == "A":
    if effect == "-":
      targetStats[0] -= 1
      displayMessage(defenderName + "'s" + " Attack fell.")
      return targetStats
    else:
      targetStats[0] += 1
      displayMessage(defenderName + "'s" + " Attack rose.")
      return targetStats
  else:
    if effect == "-":
      targetStats[1] -= 1
      displayMessage(defenderName + "'s" + " Defense fell.")
      return targetStats
    else:
      targetStats[1] += 1
      displayMessage(defenderName + "'s" + " Defense rose.")
      return targetStats

def StatIndex(stats, statType):
  statIndex = [(1.0/4),(2.0/7),(1.0/3),(2.0/5),(1.0/2),(2.0/3), 1, 1.5, 2, 2.5, 3, 3.5, 4]
  if statType == "A":
    statInQuestion = stats[0]
  else:
    statInQuestion = stats[1]
  trueStat = statIndex[statInQuestion+5]
  return trueStat

def AdvantageCalc(attack, target):
  combo = attack[1] + target[3]
  if combo == "FG":
    typeAdvantage = 2
  elif combo == "FW":
    typeAdvantage = .5
  elif combo == "FN":
    typeAdvantage = 1
  elif combo == "WF":
    typeAdvantage = 2
  elif combo == "WG":
    typeAdvantage = .5
  elif combo == "WN":
    typeAdvantage = 1
  elif combo == "GF":
    typeAdvantage = .5
  elif combo == "GW":
    typeAdvantage = 2
  elif combo == "GN":
    typeAdvantage = 1
  elif combo == "NF":
    typeAdvantage = 1
  elif combo == "NW":
    typeAdvantage = 1
  elif combo == "NG":
    typeAdvantage = 1
  return typeAdvantage
  
def cMoveSelect(cMoveList):
  cMove = cMoveList[random.randint(0,3)]
  return cMove
  
def pMoveSelect(pMoveList):
  DISPLAYSURF.blit(background, (0,0))
  drawText("What will " + pPokemon[0] + " do?", font, DISPLAYSURF, 10,400, BLACK)
  redraw()
  print "What will " + pPokemon[0] + " do?"
  print "Your choices are... "
  
  button1.drawButton(button)
  drawMoveText(pMoveList[0][5] , font, DISPLAYSURF, 100, 499, BLACK)
  button2.drawButton(button)
  drawMoveText(pMoveList[1][5] , font, DISPLAYSURF, 300, 499, BLACK)
  button3.drawButton(button)
  drawMoveText(pMoveList[2][5] , font, DISPLAYSURF, 100, 566, BLACK)
  button4.drawButton(button)
  drawMoveText(pMoveList[3][5] , font, DISPLAYSURF, 300, 566, BLACK)
  pygame.display.update()
  
  picked = 0
  while picked == 0:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if button1.pressed(mouse) == True:
          pMove = pMoveList[0]
          picked = 1
        if button2.pressed(mouse) == True:
          pMove = pMoveList[1]
          picked = 1
        if button3.pressed(mouse) == True:
          pMove = pMoveList[2]
          picked = 1
        if button4.pressed(mouse) == True:
          pMove = pMoveList[3]
          picked = 1
  
  #PrintMoves(pMoveList)
  #pMoveChoice = raw_input("")
#  tracker = 0
#  for x in pMoveList:
#    if x[5] == pMoveChoice:
#      pMove = pMoveList[tracker]
#      break
#    else:
#      tracker += 1
  return pMove

################################################################################
#Image Initialization Functions
################################################################################

def BulbImages():
  fileNames = ["bulbasaurFront.png","bulbasaurBack.png"]
  bulbArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    bulbArray.append(newImg)
  return bulbArray
  
def CharImages():
  fileNames = ["charmanderFront.png","charmanderBack.png"]
  charArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    charArray.append(newImg)
  return charArray
  
def SquirtImages():
  fileNames = ["squirtleFront.png","squirtleBack.png"]
  squirtArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    squirtArray.append(newImg)
  return squirtArray

def Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList):
  pStats = [1, 1]
  cStats = [1, 1]
  fainted = False
  
  DISPLAYSURF.blit(background, (0,0))
  drawText(pPokemon[0].upper() + "! I choose you!", font, DISPLAYSURF, 10,400, BLACK) 
  time.sleep(2)
  DISPLAYSURF.blit(playerImgList[1], (0,195))
  drawText(pPokemon[0], font, DISPLAYSURF, 200, 320, BLACK)
  playerBar.drawRects()
  time.sleep(2)
  DISPLAYSURF.blit(background, (0,0))
  drawText("Computer sent out " + cPokemon[0] + "!", font, DISPLAYSURF, 10,400, BLACK)
  DISPLAYSURF.blit(playerImgList[1], (0,195))
  drawText(pPokemon[0], font, DISPLAYSURF, 200, 320, BLACK)
  playerBar.drawRects()
  time.sleep(2)
  DISPLAYSURF.blit(background, (0,0))
  redraw()
  
  while fainted != True:  
    pMove = pMoveSelect(pMoveList)
    cMove = cMoveSelect(cMoveList)
    ClearTerminal()
    
    if pPokemon[2] < cPokemon[2]:
      pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
      computerBar.updateBar(cPokemon)
      computerBar.drawRects()
      pygame.display.update()
      if cPokemon[1] <= 0:
        fainted = True
        winner = "Player"
        break
      cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
      playerBar.updateBar(pPokemon)
      playerBar.drawRects()
      pygame.display.update()
      if pPokemon[1] <= 0:
        fainted = True
        winner = "Computer"
        break
    else:
      cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
      playerBar.updateBar(pPokemon)
      playerBar.drawRects()
      pygame.display.update()
      if pPokemon[1] <= 0:
        fainted = True
        winner = "Computer"
        break
      pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
      computerBar.updateBar(cPokemon)
      computerBar.drawRects()
      pygame.display.update()
      if cPokemon[1] <= 0:
        fainted = True
        winner = "Player"
        break
    redraw()
    #print pPokemon[0] + "'s health is:", pPokemon[1]
    #print cPokemon[0] + "'s health is:", cPokemon[1]
  if winner == "Player":
    DISPLAYSURF.blit(endBackground,(0,0))
    DISPLAYSURF.blit(playerImgList[0],(100,375))
    drawText("The winner is "+pPokemon[0]+ "!", font, TEXTSURF, 120, 100, BLACK)
    pygame.display.update()
    time.sleep(2)
  else:
    DISPLAYSURF.blit(endBackground,(0,0))
    DISPLAYSURF.blit(computerImgList[0],(100,375))
    drawText("The winner is "+cPokemon[0]+ "!", font, TEXTSURF, 120, 100, BLACK)
    pygame.display.update()
    time.sleep(2)
  
  def InitializeImages():
    bulbImages = BulbImages()
    bulbFront = bulbImages[0]
    bulbBack = bulbImages[1]
    squirtImages = SquirtImages()
    squirtFront = squirtImages[0]
    squirtBack = squirtImages[1]
    charImages = CharImages()
    charFront = charImages[0]
    charBack = charImages[1]
    button = pygame.image.load("button.png")
    background = pygame.image.load("background.png")
    introBackground = pygame.image.load("introBackground.png")
    endBackground = pygame.image.load("endBackground.png")
    titleBackground = pygame.image.load("titleBackground.png")

if __name__ == '__main__':
  pygame.init()
  fpsClock = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((400, 600))
  TEXTSURF = pygame.display.set_mode((400,600))
  TEXTSURF.set_colorkey(ALPHA)
  pygame.display.set_caption('Pykemon')
  FPS = 15
  font = pygame.font.SysFont(None, 20)
  
  InitializeImages()
  
  DISPLAYSURF.blit(titleBackground, (0,0))
  drawText("Click anywhere to Begin...", font, TEXTSURF, 200, 500, WHITE)
  pygame.display.update()
  
  started = 0
  while started == 0:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        started = 1
        
        
  charButton = Button()
  charButton.assignImage(charFront)
  charButton.setCoords(0, 200)
  squirtButton = Button()
  squirtButton.assignImage(squirtFront)
  squirtButton.setCoords(200, 200)
  bulbButton = Button()
  bulbButton.assignImage(bulbFront)
  bulbButton.setCoords(100, 400)
  
  DISPLAYSURF.blit(introBackground, (0,0))
  charButton.drawButton(charFront)
  squirtButton.drawButton(squirtFront)
  bulbButton.drawButton(bulbFront)
    
  drawText("Choose your Pokemon...", font, TEXTSURF, 120, 100, BLACK)
     
  pygame.display.update()
  
  choices = ['Charmander', 'Squirtle', 'Bulbasaur']

  picked = 0
  while picked == 0:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if charButton.pressed(mouse) == True:
          choice = "Charmander"
          playerImgList = charImages
          picked = 1
        if squirtButton.pressed(mouse) == True:
          choice = "Squirtle"
          playerImgList = squirtImages
          picked = 1
        if bulbButton.pressed(mouse) == True:
          choice = "Bulbasaur"
          playerImgList = bulbImages
          picked = 1
#  print 'Your choices are: '
#  PrintChoices(choices)
#  choice = raw_input('Which Pokemon will you choose?... ')
  targetFile = choice.lower() + '.txt'
  choices.remove(choice)
 
  playerChoice = PlayerChoice(targetFile)
  pPokemon = playerChoice[0]
  pMoveList = playerChoice[1]
  ClearTerminal()
  print pPokemon[0].upper() + "! I choose you!"
  print ""
  time.sleep(.5)
  computerChoice = ComputerChoice(choices)
  cPokemon = computerChoice[0]
  cMoveList = computerChoice[1]
  computerImgList = computerChoice[2]
  print "Computer sent out " + cPokemon[0]
  print ""
  
  playerBar = HealthBar()
  playerBar.init(200,305)
  computerBar = HealthBar()
  computerBar.init(10,35)
  
  button1 = Button()
  button1.assignImage(button)
  button1.setCoords(2, 468)
  button2 = Button()
  button2.assignImage(button)
  button2.setCoords(202, 468)
  button3 = Button()
  button3.assignImage(button)
  button3.setCoords(2, 535)
  button4 = Button()
  button4.assignImage(button)
  button4.setCoords(202, 535)
  
  Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList)

  
  
