import time,os,pyperclip,random

#import pyqrcode
#def QR(text, filename = "."):
#  url = pyqrcode.create(text) 
#  url.svg(f"{filename.replace(" ",'_') if filename!='.' else text[0:(len(text) if len(text)<10 else 9)].replace(" ",'_')}.svg", scale = 10)


def checking():
  while (scan:=input("> ")) != "Done":
    ones = '''
	Put stuff to check here
'''
    if scan in ones:
      print("This ones in the list!!")
    else:
      print("Nothing")

#checking()

#def get_current_mac_wind():
#  from AppKit import NSWorkspace
#  from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo
#
#  workspace = NSWorkspace.sharedWorkspace()
#  activeApps = workspace.runningApplications()
#  for app in activeApps:
#      if app.isActive():
#          options = kCGWindowListOptionOnScreenOnly
#          windowList = CGWindowListCopyWindowInfo(options,
#                                                  kCGNullWindowID)
#          for window in windowList:
#              if window['kCGWindowOwnerName'] == app.localizedName():
#                  return app
#          break
#  return None

#window = get_current_mac_wind()
#window.hideOtherApplications()
#time.sleep(2)
#window.unhideOtherApplications()

def distance(spot,dist=2,W=52,ex_W=0):
    '''Returns distance from SPOT, DIST distance, with a board of W width, with extra width horizontally of EX_W'''
    #top/bottom parts
    if len(spot) == 4 : #splitting up list
      spot,dist,W,ex_W = spot[0], spot[1], spot[2], spot[3]
    spot=[spot,0] if type(spot)==int else spot
    multi = spot[1]>spot[0]
    y = [i for k in [-1,1] for i in range(spot[0]-dist+(W*dist*k)+(W if k==1 and multi else 0) - ex_W,spot[0]+(2 if multi else 1)+dist+(W*dist*k)+(W if k==1 and multi else 0) + ex_W)]
    y.extend(spot[0]+(dist*k)+(W*q)+(int(multi and k==1))+ex_W*k for k in ([-1,1]) for q in range(dist*-1,dist+1))
    return y

#OLD Distance def distance(spot,dist=2,limit=6969,W=52):
#  #top/bottom parts
#  spot=[spot,0] if type(spot)==int else spot
#  multi = spot[1]>spot[0]
#  y = [i for k in [-1,1] for i in range(spot[0]-dist+(W*dist*k)+(W if k==1 and multi else 0),spot[0]+(2 if multi else 1)+dist+(W*dist*k)+(W if k==1 and multi else 0)) if 0<i<limit]
#  y.extend(spot[0]+(dist*k)+(W*q)+(int(multi and k==1)) for k in ([-1,1]) for q in range(dist*-1,dist+1) if 0<spot[0]+(dist*k)+(W*q)<limit)
#  y.append(spot[0])
#  return y

#------#
#      #
#  e   #
#   d  #
#      #
#------#


def printItem():
  temper = {i:(e if '"' not in (e:=ITEMSd[i]) else eval(e)) for i in ITEMSd}
  for ind,i in enumerate(ITEMS): 
      print(temper.get(i,i) if ind not in distant else "\033[48;5;203m ",end="\033[0m")


