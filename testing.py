import time,os
def get_current_mac_wind():
  from AppKit import NSWorkspace
  from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo

  workspace = NSWorkspace.sharedWorkspace()
  activeApps = workspace.runningApplications()
  for app in activeApps:
      if app.isActive():
          options = kCGWindowListOptionOnScreenOnly
          windowList = CGWindowListCopyWindowInfo(options,
                                                  kCGNullWindowID)
          for window in windowList:
              if window['kCGWindowOwnerName'] == app.localizedName():
                  return app
          break
  return None

#window = get_current_mac_wind()
#window.hideOtherApplications()
#time.sleep(2)
#window.unhideOtherApplications()

def distance(spot,distance=2,limit=6969,W=52):
  # if 2nd thing in spot is greater just do the greater thing lol, 1st spot is ALWAYS the reference point or somethin 
  #top/bottom parts
  spot=list(spot)
  if len(spot) == 1: spot.append(0)
  y = [i for k in [-1,1] for i in range(spot[0]-distance-W*distance*k,spot[0]+(1 if spot[1]<spot[0] else 2)+distance-W*distance*k) if 0<i<limit]
  y.extend(spot[0]+(distance*k)+(W*q) for k in ([-1,1] if spot[0]>spot[1] else [-1,1,2]) for q in range(distance*-1,distance+1+int(spot[1]>spot[0])) if 0<spot[0]+(distance*k)+(W*q)<limit)
  return y

#------#
#      #
#  e   #
#   d  #
#      #
#------#


def printItem():
  for i in ITEMS:
    print(e if '"' not in (e:=ITEMSd.get(i,i)) else eval(e),end="\033[0m")
ITEMS = """-----------------------------------------------------------------
-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-
-o                      lllllllllllllllll                      o-
-o                     lllllllllllllllllll                     o-
-o                    lllllllllllllllllllll                    o-
-o                   lllttlllbbbbbbbbbblllll                   o-
-o                  llllllabbbllllllsssllllll                  o-
-o                lllllllbbbaallllsslllllllllll                o-
-o               lllllllbblllaalssllllllllllllll               o-
-o              llllllllblllllsslllllllllllllllll              o-
-o              llllllllblllsslllllllllllllllllll              o-
-o          llllllllllllbssslllllllllllllllllllllllll          o-
-o       lllllllllllllllllllllllllllllllllllllllllllllll       o-
-o   ggggggggggggggggggggggggggggggggggggggggggggggggggggggg   o-
-ogggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggo-
-ogggSSRRggggggggggggggVVVgggggggggggggOOOgggggggggHgggggggggggo-
-ogggRRgggggggggggggggVVVVVggggP=PggggOOOOOgggggggJJggggggZggggo-
-oggggggggggGGGGggggggg111ggggggggggggg222gggggggJJgggggCCCCCggo-
-oggBLgggggggggggggggggg1ggggggggggggggg2gggggggggggggggcccccggo-
-ogAAAgggggggggggggggggggggggggggggggggggggggggggggggggggggggggo-
-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-
-----------------------------------------------------------------
"""
distant = distance(240,3,9999,65)
HEAVEN_LIGHT,HEAVEN_BOW,HEAVEN_ARROW = True,True,True
iinv = []
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
  '2': '"\033[48;5;215m " if "Chocolate Cone" in iinv else ITEMSd["g"]' #choc cone

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




while True:
  printItem()
  if (h:=input("(Enter to refresh)"))!='':
    eval(h)
  with open("TEST.txt",'r') as j:
    ITEMS = j.read()
  os.system('cls' if os.name=='nt' else 'clear')
