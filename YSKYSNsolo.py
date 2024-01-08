import os,time,sys,random,json,AUDIO
from pygame import mixer
from threading import Thread

#Change doomsday to darkness minus red lightning/eyes ?, "The Last One Standing." make doomsday dialogues

if os.name == 'nt': #doesnt work on mac? 
  from ctypes import windll

  mid = (windll.user32.GetSystemMetrics(78)//2, windll.user32.GetSystemMetrics(79)//2)

def changespeed(file, speed=1.0):
    return AUDIO.spawnsound(file, (1/speed)*4.25) #*4.25 cause idk

#PYINSTALLER:
#windows:
#pyinstaller -F --add-data "YSKYSN/*.wav;YSKYSN/" --add-data "YSKYSN/*.mp3;YSKYSN/" YSKYSNsolo.py 
#mac (i think):
#pyinstaller -F --add-data "YSKYSN/*.wav:YSKYSN/" --add-data "YSKYSN/*.mp3:YSKYSN/" YSKYSNsolo.py --paths /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages

'''
HELL MODE ITEM VIEWER????
- Switch "MAGIC" with "PRAY " and "HEAL UP" with " ITEM "
- pray same as magic but ALL hell choices, ITEM taks you to a sort of maze that lets you see what you have
Heavnly lghtmakes thebackgroundwhite, can see items like red pill, apple etc
spidy replaced with Heaven's Bow, need first heavnly light (Light shines down from above.... The light fills you with warmth. (1/3 parts!))
heavenly Bow, (Suddenly, a bow from the light above. Light as the clouds and shining bright as a star, hope emerges. (2/3 parts!))
Golden Arrow, (A message from a god... an arrow! A gold engraving says "Golden Finale." The complete bow gives you the perfect endgame... (3/3, dont give up now!)


- HELL MODE
  - two phases, need to kill him for 2nd phase, which is a savepoint you can continue from (since phase 2 not gonna be easy at all)
  - 2nd phase is actually completley different
  - 100% random attack schedule thing, one more extra attack that can happen
  - Add multi word attack 1
  - Section where the board expands like a ton
  - he no longer has random dialogues, his health is times a random amount (which is also what your attack is multipled by)
  
  
  - phase 1: attack 1: multi words, attack 2: norm + slow lasers/lasers on every red basically, attack3: fast lasers, attack 4: double horizontal lasers, attack 5: lightning but can come from top and bottom, attack 6: MULTIPLE IN ONE, randomness 
  - phase 1 end: "A bolt of lightning comes to strick YSKYSN, but the spidy bot.... takes it. It's gone,

ALTER:
  - dmg multiplier gets +/- somewhere between .5-2 or something?


WHAT IVE DONE (so no forgor)
changed achievement SAVING (only) to be a list of all modes' numbers, need to update reading of it etc
made all modes mixable (minus the special one)
added bonus of Doomsday!
'''

r='\033[0m'
def rc():
  print("\033[H", end="")
  
def c(time_sleep=0,skip=False):
  print(r);os.system('clear' if os.name!='nt' else 'cls')
  if time_sleep==0: return ""
  if not skip:
    time.sleep(time_sleep)
  else:
    slepy(time_sleep)

#------ Starting things ------
achievements = {}
#check for truthdata/yskysndata
def starter(expand={}):
  global name,achievements
  with open('yskysndata.json','r') as j:
    big_ach=json.load(j)
  for i in expand:
    if i not in big_ach:
      big_ach[i] = {}
    for k in expand[i]:
      big_ach[i][k] = expand[i][k] or big_ach[i].get(k,False)
  names=list(big_ach.keys())
  def col(o):
    for ind,g in enumerate(o):
      yield f"{ind+1}) {g}"+'\n'
    
  nameZ="".join([i for i in col(names)])
  j = input(f"\033[38;5;222mSave data detected!\033[0m\nIf you think this is a mistake, delete yskysndata.json in this folder.\n(This folder is {os.getcwd()})\n\n\033[38;5;222mOtherwise, who are you?\033[0m (n for new user)\n"+nameZ+"\n\n>\033[38;5;222m ")
  while (int(j) if j.isdigit() else j) not in range(1,len(names)+1) and j!='n':
    c()
    j = input(f"\033[38;5;124mInvalid input!\n\n\033[38;5;222mWho are you?\033[0m (n for new user)\n"+nameZ+"\n\n>\033[38;5;222m ")
  c()
  if j=='n':
    while j in names or j=='n':
      j = input(f"Welcome new person! You are a person right?\n\nWhat would you like to be called? \n\033[38;5;52m[must not be in: \033[0m{nameZ.replace(os.linesep,',')[:-1]}\033[38;5;52m]\033[0m\n\n>\033[38;5;222m ") #pov os.linesep instead of \n lol
      c()
    name=j
    #printt but smaller
    for i in f"Welcome to this world {j}!":
      sys.stdout.write(i)
      sys.stdout.flush()
      time.sleep(.1)
    time.sleep(2)
    input(r+"\n[Any key to continue to the game]")
    big_ach[name] = achievements
  else:
    name = names[int(j)-1]
    achievements = big_ach[name]
  with open('yskysndata.json','w') as j:
    j.write(json.dumps(big_ach))

c()
if 'yskysndata.json' not in os.listdir():
  with open("yskysndata.json",'w') as u:
    u.write(json.dumps({}))
tempr = {}
if "truthdata.json" in os.listdir(): #load truth data!!!
  with open("truthdata.json",'r') as j:
    ji = json.load(j)
    for i in ji:
      tempr[i] = {}
      for a in ['LYS','LEAN','True Chad','Double takedown','YSLYSN']:
        if ji[i].get(a,False):
          tempr[i][a] = True

with open('yskysndata.json','r') as j:
  tempr.update(json.load(j))
starter(tempr)
c()


#-----Music-----
mixer.init(channels = 2)
#works?????

Music = mixer.music

all_music = {}

def file_name(name):
  try:
      base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
  except Exception:
      base_path = os.path.abspath(".")
  return os.path.join(base_path, name)

all_sounds,sound_volume,music_volume = {},1,1
def sound(path:str,filename=True,name='SOUND',setvolume=1):
  global all_sounds,sound_volume
  all_sounds[name]=mixer.Sound(file_name(path) if filename else path)
  sound_volume = setvolume
  mixer.Sound.set_volume(all_sounds[name],setvolume*defaultvolume)
  mixer.Sound.play(all_sounds[name])
def stopsound(name):
  global all_sounds
  if name in all_sounds:
    mixer.Sound.stop(all_sounds[name])
    del all_sounds[name]
defaultvolume = 1
def music(name:str,music_path:str,canloop:bool=True,setvolume=1):
  global all_music,music_volume
  if not all_music.get(name,False):
    if all_music!={}:
      Music.unload()
    all_music = {name:True}
    Music.load(file_name(music_path))
    Music.set_volume((music_volume := setvolume)*defaultvolume)
    Music.play(-1 if canloop else 0)
  elif not Music.get_busy():
    Music.unpause()
def musicstop():
  global all_music
  Music.pause()
  all_music = {}


#-----getkey/big important things-----
WINDOWS = os.name=='nt'
if WINDOWS:
  import msvcrt

  #WALRUS OPERATOR OP
  somekeys = {'H': 'up', 'P': 'down', 'K': 'left', 'M': 'right', '\\r': 'enter', '\\x08': 'backspace','\\xe0':'yippe yay','\\t':'tab'}
else:
  from getkey import keys,getkey as GETkey

def getkey():
  return (h if (h:=str(msvcrt.getch())[2:-1]) not in somekeys.keys() or h in ['P','H','K','M'] else somekeys[h] if h!='\\xe0' else somekeys[str(msvcrt.getch())[2:-1]]) if WINDOWS else GETkey()
UP,DOWN,RIGHT,LEFT='up' if WINDOWS else keys.UP,'down' if WINDOWS else keys.DOWN,'right' if WINDOWS else keys.RIGHT,'left' if WINDOWS else keys.LEFT
BACKSPACE,ENTER,TAB='backspace' if WINDOWS else keys.BACKSPACE,'enter' if WINDOWS else keys.ENTER,'tab' if WINDOWS else keys.TAB

def clearline(amo=1):
  sys.stdout.write(f'\x1b[1A\x1b[2K'*amo)

def getkey1():
  global afk,keyz,keyz2
  afk=True
  while afk:
    pass
  po0=keyz
  keyz=''
  return po0.lower() if po0 not in [UP,DOWN,LEFT,RIGHT] else po0

def anykey(ffg=True):
  if ffg:
    print(r+'\n[Any key to continue]')
  getkey1()
  c()

def achieve(h='`',h1=True):
  global achievements
  if type(h) == list:
    achieve(i for i in h)
    return
  f=achievements[h] if h in achievements.keys() else False
  if h!='`':
    if not f or h in ['s','m1','m2']:
      achievements[h]=h1
      if h1==True:
        print(r+'[You got \033[38;5;86m'+h+r+'!]')
  with open("yskysndata.json",'r') as k: #make sure you dont override things, with yourself AND others
    achievements2=json.load(k)
  for i in achievements2[name].keys():
    if type(achievements2[name][i])==bool:
      achievements[i]=True if achievements2[name][i] else achievements[i]
  achievements2[name]=achievements
  with open('yskysndata.json','w') as j:
    j.write(json.dumps(achievements2))

def acheck(thing):
  return achievements.get(thing,False)

def s(jh,achievement=True):
  return ('\033[48;5;46m' if (acheck(jh) if achievement else jh) else '\033[48;5;160m') + (" " if not achievement or not acheck(jh+"A") else "A") + r

def upped_achieves():
  te = all([acheck(i) for i in ['True Chad','LYS','LEAN','Double takedown','YSLYSN']])
  return f'''
  ┌────────────────────────────────────────────────┐
  |                  \033[38;5;88mAchievements\033[0m                  |
  |------------------------------------------------|
  |LYS - guys, love yourself                      {s('LYS')}|
  |------------------------------------------------|
  |True chad - average no heal enjoyer :moai:     {s('True Chad')}|
  |lean destroyer - purple power                  {s('LEAN')}|
  |Double takedown - twice the hp is nothing.     {s('Double takedown')}|
  |YSLYSN - The true ending, good luck...         {s('YSLYSN')}|
  |------------------------------------------------|
  |{"??????" if not acheck("LEAN") else "Cancer"} - {"Beat lean mode first.    " if not acheck("LEAN") else "you asked, i merely gave."}             {s("Cancer")}|
  |{"???????" if not acheck("LEAN") else "CLOUD 9"} - {"Beat lean mode first.   " if not acheck("LEAN") else "and so drugs truly lose."}             {s("CLOUD 9")}|
  |{"?????" if not te else "Hell."} - {"Beat ALL NORMAL MODES first.      " if not te else "its not possible. please.         " if not acheck("Hell.") else "yet somehow, the player prevailed."}     {s("Hell.")}|
  |------------------------------------------------|
  |no - beat level 1, speed 7+ (youve beaten: {achievements.get("m1",0)})  {s("aint no way")}|
  |god - beat level 2, speed 7+ (youve beaten: {achievements.get("m2",0)}) {s("HOW")}|
  └────────────────────────────────────────────────┘
  '''

def achievers():
  c()
  print(f"{'Anykey to exit':^54}\n{upped_achieves()}")
  time.sleep(1)
  getkey1()
  c()

def THREAD(**targe):
  y = Thread(target = targe['target'],args=() if 'args' not in targe else [targe['args']] if type(targe['args'])!=tuple else targe['args'])
  y.daemon = True
  return y







#-----Maps-----
main=list('''
777776666666744444476666666666744444476666666677777
777666666666674444766666666666674444766666666666777
766666666666674444766667777666674444766666666666667
666677777766674444766677☼☼7766674444766677777766666
66677☼☼☼☼77667444476667☼☼☼☼76667444476677☼☼☼☼776666
6667☼☼☼☼☼☼7667444476677☼☼☼☼7766744447667☼☼☼☼☼☼76666
6677☼☼☼☼☼☼776744447677☼☼☼☼☼☼776744447677☼☼☼☼☼☼77666
667☼☼☼☼☼☼☼☼7674444767☼☼☼☼☼☼☼☼7674444767☼☼☼☼☼☼☼☼7666
667777777777674444767777777777674444767777777777666
666666666666674444766666666666674444766666666666666
666666666666674444766666666666674444766666666666666
6-------------------------------------e----◔◔◔◔◔◔◔◔
6-------------------------------------e◔-◔◔◔◔◔◔◔◔◔◔
6-------------------------------------e-◔◔◔◔◔◔◔◔◔◔◔
6-------------------------------------e-◔◔◔◔◔⎾⏋◔◔◔◔
!--┌┐---------------------------------e◔◔◔◔◔◔╘╛◔◔◔◔
!--└┘---------------------------------e◔◔◔◔◔◔◔◔◔◔◔◔
6-------------------------------------e◔◔◔◔◔◔◔◔◔◔◔◔
6-------------------------------------e--◔◔◔◔◔◔◔◔◔◔
''')
notmain=list('''
))]]]]]))]]]74444447]))]]]]]6)74444447]6]]66]666]66
))]]]]]))]]]]744447]]))]]]]6))]7444476]]]6)66]66666
))-----------------------------------------------66
))-ab-------------------ij-----------------------66
))-cd-------------------kl-----------------------66
))---------------------------------------uv------66
))---------------------------------------wx------66
)---------------------------------ef-------------66
)0--------------------------------gh-------------66
)------------------------------------------------66
))-----------------------------------------------66
))------qr---------------------------------------66
))------st---------------------------------------66
))-----------------------------------------------66
))-----------------------------------------------66
!--------------------------------------mn------┌┐-!
!--------------------------------------op------└┘-!
))]]]]]))]]]]]))]]]]]))]]]]]6)]]6]]66]6666)6]666666
))]]]]]))]]]]]))]]]]]))]]]]]))6]]66))6]6]]6666]6666
''')
colors = {'6':'\033[48;5;222m ','7':'\033[48;5;232m ','4':'\033[48;5;238m ',']':'\033[48;5;243m ',')':'\033[48;5;245m ','☼':'\033[48;5;88m ','◔':'\033[48;5;254m ','⎾':'\033[48;5;254m┌',"⏋":'\033[48;5;254m┐','╘':'\033[48;5;254m╘','╛':'\033[48;5;254m╛','!':'\033[48;5;110m ','+1':'\033[48;5;91m ','+2':'\033[48;5;97m ','(1':"\033[48;5;237m ","(2":"\033[48;5;135m ",'Q1':"\033[48;5;27m","Q2":"\033[48;5;27m","W1":'\033[48;5;41m',"W2":'\033[48;5;41m','Z':'\033[48;5;207m ',"~":"",'1':'\033[48;5;99m ','++1':'\033[48;5;1m ','++2':'\033[48;5;25m ','21':'\033[48;5;196m ','2':'\033[48;5;27m ','0':'\033[48;5;58m ','@':'\033[48;13m ','3':'\033[48;5;99m '}
gamering=list('''
))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))
))]]]]]))=~~~~~~~~~~~~~~~~~~))]]]]]))]]]]]))]]]]]))
)+--------------------------((-------AB]]QQ--QQ]]))
)+--------------------------((-------CD]]QQ--QQ]]))
)+--------------------------((------]]]]]]]--]]ZZ))
)+--------------------------((-------------------))
)+--------------------------((-------------------))
)+--------------------------((-------]]]]]]--]]ZZ))
)+--------------------------((-------]]]]WW--WW]]))
)+--------------------------((-------]]]]WW--WW]]))
)+--------------------------((-------]]]]]]]]]]]]))
)+--------------------------((----------------]]]))
)+--------------------------((----------------@]]))
)+--------------------------((-------]]-------]]]))
)+--------------------------((-------]]]]]]]]]]]]))
)+--------------------------((-----------------┌┐-!
)+--------------------------((-----------------└┘-!
))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))
))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))]]]]]))
''')
#-----moving stuff-----
d11,d12,d21,d22,d31,d32,d41,d42,d51,d52,d61,d62,d71,d72 = "hey hi\ndid you know you could actually use your truth data for this game\nfr!!!!!! just like put it in the same folder as this exe and bam haha achievement extraction go brrrrr\nits like actually kinda good game design\nimpossible","pretty sure the guy who made this didnt take into account the other way around then called it a feature....\nmaybe this game kinda sucks","wait how did you find me\nmy disguise is crazy good bro\nloooooook at me you cant\nin fact i cant see myself...\nwhy is the depth thing realistic like i want to see myself???","like these stupid things carry onto the next screen in the same exact location\nits like a filter man....","You know, I was incredibly scared of that guy to the east until I found out his real name.\nIt's 'You Should Keep Yourself Safe Now.'\nAt least that's what that guy over there told me...","He's still super scary, but now I can pretend I'm better than him because his name doesnt mean the other thing I thought about, that isnt his real name I swear, it's only that name that the other guy told me because I know I could trust the other guy and not my gut since my gut always lies to me, and there's nothing like a friend that I met two seconds ago, but we didnt even meet fr I'm just pretending we did so there's context behind this conversation because I'm socially incapable of not being awkward.\n\nYou know?","hiiiiiiiiiii did you see the new update\nlike sure half of the boss is just copied from that other game but the new modes are coool hehe\nfunny names too and i think theres gonna be one more, que epico","i heard there was this one guy, a true legend...\nhe beat every single mode on this boss fight....\n\nthe creator took that personally, creating Cancer difficulty for that exact reason....\nif you havent seen it yet, i suggest saving your brain cells","you know the achievements tab right?\nat the bottom is something that says like 'beat all the ez modes' or something right\nand i beat them JUST FOR THAT, took me a few seconds since im like that yk\nBUT THE GOD DAMN MODE ISNT EVEN OUT YET?????\nlike how can you say to unlock something that doesnt even exist.","did i beat the other modes? no, of course not.\nthey are impossible.","nah bro you talk to that guy to the left of me?\nbros bonkers\ni dont think mans seen the sun period\ni mean i havent either but thats besides the point\nat least i know what the sun is","you dont know what the sun is?\nstop capping this isnt the truth\ngo outside look at the sky","Never mind, I'm alive!!!!!\nThat is if you remember me from last update...\nEither way, I figured the game out!\n\nThe top part is to control the overall speed of the level, and change said level if you want to go back....\n\nOh yeah, to actually play, first start the game by activating the pink buttons, which should start something like a countdown...\nOrbs will spawn from the left, and I think you need to catch them by standing next to the tile they will land on, I couldn't quite win though....","It's quite cool you can activate two tiles at once, it makes the game at least playable....\n\nBut if you forgot how to work it, next to me controls, blue for speed, green for level 'select', pink to start the game\nCatch the orbs coming from the left after the countdown, and beyond that, I got no clue."
charss = {'AaEimqu':'┌','Bbfjnrv':'┐','Ccgkosw':'└','Ddhlptx':'┘'}
charss2,npcers,npnums = ''.join(charss),{'abcd':[d11,d12],'Efgh':[d21,d22],'ijkl':[d31,d32],'mnop':[d41,d42],'qrst':[d51,d52],'uvwx':[d61,d62],"ABCD":[d71,d72]},{}
def np(o):
  global npnums
  npnums[o]=npnums.get(o,0)+1
  return 0 if npnums[o]==1 else 1
def checknpcs(dire):
  for i in npcers:
    if ischar(dire,list(i)):
      print()
      printt(npcers[i][np(i)],1,True,True)
      time.sleep(1)
      anykey()
      return
      
def movedir(direc):
  global mazeq
  star = mazeq.index('┌')
  q = star+(1 if direc=='right' else -1 if direc=='left' else 52 if direc=='down' else -52)
  if q+53 < len(mazeq):
    mazeq[star],mazeq[star+1],mazeq[star+52],mazeq[star+53] = '-','-','-','-'
    for i,e in zip(['┌','┐','└','┘'],[q,q+1,q+52,q+53]):
      mazeq[e] = i
      
def ischar(direc,chars,both_needed=False,default=True):
  thecheck = box1 if default==True else default
  chars=chars if type(chars)==str else chars
  try:
    q = [mazeq[thecheck-1] in chars, mazeq[thecheck+51] in chars] if direc=='left' else [mazeq[thecheck+2] in chars, mazeq[thecheck+54] in chars] if direc=='right' else [mazeq[thecheck-52] in chars, mazeq[thecheck-51] in chars] if direc=='up' else [mazeq[thecheck+104] in chars, mazeq[thecheck+105] in chars] if direc=='down' else [False,False]
    return any(q) if not both_needed else all(q)
  except: #for down cases
    return False
def distance(spot,distance=2,limit=6969):
  # returns distance to a spot (used for radio lol)
  y = [i for k in [-1,1] for i in range(spot-distance-52*distance*k,spot+1+distance-52*distance*k) if 0<i<limit]
  y.extend(spot+(distance*k)+(52*q) for k in [-1,1] for q in range(distance*-1,distance+1) if 0<spot+(distance*k)+(52*q)<limit)
  return y

mazeq,nextone = main,[]  #find mazeq
radio_on,radio_off,canspam = distance(419,3),distance(419,4),mazeq==notmain

tips = ["Use ]/[ to adjust song offset, ] to add, [ to substract!","There will be a secret for going to yskysn with the alter, just you wait!!!","Your character is two tall... would be a shame if you only had to move once most of the time.","Splitting your SOUL doesn't mean you can move them at the same time... You still are one person after all!","Don't know where the audio is coming from? Check the room next to this one, this totally makes sense!","Remember, the easiest controls are WASD for your main self, and IJKL for the other half...","It is possible to beat speed 9. I havent, but you can.","Annoyed by the countdown? Press 5 to start the game instantly! (also works anywhere!)","Can't hit the notes? Try being better!\n(and understanding the notes register when they HIT it/disappear, not when they get there)","Can't hit the last note in level 2? Be less color blind!","Bad at videogame? Decrease the speed! And touch less grass!","Trying speed 9 constantly? Touch grass, drink water, look up what a shower is, and stop.","I don't know what to put here. How are you :) (i hope you said good)",'You can use +/- on your keyboard to change the volume of everything! (Also works for boss music/sounds!)','Make sure to meet spiderman before beating the boss... thank me later.']

def checkthing():
  global hassseen2
  if not hassseen2 and level==2:
    c()
    printt(["\033[01mIt's as if your very SOUL was splitting....\n\033[0m","There are now two parts to control!\nUse WASD to control red, and IJKL to move blue!","Hit corresponding colors with each part...","\nYou are still one person, you cannot move both at the same exact time..."],[1,2,2,2])
    print("Good luck!")
    anykey()
    hassseen2=True

def move(dir):
  global mazeq,speed,level,colors,both,canspam
  checknpcs(dir)
  if ischar(dir,"!"):
    mazeq=(main if mazeq==notmain else notmain) if dir=="right" else (notmain if mazeq==main else gamering)
    mixer.pause()
    both,canspam=False,mazeq==notmain
  elif ischar(dir,'0'):
    printt(["It's an incredibly old radio, barely able to play audio...", "A poster on the back confirms a salesman used to own it...","Must not have sold."],[2,2,1])
    anykey()
  elif ischar(dir,'@'):
    print("A tip jar...\n\033[38;5;135mReach in for a tip?\033[0m (y for yes)")
    if getkey1()=='y':
      printt(f"\nThe paper reads:\n\tTip #{tips.index(n:=random.choice(tips))+1}: {n}",.02)
      anykey()
    c()
  elif ischar(dir,'e') and mazeq==main:
    yskysn()
  elif ischar(dir,'Q'):
    speed += 1 if dir=='right' else -1
    colors['Q1' if dir=='left' else 'Q2'] = '\033[48;5;99m' if 0<speed<10 else '\033[48;5;88m'
    speed = 9 if speed==10 else 1 if speed==0 else speed
  elif ischar(dir,'W'):
    level += 1 if dir=='right' else -1
    colors['W1' if dir=='left' else 'W2'] = '\033[48;5;99m' if 0<level<=maxlevel else '\033[48;5;88m'
    level = maxlevel if level>maxlevel else 1 if level==0 else level
  elif ischar(dir,'Z') and '207m' in colors['Z']:
    checkthing()
    THREAD(target=spawners).start()
    mixer.pause()
  elif ischar(dir,'-',True):
    movedir(dir)
    if canspam:
      if (k:=mazeq.index('┌')) in radio_on:
        music('spam',"YSKYSN/realboy.mp3",True,.8)
      elif k in radio_off:
        Music.pause()

def move2(dir): #for alter
  global ALTER1,mazeq
  if ischar(dir,'!',False,ALTER1):
    mazeq=(main if mazeq==notmain else notmain) if dir=="right" else (notmain if mazeq==main else gamering)
    ALTER1 = 782 if dir=='right' else 829 #works out so its easy lol
    mixer.pause()
  if ischar(dir,'-└┘┌┐',True,ALTER1):
    ALTER1 += 52 if dir=='down' else -52 if dir=='up' else -1 if dir=='left' else 1
  if ischar(dir,'e',False,ALTER1) and mazeq==main:
    yskysn()
  
#-------minigame stuff-------


level,maxlevel,speed,message,both,ALTER1 = 1,2 if acheck("aint no way") else 1,5,"Pink to start...",False,135 #find both


#find songs
song1 = [7.5, ["8", 34], ["C", 1], ["B", 1], ["A", 1], ["9", 1], ["A", 1], ["9", 1], ["A", 1], ["B", 32], ["5", 1], ["6", 1], ["5", 1], ["6", 1], ["5", 1], ["6", 1], ["7", 32], ["C", 1], ["B", 1], ["A", 1], ["B", 1], ["A", 1], ["9", 1], ["8", 19], ["6", 1], ["7", 1], ["8", 7], ["7", 1], ["6", 1], ["5", 7], ["4", 1], ["5", 1],["6",1]] #tuples = ([note positions to spawn (STRING)],iterations to wait)
song2 = song1.copy() #yea lol
song2[0] = 6.75

song2_ALTER = [["AMONGUS",23],["4", 4], ["3", 4], ["4", 4], ["5", 3], ["5", 3], ["5", 22], ["A", 3], ["B", 3], ["A", 4], ["9", 3], ["9", 3], ["9", 23], ["D", 3], ["C", 3], ["B", 4], ["D", 4], ["E", 3], ["D", 20], ["B", 4], ["A", 4], ["9", 4], ["8", 3],["7",3]]

SPEEDS = {"1": 0.48025, "2": 0.5355, "3": 0.612, "4": 0.70975, "5": 0.85, "6": 1.04125, "7": 1.36, "8": 1.9125, "9": 3.4} #updated :DDD

nextone2,candie,hassseen2 = [],True,False #for testing stuff

def spawners(skip=False,alter_song=song2_ALTER): #find minigame
  global gamering,maxlevel,level,colors,SCREENUP,ALTER1,message,nextone,nextone2,both
  
  song = song1 if level==1 else song2
  #alter ego moment
  both,ALTER1 = level == 2, 135
  #26 spaces to get to the right
  #.1 per iteration cause 2.6
  sd = {'ind1':1,'ind2':0,'its1':0,'its2':0,'end1':False,'end2':not both} 
  aliver, end, nextone, nextone2, colors['Z'], message, SCREENUP =\
  True, False,[55+(52*int(song[1][0][0],16))],[] if not both else [55+(52*int(alter_song[1][0][0],16))],'\033[48;5;8m ',"Countdown: in...",True
  
  def moveall():
    global gamering
    nonlocal aliver
    ind2 = len(gamering) 
    gm = ''.join(gamering)
    for sym,check in zip(['1','2','3'],[[box1],[ALTER1],[box1,ALTER1]]):
      ind = ind2
      if not both and sym in ['2','3']:
        continue
      while (ind:=gm.rfind(sym,0,ind))!=-1:
        gamering[ind]='-'
        if gamering[ind+1]!='(':
          gamering[ind+1]=sym
        else:
          if not all(chec%52==31 and ind-55<chec<ind+55 for chec in check):
            aliver=not candie
      
  def startmusic():
    time.sleep(song[0]-((song[0]/10)*speed)+offset)
    if aliver:
      sound(changespeed("YSKYSN/dial1.wav" if level==1 else "YSKYSN/dial2.wav", SPEEDS[str(speed)]*s_offset),False,'DIAL')
      if level==2:
        mixer.Sound.set_volume(all_sounds['DIAL'],.5*defaultvolume)
        time.sleep(1)
        if 'DIAL' in all_sounds:
          mixer.Sound.set_volume(all_sounds['DIAL'],1*defaultvolume)
  
  def START():
    global message,SCREENUP
    time.sleep(2)
    for i in range(3,-1,-1):
      message,SCREENUP=f"Countdown: {i}",True
      sound("YSKYSN/beep1.mp3")
      time.sleep(1)
  
  #starting things
  if not skip:
    START() 
  message="Good Luck!"
  if mazeq==gamering:
    gamering[55+(52*int(song[sd['ind1']][0][0],16))] = '1'
  else:
    aliver=False
  
  THREAD(target=startmusic).start()

  while aliver and not end:
    nextone=[55+(52*int(i,16)) for i in song[sd['ind1']+1][0]] if sd['ind1']+1<len(song) else []
    if both:
      nextone2 = [55+(52*int(i,16)) for i in alter_song[sd['ind2']+1][0]] if sd['ind2']+1<len(alter_song) else []
    SCREENUP = True
    
    time.sleep(.28-(.028*speed)) #we do a lot of scaling
    
    for (IND,ITS,SYMB,END,SONG) in zip(['ind1','ind2'],['its1','its2'],['1','2'],['end1','end2'],[song,alter_song]): #its = iterations, ind = index
      if not both and SYMB=='2':
        continue
      if sd[IND]!=len(SONG):
        sd[ITS]+=1
        if sd[ITS]==SONG[sd[IND]][1]:
          sd[IND]+=1
          if sd[IND]!=len(SONG):
            for i in SONG[sd[IND]][0]:
              gamering[55+(52*int(i,16))] = SYMB if not (both and sd[IND]==len(SONG)-1 and SYMB=='1') else '3'
          sd[ITS]=0
      else:
        if SYMB not in gamering:
          sd[END]=True
    end = all([sd['end1'],sd['end2']])
    moveall()
    if mazeq!=gamering:
      aliver=False
      
  if aliver:
    if speed>=7:
      achieve("aint no way" if level==1 else 'HOW' if level==2 else "idk add your achievement here??????????") 
    if speed>achievements.get(f'm{level}',0):
      achieve(f'm{level}',speed)
    level,maxlevel=2 if maxlevel==1 else level,2 #win stuff
  for i in ['1','2','3']:
    while i in gamering:
      gamering[gamering.index(i)] = '-'
  colors['Z'],message,nextone,nextone2,SCREENUP='\033[48;5;207m ',"Try again!" if not aliver else "Good job!",[],[],True
  stopsound('DIAL')

#slepy/printt
def printt(thingggg,dela=.03,iiu=True,npc=False):
  global keyz2
  keyz2,indeci='',dela in [.03,.02,.04,.05,.06,.07,.08,.09,.1,.2,.01,.005]
  if type(thingggg)!=str: #FOR LISTS ONLY, NEEDS EQUAL LENGTHS FOR THING AND DELA UNPACKING GO BRRRRRR
    for ind,i in enumerate(thingggg):
      printt(thingggg[ind],dela[ind] if ind<len(dela) else .03,True if type(iiu)!=list or ind<len(dela) else iiu[ind]) #if anything just pass in False to printt no line between each hehe
    return 'recursion :)'
  for ind,i in enumerate(thingggg):
    sys.stdout.write(i)
    sys.stdout.flush()
    if keyz2!='x':
      time.sleep((dela if indeci else .02) if not npc or i!='\n' else 1)
  if dela!=False and iiu!=False: #i get lazy lol
    print("")
  if dela>=.5 or type(iiu)!=bool: #thank you binary for existing
    slepy(dela if type(iiu)==bool else iiu) #you can put in the waiting time for each char or at the end for dela
  keyz2=''

def slepy(amonu):
  global keyz2
  for _ in range(6):
    if keyz2!='x':
      time.sleep(amonu/6)
  keyz2=''
  return "\033[0m\n" #now i can put this at the end of print() lol


#key things
afk,keyz,keyz2=True,'',''
class KeyboardThread(Thread):
  def __init__(self, input_cbk = None, name='keyboard-input-thread'):
    self.input_cbk = input_cbk
    super(KeyboardThread, self).__init__(name=name)
    self.daemon = True
    self.start()
  def run(self):
    while True:
      self.input_cbk(getkey())
def thingthing(key):
  global afk,keyz,keyz2
  keyz2=key
  if afk:
    afk=False
    keyz=key

#-------------------------YSKYSN----------------------
YL='''ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo\no----------------------GGGGGGGGGGGGG--------------------------o\no--------------------GGGGGGGGGGGGGGGG-------------------------o\no--------------------GbbbbbbbbbbbbbGGG------------------------o\no--------------------bbbbbbbbbbbbbbbGG------------------------o\no--------------------bbbWWWbbbbWWWbbbB------------------------o\no--------------------bbbbbbbbbbbbbbbbB------------------------o\no---------------------bbbbbbbbbbbbbbB-------------------------o\no---------------------BbbbmmmmmbbbBB--------------------------o\no----------------------BbbbbbbbbbBB---------------------------o\no-----------------------BBBBBBBBBBb---------------------------o\no-------------------nnnnbbbbbbbbbbbnnn------------------------o\no---------------nnnnnnnnnnnnnnnnnnnnnnn-----------------------o\no--------------nnnnnnnnnnnnnnnnnnnnnnnnn----------------------o\no--------------nnnnnnnnnnnnnnnnnnnnnnnnnnn--------------------o\no-------------nnnnnnnnnnnnnnnnnnnnnnnnnnnnn-------------------o\no-------------nnnnnnnnnnnnnnnnnnnnnnnnnnnnnn------------------o\no-------------nnnnnnnnnnnnnnnnnnnnnnnnnnnnnn------------------o'''
YS='''ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo\no--__gggwwgg_--------rrGGGGGGGGGGGGGr---------------__gwg__---o\no--__ggwwwgg_-------rGGGGGGGGGGGGGGGGr--------------_gwwgg_---o\no--__gwwggg_--------rGBbbbbbbbbbbbBGGGr------------__ggwwg_---o\no--__ggwwggg_-------rBBBBBBbbbBBBBBBGGr-----------__gggwwg_---o\no--__gggwwwg__------rbbbWWWbbbbWWWbbbr------------_ggwwwgg_---o\no--__ggggwwgg_------rbbbbbbbbbbbbbbbbr----------___gwwwgg__---o\no-__gggwwwwgg_------rrbbbbbbbbbbbbbbrr----------_ggwgwwgg__---o\no-__ggwwwgggg_-------rrbbbmmmmmbbbBrr----------__gwwggwwgg__--o\no-__gggwwwgg_---------rrBbbbbbbbBBBr-----------__gwwgggwwgg__-o\no-__ggggwwwgg_-----rrrrnBBBBBBBBBbbrrr-----_____ggwwgggwgwgg_-o\no--_gggwwggg_--rrrrrnnnnnbbbbbbbbbnnnnrr____gggggwwwggwggwwgg_o\no-_gggwwgg____rrnnnnnwwwwwwnnnnnnnnnnnnrrggggwwwwggwgwggggwwggo\no__ggwwgggggggrnnwwwwwwwwwwwwwwwnnnnnnnnrrwwwwggggggwggg_ggwwwo\no__gwwggggggwwwwwwwnnnnnnnnnnnwwwwnnnnnwwwwrrggggwwwwwwgg_ggggo\no_gggwwwwwwwwwwnnnnnnnnnnnnnnnnnnwwwwwwwnnnnrwwwwwwgggwwgg___-o\no-_gggwwgggggrnnnnnnnnnnnnnnnnnnnnnnwwwwwwwwwggggggg_ggwwgg_--o\no-__gggggg___rnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnrgg_______ggwwg_--o'''
ITEMS='-----------------------------------------------------------------\n-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-\n-o                      lllllllllllllllll                      o-\n-o                     lllllllllllllllllll                     o-\n-o                    lllllllllllllllllllll                    o-\n-o                   lllttlllbbbbbbbbbblllll                   o-\n-o                  llllllabbbllllllsssllllll                  o-\n-o                lllllllbbbaallllsslllllllllll                o-\n-o               lllllllbblllaalssllllllllllllll               o-\n-o              llllllllblllllsslllllllllllllllll              o-\n-o              llllllllblllsslllllllllllllllllll              o-\n-o          llllllllllllbssslllllllllllllllllllllllll          o-\n-o       lllllllllllllllllllllllllllllllllllllllllllllll       o-\n-o   ggggggggggggggggggggggggggggggggggggggggggggggggggggggg   o-\n-ogggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggo-\n-ogggSSRRggggggggggggggVVVgggggggggggggOOOgggggggggHgggggggggggo-\n-ogggRRgggggggggggggggVVVVVggggP=PggggOOOOOgggggggJJggggggZggggo-\n-ogggggggggGGGGGggggggg111ggggggggggggg222gggggggJJgggggCCCCCggo-\n-oggBLgggggggggggggggggg1ggggggggggggggg2gggggggggggggggcccccggo-\n-ogAAAgggggggggggggggggggggggggggggggggggggggggggggggggggggggggo-\n-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-\n-----------------------------------------------------------------'
r='\033[0m'
#vars you can change in settings, preferences
centerit,centermodes,skipintro = "center",["center","right","left"],False # make settings!/hell mode things

def yskysn():
  global afk,centerit,skipintro
  if both:
    printt("Something feels off... Maybe its you?\n[ALTER mode activated...]")
    anykey()
  playin=list('''\n wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwR\n wgwwggggggggggggggggggggggggggggggggggggggggggggggggggggwwwwwR\n wwwg____________________________________________________gggwwR\n wgg__~_______~_______~_______~_______~_______~_______~___gwwwR\n wwg_____________________________________________________ggggwR\n wwwg____________________________________________________gwwgwR\n wwwg_~_______~_______~_______▢_______~_______~_______~__ggwwwR\n wgwg_____________________________________________________gwgwR\n wgg______________________________________________________ggwwR\n wg___~_______~_______~_______~_______~_______~_______~___wgwwR\n wwg_____________________________________________________ggwwwR\n wgwg____________________________________________________gwgwwR\n wwwg_~_______~_______~_______~_______~_______~_______~__gwwgwR\n wwwg____________________________________________________gwwgwR\n wwwwggggggggggggggggggggggggggggggggggggggggggggggggggggggwwwR\n wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwR''')
  playinref = playin.copy()
  playinref[415] = "~"
  bhp,yehp,owie,iframamo=1000,100,0,1.5 
  dang,orang,theows,thereds,thewhites=[],[],[],[],[]
  cutscene,iframes,attackin=False,True,True
  thesymlist,theintlim=['⊿','▲','△','▴','▵'],-1 #was going to be for attack 1 multiple words at once so eh
  upimps,leftside,leftimps,rightside,rightimps,spaced=[135,143,151,159,167,175,183],[134,198,262,326,390,454,518,582,646,710,774,838],[198,390,582,774],[185,249,313,377,441,505,569,633,697,761,825,889],[249,441,633,825],[199,207,215,223,231,239,247,391,399,407,415,423,431,439,583,591,599,607,615,623,631,775,783,791,799,807,815,823]
  turnramp={0:-1,1:-1,2:-1,3:-1,4:-1,5:-1} #:flushed:
  JUSTUPIT,kys,itsafirst,hasspidy=False,False,not acheck("LYS"),False #itsafirst first attacking turn, 2.6 spidy cycle
  zeeeee,whereheat,dmgmul,backer=0,0,1,"\033[48;5;235m" #doomsday change this to 0 so like i need it
  noheal,xtreme,bmulti,hell,hell2,cloud9,cancer,nonr=False,False,1,False,False,False,False,False #different modes
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
    'R':'\033[0m','▢':'\033[38;5;51m▢', #player
    '~':'\033[38;5;62m◌'#empty space to move in
  }
  #HELLMODE STUFF
  iinv, ITEM_l_real,ITEM_r_real = ["Apple","Jalepeno"],["Apple","Cherry","Gum","Vanilla Cone","Placebo","Chocolate Cone","Jalepeno","Cheesecake"],["Red Pill","Blue Pill","Heaven's Light","Heaven's Bow","Heaven's Arrow"] #order to view items 
  HEAVEN_LIGHT,HEAVEN_BOW,HEAVEN_ARROW = True,True,True
  #theres gotta be a better way for this
  def up_items():
    return { #distance thing, stats (plus defense, heal etc), description, check (only for the ones at the top, red pill, light etc)
    'Jalepeno': [[[1106, 0], 3, 66, 0],"+75 HP","Scorching hot... A fiery start leads to a smoother end."],
    'Cheesecake': [[[1180, 0], 3, 66, 1],"+100 HP, 2x damage taken next turn","A treat for the tolerant. Not for the lactose intolerant."],
    'Chocolate Cone': [[[1096, 0], 3, 66, 1],"+25 HP, +1 defense!","A dark delight, made for the tough."],
    'Vanilla Cone': [[[1080, 0], 3, 66, 1],"+25 HP, +5 attack!","A coned confection, made for the strong."],
    'Placebo': [[[1088, 0], 2, 66, 1],"Once taken, never forgotten.","A truly effective medicine. Made to decieve, used to rationalize."],
    'Gum': [[[1135, 0], 2, 66, 2],"+25 HP, +defense next turn","A tough chew...  Not the most nutritious, but hard to hurt."],
    'Cherry': [[[996, 997], 2, 66, 2],"+50 HP, +defense next turn","A lucky break, a jackpot of sorts. A quick fix to lost attention."],
    'Apple': [[[1192, 0], 2, 66, 1],"+10 HP","An apple a day keeps the defibrillator away... The first resort."],
    "Heaven's Bow": [[[559, 0], 6, 66, 5],"Delivery. (Part 2/3)","A glow trapped in gold. Limitless potential, yet limited to the gods.",HEAVEN_BOW],
    "Heaven's Arrow": [[[559, 0], 6, 66, 5],"Swift justice. (Part 3/3)","A message straight to the point. Dont give up now!",HEAVEN_ARROW],
    "Heaven's Light": [[[494, 0], 6, 66, 18],"Radiance. (Part 1/3)","A blessing from above, in times of need.",HEAVEN_LIGHT],
    'Red Pill': [[[494, 0], 6, 66, 25],"+15 crit damage, can be heightened...","The sky lights up, replaced with blood red. Once taken, never forgotten.",pill=='r'],
    'Blue Pill': [[[494, 0], 6, 66, 25],"+5 blue shield, can be heightened...","The sky lights up, replaced with a solid blue. Once taken, never forgotten.",pill=='b'],
    "None1":[[[1088, 0], 5, 66, 25],"None","None"],"None2":[[[494, 0], 6, 66, 25],"None","None",True]}
  def up_symbs():
    def_space = "\033[48;5;52m " if pill=="r" else "\033[48;5;17m " if pill=="b" else " "
    def_l, def_g =  "\033[48;5;7m " if HEAVEN_LIGHT else def_space, '\033[48;5;242m ' 
    return  {
      '-':" ",'g' : def_g,
      " " : def_space,
      'o' : "\033[48;5;0m " if not HEAVEN_LIGHT else "\033[48;5;234m ",
      'l' : "\033[48;5;7m " if HEAVEN_LIGHT else def_space,
      's' : "\033[48;5;100m " if HEAVEN_BOW else def_l, #bow string
      'b' : "\033[48;5;226m " if HEAVEN_BOW else def_l, #bow well bow
      'a' : "\033[48;5;231m " if HEAVEN_ARROW else def_l, #arrow shaft
      't' : "\033[48;5;195m " if HEAVEN_ARROW else def_l, #arrow tip
      'A': "\033[48;5;196m " if "Apple" in iinv else def_g, #apple red
      'B': "\033[48;5;131m " if "Apple" in iinv else def_g, #apple brown (stem)
      'L': "\033[48;5;112m " if "Apple" in iinv else def_g, #apple leaf
      'P': "\033[48;5;124m " if pill=="r" else "\033[48;5;27m " if pill=="b" else def_g,#placebo pill
      '=': "\033[48;5;253m " if pill in "br" else def_g,#placebo middle
      'R': "\033[48;5;160m " if "Cherry" in iinv else def_g, #cherry red
      'S': "\033[48;5;64m " if "Cherry" in iinv else def_g, #cheery stem/connector
      'C': "\033[48;5;230m " if "Cheesecake" in iinv else def_g, #cheesecake top
      'c': "\033[48;5;222m " if "Cheesecake" in iinv else def_g, #cheesecake bottom
      'Z': "\033[48;5;162m " if "Cheesecake" in iinv else def_g, #cheesecake strawberry
      'J': "\033[48;5;1m " if "Jalepeno" in iinv else def_g, #jalepeno red
      'H': "\033[48;5;28m " if "Jalepeno" in iinv else def_g, #jalepeno green
      'G': "\033[48;5;207m " if "Gum" in iinv else def_g, #gum pink
      'V': "\033[48;5;255m " if "Vanilla Cone" in iinv else def_g, #vanilla ice cream
      'O': "\033[48;5;94m " if "Chocolate Cone" in iinv else def_g, #chocolate ice cream
      '1': "\033[48;5;215m " if "Vanilla Cone" in iinv else def_g, #vanilla cone
      '2': "\033[48;5;215m " if "Chocolate Cone" in iinv else def_g #choc cone
    }
  pill = " "
  def distance(spot,dist=2,W=52,ex_W=0):
    #top/bottom parts
    if len(spot) == 4 : #splitting up list
      spot,dist,W,ex_W = spot[0], spot[1], spot[2], spot[3]
    spot=[spot,0] if type(spot)==int else spot
    multi = spot[1]>spot[0]
    y = [i for k in [-1,1] for i in range(spot[0]-dist+(W*dist*k)+(W if k==1 and multi else 0) - ex_W,spot[0]+(2 if multi else 1)+dist+(W*dist*k)+(W if k==1 and multi else 0) + ex_W)]
    y.extend(spot[0]+(dist*k)+(W*q)+(int(multi and k==1))+ex_W*k for k in ([-1,1]) for q in range(dist*-1,dist+1))
    return y

  distant = distance([410,500],3,66,-1)
  def printItem(distant=distant):
    upped,fina = up_symbs(),""
    for ind,i in enumerate(ITEMS): #does something, but doesnt actually work
        fina += (upped.get(i,i) if ind not in distant or i=='\n' else "\033[48;5;203m ") + "\033[0m"
    print(fina)
  
  def itemView():
    nonlocal distant,HEAVEN_LIGHT,HEAVEN_ARROW,HEAVEN_BOW,pill
    ITEM_items = up_items()
    pill = "r" if "Red Pill" in iinv else "b" if "Blue Pill" in iinv else " "
    ITEM_l,ITEM_r = f if (f:=[i for i in ITEM_l_real if i in iinv])!=[] else ["None1"],f if (f:=[i for i in ITEM_r_real if ITEM_items.get(i,['','','',False])[3]]) else ["None2"]
    CUR,current = ITEM_l,0
    c()
    while True:
      clearline(5)
      rc()
      distant = ITEM_items[CUR[current]]
      print("(WASD/Arrow keys, enter/z to select, x to exit)",end="")
      printItem(distance(distant[0]))
      print(f"{CUR[current]}({iinv.count(CUR[current])})...    {distant[1]}\n\t{distant[2]}")
      if (g:=getkey1()) in ['a','d',LEFT,RIGHT]:
        current += 1 if current<len(CUR)-1 and g in ['d',RIGHT] else -1 if current>0 and g in ['a',LEFT] else 0
      elif g == 'x':
        break
      elif g in ['w','s',UP,DOWN]:
        CUR = ITEM_r if g in ['w',UP] else ITEM_l
        current = 0
      elif g==ENTER:
        sound("YSKYSN/iselect.wav",True,"bep",2.5)
        if "None" not in CUR[current]:
          pass #actually use
    c()
      

  stats4nerds={'turns':0,'speak':0,'magic':0,'heal up':0,'kys':0,'yskysn heals':0,'dream mask':0,'rusty mask':0,'hockey mask':0,'doctors':0,'damage taken':0,'useless turns':0}
  def mode(data:list=[]):
    if '22' in data: return "Normal" #quick normal loading moment
    LEAN,NOHIT,NOHEAL,HP2X,CANCER,CLOUD9,HELL,HELL2 = \
    xtreme or '16' in data, nonr or '94' in data, noheal or '12' in data, bmulti==2 or '3' in data,'50' in data,cloud9 or '49' in data,hell or '64' in data, hell2 or '65' in data
    return f'\033[38;5;{"88" if (e:=all([LEAN,NOHIT,HP2X])) else "0" if HELL or HELL2 else "99" if (LEAN and NOHIT) or CANCER else "171" if LEAN or CLOUD9 else "202" if HP2X else "194" if NOHIT else "7"}m'+\
      ("Hell." if HELL else "Doomsday." if e else "Cloud 9." if cloud9 else "Cancer." if (LEAN and NOHIT) or CANCER else f"NO HIT{'+' if any([LEAN,HP2X]) else ''}" if NOHIT else\
        f"LEAN{'+' if any([NOHEAL,HP2X]) else ''}" if LEAN else f"NO HEALS{'+' if HP2X else ''}" if NOHEAL else "2x HP" if HP2X else "Normal")+\
        "\033[0m"

  if not itsafirst:
    c()
    #new select!!!!!!!
    
    SAVE,modes_allow,sets_allow,save_allow = ['','','','',''],['0','1','2','3'],['0','1','y'],['x','y'] #set up list of things you can see/do in main menu
    for i,casee in zip(['4','5','y','x','z',"-"],[acheck("LEAN"), all(acheck(i) for i in ['LEAN','True Chad','YSLYSN','Double takedown']),True,True,True,(SAVE:=acheck("s"))[0][0]!=False]):
      if casee: modes_allow.append(i)
    
    
    #special printing things
    special_ends,special_starts = ['^','0','1','2','4'],{";":both,"}":"Hell" not in mode(SAVE[0])}
    def blinks(): return {'a':bmulti==2,'b':nonr,'c':noheal,'d':xtreme,'e':cloud9,'f':hell,'&':not skipintro,':':both}
    def endit(ending): #update this with special_ends!!!
      return str({"^":f"< {centerit} >","0":mode(SAVE[0]),"1":SAVE[1],"2":SAVE[2],"4":SAVE[4]}.get(ending,''))

    #if there is a colorcode, add on that # ofchars to the left offset
    def CENTEROFF(st):
      if '\033' not in st: return 0
      else:
        count,fina = 0,0
        while (count:=st.find('\033',count))!=-1:
          fina += len(st[count:(count:=st.find('m',count))])+1
        return fina
    
    def prints(e,width='default',butting=False,addon_mode=False,JUSTPRINT=False): #addon_mode cause color codes make centering bad
      """Use JUSTPRINT to simply center/right/left the text"""
      global both,skipintro
      nonlocal curlist
      if type(width)==str or width<10: width=os.get_terminal_size().columns
      for i in e.split("\n"):
        if i.strip()=='':
          print()
        elif (not JUSTPRINT and i[-1]!="#") and (not butting or (i[0] in curlist+['#'] or (special_starts.get(i[0],False)) or i[0].isupper())):
          Q = i[1:-1]+endit(i[-1]) if butting and i!='' and i[-1] != " " else i
          cleft = CENTEROFF(Q+(eval(addon_mode) if addon_mode!=False else '')) + (1 if butting and i!='' and i[-1]!=" " else 0) #definitely brokenfor right lol
          if (f:=CENTEROFF(Q)) > 0: cleft -= f*2 #stich fix :heart:
          print((seledchar:="\033[48;5;5m" if butting and i!='' and curlist[cur] == i[0] else '') + \
            ((f"{Q:>{width//2+(len(Q))//2-(3 if addon_mode=='mode' else 0)}}" if '|' in i or addon_mode else f"{Q:^{width-cleft}}") if centerit=='center' else f"{Q:>{width-(len(eval(addon_mode))-cleft if addon_mode!=False else 1)}}" if centerit=='right' else Q) +\
            ('' if not butting or i[-1] in [" "]+special_ends else (s(blinks().get(i[-1],False),False))+seledchar+(" "*(width//2-len(i)//2 if centerit=='center' else 0 if centerit=="right" else width-len(i)-1)))+(mode()+("    " if centerit!='right' else '') if addon_mode=="mode()" else r))
        
        elif JUSTPRINT or (i[-1] == "#" and i[0] in curlist+['#']):
          g = i if JUSTPRINT or i[-1] != "#" else i[1:-1]
          print(("\033[48;5;5m" if not JUSTPRINT and butting and curlist[cur] == i[0] else '') \
              + (f"{g:^{width}}" if centerit=='center' else f"{g:>{width}}" if centerit=='right' else g) + "\033[0m")

    #extra space (" ") after word means its 100% normal, a hashtag ("#") is for ones that can be selected but not achiev
    buts = '\n-Save Data#\n\n0Double Boss HP | a\n\n1No hit (1 hp)  | b\n2     No heals  | c\n\n3Extreme mode   | d\n\n4CLOUD 9        | e\n5Hell.          | f\n\nySettings#\nxExit#\nzContinue#\n;ALTER          | :\n'
    buts_settings = """\nSettings \n\n0Center mode: ^\n1Show introduction text: | &\n\nyExit Settings#\n"""
    buts_save = """Save Data \nWill be overidden if you start another game! \nLoaded game will instantly start! \n\n#Mode: 0\n#Your hp: 1\n#Boss hp: 2\n}Spidy?: 4\n\nxLoad Save#\nyBack#\n"""
    SAVEITPLEASE, cur,curlist = False, 0, modes_allow #saveitplease = load the save after it breaks or something idk what im doing
    print("\033[38;5;88m")
    prints("YSKYSN\033[0m recognizes you...\nIt's as if he is expecting something.\nUse Up/Down to move, Z/Enter/Left/Right to select!\n\n",'','','',True)
    prints("Selected mode: ",'def',False,"mode()")
    prints(buts,'default',True)
    while (t:=getkey1()):
      if t in ['w','s',UP,DOWN]:
        sound('YSKYSN/sel.wav',True,"sel",.5)
        cur+=1 if t in ['s',DOWN] else -1
        cur = 0 if cur==len(curlist) else len(curlist)-1 if cur==-1 else cur
      elif t in [ENTER,LEFT,RIGHT,'z','a','d']:
        sound('YSKYSN/sel.wav',True,"sel",.5)
        if curlist==modes_allow:
          (bmulti:=2 if bmulti==1 else 1) + (bhp:=2000 if bhp==1000 else 1000) if (g:=curlist[cur])=='0' else (nonr:=not nonr) + (noheal:=nonr) if g=='1' else (noheal:=not noheal) if g=='2' and not nonr else (xtreme:=not xtreme) if g=='3' else (cloud9:=not cloud9) if g=='4' else (hell:=not hell) if g=='5' else (curlist:=sets_allow) + [c(),(cur:=0)] if g=='y' else (curlist:=save_allow) + [c(),(cur:=0)] if g=='-' else ''
          if g=='x':
            return c()
          if g=='z':
            break
        elif curlist==sets_allow:
          (curlist:=modes_allow) + [c(),(cur:=0)] if (g:=curlist[cur])=='y' else (centerit := centermodes[(ind:=centermodes.index(centerit))-(1 if t in [LEFT,'a'] else -1 if ind!=len(centermodes)-1 else len(centermodes)-1)]) + c() if g=='0' else (skipintro:=not skipintro) if g=='1' else ''
        elif curlist==save_allow:
          (curlist:=modes_allow) + [c(),(cur:=0)] if (g:=curlist[cur])=='y' else (SAVEITPLEASE := True)
          if g=='x':
            break
      if cloud9 or hell:
        nonr,bmulti,bhp,xtreme,noheal,cloud9 = False,1,1000,False,False,not hell
      print("\033[H",end="\n"*6)
      if curlist==modes_allow:
        prints("Selected mode: ",'def',False,"mode()")
      prints(buts if curlist==modes_allow else buts_settings if curlist==sets_allow else buts_save,'f',True)
    c()
    if not SAVEITPLEASE: #loading save things, maybe use monke print to make it look cool? (that would be damn hard)
      if hell:
        printt(["....","You know what you've done.","Instead of giving in, or merely fighting back, you decided to end this, once and for all.","\033[38;5;88mGood luck mortal. You rats always need it.\033[0m"],[3,1,2,.03])
        print("[Any key to continue to hell. Good luck.]")
      elif cancer:
        printt(["As he sips his lean, you start to tremble.","\033[38;5;88mHe\033[0m stands over you, entirely omniscient...."],[2,2])
        print("(No heals/Lean mode activated! Your hp: 1. You asked, I delivered. This IS possible, \033[38;5;16mthere are new tools to help.\033[0m)")
        xtreme,nonr,noheal = True,True,True
      elif cloud9:
        printt(["A single sip of the stuff sends you higher than you've ever dreamt of.....","The world is spinning, spinning!"],[2,.03])
        xtreme = True
      elif xtreme and nonr and bmulti==2:
        printt(["There's really no hope left.","\033[38;5;88mThere's only time to suffer."],[2,.03])
        print("\033[0m(Doomsday activated! Good luck!!!!)")
      else:
        if nonr:
          printt(["You feel....."+r+" meaningless.","At any moment, your life can be worth nothing."],[1,1])
          print("\033[38;5;130m[No hit mode enabled!]",end=slepy(1))
        elif noheal:
          printt('The lightning feels \033[38;5;88mgreat\033[0m. You feel like giving in at any time...',)
          print('\033[38;5;124m[Healing has been disabled!]')
        if xtreme:
          printt("With one chug, his face grows even brighter...",)
          print("(\033[38;5;171m[Extreme mode enabled!]",end=slepy(1))
        if bmulti==2:
          printt('The window opens, letting in even more lightning.')
          print("[\033[38;5;88mYSKYSN\033[0m HP x2!]",end=slepy(1))
        if bmulti!=2 and not xtreme and not noheal:
          printt('\033[38;5;88mYSKYSN\033[0m looks back in anger. He expected more.')
          print("[Normal mode active!]")
      anykey(not hell)
      yehp = 1 if nonr else 100
    else:
      noheal, xtreme, bmulti, nonr, hell, hell2, cloud9, cancer, yehp, bhp, stats4nerds, hasspidy = \
      '12' in SAVE[0],'16' in SAVE[0], 2 if '3' in SAVE[0] else 1, '94' in SAVE[0], '64' in SAVE[0], '65' in SAVE[0], '49' in SAVE[0],'50' in SAVE[0],\
      SAVE[1],SAVE[2],SAVE[3],SAVE[4]
      print("Game loaded!")
      anykey()
  elif (SAVE:=acheck("s")) != False and SAVE[0] != False: #prevent it from erroring!!
    print(f"\033[38;5;153mSave data detected! (l to load, any other key to overide and start fight!)\033[0m\n\tMode: Normal{r}\n\tYour hp: {SAVE[1]}\n\tBoss hp: {SAVE[2]}\n\tSpidy?: {SAVE[4]}\n\tOther stats: Would take up too much space rn. L.")
    time.sleep(.5)
    if getkey1()=='l':
      print("\033[38;5;88mYSKYSN\033[0m smiles.\n(Loaded game!)")
      noheal,xtreme,bmulti,nonr,hell,hell2,cloud9,cancer,yehp,bhp,stats4nerds,hasspidy,turnramp=SAVE[0] not in ['16','3','22','64','61','49'],SAVE[0] in ["16",'49','50'],2 if SAVE[0]=="3" else 1,SAVE[0] not in ['49','50','16','3','12','22','64','61'],SAVE[0] in ['64','61'],SAVE[0]=='61',SAVE[0]=='49',SAVE[0]=='50',SAVE[1],SAVE[2],SAVE[3],SAVE[4],SAVE[5]
      anykey()
  else:
    pass #stuff for normal mode
  if cancer:
    for i in ['shields','reds','red bulls']: stats4nerds[i]=0
  #setting up colored stuff
  coloreddict['r']='\033[48;5;52m ' if hell else '\033[48;5;253m ' if noheal else '\033[48;5;91m ' if xtreme else coloreddict['r']
  if nonr: coloreddict['n']='\033[48;5;52m '
  if cloud9: coloreddict['o'] = '\033[48;5;91m '
  if cancer: coloreddict['w'] = '\033[48;5;5m '
  if hell:
    coloreddict['n'],coloreddict['g'],coloreddict['w'] = "\033[48;5;0m ",'\033[48;5;52m ','\033[48;5;90m '
    #hell mode 2: coloreddict['W'] = '\033[48;5;1m '
  if xtreme and bmulti==2 and nonr: #doomsday
    for thing,col in zip(['-','_','g','r','G','n','B','b','w','W','m'],['0','0','0','0','232','232','232','232','34','52','232']):
      coloreddict[thing] = f"\033[48;5;{col}m "
    backer = "\033[48;5;0m"
  
  
  #------------------------- End Save/load data stuff ------------------------------
  
  
  buttons='''
   !╓─────────╖  R @╓─────────╖      R #╓─────────╖    R$╓─────────╖
   !║  SPEAK  ║ R  @║  '''+("MAGIC" if not hell else "PRAY ")+'''  ║      R #║ '''+("HEAL UP" if not hell else "ITEM  ")+''' ║   R $║   KYS   ║
   !╙─────────╜ R  @╙─────────╜     R  #╙─────────╜  R  $╙─────────╜
  '''
  #thresholds: 600, 300
  #for health: 750, 500, 250
  
  #optimize these sayings, this looks hella spaget
  saying = ['Why are you here, just to worship me?', 'You serve ZERO purpose.', 'YSKYSN hates the crowd, YSKYSN kills the crowd.', 'There is no more crowd.', 'Lightning crackles all around you.', 'YSKYSN is getting mad...', "Get a life.", 'But something about him seems less menacing.', 'YSKYSN looks very tired...', 'An ending in reach.', 'Peace soon to come.']
  HELL_s = ["It's time.|Another soul captured.|The start of the end.|The last story.|To end it all.|A maze impossibly complex.","Make it last.|Chaos from below.|Sparks fly around him.","Could it be possible?|Stay alive.|Adapt to the lightning.","He hasn't broken a sweat.|Still going strong?|This new world is his.","Unfathomable rage.|Did you want to be here?|Sonic boom!","Halfway through?|A fragment of light can be seen...|The power of words compels him!",""] #Completed: 0,1,2,3,4,5 ,6,7,8,9
  def up(gu=False):
    print("\033[H",end="\n"*14)
    if gu:
      printman(playin,False)
      if not nonr: 
        print('\n\033[38;5;'+str(93-(5-(yehp//20)))+\
          f'm{("Shields: "+str(stats4nerds["shields"]) if cancer else "")+"  Health - "+str(yehp)+("  RBs: "+str(stats4nerds["red bulls"]) if cancer else "  ")+("DMG: "+str(dmgmul) if both else ""):^63}')
      
  def turn2(ab,lol):
    nonlocal turnramp
    if not cloud9:
      for i in turnramp.keys(): #disables ramping for the uh bad ones
        if i!=ab and lol==ab:
          turnramp[i]=-1
        elif i!=ab and turnramp[i]>-1:
          turnramp[i]-=1
    turnramp[ab]+=(1 if not xtreme or cloud9 else random.randrange(1,3) if not cloud9 else random.randint(1,3))
  def danger(space,nubi=1,timee=2):
    nonlocal JUSTUPIT,dang
    if type(nubi)==int:
      for i in range(0,nubi):
        dang.append(space-i if space in rightside else space+i if space in leftside else space+(64*i))
    else:
      for i in nubi:
        dang.append(i)
    JUSTUPIT=True
    time.sleep(timee)
    dang=[];JUSTUPIT=True
    return -1 if space in rightside else 1
  def more(theone,amoint,symb,dirt=1,timri=.5): #space to place, amount more, symbol to place, direction going (1/-1), time inbetween moves
    nonlocal playin,theows,JUSTUPIT,thereds
    if type(theone)!=list:
      for ib in range(amoint):
        if playin[theone+(ib*dirt)] not in ['▢','g','w','\n','R']:
          theows.append(theone+(ib*dirt))
          if symb=='r':
            thereds.append(theone+(ib*dirt))
          playin[theone+(ib*dirt)]=(symb if (ib==0 and dirt==1 or ib==amoint-1 and dirt==-1 or symb=='r') else 'x')
        else:
          if symb!='r':
            for ie in range(ib):
              playin[theone+(ie*dirt)]=playinref[theone+(ie*dirt)]
            return 'hit' if playin[theone+(ib*dirt)]=='▢' else 'end'
          else:
            thereds.append(theone+(ib*dirt))
            theows.append(theone+(ib*dirt))
    else:
      for i in theone:
        theows.append(i)
        thewhites.append(i)
        if playin[i]!='▢':
          playin[i]=symb
    JUSTUPIT=True
    time.sleep(timri)
    if type(theone)!=list:
      for ib in range(amoint): #undo the stuff
        if playin[theone+(ib*dirt)]!='▢': #no killing yourself >:(
          playin[theone+(ib*dirt)]=playinref[theone+(ib*dirt)]
        theows.remove(theone+(ib*dirt))
    else:
      for i in theone:
        if playin[i]!='▢':
          playin[i]=playinref[i]
        theows.remove(i)
        thewhites.remove(i)
  def returnit(h=False):#True=in left, False = in right
    return ((198 if h else 249) if (e:=playin.index('▢')) in [199,207,215,223,231,239,247] else (390 if h else 441) if e in [391,399,407,415,423,431,439] else (582 if h else 633) if e in [583,591,599,607,615,623,631] else (774 if h else 825))
  
  def upit():
    nonlocal JUSTUPIT
    JUSTUPIT = True
  
  # -------------------------------------------------------- Attacks --------------------------------------------------------------
  
  #attack vars
  phase1li= ["BURN"]*5 + ["KYSN"] * 4 + ["DIE."]*3 + ["HATE"]*3 + ["CRY."]*3 + ["STOP"]*2 + ["HAHA","HEHE",'hihi','LMAO','XDXD','BUMB','LUCI'] #words
  RED = False #red bull
  def attack(lol=9): #find attack
    nonlocal dmgmul,playin,attackin,theintlim,coloreddict,iframes,yehp,orang,theows,owie,turnramp,cutscene,iframamo,thereds
    time.sleep(1)
    if both: dmgmul *= random.choice([i/10 for i in range(8,26)])
    if yehp<1: return
    
    lol2=99 if not cloud9 else random.randrange(0,7)
    
    if bhp in [420,69,666]:
      yehp=999999
      c()
      cutscene=True
      time.sleep(1)
      c()
      print('\033[38;5;88mYSKYSN\033[0m HP: '+str(bhp))
      time.sleep(1)
      printt("\033[38;5;196mYou have activated his trap card...."+r)
      time.sleep(2)
      cutscene=False
      c()
      printman(YS[0:960])
      upit();time.sleep(2)
      sound("YSKYSN/KYSAFE.wav")
      iframamo=.25
      yehp+=round(690*dmgmul) #even though this is almost perfect, theres a way to cheese it...
      owie=20
      for i in range(0,69):
        if yehp>40:
          orang=spaced.copy()
          orang.remove(random.choice(orang))
          upit();time.sleep(.1)
          for i in orang:
            theows.append(i)
          upit();time.sleep(.1)
          theows=[];upit()
      yehp,iframamo,attackin=1,1.5,False
      return
    elif (bhp>=900*bmulti and not cloud9) or lol==0 or lol2==0:#phase 1, words come frop left/right
      turn2(0,lol)
      owie=5+turnramp[0]
      
      for i in range(random.randrange(7,(10 if lol!=0 else 15)+turnramp[0])):
        kf,rw=random.choice(random.choice([leftimps,rightimps])),((1 if lol!=0 else .25)-(.25 if xtreme else 0)-turnramp[0]/10)
        tru = danger(kf,4,rw if rw>0 else 0) #returns the direction its gonna go (-1 or 1)
        metan=thesymlist[(theintlim:=theintlim+1)] #this and thesymlist were for if i was gonna make many words at once which i never did lol (maybe some day!!!)
        coloreddict[metan]=random.choice(phase1li)
        h4='hehehaha'
        while h4 not in ['end','hit']:
          hei=(.4 if lol!=0 else .2)-(.1 if xtreme else 0)-turnramp[0]/40/(3 if xtreme else 1)
          h4=more(kf,4,metan,tru,hei if hei>.1 else .1)
          kf+=(8*tru)
        if h4=='hit' and not iframes:
          damage(((5 if lol!=0 else 10)+turnramp[0]+(2 if xtreme else 0))*dmgmul)
        theintlim-=1
    
    elif (bhp>=750*bmulti and not cloud9) or lol==1 or lol2==1:#phase2, random spaces
      turn2(1,lol)
      owie=(8 if lol!=1 else 10)+(5 if xtreme else 0)+turnramp[1]
      for i in range(random.randrange((5 if lol!=1 else 8)+turnramp[1],(9 if lol!=1 else 14)+turnramp[1])):
        if yehp>0:
          orang=[]
          for i in range(random.randrange((10 if lol!=1 else 15),(17 if lol!=1 else 21))):
            orang.append(random.choice(spaced))
          upit()
          time.sleep((1.5 if not xtreme else .75)-(.75 if lol==1 and not xtreme else .25 if lol==1 else 0))
          for i in orang:
            theows.append(i)
          upit()
          time.sleep((1 if lol!=1 else .25)-(.2 if xtreme else 0))
          theows,orang=[],[];upit()
          wer=(1 if lol!=1 else .5)-(.5 if xtreme else 0)-turnramp[1]/20
          time.sleep(wer if wer>0 else 0)
    elif (bhp>=600*bmulti and not cloud9) or lol==2 or lol2==2:#phase3, lasers up/down
      turn2(2,lol)
      owie=(10 if lol!=2 else 15)+(5 if xtreme else 0)+turnramp[2]
      for i in range(random.randrange((7 if lol!=2 else 10),(10 if lol!=2 else 13)+turnramp[2])):
        if yehp>0:
          spacer=random.choice(upimps)
          danger(spacer,12,(1 if lol!=2 else .6)-(.3 if xtreme else 0))
          more(spacer,12,'r',64,(.9 if lol!=2 else .5)-(.3 if xtreme else 0))
          time.sleep((1 if lol!=2 else .25)-(.2 if xtreme else 0))
          thereds=[]
    elif (bhp>=500*bmulti and not cloud9) or lol==3 or lol2==3: #phase3.2, lasers up/down but faster (MAYBE CHANGE TO 2 lasers??)
      turn2(3,lol)
      owie=(10 if lol!=3 else 13)+turnramp[3]
      for i in range(random.randrange((0 if lol!=3 else 3)+(9 if not xtreme else 12),(0 if lol!=3 else 5)+(15 if not xtreme else 19)+turnramp[2])):
        if yehp>0:
          spacer=random.choice(upimps) #for this attack doesnt change for random one, cause its basically the one above but harder (at least not much)
          danger(spacer,12,.5-(.2 if xtreme else 0))
          more(spacer,12,'r',64,.4-(.25 if xtreme else 0))
          time.sleep((.5 if lol!=3 else .25)-(.25 if xtreme else 0))
          thereds=[]
    elif (bhp>=400*bmulti and not cloud9) or lol==4 or lol2==4: #phase 4, lasers on rows
      turn2(4,lol)
      owie=(15 if lol!=4 else 20)+(5 if xtreme else 0)+turnramp[4]
      for i in range(random.randrange((7 if lol!=4 else 13),(14 if lol!=4 else 18))):
        if yehp>0:
          spacer=random.choice(random.choice([leftimps,rightimps]))
          surt=danger(spacer,51,(.75 if lol!=4 else .5)-(.2 if xtreme else 0))
          more(spacer,51,'r',surt,(.5 if lol!=4 else .3)-(.2 if xtreme else 0))
          time.sleep((.5 if lol!=4 and not xtreme else 0))
          thereds=[]
    elif (bhp>=100*bmulti and not cloud9) or lol==5 or lol2==5:
      turn2(5,lol)
      owie=13+(5 if xtreme else 0)+turnramp[5]
      for i4 in range(random.randrange((15 if lol!=5 else 20),(25 if lol!=5 else 30))):#phase 5, lightning bolts come from both sides to your space using algorithm thing
        ni1,ni2=random.choice(leftimps),random.choice(rightimps)
        pos=whereheat #so 0% chance for error lol (whereheat is player pos)
        lists={ni1:[],ni2:[]}
        for i in [ni1,ni2]:
          hei=abs(returnit(i in leftside)-i)//64
          wid=abs((i+(hei*64) if pos>i else i-(hei*64))-pos)
          muli=(-1 if i in rightside else 1)
          try:
            nuqe=i
            lists[i].append(i)
            refn=wid//hei*hei
            for i2 in range(hei):
              for i3 in range(wid//hei):
                nuqe+=(1*muli)
                lists[i].append(nuqe)
              if wid>refn:
                nuqe+=(1*muli)
                refn+=1
                lists[i].append(nuqe)
              nuqe+=(-64 if i>pos else 64)
              lists[i].append(nuqe)
          except:
            for id in range(1,wid+1):
              lists[i].append(i+(id*(-1 if i in rightside else 1)))
        hib=lists[ni1]
        for i in lists[ni2]:
          hib.append(i)
        danger(0,hib,(.75 if lol!=5 else .5)-(.4 if xtreme and lol!=5 else .25 if lol==5 and xtreme else 0))
        more(hib,0,'w',1,(.4 if lol!=5 else .25) - (.1 if xtreme else 0))
    else: #phase 6, random attacks
      for i in turnramp.keys():
        turnramp[i]=-1
      attack(random.randrange(0,6))
    attackin=False
  
  
  def printman(yt,l=True, ever = ""): #find print
    YY,final='',''
    if cancer and stats4nerds['shields']>0:
        YY='\033[48;5;21m'
    for coi,i in enumerate(yt):
      final += ever
      if i in coloreddict.keys() and l or (not l and (i in thesymlist or i in ['!','@','#','$','R','w','_','g','~','▢','r','x'])):
        if coi not in dang and ((coi not in theows and coi not in orang) or i not in ['~','▢']) or l:
          final += (backer+(YY if i=='▢' else '') if (i in ['~','▢'] or i in thesymlist) else '')+coloreddict[i] + (r if ('!' not in yt and i!='Q') else '')
        else:
          if coi in dang:
            if i not in ['~','▢']:
              final += '\033[48;5;88m '
            else:
              final += '\033[48;5;88m'+(YY if i=='▢' else '')+ coloreddict[i] + r
          elif coi in theows:
            final += backer+(coloreddict['r'][:-1] if coi in thereds else coloreddict['w'][:-1] if coi in thewhites else '')+(coloreddict[i]+(YY if i=='▢' else '') if i!='~' else  coloreddict['w'] if coi in thewhites else '\033[38;5;88m◌') + r
          else:
            final += backer+"\033[38;5;208m"+{'~':'◌','▢':'▢'+YY}[i]+r
      else:
        final += i
    print(final)
  def movi(dire): #8 left to right, 192 up/down
    nonlocal playin
    beez=playin.index('▢')
    playin[beez]='~'
    if dire in ['d',RIGHT] and beez not in [247,439,631,823]:
      playin[beez+8]='▢'
    elif dire in ['w',UP] and beez not in [199,207,215,223,231,239,247]:
      playin[beez-192]='▢'
    elif dire in ['a',LEFT] and beez not in [199,391,583,775]:
      playin[beez-8]='▢'
    elif dire in ['s',DOWN] and beez not in [775,783,791,799,807,815,823]:
      playin[beez+192]='▢'
    else:
      playin[beez]='▢'
      return 'bruh'
    return 'ok'
  def damage(amo):
    nonlocal iframes,yehp,JUSTUPIT,stats4nerds
    if not iframes:
      iframes=True
      sound("YSKYSN/hurt.wav")
      if not cancer:
        yehp-=round(amo)
      else:
        if stats4nerds['shields']>0:
          stats4nerds['shields']-=1
        elif stats4nerds['red bulls']>0:
          stats4nerds['red bulls']-=1
          sound('YSKYSN/break.mp3')
          THREAD(target=redframes).start()
        else:
          yehp-=round(amo)
      JUSTUPIT=True
  def OWW():
    nonlocal owie
    while attackin and yehp>0:
      try:
        if playin.index('▢') in theows:
          damage(round(owie*dmgmul))
        time.sleep(.04)
      except:
        time.sleep(.1)
  def redframes():
    nonlocal iframes,coloreddict,RED,JUSTUPIT
    RED,iframes,JUSTUPIT,coloreddict['▢']  = True,True,True,'\033[38;5;1m▢'
    time.sleep(5)
    iframes,RED,coloreddict['▢'],JUSTUPIT=False,False,'\033[38;5;51m▢',True
    return
  def iframe():
    nonlocal iframes,coloreddict,RED,JUSTUPIT
    while attackin and yehp>0:
      while not iframes or RED:
        time.sleep(.1)
      coloreddict['▢'],JUSTUPIT='\033[38;5;225m▢',True
      time.sleep(iframamo)
      coloreddict['▢']='\033[38;5;51m▢'
      iframes,JUSTUPIT=False,True
  def heal(at,playering=True): #a lil spaget but who cares
    return ((0 if yehp > 100 else 100 - yehp if yehp >= 100 - at else at) if not noheal else 'no') if playering else (1000*bmulti-bhp if bhp>=(1000*bmulti-at) else at)
  
  c()
  
  
  selection,turn,theender,pause,noballs,hddict=0,'gamer',False,False,['!','@','#','$'],{4:'\033[38;5;46m',3:'\033[38;5;46m',2:'\033[38;5;6m',1:'\033[38;5;166m',0:'\033[38;5;196m'}
  
  #start yskysn
  music("yskysn","YSKYSN/smiling.mp3" if cancer or hell else "YSKYSN/election.mp3" if xtreme else "YSKYSN/tears.mp3" if nonr else "YSKYSN/unwave.mp3",True)
  while bhp>0 and (yehp>0 or iframamo!=1.5):
    coloreddict['Q']=hddict[bhp//(250*bmulti)]
    pickin=True
    if turn!='gamer':
      print("\033[H",end="")
      printman(YS[0:960])
    if turn=='gamer':
      c()
      while pickin:
        print("\033[H",end="")
        printman(YS)
        printman('o                      QYSKYSN HP: '+f"{bhp:>5}"+'                       o\n'+'o'*63,True,coloreddict['-'][:-1])
        j=10 - bhp//(100*bmulti) #find saying things
        print("\n"+("\033[38;5;180m" if not (hell or cancer) else '')+f'{"?" if xtreme and bhp==2 and nonr else saying[j] if not (hell or cancer) else "Cancer." if cancer else random.choice(HELL_s[j].split("|")) if not hell2 else "This is it. The end.":^63}'+r)
        print(f"\n{'[A/D to move, Z to select, N = stats, P = Toggle music]':^63}\n{'[C to reset screen, l = leave, game saves!]':^63}")
        print(f'\033[38;5;1m{"[Spidy]":^63}'+r if hasspidy else "")
        
        coloreddict[noballs[selection]]='\033[38;5;177m'
        
        print(f"\033[38;5;79m{'Health - '+str(yehp):^63}")
        printman(buttons,False)
        zeeeee = stats4nerds['rusty mask']*20
        
        achieve("s",[[i for i,y in zip(['22','3','16','12','94','49','50','64','65'],[not any([bmulti==2,xtreme,noheal,cloud9,cancer,hell]),bmulti==2,xtreme,noheal,nonr,cloud9,cancer,hell,hell2]) if y],yehp,bhp,stats4nerds,hasspidy,turnramp])
        wee=getkey1() #yskysn input (INPUT NPUT oiDWNIOWNDJKFdkkfnkalKWMDLKWmd)
        if wee in [RIGHT,LEFT,'a','d']:
          coloreddict[noballs[selection]]='\033[38;5;174m'
        if wee in [LEFT,'a']:
          selection -= 1
        elif wee in [RIGHT,'d']:
          selection += 1
        elif wee=='c':
          c()
        elif wee in ['-','=','+']:
          setvolume(wee)
        elif wee=='p':
          pause=not pause
          Music.pause() if pause else Music.unpause()
        elif wee=='n':
          c()
          s4=stats4nerds
          print(r+'\n----------------\nStats for nerds:\n\n\033[38;5;82m\nHealth: '+str(yehp)+'\nBoss Health: '+str(bhp)+'\nTotal Turns: '+str(s4['turns'])+'\nTotal Speaks: '+str(s4['speak'])+'\nTotal Magics: '+str(s4['magic'])+'\nTotal Heal Ups: '+str(s4['heal up'])+'\nTotal KYS: '+str(s4['kys'])+'\nTotal Dream Masks: '+str(s4['dream mask'])+f'\n{"Total Hockey Masks" if not cancer else "Total Shields"}: '+str(s4['hockey mask'])+("\nShields avaliable: "+str(s4['shields'])+'\nTotal Red Bulls: '+str(s4['reds'])+"\nRed bulls available: "+str(s4['red bulls']) if cancer else "")+'\nTotal Rusty Masks: '+str(s4['rusty mask'])+'\nTotal Doctor\'s Kits: '+str(s4['doctors'])+'\nTotal YSKYSN Heals: '+str(s4['yskysn heals'])+'\nTotal Damage Taken: '+str(s4['damage taken'])+'\nTotal Useless Turns: '+str(s4['useless turns'])+r+'\n----------------')
          anykey()
          c()
        elif wee=='i': #item view testing
          itemView()
        if wee in [ENTER,'z','l']:
          pickin=False
          theender = wee=='l'
        if selection==4:
          selection=0
        elif selection==-1:
          selection=3
      clearline(11)
      print(r)
      if theender:
        pass
      elif selection==0: #attack
        stats4nerds['speak']+=1
        damdan=random.randrange(40,101)
        printt(['A'+random.choice([' loving',' graceful',' caring',' thoughtful','n emotional',' kind',' heartfelt',' cool'])+' remark makes \033[38;5;88mYSKYSN'+r+' feel a little more love...',('Just a small bit though...' if damdan<60 else 'It had some effect..' if damdan<74 else 'He seems to have felt that...' if damdan<90  else 'You hit him in a sensitive spot...')],[2,.03])
        print(f'\033[38;5;{26 if damdan>50 else 32 if damdan>60 else 38 if damdan>70 else 44 if damdan>80 else 50 if damdan>90 else 135}m('+str(damdan+zeeeee)+' damage dealt!)'+r)
        bhp -= damdan + zeeeee
      elif selection==1: #magic
        stats4nerds['magic']+=1
        printt("If only you were a wizard...",1)
        theeven=random.randrange(0,6) #4 options?
        while theeven==1 and (hasspidy and not cancer):
          theeven=random.randrange(0,6)
        if theeven in [0,4,(2 if cancer else 6)]:
          printt("You spot a mask on the floor...",2)
          gret=random.randrange(0,3)
          if gret==0 and not cancer:
            stats4nerds['dream mask']+=1
            printt(["A completly white one, with a slight smile on it.","You suddenly feel like a cheater...."],[.03,.03,1])
            print('\033[38;5;123m(Health doubled!)\n(Thats what the point of the mask is)\033[0m')
            yehp=yehp*2
          if gret in [1,3]:
            stats4nerds['rusty mask']+=1
            printt(["It's a rusty metal mask, with a slight hint of blood...","Much to old to wear, but it sure looks cool..."],[2,.03,.03])
            print('\033[38;5;202m(Speech power permanently +20!)\033[0m')
          if gret in [2,4,0 if cancer else 4]:
            stats4nerds['hockey mask']+=1
            if not cancer:
              printt(["It's a big hockey mask.","Seems big enough to help for a little..."],[2,.03])
              print("\033[38;5;98m(Halved damage taken next attack!)\033[0m")
              dmgmul=.5
            else:
              stats4nerds['shields']+=1
              printt(["A pink one! Looks like a very chubby face...","Seems to be able to absorb a hit...."],[2,.03])
              print("\033[38;5;26m+1 Shield!\033[0m")
        elif theeven==1: #spiderman is that you
          if not hasspidy:
            printt(["Suddenly a man in a red suit breaks through the wall...","Spiderman is that you??/1?!?!?","He leaves just as fast as he came.",'Seems like he forgot something...'],[2,2,1,1])
            hasspidy=True
            print("\033[38;5;1m(Spidy bot obtained!)\033[0m")
          else:
            Music.pause()
            printt(["What is this? A red bull?","You start floating??","...."],[2,1,1])
            time.sleep(2)
            Music.unpause()
            clearline(3)
            printt("Never mind, I can confirm this is a canon event.",2)
            print("(+1 life! After dying, become automatically invincible for 5 seconds! Red bull gives you wings.)")
            stats4nerds['reds']+=1
            stats4nerds['red bulls']+=1
        elif theeven in [(2 if not cancer else 6),5]: #funny (defib)
          stats4nerds['doctors']+=1
          printt(['Suddenly, a full doctors kit appears.',"It is loaded with a military grade med-kit, a defibrillator, medical gause, and much more.","Luckily, there are a few band-aids® nearby that useless set."],[1,2,.03])
          yehp += q if type(q:=heal((40 if not xtreme else 30))) == int else 0
          print('\033[38;5;123m(Healed '+str(q)+' hp!)')
          if q=='no':
            print("\033[38;5;88m(The lightning prevents it.)"+r)
          elif q<10:
            print('(How useful...)')
          if q in ['no',0]:
            stats4nerds['useless turns'] += 1
        elif theeven==3: #heal him
          stats4nerds['yskysn heals'] += 1
          if not cloud9:
            printt("Suddenly the thunder outside gets even more intense...",2)
            printt("His eyes crackle even brighter.")
            print('(\033[38;5;88mYSKYSN\033[0m healed '+str(HEALING:=heal(random.randrange(40,65),kys))+'..)')
            bhp += HEALING
            if HEALING==0:
              stats4nerds['useless turns']+=1
              print("(What a loser...)")
      elif selection==2: #heal up
        stats4nerds['heal up']+=1
        printt(random.choice(['Staring straight into his eyes gives you a sudden confidence...','You remember that KYS can mean keep yourself safe...','The lightning seems to fill YOU with strength...','You try to imagine his face as the man face...']),1)
        hp += miheal if (miheal:=heal(random.randrange(20,31)))!='no' else 0
        if miheal=='no':
          stats4nerds['useless turns']+=1
          print("\033[38;5;88m(The lightning prevents it.)\033[0m")
        else:
          printt('\033[38;5;123m(Healed '+str(miheal)+' hp!)')
        if miheal==0:
          print("(What a great choice...)")
      elif selection==3: #kys
        stats4nerds['kys']+=1
        printt(["You decide to Keep Yourself Safe.","(-25% damage next turn!)"],[1,.03])
        dmgmul=.75
      if not theender:
        anykey()
        stats4nerds['turns']+=1
        turn='kill yourself, now!!!!!!!!!!!!!!!!!'
      else:
        yehp = 0
    else:
      printman('''
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo\n\n''')
      if itsafirst and name!='Muffinlavania':
        itsafirst=False
        printt(["\033[38;5;88mYSKYSN\033[0m attacks!","Use WASD or Arrow keys to dodge his various attacks!","You can move your blue square to purple circles, if the color changes you might want to move...",'Don\'t touch the walls, they are made of lightning.',"Be careful of warnings and in general dark-colored elements!","As \033[38;5;88mYSKYSN\033[0m gets weaker, his attacks get harder!","[One time explaination!, any key to continue to attack one]"],[1,2,2,1,1,2,.03])
        getkey1()
        clearline(5)
      if bhp>0:
        attackin=True
        owie=5 #change what the damage is if you are in bad space
        THREAD(target=attack).start()
        THREAD(target=iframe).start()
        THREAD(target=OWW).start()
        coloreddict['▢']='\033[38;5;51m▢'
        c()
        afk=True
        printman(YS[:960])
        coloreddict['m'],okle="\033[48;5;232m " if xtreme and bmulti==2 and nonr else '\033[48;5;3m ' if bhp>=600*bmulti else '\033[48;5;131m ' if bhp>=300*bmulti else '\033[48;5;196m ',yehp
        while attackin and yehp>0:
          whereheat=playin.index('▢')
          if not cutscene:
            up(True)
          while afk and attackin and yehp>0:
            time.sleep(.05)
            if JUSTUPIT==True and not cutscene:
              JUSTUPIT=False
              up(True)
          if keyz in ['a','s','w','d',LEFT,DOWN,UP,RIGHT] and yehp>0 and not cutscene:
            h=movi(keyz)
            if h=='bruh' and attackin:#hit walls, take damage
              damage((10 if bhp in [666,420,69] else 5)*dmgmul)
          if keyz=='p':
            pause=not pause
            Music.pause() if pause else Music.unpause()
          afk=True
        if yehp>0:
          time.sleep(.1)
          c()
          stats4nerds['damage taken'] += okle-yehp
          dmgmul = 1
          print(r+"\nAttack cleared!")
          time.sleep(.5)
          anykey()
          turn='gamer'

  musicstop()

  if bhp<0:
    achieve('s',[[False],False,False,False,False])
    c()
    coloreddict['m']='\033[48;5;166m '
    coloreddict['W']='\033[48;5;9m '
    printman(YL)
    time.sleep(2)
    printt("\n\033[38;5;204m...")
    slepy(2)
    s4=stats4nerds
    if hasspidy:
      
      #revamp this achievement system
      printt(r+'\n[One final bolt of lightning comes from the sky,\n but luckily the \033[38;5;1mspidy bot'+r+' is there to block it...]\033[38;5;204m\n')
      if nonr:
        printt(["Even against all odds, you managed to do it.","No matter how much I got mad, you just spoke.","That means a lot man, for real.","\033[48;5;14mYou should love yourself, now!"+r],[2,1,2,.03])
        achieve("YSLYSN")
      elif cloud9:
        printt(['You beat me at my own game.','Even while I perked up, you perked up just the same...','I could learn a thing or two from you. Thanks.'],[1,2,1])
        achieve("CLOUD 9")
      elif cancer:
        printt(["You're..... invincible.","Even through my uncontrollable rage, you beat me, flawlessly.","There aren't many people like you anymore. Love yourself man, now! (fr)"],[1,2,.03])
        achieve("Cancer")
      elif noheal or bmulti==2 or xtreme:
        printt(['Wow.',"I was so mad I didn't even see how cool you were man.","Love yourself."+r],[1,2,.03])
        achieve(("True Chad" if noheal else 'LEAN' if xtreme else 'Double takedown'))
      else:
        printt(['So much.... peace.',"You are worth something.","Your life serves tons of purpose!","\033[38;5;154m[\033[38;5;204mYSLYSN\033[38;5;154m walks away with new purpose...]"+r],[2,1,2,.03])
        for i in coloreddict:
          if i not in ['o','-']:
            coloreddict[i]=coloreddict['-']
        print("\033[H",end="")
        printman(YL)
        print('\n'*9)
        slepy(3)
      print(r+'\n----------------\nYour final stats:\n\n\033[38;5;82m\nHealth: '+str(yehp)+'\nBoss Health: '+str(bhp)+'\nTotal Turns: '+str(s4['turns'])+'\nTotal Speaks: '+str(s4['speak'])+'\nTotal Magics: '+str(s4['magic'])+'\nTotal Heal Ups: '+str(s4['heal up'])+'\nTotal KYS: '+str(s4['kys'])+'\nTotal Dream Masks: '+str(s4['dream mask'])+f'\n{"Total Hockey Masks" if not cancer else "Total Shields"}: '+str(s4['hockey mask'])+("\nShields avaliable: "+str(s4['shields'])+'\nTotal Red Bulls: '+str(s4['reds'])+"\nRed bulls available: "+str(s4['red bulls']) if cancer else "")+'\nTotal Rusty Masks: '+str(s4['rusty mask'])+'\nTotal Doctor\'s Kits: '+str(s4['doctors'])+'\nTotal YSKYSN Heals: '+str(s4['yskysn heals'])+'\nTotal Damage Taken: '+str(s4['damage taken'])+'\nTotal Useless Turns: '+str(s4['useless turns'])+r+'\n----------------')
      achieve('LYS')
      anykey()
    else:
      printt('\033[38;5;60mSuddenly, one last bolt of lightning comes from the sky,\nand hits the now \033[38;5;204mYSLYSN\033[0m \033[38;5;60mdirectly in the head...',2)
      c()
      coloreddict['m'],coloreddict['W']='\033[48;5;3m ','\033[48;5;7m '
      printman(YS)
      slepy(2)
      printt(["\n\n\033[38;5;88mYSKYSN has rebirthed!\033[0m","[If only there was something magical to block that bolt...]"],[2,1])
      print(r+"\033[38;5;6m'R' to retry the fight\n\033[38;5;60mAny other key to exit\n\033[0m[Any key to continue]")
      if getkey1()=='r':
        c()
        print('\033[38;5;196mReturning to the land of KYS...\033[0m')
        slepy(2)
        c()
        yskysn()
  elif yehp<=0 and not theender:
    achieve('s',[[False],False,False,False,False])
    c(1)
    printt(r+"...",2)
    if nonr:
      printt(["It happened, was bound to.","\033[38;5;88mYour life is worth nothing!\033[0m"],[1,.03])
    elif noheal:
      printt(["The lightning surrounds you, becomes you.","\033[48;5;90mEveryone else is worth nothing!"],[2,.03])
      #insert box yskysn lol
    elif bmulti==2:
      printt('\033[38;5;88mIdiots like you shouldn\'t breathe the same air as me.',1)
    else:
      printt(["\033[38;5;88mGood job bro.","You killed yourself.","Why are you still here, just to worship me?\n"],[1,2,.03])
    print(r+"\033[38;5;6m'R' to retry the fight\n\033[38;5;60mAny other key to exit\n\033[0m[Any key to continue]")
    if getkey1()=='r':
      c()
      print('\033[38;5;196mReturning to the land of KYS...\033[0m')
      slepy(2)
      c()
      yskysn()
  c()




KeyboardThread(thingthing)
#-------start game--------
printt("\033[38;5;88mWelcome to the YSKYSN boss!\033[0m\nPress 'a' to view achievements!\n")
print("\033[?25l",end='') #hide cursor
while True:
  if acheck("LYS"):
    print("\033[38;5;88mYou again...\033[0m\n")
  print("Basic controls (ingame only!!):\n\tWASD/Arrow keys to move\n\tV - view achievements\n\tC - redraw screen\n\tYSKYSN boss controls are simple, but will be shown!!\n\n\033[38;5;40mPress 's' to go to the game!\033[0m")
  e = getkey1()
  if e == 's':
    break
  elif e == 'a':
    achievers()
  c()
  print("\033[38;5;88mWelcome to the YSKYSN boss!\033[0m\nPress 'a' to view achievements!\n")

c()
def remains(i,list):
  return len([e for e in list if (i-e)%52==0])>0
lancd=[i for i in range(1000) if remains(i,[32,37,33,34,35,36])]
lanc = {'black':[i for i in range(1000) if remains(i,[14,19,32,37])],'gray':[i for i in range(1000) if remains(i,[15,16,17,18,33,34,35,36])]}
#--------main stuff-------
def printr(t,ok=True):
  return ('\033[38;5;95m' if ok==False else "\033[38;5;0m" if [i for i in '└┘┌┐╘╛' if i in t] and ok==True else "" if ok==True or not ok[0] else "\033[38;5;57m") + t + r #come here to add
ez = {'-':' ','e':' '}
def retalter(alternum,condition,back=False):
  j = '3' if not back else '4'
  return (f'\033[{j}8;5;1m' if alternum==1 else f'\033[{j}8;5;12m') if not condition else ("\033[38;5;0m" if j=='3' else "\033[48;5;99m")
def printmaze(maze):
  global both
  g = maze!=gamering
  final = ""
  for counti,i in enumerate(maze):
    if i not in ['-','e','┌','┐','└','┘'] and i not in charss2 and g:
      final += colors.get(i,i) + r
    else:
      if g:
        if counti in lanc['gray']:
          final += '\033[48;5;238m '+r
        elif counti in lanc['black']:
          final += '\033[48;5;232m '+r
        elif both and any([(TMP2:=i in '┌┐└┘'),(TMP3:=counti in [ALTER1,ALTER1+1,ALTER1+52,ALTER1+53])]):
          final += printr('\033[48;5;' + ('178m' if ((counti-52)//104)%2==1 else '172m') + retalter(1 if TMP2 else 2,(TMP2 and TMP3))+(i if TMP2 else "┌┐└┘"[[ALTER1,ALTER1+1,ALTER1+52,ALTER1+53].index(counti)]))
        else:
          final += printr('\033[48;5;' + ('178m' if ((counti-52)//104)%2==1 else '172m') + ez.get(i,i if (TMP:=i not in charss2) else [charss[k] for k in charss if i in k][0]),TMP)
      else:
        if i=='+':
          final += printr(colors[('+1' if counti+1 not in nextone else "+2") if not both else ("+1" if counti+1 not in nextone and counti+1 not in nextone2 else "++1" if counti+1 not in nextone2 else "++2")])
        elif i=='(':
          o = [(counti-55<ALTER1<counti+3 and ALTER1%52==31),(counti-55<box1<counti+3 and box1%52==31)] #saves a lot of space lol
          final += printr(colors['(2' if box1%52==31 and counti-55<box1<counti+3 else '(1'] if not both or not any(o) else retalter(1 if o[1] else 2,all(o),True)+' ') #find hit thing
        elif i=='=':
          final += f"\033[48;5;243m{message:^19}" + r
        elif i=='W':
          final += colors['W1' if counti%52<45 else 'W2']+{510:"L",511:"V",514:str(level)[0]}.get(counti,' ') + r
        elif i=='Q':
          final += colors['Q1' if counti%52<45 else 'Q2']+{146:"S",147:"P",151:str(speed)[0]}.get(counti,' ') + r
        elif i=='1':
          final += colors['1' if not both else '21'] + r
        elif both and (i in '┌┐└┘' or counti in [ALTER1,ALTER1+1,ALTER1+52,ALTER1+53]):
          final += printr(("\033[48;5;172m" if counti%52>30 else "\033[48;5;178m")+retalter(1 if i in '┌┐└┘' else 2,(i in '┌┐└┘' and counti in [ALTER1,ALTER1+1,ALTER1+52,ALTER1+53]))+(i if i in '┌┐└┘' else "┌┐└┘"[[ALTER1,ALTER1+1,ALTER1+52,ALTER1+53].index(counti)]))
        else:
          final += printr(colors.get(i,("\033[48;5;172m" if counti%52>30 else "\033[48;5;178m")+(i if i not in 'ABCD-' else " " if i=='-' else [charss[k] for k in charss if i in k][0])),i not in charss2)
  print(final)
  for i in ['Q1','Q2','W1','W2']: colors[i] = "\033[48;5;27m" if 'Q' in i else '\033[48;5;41m'
SCREENUP=False
def setvolume(h):
  global defaultvolume
  defaultvolume += .05*(-1 if h=='-' else 1)
  defaultvolume = 2 if defaultvolume>2 else .01 if defaultvolume<.05 else .05 if round(defaultvolume,2)==.06 else round(defaultvolume,2)
  Music.set_volume(music_volume*defaultvolume)
  if len(all_sounds)>0:
    for i in all_sounds:
      mixer.Sound.set_volume(all_sounds[i],sound_volume*defaultvolume)
clear,s_offset,offset = False,1,0
while True:
  box1,box2,box3,box4=mazeq.index('┌'),mazeq.index('┐'),mazeq.index('└'),mazeq.index('┘')
  printmaze(mazeq)
  afk=True
  while afk:
    if SCREENUP:
      print("\033[H",end="")
      printmaze(mazeq)
      SCREENUP=False
  h=keyz
  if clear:
    clear = False
    c()
  if h in ['w','a','s','d',UP,DOWN,LEFT,RIGHT]:
    move("up" if h in ['w',UP] else "down" if h in ['s',DOWN] else 'right' if h in ['d',RIGHT] else 'left')
  if h in ['i','j','k','l'] and both:
    move2({"i":'up','j':'left','k':'down','l':"right"}[h])
  if h == 'c':
    c()
  if h == 'v':
    achievers()
  if h == TAB:
    print("hi "+name)
    clear = True
  if h == 'z':
    print("End game? (y for yes)")
    if getkey1()=='y':
      break
    c()
  if h=='t':
    sound(changespeed("YSKYSN/dial2.wav", 2),False,'DIAL')
  if h == '5' and '207m' in colors['Z'] and mazeq==gamering:
    checkthing()
    THREAD(target=spawners, args=(True)).start()
  if h in '[]':
    s_offset = round(s_offset-.02 if h=='[' and s_offset>.5 else s_offset+.02,2)
    print(f"Song speed: x{s_offset}, only applies to minigame!")
    clear=True
  if h in ";'":
    offset = round(offset-.05 if h==';' else offset+.05,2)
    print(f"Song offset: {offset}sec, only applies to minigame!")
    clear=True
  print("\033[H",end="")
  if h in '=-+':
    setvolume(h)
    print(f"Volume multiplier: {defaultvolume}, Applies to everything!",end="")
    clear=True

sys.stdout.write("\033[?25h")
mixer.quit()

'''
enable,timeE,SONG,THEONE,LOGS = False,time.time(),[7.5,['8',34]],0,"sd dict, nextone, nextone2"
if i ever need it again (just remember places they were lol) - charting testing things
with open("SONGS.json",'r') as k:
    alter_song = json.load(k)['song2_ALTER'] #for testing
keyz things:
  in moving:
    if enable: #chartings
      SONG.append([{"10":"A",'11':"B",'12':"C",'13':"D",'14':"E"}.get(str(box1//52-1),str(box1//52-1)),round((time.time()-timeE)/.14)])
      timeE=time.time()
  if h=='1':
    enable = not enable
  if h=='0':
    print(SONG)
    with open("SONGS.json") as n:
      u = json.load(n)
    with open("SONGS.json",'w') as n:
      u['song2TEST'] = SONG
      n.write(json.dumps(u))
    SONG=[]
  if h=='b':
    both = not both
  if h=='8': #press when song ends to time it and stuff
    THEONE = time.time()
  if h=='r':
    print(f"Can die: {candie}")
    candie = not candie
  if h=='l':
    c()
    print(LOGS)
    anykey()
  if h=='5':
    mixer.pause()
    level=2
    THREAD(target=spawners).start()
'''