ITEMS = '-----------------------------------------------------------------\n-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-\n-o                      lllllllllllllllll                      o-\n-o                     lllllllllllllllllll                     o-\n-o                    lllllllllllllllllllll                    o-\n-o                   lllttlllbbbbbbbbbblllll                   o-\n-o                  llllllabbbllllllsssllllll                  o-\n-o                lllllllbbbaallllsslllllllllll                o-\n-o               lllllllbblllaalssllllllllllllll               o-\n-o              llllllllblllllsslllllllllllllllll              o-\n-o              llllllllblllsslllllllllllllllllll       drd    o-\n-o          llllllllllllbssslllllllllllllllllllllllll   drdd   o-\n-o       lllllllllllllllllllllllllllllllllllllllllllllllddd    o-\n-o   ggggggggggggggggggggggggggggggggggggggggggggggggggggggg   o-\n-ogggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggo-\n-ogggSSRRggggggggggggggVVVgggggggggggggOOOgggggggggHgggggggggggo-\n-ogggRRgggggggggggggggVVVVVggggP=PggggOOOOOgggggggJJggggggZggggo-\n-ogggggggggGGGGGggggggg111ggggggggggggg222gggggggJJgggggCCCCCggo-\n-oggBLgggggggggggggggggg1ggggggggggggggg2gggggggggggggggcccccggo-\n-ogAAAgggggggggggggggggggggggggggggggggggggggggggggggggggggggggo-\n-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-\n-----------------------------------------------------------------\n'
distant = distance([494, 0], 6, 66, 25)
HEAVEN_LIGHT,HEAVEN_BOW,HEAVEN_ARROW = True,True,True
iinv = { #distance thing, stats (plus defense, heal etc), description
    'Jalepeno': [[[1106, 0], 3, 66, 0],"+65 HP","Scorching hot... A fiery start leads to a smoother end."],
    'Cheesecake': [[[1180, 0], 3, 66, 1],"+100 HP, 2x damage taken next turn","A treat for the tolerant. Not for the lactose intolerant."],
    'Chocolate Cone': [[[1096, 0], 3, 66, 1],"+25 HP, +1 defense!","A dark delight, made for the tough."],
    'Vanilla Cone': [[[1080, 0], 3, 66, 1],"+25 HP, +5 attack!","A coned confection, made for the strong."],
    'Placebo': [[[1088, 0], 2, 66, 1],"Once taken, never forgotten.","A truly effective medicine. Made to decieve, used to rationalize."],
    'Gum': [[[1135, 0], 2, 66, 2],"+25 HP, +defense next turn","A tough chew...  Not the most nutritious, but hard to hurt."],
    'Cherry': [[[996, 997], 2, 66, 2],"+50 HP, +defense next turn","A lucky break, a jackpot of sorts. A quick fix to lost attention."],
    'Apple': [[[1192, 0], 2, 66, 1],"+10 HP, +1 MAX HP","An apple a day keeps the defibrillator away... The first resort."],
    "Heaven's Bow": [[[559, 0], 6, 66, 5],"Delivery. (Part 2/3)","A glow trapped in gold. Limitless potential, yet limited to the gods."],
    "Heaven's Arrow": [[[559, 0], 6, 66, 5],"Swift justice. (Part 3/3)","A message straight to the point."],
    "Heaven's Light": [[[494, 0], 6, 66, 18],"Radiance. (Part 1/3)","A blessing from above, in times of need."],
    'Red Pill': [[[494, 0], 6, 66, 25],"+15 crit damage, can be heightened...","The sky lights up, replaced with blood red. Once taken, never forgotten."],
    'Blue Pill': [[[494, 0], 6, 66, 25],"+5 blue shield, can be heightened...","The sky lights up, replaced with a solid blue. Once taken, never forgotten."],
    'Dr. Thunder': [[[783, 0], 3, 66, 1],"Heal 50 boss HP?","Heal YSKYSN, if all else fails. The devil's advocate."]
}.keys()
ITEMSd = {
  '-':" ",
  " " : '"\033[48;5;52m " if "Red Pill" in iinv else "\033[48;5;17m " if "Blue Pill" in iinv else " "',
  'o' : '"\033[48;5;0m " if not HEAVEN_LIGHT else "\033[48;5;234m "',
  'l' : '"\033[48;5;7m " if HEAVEN_LIGHT else eval(ITEMSd[" "])',
  'g' : '\033[48;5;242m ', 
  's' : '"\033[48;5;100m " if HEAVEN_BOW else eval(ITEMSd["l"])', #bow string
  'b' : '"\033[48;5;226m " if HEAVEN_BOW else eval(ITEMSd["l"]) ', #bow well bow
  'a' : '"\033[48;5;231m " if HEAVEN_ARROW else eval(ITEMSd["l"]) ', #arrow shaft
  't' : '"\033[48;5;195m " if HEAVEN_ARROW else eval(ITEMSd["l"]) ', #arrow tip
  'A': '"\033[48;5;196m " if "Apple" in iinv else ITEMSd["g"]', #apple red
  'B': '"\033[48;5;131m " if "Apple" in iinv else ITEMSd["g"]', #apple brown (stem)
  'L': '"\033[48;5;112m " if "Apple" in iinv else ITEMSd["g"]', #apple leaf
  'P': '"\033[48;5;124m " if "Red Pill" in iinv else "\033[48;5;27m " if "Blue Pill" in iinv else ITEMSd["g"]',#placebo pill
  '=': '"\033[48;5;253m " if "Red Pill" in iinv or "Blue Pill" in iinv else ITEMSd["g"]',#placebo middle
  'R': '"\033[48;5;160m " if "Cherry" in iinv else ITEMSd["g"]', #cherry red
  'S': '"\033[48;5;64m " if "Cherry" in iinv else ITEMSd["g"]', #cheery stem/connector
  'C': '"\033[48;5;230m " if "Cheesecake" in iinv else ITEMSd["g"]', #cheesecake top
  'c': '"\033[48;5;222m " if "Cheesecake" in iinv else ITEMSd["g"]', #cheesecake bottom
  'Z': '"\033[48;5;162m " if "Cheesecake" in iinv else ITEMSd["g"]', #cheesecake strawberry
  'J': '"\033[48;5;1m " if "Jalepeno" in iinv else ITEMSd["g"]', #jalepeno red
  'H': '"\033[48;5;28m " if "Jalepeno" in iinv else ITEMSd["g"]', #jalepeno green
  'G': '"\033[48;5;207m " if "Gum" in iinv else ITEMSd["g"]', #gum pink
  'V': '"\033[48;5;255m " if "Vanilla Cone" in iinv else ITEMSd["g"]', #vanilla ice cream
  'O': '"\033[48;5;94m " if "Chocolate Cone" in iinv else ITEMSd["g"]', #chocolate ice cream
  '1': '"\033[48;5;215m " if "Vanilla Cone" in iinv else ITEMSd["g"]', #vanilla cone
  '2': '"\033[48;5;215m " if "Chocolate Cone" in iinv else ITEMSd["g"]', #choc cone
  'd': '"\033[48;5;59m " if "Dr. Thunder" in iinv else ITEMSd[" "]', #dr thunder glass
  'r': '"\033[48;5;88m " if "Dr. Thunder" in iinv else ITEMSd[" "]', #dr thunder drink

}  
#items: 
# blue/red pill, slight tints the sky, becomes selectable? (Once taken, never forgotten..)
# placebo - ONLY AFTER RED/BLUE, adds on to effect, gives +10 max hp/+5 blue shield
# apple - heals small amount 
# cherry - jackpot!!! heals 50
# cheesecake - if only you werent lactose intolerant.... heals 100 BUT x2 damage next turn
# jalepeno - scorchin... heals 75 (RARE) 
# gum - heals 25, plus defense for next turn? 
#both kinda rare:
# vanilla - heals smalish amount, +5 attack PERMANENTLY 
# chocolate - heals smallish, +1 defense PERMENTLY (maybe change hp and dmg mul to 200 and x2?)



def thing():
  global distant, ITEMS
  while True:
    printItem()
    if (h:=input("(Enter to refresh)"))!='':
      eval(h)
    with open("TEST.txt",'r') as j:
      ITEMS = j.read()
    with open("testing-test.txt",'r') as k:
      distant = eval(k.read())
    os.system('cls' if os.name=='nt' else 'clear')
#thing()
def Spindle():
  while True:
    CS,D = [float(i) for i in input("Enter CS, diameter > ").split(",")]
    S = f"N = ({CS} * 12 in/ft) / (3.14 * {D})\n"
    S += f"N = {round(CS * 12 / (3.14*D),1)}"
    print(S)
    pyperclip.copy(S)

yskysn_org = list("""
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
o--__gggwwgg_--------rrGGGGGGGGGGGGGr---------------__gwg__---o
o--__ggwwwgg_-------rGGGGGGGGGGGGGGGGr--------------_gwwgg_---o
o--__gwwggg_--------rGBbbbbbbbbbbbBGGGr------------__ggwwg_---o
o--__ggwwggg_-------rBBBBBBbbbBBBBBBGGr-----------__gggwwg_---o
o--__gggwwwg__------rbbbWWWbbbbWWWbbbr------------_ggwwwgg_---o
o--__ggggwwgg_------rbbbbbbbbbbbbbbbbr----------___gwwwgg__---o
o-__gggwwwwgg_------rrbbbbbbbbbbbbbbrr----------_ggwgwwgg__---o
o-__ggwwwgggg_-------rrbbbmmmmmbbbBrr----------__gwwggwwgg__--o
o-__gggwwwgg_---------rrBbbbbbbbBBBr-----------__gwwgggwwgg__-o
o-__ggggwwwgg_-----rrrrnBBBBBBBBBbbrrr-----_____ggwwgggwgwgg_-o
o--_gggwwggg_--rrrrrnnnnnbbbbbbbbbnnnnrr____gggggwwwggwggwwgg_o
o-_gggwwgg____rrnnnnnwwwwwwnnnnnnnnnnnnrrggggwwwwggwgwggggwwggo
o__ggwwgggggggrnnwwwwwwwwwwwwwwwnnnnnnnnrrwwwwggggggwggg_ggwwwo
o__gwwggggggwwwwwwwnnnnnnnnnnnwwwwnnnnnwwwwrrggggwwwwwwgg_ggggo
o_gggwwwwwwwwwwnnnnnnnnnnnnnnnnnnwwwwwwwnnnnrwwwwwwgggwwgg___-o
o-_gggwwgggggrnnnnnnnnnnnnnnnnnnnnnnwwwwwwwwwggggggg_ggwwgg_--o
o-__gggggg___rnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnrgg_______ggwwg_--o
""")

coloreddict={
  'o':'\033[48;5;0m ', #black for the border
  '-':'\033[48;5;233m ', #black (background)
  '_':'\033[48;5;235m ', #gray blac (background)
  'w':'\033[48;5;253m ', #white (lightning)
  'W':'\033[48;5;7m ', #white (normal)
  'b':'\033[48;5;130m ','m':'\033[48;5;3m ', #mouth color
  'B':'\033[48;5;94m ', #brown (darker)
  'r':'\033[48;5;88m ', #red (glow)
  'n':'\033[48;5;18m ','x':'',
  'g':'\033[48;5;242m ', #gray (for background)
  'G':'\033[48;5;236m ', #gray (for hair)
  'Q':'\033[38;5;46m','!':'\033[38;5;177m','@':'\033[38;5;174m','#':'\033[38;5;174m','$':'\033[38;5;174m',
  'X':'\033[0m','▢':'\033[38;5;51m▢', #player
  '~':'\033[38;5;62m◌'#empty space to move in
}

def printman(man = ""):
  for i in man:
    if i == '\n': 
      print('\033[0m')
      continue
    print(coloreddict.get(i,i),end='')
def rc():
  print("\033[H", end="")

noheal,xtreme,bmulti,nonr,hell,hell2,cloud9,cancer,bhp,doomsday = False, False, False, False, False, False, False, False, 1, False

def mode():
  global coloreddict,cancer,doomsday

  cancer = cancer or (xtreme and nonr)
  doomsday = xtreme and nonr and bmulti==2
  
  coloreddict['r']= '\033[48;5;52m ' if hell else '\033[48;5;91m ' if xtreme else '\033[48;5;253m ' if noheal else coloreddict['r']
  if nonr and not cancer: coloreddict['n']='\033[48;5;52m '
  if cloud9:
    coloreddict['o'] = '\033[48;5;54m '
    coloreddict['w'] = '\033[48;5;54m '
    coloreddict['g'] = '\033[48;5;91m '
  if cancer:
    coloreddict['w'] = '\033[48;5;5m '
    for i in ['shields','reds','red bulls']: stats4nerds[i]=stats4nerds.get(i,0)
  if hell:
    coloreddict['n'],coloreddict['g'],coloreddict['w'] = "\033[48;5;0m ",'\033[48;5;52m ','\033[48;5;90m '
    #hell mode 2: coloreddict['W'] = '\033[48;5;1m '
  if doomsday:
    for thing,col in zip(['-','_','g','r','G','n','B','b','w','W','m'],['232','232','232','232','0','0','0','0','34','52','0']):
      coloreddict[thing] = f"\033[48;5;{col}m "
    backer = "\033[48;5;0m"

def ysk_animating():
  yskysn = list("""
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
o--__gggwwgg_--------rrGGGGGGGGGGGGGr---------------__gwg__---o
o--__ggwwwgg_-------rGGGGGGGGGGGGGGGGr--------------_gwwgg_---o
o--__gwwggg_--------rGBbbbbbbbbbbbBGGGr------------__ggwwg_---o
o--__ggwwggg_-----__rBBBBBBbbbBBBBBBGGr-----------__gggwwg_---o
o--__gggwwwg__-____grbbbWWWbbbbWWWbbbr------------_ggwwwgg_---o
o--__ggggwwgg___ggggrbbbbbbbbbbbbbbbbr____------___gwwwgg__---o
o-__gggwwwwggggggwwwrrbbbbbbbbbbbbbbrrggg___----_ggwgwwgg__---o
o-__ggwwwgggggwwwggggrrbbbmmmmmbbbBrrwwwggg______gwwggwwgg__--o
o-__gggwwwwwwwggggg___rrBbbbbbbbBBBrggwwwwgggg___gwwgggwwgg__-o
o-__ggggwwwgggg____rrrrnBBBBBBBBBbbrrrgggwwwwgg_ggwwgggwgwgg_-o
o--_gggwwggg___rrrrrnnnnnbbbbbbbbbnnnnrrggggwwgggwwwggwggwwgg_o
o-_gggwwgg____rrnnnnnwwwwwwnnnnnnnnnnnnrr__ggwwwwggwgwggggwwggo
o__ggwwgg__gggrnnwwwwwwwwwwwwwwwnnnnnnnnrrwwwwggggggwggg_ggwwwo
o__gwwggggggwwwwwwwnnnnnnnnnnnwwwwnnnnnwwwwrrggggwwwwwwgg_ggggo
o_gggwwwwwwwwwwnnnnnnnnnnnnnnnnnnwwwwwwwnnnnrwwwwwwgggwwgg___-o
o-_gggwwgggggrnnnnnnnnnnnnnnnnnnnnnnwwwwwwwwwggggggg_ggwwgg_--o
o-__gggggg___rnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnrgg_______ggwwg_--o
""")
  I = yskysn.index("W")
  eye_coords = [I,I+1,I+2,I+7,I+8,I+9]
  while True:
    with open("testing-test.txt",'r') as eater:
      yskysn = list(eater.read())
    printman(yskysn)
    time.sleep(random.randint(3,5))
    for i in random.choice([[1,-1],[-1,1]]):
      for j in range(2):
        eye_coords = [I+i for I in eye_coords.copy()]
        while "W" in yskysn:
          yskysn[yskysn.index("W")] = 'b'
        for e in eye_coords:
          yskysn[e] = "W"
        rc()
        printman(yskysn)
        time.sleep(.1)
      time.sleep(.5)
      rc()
os.system('clear')
ysk_animating()
