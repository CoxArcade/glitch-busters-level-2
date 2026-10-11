import asyncio
import pygame, random, math
pygame.init()
W,H=640,400
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption('QUESTFORGE / GLITCH BUSTERS LEVEL 2: COORDINATE CHAOS')
clock=pygame.time.Clock()
F=pygame.font.Font(None,21); S=pygame.font.Font(None,16); L=pygame.font.Font(None,37)
WHITE=(241,244,255); BG=(12,15,31); CYAN=(81,224,222); GOLD=(255,207,83)
PINK=(252,91,152); RED=(237,75,99); GREEN=(102,228,137); PURPLE=(173,117,249)
GRAY=(147,153,183); BLUE=(80,129,227)
AREA=pygame.Rect(25,65,590,264)
ROOMS=['COORDINATE TERMINAL','BOUNDARY GRID','COIN CIRCUIT','VECTOR FACTORY','SCORE VAULT']
# Level 2: only Week 1 and Week 2 concepts (x/y, arrows, boundaries, proximity, coins, score).
Q=[
('BYTE: BROKEN FUNCTION','Which repair lets this function run?',['def draw()','    print("READY")'],['Add : after draw()','Delete the parentheses','Remove print()'],0,'A function header ends with a colon.','def draw():','    print("READY")'),
('PIXEL: FROZEN BALL','The ball does not follow x. What changes?',['x = x + 3','draw_circle(100, 80)'],['Increase the radius','Replace 100 with x','Change the color'],1,'Drawing at 100 ignores the changing x variable.','x = x + 3','draw_circle(x, 80)'),
('GHOST: INVISIBLE HERO','Why can nobody see the hero?',['background = "black"','hero_color = "black"'],['Make both colors black','Move the hero away','Choose a contrasting color'],2,'An object matching its background is hard to see.','background = "black"','hero_color = "yellow"'),
('CORE: MOVING RIGHT','Which line moves the player right?',['x = 50','# Move right each update'],['x = x + 3','x = x - 3','x = 50'],0,'Adding to x moves the player toward the right.','x = 50','x = x + 3'),
('CORE: MOVE LEFT','Which line moves the player left?',['x = 80','# Move left each update'],['x = x + 2','x = 80','x = x - 2'],2,'Subtracting from x moves an object left.','x = 80','x = x - 2'),
('MAZE: GOLD SENSOR','What tests whether x is close to gold_x?',['x = 95','gold_x = 100'],['if x > 200:','if x >= gold_x - 10:','if x < 0:'],1,'A simple if can test whether x is near a target.','if x >= gold_x - 10:','    print("FOUND")'),
('MAZE: DRAWING POSITION','Which line draws the hero at its x position?',['x = 45','# Hero should follow x'],['draw_hero(45, 90)','draw_hero(100, 90)','draw_hero(x, 90)'],2,'Use the variable, not a fixed number, for movement.','x = x + 2','draw_hero(x, 90)'),
('FACTORY: UPDATE','Which function usually changes positions?',['def draw():','    draw_hero(x, 90)'],['update()','draw()','print()'],0,'update() changes values; draw() displays them.','def update():','    x = x + 2'),
('FACTORY: SIMPLE IF','Which line checks that x is past 100?',['x = 110','# Check the position'],['if x < 100:','if x > 100:','x = 100'],1,'The > symbol asks whether x is greater than 100.','if x > 100:','    print("GO")'),
('VAULT: FINAL REPAIR','Which code correctly starts draw()?',['# Draw the player',''],['def draw()','def draw():','draw = draw()'],1,'A function definition needs def, (), and a colon.','def draw():','    print("PLAYER")'),
('VAULT: FINAL SENSOR','What checks whether the hero reached gold?',['x = 98','gold_x = 100'],['if x < 0:','x = gold_x','if x >= gold_x - 5:'],2,'A comparison inside if can detect arrival.','if x >= gold_x - 5:','    print("YOU WIN")')]
# Guardian hacks are unique per room and never reuse repair-station questions.
# Only Week 1 concepts: x, variables, draw/update, colors, simple if.
Q += [
('ARCADE SHIELD A','Which change makes x move right?',['x = 12',''],['x = x + 2','x = x - 2','x = 12'],0,'Adding increases x, moving right.','x = 12','x = x + 2'),
('ARCADE SHIELD B','The hero should be blue on black.',['background = "black"','hero = "black"'],['Change both to black','Change hero to blue','Delete hero'],1,'Contrasting colors make the hero visible.','background = "black"','hero = "blue"'),
('ARCADE SHIELD C','Which header correctly defines update?',['# Update movement',''],['def update()','update():','def update():'],2,'Function headers end with a colon.','def update():','    print("MOVE")'),
('CORE SHIELD A','Which value is a variable?',['speed = 4','x = x + speed'],['speed','4','+'],0,'speed is a named value.','speed = 4','x = x + speed'),
('CORE SHIELD B','What happens after x = x - 5?',['x = 70','x = x - 5'],['x becomes 75','x becomes 65','x stays 70'],1,'Subtract five from seventy.','x = 70','x = 65'),
('CORE SHIELD C','Which function displays objects?',['def draw():','    draw_hero(x, 90)'],['update()','if','draw()'],2,'draw() controls what appears on screen.','def draw():','    draw_hero(x, 90)'),
('MAZE SHIELD A','Which condition is true for x = 9?',['x = 9',''],['if x > 5:','if x < 5:','if x > 20:'],0,'Nine is greater than five.','x = 9','if x > 5:'),
('MAZE SHIELD B','The ball should follow x.',['x = x + 1','draw_ball(25, 60)'],['Change the color','Use draw_ball(x, 60)','Keep 25'],1,'A fixed coordinate does not follow x.','x = x + 1','draw_ball(x, 60)'),
('MAZE SHIELD C','Which line changes a variable?',['speed = 2',''],['print("GO")','def draw():','speed = 5'],2,'Assignment updates a named value.','speed = 2','speed = 5'),
('FACTORY SHIELD A','What makes a player move left?',['x = 100',''],['x = x - 1','x = x + 1','x = 100'],0,'Smaller x means farther left.','x = 100','x = x - 1'),
('FACTORY SHIELD B','Which color makes the hero visible?',['background = "blue"','hero = "blue"'],['blue','yellow','blue again'],1,'A different color stands out.','background = "blue"','hero = "yellow"'),
('FACTORY SHIELD C','What belongs after a function header?',['def draw():',''],['No code ever','A second def only','An indented instruction'],2,'Indented instructions belong to the function.','def draw():','    print("READY")'),
('VAULT SHIELD A','Which test checks if x is large?',['x = 120',''],['if x > 100:','if x < 20:','x = 100'],0,'120 is greater than 100.','x = 120','if x > 100:'),
('VAULT SHIELD B','What does update() normally handle?',['def update():','    x = x + 2'],['Drawing only','Changing game values','Naming colors'],1,'update() changes values as the game runs.','def update():','    x = x + 2'),
('VAULT SHIELD C','Which is a valid draw function?',['# Choose the header',''],['draw():','def draw()','def draw():'],2,'Use def, parentheses, and a colon.','def draw():','    print("PIXEL")')
]
# One additional terminal in each of the five areas (16 station repairs total).
Q += [
('GRID: Y MOVEMENT','Which line moves the hero DOWN?',['y = 45','# Move downward'],['y = y - 3','y = y + 3','x = x + 3'],1,'On the screen, increasing y moves down.','y = 45','y = y + 3'),
('EDGE: LEFT BOUNDARY','Keep the player inside the left edge.',['x = -4','# Minimum x is 0'],['if x < 0: x = 0','if x > 0: x = -4','y = 0'],0,'If x is below zero, return it to zero.','if x < 0:','    x = 0'),
('COIN: COLLECT RANGE','Which check finds a nearby coin?',['x = 49','coin_x = 50'],['if x > 200:','if x < 0:','if x >= coin_x - 5:'],2,'Comparing x with a nearby coordinate can detect a pickup.','if x >= coin_x - 5:','    score = score + 1'),
('VECTOR: MOVE UP','Which change moves a hazard upward?',['y = 160','# Move upward'],['x = x + 2','y = y - 2','y = y + 2'],1,'Smaller y is higher on the screen.','y = 160','y = y - 2'),
('SCORE: COUNT COINS','You have 4 points and collect one coin.',['score = 4','# Collect a coin'],['score = score + 1','score = score - 1','score = 0'],0,'Increase score by one for a collected coin.','score = 4','score = score + 1')
]
BOSS_Q={r:[11+r*3+i for i in range(3)] for r in range(5)}
STATIONS={0:[(110,142,0),(494,144,1),(490,285,2),(105,218,26)],
1:[(168,135,3),(463,258,4),(507,194,27)],
2:[(156,133,5),(480,267,6),(147,285,28)],
3:[(167,145,7),(464,260,8),(505,197,29)],
4:[(176,145,9),(460,264,10),(105,220,30)]}
NPCS={0:[(308,284,'GUIDE','Look closely at the north wall. One stone has an odd seam. The sword is east.')],
1:[(313,130,'PATCH','I hear bugs behind the north wall. Search for a loose tile.')],
2:[(300,287,'ARROW','The crystal is behind a northern wall panel. Find the seam.')],
3:[(315,130,'CIPHER','I found unusual marks near the southern wall. Bombs are in a chest.')],
4:[(313,286,'KEEPER','Check the north wall. Three artifacts unlock legendary armor!')]}
# Additional talking characters. Every Python tip uses Week 1 knowledge only.
MENTORS={
  'PROFESSOR PIXEL': {'room':0,'pos':(199,269),'color':(83,183,224),
     'intro':'A retired programmer who knows why games move.',
     'topics':[('What do x and y mean?', 'x tracks left and right. y tracks up and down. Add to x for right or y for down.', 'TIP: x changes left and right.'),
               ('How do I move in four directions?', 'Use left and right to change x, and up and down to change y. Keep both within the screen.', 'TIP: update() changes x; draw() uses x.'),
               ('Any advice about the arcade?', 'The CIRCUIT PANEL is near the southeast wall, away from GUIDE. Rotate the wires until power reaches EXIT. Look north for a secret seam.', 'CLUE: The southeast circuit panel restores power; search the north wall for a secret.')],
     'gift':('potion',1)},
  'SPROCKET': {'room':1,'pos':(465,133),'color':(240,120,82),
     'intro':'A mechanic who fixes arcade machines.',
     'topics':[('How do boundaries work?', 'If x becomes less than zero, set x back to zero. Do the same for y at the top edge.', 'TIP: Contrast makes game objects visible.'),
               ('Why does the player leave the screen?', 'Check the boundary conditions. Keep x and y between the screen edges.', 'TIP: draw() should use the changing x.'),
               ('Where are the spare parts?', 'One panel in the north wall sounds hollow. Try examining the masonry closely.', 'CLUE: A north wall panel hides supplies.')],
     'gift':('potion',1)},
  'ARCHIVIST': {'room':3,'pos':(463,132),'color':(179,119,232),
     'intro':'A quiet keeper of forgotten arcade secrets.',
     'topics':[('Tell me about the artifacts.', 'Three lost artifacts are concealed in secret chambers. Finding all three unlocks the vault armor.', 'LORE: Three artifacts unlock legendary armor.'),
               ('Where should I search?', 'Look north in the arcade and maze. In the factory, investigate the southern wall. The vault code begins STAR, then MOON.', 'CLUE: North in arcade/maze; south in factory. Vault starts STAR, MOON.'),
               ('What makes a good debugger?', 'Observe what should happen, change one line, then test again. Even a colon can matter.', 'TIP: Observe, change one thing, test.')],
     'gift':('bombs',2)},
  'RANGER ARROW': {'room':2,'pos':(303,122),'color':(119,202,118),
     'intro':'A ranger who studies bug movement patterns.',
     'topics':[('How do coins use coordinates?', 'A coin has an x and y position. Compare the player position with the coin position to collect it.', 'GEAR: Find bow in maze chest; C fires.'),
               ('How do I avoid enemy shots?', 'Keep moving sideways when a Static Wisp fires. Use X to dash past dangerous shots.', 'COMBAT: Move sideways and use X to dash.'),
               ('Can code help with collecting?', 'Yes! Check whether player x is near coin x and player y is near coin y.', 'TIP: x tracks horizontal position.')],
     'gift':('arrows',6)},
  'ECHO': {'room':'secret','pos':(450,253),'color':(117,217,241),
     'intro':'A lost programmer who lives between the walls.',
     'topics':[('What is the difference between draw and update?', 'update() changes positions. draw() shows the positions on screen.', 'TIP: update changes; draw displays.'),
               ('Why does my function fail?', 'A function definition such as def draw(): needs a colon. The lines inside it are indented.', 'TIP: Function header ends with a colon.'),
               ('How did you find this place?', 'A tiny seam gave away the hidden passage. Check walls for subtle differences.', 'CLUE: Tiny seams reveal hidden passages.')],
     'gift':('potion',1)}
}
# Five distinct, mandatory puzzle systems. Every puzzle has a retryable hint.
PUZZLE_NAMES=['COORDINATE CIRCUIT','BOUNDARY CRATE LAB','COIN LASER RELAY','VECTOR CODE VAULT','SCORE RESTORATION']
PUZZLE_POS=[(397,284),(528,287),(535,205),(530,286),(530,286)]
puzzle_done=set(); puzzle_attempts=[0]*5; puzzle_hints=[0]*5
puzzle_step=0; puzzle_switches=[False]*3
# Rotate six wire pieces to connect the power source to the receiver.
circuit_tiles=[1,1,0,1,1,2]; circuit_selected=0
crate_player=[0,3]; crate_boxes={(1,1),(3,2)}; crate_targets={(3,1),(1,2)}
mirror_angles=[0,0,0]; mirror_selected=0
vault_input=[]; vault_order=[2,0,3,1]
conduits=[0,0,0]; conduit_selected=0; conduit_timer=0; conduit_damage=0
puzzle_feedback=''; puzzle_feedback_timer=0
PUZZLE_HINTS=[
 'PROFESSOR PIXEL: Trace x across the top row, then increase y to turn down; connect the lower row from right to left.',
 'SPROCKET: Watch the grid boundaries. A crate cannot leave the grid or push through another crate. R resets.',
 'RANGER ARROW: Follow the light along x and y. Align mirrors to /, backslash, /.',
 'ARCHIVIST: The score vault accepts STAR, MOON, GEAR, BOLT in that order.',
 'ECHO: Activate all three score conduits. Repair any that shut off before the timer fills.'
]
# Mandatory guided learning: three topics and a comprehension check per main-stage mentor.
MAIN_MENTORS=['PROFESSOR PIXEL','SPROCKET','RANGER ARROW','ARCHIVIST','KEEPER']
# The Keeper is a main-stage mentor; Echo remains a bonus secret contact.
MENTORS['KEEPER']={'room':4,'pos':(460,125),'color':(236,198,96),
 'intro':'Guardian of the final arcade restoration.',
 'topics':[('How do functions begin?', 'Write def draw(): with a colon. Put instructions on the next indented line.', 'TIP: def draw(): starts a function.'),
           ('What changes the game?', 'update() changes x or other variables; draw() displays objects using those values.', 'TIP: update changes values; draw displays.'),
           ('How can if help with score?', 'An if statement can check whether the player is near a coin, then add one to score.', 'TIP: if checks conditions.')],
 'gift':('potion',1)}
LESSON_CHECKS={
 'PROFESSOR PIXEL':[
  ('What happens when x = x + 3?', ['The hero moves right','The hero moves left','The hero disappears'],0,'Adding to x moves right.'),
  ('Which function changes positions?', ['draw()','update()','print()'],1,'update() changes game values.'),
  ('Which draws the hero using its x value?', ['draw_hero(100, 80)','draw_hero(x, 80)','x = 100'],1,'draw() must use the variable x.')],
 'SPROCKET':[
  ('Which hero color is visible on black?', ['Black','Dark black','Yellow'],2,'Use contrasting colors.'),
  ('What should draw() use for a moving ball?', ['The changing x variable','A fixed x of 100','No x position'],0,'Fixed positions ignore movement.'),
  ('Which line stores a value?', ['speed = 4','speed > 4','def speed()'],0,'An equals sign assigns a value to a variable.')],
 'RANGER ARROW':[
  ('Which line moves an object left?', ['x = x + 2','x = x - 2','x = 2'],1,'Subtracting decreases x.'),
  ('If x changes, what should draw() use?', ['A fixed number','The changing x','The background color'],1,'Draw at the changing x position.'),
  ('Which line checks whether x is past 100?', ['if x > 100:','x = 100','if x < 0:'],0,'An if condition can compare x with 100.')],
 'ARCHIVIST':[
  ('What is the first step in debugging?', ['Change everything','Observe the problem','Delete the game'],1,'Observe before changing code.'),
  ('Why does def draw() fail?', ['It needs a colon','It needs more colors','It needs a larger x'],0,'Function headers need a colon.'),
  ('After changing one line, what next?', ['Test again','Change ten more lines','Ignore the result'],0,'Test after each change.')],
 'KEEPER':[
  ('Which function header is valid?', ['def draw()','def draw():','draw():'],1,'Function headers use def and a colon.'),
  ('Which function changes x during play?', ['draw()','print()','update()'],2,'update() changes game values.'),
  ('What does if x > 100: do?', ['Checks a condition','Draws a hero','Sets x to 100'],0,'if tests whether a condition is true.')]
}
mentor_topics_done=set(); mentor_checks_done=set(); mentor_check_attempts={name:[0,0,0] for name in MAIN_MENTORS}
check_name=''; check_topic=0; check_selected=0; check_feedback=''
mentor_met=set(); mentor_gifts=set(); journal=[]; journal_page=0
chat_name=''; chat_selected=0; chat_page='menu'; chat_topic=0
player_name=''; player_experience=''; conversation_steps=0
CHESTS={0:(538,217,'sword'),1:(316,212,'potion'),2:(524,139,'bow'),3:(528,136,'bombs'),4:(312,207,'armor')}
ARTIFACTS={0:(94,285,'COORDINATE KEY'),2:(110,136,'GRID CRYSTAL'),3:(94,285,'SCORE CHIP')}
WALLS={0:[],1:[pygame.Rect(265,164,105,20),pygame.Rect(265,164,18,88)],
2:[pygame.Rect(220,95,20,154),pygame.Rect(220,230,174,19),pygame.Rect(376,128,19,121)],
3:[pygame.Rect(234,104,19,134),pygame.Rect(380,183,19,126),pygame.Rect(253,218,128,18)],
4:[pygame.Rect(247,180,45,17),pygame.Rect(345,180,45,17)]}
rooms_done=set(); solved=set(); chests=set(); artifacts=set(); opened=set()
# Wall secrets are not drawn as objects. Each north/south wall has normal-looking tiles.
# Nearby NPC clues and subtle tile seams reward careful observation.
SECRETS={
 0:[(65,112,'ARTIFACT','A loose wall tile hides the GOLD CARTRIDGE.'),(557,112,'CACHE','An old cabinet contains a speed module.')],
 1:[(86,112,'CACHE','A cracked panel conceals two health potions.'),(553,305,'CACHE','A hidden drawer holds eight arrows.')],
 2:[(86,112,'ARTIFACT','Behind the wall is the PIXEL CRYSTAL.'),(557,112,'CACHE','A dusty machine contains a sword upgrade.')],
 3:[(86,306,'ARTIFACT','You uncover the GLITCH CHIP.'),(555,112,'CACHE','A hidden compartment holds three bombs.')],
 4:[(86,112,'CACHE','A vault panel hides a full heal.'),(555,112,'CACHE','A forgotten terminal holds extra arrows.')]
}
secret_found=set(); chamber_cleared=set(); secret_room=False; secret_origin=0; secret_index=0; npc_gifts=set(); boss_hacks_room={r:0 for r in range(5)}

stats={'runs':0,'gameovers':0,'lives':0,'damage':0,'kills':0,'attempts':[0]*len(Q),'wrong':0,'victories':0,'seconds':0.,'rooms':set(),'secrets':0,'chests':0,'dashes':0,'talks':0,'lessons':0,'puzzles':0}
room=0; player=pygame.Rect(75,283,19,25); facing=(0,1); frame=0
hp=5; max_hp=5; lives=3; weapon='PUNCH'; has_bow=False; bombs=0; arrows=12; potions=0
state='title'; active=0; selected=0; invuln=0; attack_time=0; attack_cd=0; dash_time=0; dash_cd=0; speed_upgrade=False; sword_upgrade=False; moving=False
message=''; msg_timer=0; bugs=[]; shots=[]; pickups=[]; sparks=[]; hit_fx=[]; boss=None; boss_hp=0
boss_open=0; boss_shot=0; boss_question=0; boss_hacks=0; boss_quiz=False; spawn_cd=0; copy_msg=''; waves=0; report_return='world'; reinforce_count=0; reinforce_timer=0; secret_bugs=[]; secret_chest_open=False
# Overdrive and legendary challenge progress reset for each new adventure.
crystals=set(); crystal_bank=0; overdrive_charges=0; overdrive_time=0
overdrive_earned=0; overdrive_uses=0; crystal_total=0; pending_crystals=0
legendary=set(); gauntlet_room=1; gauntlet_x=45; gauntlet_y=200
gauntlet_hits=0; gauntlet_cooldown=0; gauntlet_return=(70,275)
victory_kind=''; victory_countdown=0
CRYSTAL_SPOTS={
 0:[(70,210),(352,116),(531,298),(320,190)],
 1:[(85,190),(205,285),(404,115),(535,235),(347,290)],
 2:[(84,275),(173,296),(332,105),(465,191),(552,289)],
 3:[(89,199),(194,295),(338,111),(482,220),(546,291)],
 4:[(88,195),(195,293),(320,110),(474,197),(548,289)]
}
RESTRICTED={
 1:('VOLTAGE CORRIDOR','CAPACITOR ARMOR',(538,110)),
 2:('FIREWALL GAUNTLET','QUANTUM BLADE',(533,285)),
 3:('ROOT ACCESS VAULT','ROOT ACCESS MODULE',(103,110))
}

def draw_text(t,x,y,c=WHITE,font=F): screen.blit(font.render(str(t),True,c),(int(x),int(y)))
def center(t,y,c=WHITE,font=F):
    im=font.render(str(t),True,c); screen.blit(im,((W-im.get_width())//2,int(y)))
def box(x,y,w,h,c,r=0): pygame.draw.rect(screen,c,(int(x),int(y),int(w),int(h)),border_radius=r)
def tell(t,delay=180):
    global message,msg_timer
    message=t; msg_timer=delay

def bug(x,y,kind=None):
    kind=kind or random.choice(['wander','patrol','hunter','shooter','charger'])
    return {'x':float(x),'y':float(y),'kind':kind,'hp':3 if kind=='charger' else 2 if room>1 else 2,
            'phase':random.random()*7,'turn':random.uniform(-3,3),'timer':random.randrange(55,145),'speed':.76+room*.14,'vx':random.choice([-1,1]),'shot':random.randrange(70,140),'charge':0,'tell':0,'base_x':float(x),'base_y':float(y),'max_hp':3 if kind=='charger' else 2 if room>1 else 2,'flash':0,'hurt':0}

def enter_room(n):
    global room,bugs,boss,boss_hp,boss_open,boss_shot,spawn_cd,waves,shots,reinforce_count,reinforce_timer
    room=n; stats['rooms'].add(n); bugs=[]; shots=[]; pickups.clear()
    spawn_cd=150; boss=None; boss_open=0; waves=1; reinforce_count=0; reinforce_timer=140
    if n==0: positions=[(260,190),(365,210),(450,265),(185,255)]
    elif n==1: positions=[(115,220),(485,125),(448,275),(175,275),(380,275)]
    elif n==2: positions=[(130,215),(330,145),(475,145),(480,285),(320,280),(120,280)]
    elif n==3: positions=[(128,150),(315,265),(490,170),(465,290),(150,275),(345,120)]
    else: positions=[(116,170),(500,160),(120,285),(505,280)]
    if n not in rooms_done:
        for i,(x,y) in enumerate(positions): bugs.append(bug(x,y,['wander','patrol','hunter','shooter','charger'][i%5]))
    else: waves=3
    player.topleft=(56,279)
    tell('AREA '+str(n+1)+': '+ROOMS[n]+'  |  FIND STATIONS, CHESTS, AND ARTIFACTS',200)

def new_game():
    global hp,max_hp,lives,weapon,has_bow,bombs,arrows,potions,state,invuln
    global rooms_done,solved,chests,artifacts,opened,boss_hacks,boss_quiz,secret_found,npc_gifts,boss_hacks_room,dash_cd,dash_time,speed_upgrade,sword_upgrade,secret_room,secret_origin,secret_index,chamber_cleared,secret_bugs,secret_chest_open,mentor_met,mentor_gifts,journal,journal_page,puzzle_done,puzzle_attempts,puzzle_hints,mentor_topics_done,mentor_checks_done,mentor_check_attempts,player_name,player_experience
    stats['runs']+=1; hp=5; max_hp=5; lives=3; weapon='PUNCH'; has_bow=False
    bombs=0; arrows=12; potions=0; invuln=0; boss_hacks=0; boss_quiz=False
    rooms_done=set(); solved=set(); chests=set(); artifacts=set(); opened=set(); secret_found=set(); chamber_cleared=set(); secret_room=False; secret_origin=0; secret_index=0; npc_gifts=set(); boss_hacks_room={r:0 for r in range(5)}; dash_cd=0; dash_time=0; speed_upgrade=False; sword_upgrade=False
    mentor_met=set(); mentor_gifts=set(); journal=[]; journal_page=0; puzzle_done=set(); puzzle_attempts=[0]*5; puzzle_hints=[0]*5; mentor_topics_done=set(); mentor_checks_done=set(); mentor_check_attempts={name:[0,0,0] for name in MAIN_MENTORS}
    player_name=''; player_experience=''
    global crystals,crystal_bank,overdrive_charges,overdrive_time,overdrive_earned,overdrive_uses,crystal_total,pending_crystals,legendary,gauntlet_hits,gauntlet_cooldown,victory_kind,victory_countdown
    crystals=set(); crystal_bank=0; overdrive_charges=0; overdrive_time=0
    overdrive_earned=0; overdrive_uses=0; crystal_total=0; pending_crystals=0; legendary=set()
    gauntlet_hits=0; gauntlet_cooldown=0; victory_kind=''; victory_countdown=0
    enter_room(0); state='world'

def heart(x,y,on):
    c=RED if on else (72,67,91)
    pygame.draw.circle(screen,c,(x+5,y+6),5)
    pygame.draw.circle(screen,c,(x+13,y+6),5)
    pygame.draw.polygon(screen,c,[(x,y+8),(x+18,y+8),(x+9,y+19)])

def human():
    x,y=player.centerx,player.centery
    if invuln and frame%8<4: return
    bob=int(moving and frame%12<6)*2
    # Ground shadow, walking boots, jacket, hair, face and scarf.
    pygame.draw.ellipse(screen,(13,16,34),(x-12,y+13,24,8))
    box(x-8,y+5+bob,7,12,(43,51,91)); box(x+2,y+5-bob,7,12,(43,51,91))
    box(x-10,y+13+bob,9,5,(27,28,43)); box(x+2,y+13-bob,9,5,(27,28,43))
    box(x-11,y-6,22,17,(69,196,239) if 1 in legendary else (43,100,197),3)
    box(x-11,y+2,22,4,GOLD if 1 in legendary else (26,66,144))
    box(x-15,y-3,5,12,(228,171,121)); box(x+10,y-3,5,12,(228,171,121))
    box(x-8,y-19+bob,16,16,(237,183,137),4)
    box(x-10,y-21+bob,20,7,(81,48,39),3)
    box(x-10,y-17+bob,4,7,(81,48,39))
    box(x-3,y-7+bob,7,3,GOLD)
    if facing[0]: box(x+(4 if facing[0]>0 else -5),y-12+bob,2,3,(26,32,53))
    elif facing[1]>0:
        box(x-5,y-12+bob,2,3,(26,32,53)); box(x+3,y-12+bob,2,3,(26,32,53))
    if attack_time:
        fx,fy=facing; sx=x+fx*12; sy=y+fy*12
        if weapon=='PUNCH':
            pygame.draw.circle(screen,(239,189,137),(sx+fx*7,sy+fy*7),5)
        else:
            ax=fx*.75-fy*.66; ay=fy*.75+fx*.66
            tip=(int(sx+ax*34),int(sy+ay*34))
            pygame.draw.line(screen,(25,34,62),(sx,sy),tip,12)
            pygame.draw.line(screen,PURPLE if 2 in legendary else (110,185,221),(sx,sy),tip,9)
            pygame.draw.line(screen,WHITE,(int(sx+ax*9),int(sy+ay*9)),tip,4)
            pygame.draw.polygon(screen,WHITE,[tip,(int(tip[0]-ax*8+ay*5),int(tip[1]-ay*8-ax*5)),(int(tip[0]-ax*8-ay*5),int(tip[1]-ay*8+ax*5))])
            pygame.draw.line(screen,GOLD,(int(sx-ay*9),int(sy+ax*9)),(int(sx+ay*9),int(sy-ax*9)),5)

def draw_mentor(name,x,y,color):
    # Distinct hair, clothes, and a small animated face; no floating question marks.
    bob=1 if frame%40<20 else 0
    pygame.draw.ellipse(screen,(14,19,32),(x-13,y+15,26,7))
    box(x-8,y+8,7,11,(36,39,62)); box(x+2,y+8,7,11,(36,39,62))
    box(x-12,y-4,24,16,color,4)
    box(x-8,y-17+bob,16,16,(238,185,138),4)
    hair=(68,52,43) if name=='PROFESSOR PIXEL' else (173,74,40) if name=='SPROCKET' else (44,41,71) if name=='ARCHIVIST' else (78,64,38) if name=='RANGER ARROW' else (157,210,231)
    box(x-9,y-20+bob,18,6,hair,2)
    if name=='PROFESSOR PIXEL':
        pygame.draw.rect(screen,WHITE,(x-7,y-11+bob,6,5),1)
        pygame.draw.rect(screen,WHITE,(x+2,y-11+bob,6,5),1)
    elif name=='SPROCKET':
        box(x-11,y-20+bob,22,4,GOLD)
    elif name=='ARCHIVIST':
        pygame.draw.polygon(screen,hair,[(x-15,y-6),(x,y-27),(x+15,y-6)])
    elif name=='RANGER ARROW':
        pygame.draw.arc(screen,GOLD,(x+7,y-5,13,23),-1.5,1.5,2)
    else:
        pygame.draw.circle(screen,CYAN,(x,y-9+bob),11,1)
    box(x-4,y-10+bob,2,2,(24,29,46)); box(x+3,y-10+bob,2,2,(24,29,46))
    short={'PROFESSOR PIXEL':'PROF. PIXEL','SPROCKET':'SPROCKET','ARCHIVIST':'ARCHIVIST','RANGER ARROW':'RANGER','ECHO':'ECHO'}[name]
    draw_text(short,x-29,y+21,GOLD,S)

def journal_add(entry):
    if entry not in journal:
        journal.append(entry)
        stats['lessons']+=1

def wrap_lines(value,max_chars=62):
    words=value.split(); lines=[]; current=''
    for word in words:
        trial=(current+' '+word).strip()
        if len(trial)>max_chars and current:
            lines.append(current); current=word
        else: current=trial
    if current: lines.append(current)
    return lines

def hero_name():
    return player_name.strip() or 'adventurer'

def talk_to(name):
    global state,chat_name,chat_selected,chat_page,chat_topic
    chat_name=name; chat_selected=0; chat_topic=0; state='dialogue'
    if name=='PROFESSOR PIXEL' and not player_name:
        chat_page='hello'
    else:
        chat_page='hello_return' if name in mentor_met else 'hello'
    mentor_met.add(name); stats['talks']+=1
    journal_add('MET '+name+': '+MENTORS[name]['intro'])

def begin_topic(topic):
    global chat_page,chat_topic,potions,bombs,arrows
    chat_topic=topic; chat_page='story'
    title,response,note=MENTORS[chat_name]['topics'][topic]
    journal_add(note)
    mentor_topics_done.add((chat_name,topic))
    if chat_name not in mentor_gifts:
        mentor_gifts.add(chat_name)
        kind,amount=MENTORS[chat_name]['gift']
        if kind=='potion': potions+=amount
        elif kind=='bombs': bombs+=amount
        elif kind=='arrows': arrows+=amount
        journal_add('GIFT FROM '+chat_name+': '+str(amount)+' '+kind.upper())

def select_chat():
    begin_topic(chat_selected)

def dialogue_advance():
    global chat_page,chat_selected,player_experience
    if chat_page=='hello':
        chat_page='name' if chat_name=='PROFESSOR PIXEL' and not player_name else 'menu'
    elif chat_page=='hello_return': chat_page='menu'
    elif chat_page=='name':
        if player_name.strip(): chat_page='experience'
    elif chat_page=='experience':
        player_experience=['brand new to coding','tried coding before','made a game before'][chat_selected]
        journal_add('CODING EXPERIENCE: '+player_experience)
        chat_page='experience_reply'
    elif chat_page=='experience_reply': chat_page='menu'
    elif chat_page=='story': chat_page='reflection'
    elif chat_page=='reflection':
        if chat_name in MAIN_MENTORS and (chat_name,chat_topic) not in mentor_checks_done:
            start_mentor_check()
        else: chat_page='menu'
    elif chat_page=='menu': select_chat()

def dialogue_screen():
    mentor=MENTORS[chat_name]
    modal(chat_name+' // CONVERSATION','Talking with '+chat_name+'  |  '+hero_name())
    box(48,143,544,158,(27,37,59),7)
    def lines(t,y=160):
        for i,line in enumerate(wrap_lines(t,61)[:5]):
            draw_text(line,60,y+i*22,WHITE,S)
    if chat_page in ('hello','hello_return'):
        if chat_page=='hello':
            lines('Hello there! I am '+chat_name+'. '+mentor['intro']+' It is good to meet you, '+hero_name()+'!')
        else:
            lines('Welcome back, '+hero_name()+'! The arcade is still counting on us. What shall we explore next?')
    elif chat_page=='name':
        lines('Before we start, what should I call you? Type your first name or a classroom nickname. It will appear on your final Mission Report. Do not enter your full name.')
        box(65,260,485,28,(52,69,99),4)
        draw_text((player_name or 'TYPE NAME HERE')+'|',75,266,GOLD,S)
    elif chat_page=='experience':
        lines('Tell me a little about yourself, '+hero_name()+'. Have you programmed before? There is no wrong answer.')
        for i,t in enumerate(['1. I am brand new!','2. I have tried coding.','3. I have made a game.']):
            y=237+i*29
            box(60,y,516,26,(48,89,95) if i==chat_selected else (35,47,72),4)
            draw_text(t,72,y+5,WHITE,S)
    elif chat_page=='experience_reply':
        if chat_selected==0: lines('Welcome to programming, '+hero_name()+'! Every expert started by trying one little idea. We will learn by experimenting.')
        elif chat_selected==1: lines('Wonderful, '+hero_name()+'! You already know that programs can surprise us. Let us build on what you have tried.')
        else: lines('A game maker! Then you know a tiny mistake can change the whole adventure. Let us sharpen those debugging skills.')
    elif chat_page=='menu':
        done=sum((chat_name,i) in mentor_checks_done for i in range(3)) if chat_name in MAIN_MENTORS else 0
        lines('I have three things to share, '+hero_name()+'. Which should we talk about?'+(' Lessons '+str(done)+'/3.' if chat_name in MAIN_MENTORS else ''))
        for i,(title,_,_) in enumerate(mentor['topics']):
            y=213+i*29
            flag=' [DONE]' if (chat_name,i) in mentor_checks_done else ''
            box(60,y,516,26,(48,89,95) if i==chat_selected else (35,47,72),4)
            draw_text(str(i+1)+'. '+title+flag,72,y+5,WHITE,S)
    elif chat_page=='story':
        title,response,_=mentor['topics'][chat_topic]
        lines('You asked: '+title+'  '+response)
    elif chat_page=='reflection':
        title,response,_=mentor['topics'][chat_topic]
        if (chat_name,chat_topic) in mentor_checks_done:
            lines('You have already shown me you understand this, '+hero_name()+'. Excellent work. Ready for another topic?')
        elif chat_name in MAIN_MENTORS:
            lines('Now, '+hero_name()+', let us try something together. I will describe a situation from the arcade, and you tell me what you would do. Mistakes are welcome; we learn by testing.')
        else: lines('I hope that helps, '+hero_name()+'. You can come back to ask about the other secrets whenever you like.')
    box(48,306,544,29,(43,93,89),5)
    label='ENTER: CONTINUE'
    if chat_page=='name': label='TYPE NAME, THEN ENTER'
    elif chat_page in ('menu','experience'): label='UP/DOWN OR 1-3, THEN ENTER'
    elif chat_page=='reflection' and chat_name in MAIN_MENTORS and (chat_name,chat_topic) not in mentor_checks_done: label='ENTER: LET US TRY IT TOGETHER'
    draw_text(label,61,314,WHITE,S)
    draw_text('BACKSPACE: RETURN TO GAME   |   CLICK CONTINUE',50,352,GOLD,S)

def start_mentor_check():
    global state,check_name,check_topic,check_selected,check_feedback,chat_page
    if chat_name not in MAIN_MENTORS or (chat_name,chat_topic) in mentor_checks_done:
        chat_page='menu'; return
    check_name=chat_name; check_topic=chat_topic; check_selected=0; check_feedback=''; state='mentor_check'

def answer_mentor_check():
    global state,check_feedback,chat_page
    mentor_check_attempts[check_name][check_topic]+=1
    prompt,options,answer,why=LESSON_CHECKS[check_name][check_topic]
    if check_selected==answer:
        mentor_checks_done.add((check_name,check_topic))
        journal_add('LESSON PASSED: '+check_name+' '+str(check_topic+1)+' - '+why)
        check_feedback='CORRECT! '+why+'  ENTER TO CONTINUE.'
        state='mentor_result'
    else:
        stats['wrong']+=1
        check_feedback='NOT YET. '+why+'  ENTER TO TRY AGAIN.'
        state='mentor_retry'

def mentor_check_screen():
    prompt,options,answer,why=LESSON_CHECKS[check_name][check_topic]
    modal(check_name+' // LEARNING CHECK '+str(check_topic+1)+'/3','Use what your mentor explained. Wrong answers give hints, not penalties.')
    for i,line in enumerate(wrap_lines(prompt,53)):
        draw_text(line,49,148+i*23,WHITE,F)
    for i,option in enumerate(options):
        y=208+i*33
        box(46,y,548,29,(42,88,91) if i==check_selected else (32,39,59),4)
        draw_text(str(i+1)+'. '+option,57,y+6,WHITE,S)
    draw_text('UP/DOWN + ENTER   OR   PRESS 1, 2, 3',49,318,GOLD,S)

def mentor_result_screen():
    modal('LESSON CHECK // '+('COMPLETE' if state=='mentor_result' else 'TRY AGAIN'),'Learning is part of restoring the arcade.')
    for i,line in enumerate(wrap_lines(check_feedback,57)):
        draw_text(line,50,158+i*25,GREEN if state=='mentor_result' else GOLD,F)
    done=sum((check_name,i) in mentor_checks_done for i in range(3))
    draw_text('LESSONS COMPLETED: '+str(done)+'/3',50,252,CYAN,F)
    draw_text('ENTER/SPACE: CONTINUE',50,310,GOLD,F)

def journal_screen():
    modal('FIELD JOURNAL // DISCOVERIES','Knowledge, clues, and supplies found while exploring.')
    draw_text('PEOPLE MET '+str(len(mentor_met))+'/5    ENTRIES '+str(len(journal)),52,145,CYAN,F)
    start=journal_page*6
    for i,entry in enumerate(journal[start:start+6]):
        draw_text(str(start+i+1)+'. '+entry[:75],53,177+i*24,WHITE,S)
    if not journal: draw_text('Talk to people to fill your journal.',53,193,GRAY,F)
    draw_text('LEFT/RIGHT: PAGE    J OR BACKSPACE: RETURN',52,318,GOLD,S)

def draw_game_hud(chamber=False):
    # Three separate lines, each with fixed columns and no overlapping labels.
    box(0,0,640,77,(14,17,34))
    title='GLITCH BUSTERS / SECRET CHAMBER' if chamber else 'GLITCH BUSTERS / '+ROOMS[room]
    draw_text(title,12,7,CYAN,F)
    draw_text('ART '+str(len(artifacts))+'/3' + ('' if chamber else '   FIX '+str(len(solved))+'/16'),495,10,GOLD,S)
    for i in range(max_hp): heart(18+i*20,28,i<hp)
    # Label positions are fixed so changing counts never merges adjacent fields.
    equip='SWORD' if weapon!='PUNCH' else 'PUNCH'
    for x,label in [(165,'LIVES '+str(lives)),(231,equip),(310,'ARROWS '+str(arrows if has_bow else 0)),(407,'BOMBS '+str(bombs)),(502,'POTIONS '+str(potions))]:
        draw_text(label,x,33,WHITE,S)
    draw_text('CRYSTALS '+str(crystal_bank)+'/5',17,58,CYAN,S)
    draw_text('OVERDRIVE '+('READY' if crystal_bank==5 else 'CHARGING'),185,58,GOLD if crystal_bank==5 else CYAN,S)
    draw_text('LEGENDARY '+str(len(legendary))+'/3',347,58,CYAN,S)
    if not chamber:
        lessons=sum((MAIN_MENTORS[room],i) in mentor_checks_done for i in range(3))
        draw_text('LESSONS '+str(lessons)+'/3',527,58,GREEN if lessons==3 else GOLD,S)

def draw_game_footer(chamber=False):
    box(0,338,640,62,(15,18,35))
    if chamber:
        notice=message if msg_timer else 'FIND THE EXIT AFTER CLEARING THE CHAMBER'
    elif room not in puzzle_done:
        notice='EXIT LOCKED: SOLVE THE '+('CIRCUIT' if room==0 else 'PUZZLE')+' TO ADVANCE'
    else:
        notice=message if msg_timer else 'EXPLORE, REPAIR, AND DEFEAT THE GUARDIAN'
    # Fit the announcement into its own dedicated strip.
    draw_text(notice[:76],12,343,GOLD,S)
    draw_text('MOVE ARROWS   Z ATTACK   X DASH   C BOW   B BOMB   H HEAL',12,364,WHITE,S)
    draw_text('E INTERACT   V OVERDRIVE   J JOURNAL   R REPORT   M MUSIC',12,382,GRAY,S)
    if overdrive_time:
        draw_text('OD '+str((overdrive_time+59)//60)+'s',555,343,CYAN,S)

def background():
    if secret_room:
        draw_chamber(); return
    screen.fill(BG)
    palette=[(20,45,72),(30,37,82),(25,57,63),(58,29,72),(50,42,30)]
    box(23,63,594,268,palette[room],6)
    for x in range(29,610,27):
        for y in range(68,328,27):
            pygame.draw.rect(screen,(56,61,87),(x,y,25,25),1)
    # Neon floor accents and room-specific machinery.
    for j in range(7):
        xx=57+j*82
        pygame.draw.circle(screen,(42,88,108) if room%2==0 else (76,48,112),(xx,86),2)
    for i in range(3):
        xx=43+i*264
        box(xx,74,36,32,(16,23,42),5)
        box(xx+5,79,26,19,(35,71+room*8,105),3)
        pygame.draw.line(screen,PINK,(xx+9,94),(xx+26,84),2)
        box(xx+9,101,18,3,GOLD)
    for x in range(23,618,34):
        box(x,61,31,8,(78,75,119)); box(x,324,31,7,(78,75,119))
    for w in WALLS[room]:
        box(w.x,w.y,w.w,w.h,(78,71,107),3)
        pygame.draw.rect(screen,(139,119,161),w,2)
    for x,y,idx in STATIONS[room]:
        ok=idx in solved; c=GREEN if ok else (CYAN if idx%2==0 else GOLD)
        pygame.draw.circle(screen,(22,74,70) if ok else (57,47,86),(x,y),25)
        box(x-15,y-16,30,31,(20,24,43),4)
        box(x-11,y-12,22,19,c if ok else (65,59,108),2)
        draw_text('OK' if ok else '?',x-9,y-9,(19,26,43) if ok else WHITE,S)
        draw_text('REPAIR',x-23,y+20,c,S)
    for x,y,name,clue in NPCS[room]:
        box(x-10,y-8,20,23,(103,77,164),5)
        pygame.draw.circle(screen,(243,185,134),(x,y-11),9)
        box(x-6,y-16,12,4,(84,48,35))
        draw_text(name,x-18,y+17,GOLD,S)
    for name,data in MENTORS.items():
        if data['room']==room:
            x,y=data['pos']; draw_mentor(name,x,y,data['color'])
    for n,(x,y,item) in CHESTS.items():
        if n==room and n not in chests:
            box(x-15,y-9,30,20,(127,77,42),3)
            box(x-15,y-9,30,7,(213,150,67),2)
            box(x-2,y-6,5,9,GOLD)
    # Mandatory puzzle terminals are large, distinctive and clearly labelled.
    if room not in puzzle_done:
        px,py=PUZZLE_POS[room]
        box(px-28,py-25,56,47,(27,44,64),6)
        box(px-23,py-20,46,29,(64,92,122),4)
        pygame.draw.rect(screen,GOLD,(px-28,py-25,56,47),3,border_radius=6)
        for k in range(3):
            pygame.draw.circle(screen,(98,238,172) if k==0 else CYAN,(px-14+k*14,py-10),4)
        pygame.draw.line(screen,GOLD,(px-15,py+2),(px+15,py+2),2)
        draw_text('CIRCUIT PANEL' if room==0 else 'PUZZLE PANEL',px-47,py+27,GOLD,S)
        if distance(px,py)<78:
            box(max(30,min(450,px-102)),py-65,204,23,(20,37,55),5)
            draw_text('E - INSPECT CIRCUIT PANEL' if room==0 else 'E - INSPECT PUZZLE',max(36,min(456,px-96)),py-59,WHITE,S)

    # Power Crystals are collectible on the main path and in optional detours.
    for i,(cx,cy) in enumerate(CRYSTAL_SPOTS[room]):
        if (room,i) not in crystals:
            bob=math.sin(frame*.095+i)*3
            pts=[(cx,cy-10+bob),(cx+8,cy+bob),(cx,cy+10+bob),(cx-8,cy+bob)]
            pygame.draw.polygon(screen,(37,105,131),[(x+2,y+3) for x,y in pts])
            pygame.draw.polygon(screen,CYAN,pts)
            pygame.draw.line(screen,WHITE,(cx,cy-7+bob),(cx+3,cy+bob),2)
    if room in RESTRICTED and room not in legendary:
        name,reward,(gx,gy)=RESTRICTED[room]
        box(gx-24,gy-22,48,43,(29,47,73),5)
        for k in range(4):
            pygame.draw.line(screen,CYAN if frame//8%2 else PURPLE,
                (gx-20+k*13,gy-19),(gx-20+k*13,gy+17),3)
        draw_text('DANGER',gx-22,gy+25,GOLD,S)
        if distance(gx,gy)<80:
            draw_text('E: '+name[:22],max(30,gx-120),gy-43,WHITE,S)
    if 3 in legendary:
        for i,(sx,sy,kind,clue) in enumerate(SECRETS[room]):
            if (room,i) not in secret_found and distance(sx,sy)<145:
                pygame.draw.circle(screen,CYAN,(sx,sy),15+int(3*math.sin(frame*.12)),1)
    # Artifacts now live in concealed chambers, not in plain sight.
    if room<4:
        color=GREEN if ready_exit() else (85,66,100)
        box(585,255,25,48,color,4); draw_text('>',592,269,WHITE)
    if room>0:
        box(29,255,25,48,CYAN,4); draw_text('<',34,269,BG)
    # Subtle masonry: secret tiles use the same base shade as their neighbors.
    # A tiny one-pixel seam is the only visual hint. Nothing glows or has a marker.
    for i,(x,y,kind,clue) in enumerate(SECRETS[room]):
        if (room,i) not in secret_found:
            base=(78,75,119) if y<170 else (78,75,119)
            box(x-12,y-8,24,9,base)
            if i==0:
                pygame.draw.line(screen,(93,87,127),(x-4,y-6),(x+1,y-4),1)
            else:
                pygame.draw.line(screen,(91,84,125),(x+3,y-5),(x+6,y-2),1)
        else:
            box(x-13,y-9,26,13,(30,32,49))
            pygame.draw.rect(screen,(96,88,131),(x-13,y-9,26,13),1)
    for p in pickups:
        heart(int(p[0]),int(p[1]),True)
    for e in bugs:
        x,y=int(e['x']),int(e['y']); c=PINK if e['kind']=='hunter' else PURPLE if e['kind']=='patrol' else CYAN if e['kind']=='shooter' else RED if e['kind']=='charger' else GOLD
        pygame.draw.ellipse(screen,(24,25,45),(x-13,y+5,26,8))
        pygame.draw.ellipse(screen,WHITE if e.get('flash',0)>0 and frame%4<3 else c,(x-11,y-8,22,18))
        pygame.draw.circle(screen,WHITE,(x-4,y-2),3); pygame.draw.circle(screen,WHITE,(x+5,y-2),3)
        pygame.draw.circle(screen,BG,(x-4,y-2),1); pygame.draw.circle(screen,BG,(x+5,y-2),1)
        for dx in (-12,12): pygame.draw.line(screen,c,(x+dx,y+2),(x+dx*1.3,y+8),2)
        if e['kind']=='shooter':
            pygame.draw.circle(screen,WHITE,(x,y-2),4,1)
        if e['kind']=='charger' and e['tell']:
            pygame.draw.circle(screen,GOLD,(x,y),17,2)
        if e['kind']=='patrol': box(x-8,y-12,16,4,PURPLE)
        if e['hp']<e.get('max_hp',e['hp']):
            box(x-13,y-20,26,4,(75,46,68),1)
            box(x-13,y-20,26*max(0,e['hp'])/e['max_hp'],4,GREEN,1)
    for fx in hit_fx:
        x,y,life,damage_num=fx
        for k in range(6):
            a=k*math.pi/3+frame*.08; d=(15-life)*2
            pygame.draw.circle(screen,CYAN if k%2 else PINK,(int(x+math.cos(a)*d),int(y+math.sin(a)*d)),3)
        draw_text('-'+str(damage_num),x-8,y-25-(15-life),GOLD,F)
    for sh in shots:
        pygame.draw.circle(screen,GOLD if sh[4]=='arrow' else RED,(int(sh[0]),int(sh[1])),5)
    if boss:
        x,y=int(boss['x']),int(boss['y'])
        c=RED if boss_open else PURPLE
        pygame.draw.ellipse(screen,(16,15,35),(x-26,y+16,52,15))
        box(x-25,y-18,50,39,c,8)
        for dx in (-19,19): box(x+dx-5,y-27,10,15,c,3)
        pygame.draw.circle(screen,GOLD,(x-10,y-2),5); pygame.draw.circle(screen,GOLD,(x+10,y-2),5)
        if not boss_open: pygame.draw.ellipse(screen,CYAN,(x-30,y-26,60,57),2)
        box(235,83,170,7,(65,50,76),3)
        box(235,83,170*boss_hp/3,7,RED,3)
    human()
    if overdrive_time:
        pygame.draw.circle(screen,[CYAN,GOLD,PINK,GREEN,PURPLE][frame//4%5],player.center,22+frame%5,3)
        for i in range(5):
            a=frame*.15+i*math.tau/5
            pygame.draw.circle(screen,GOLD,(int(player.centerx+math.cos(a)*28),int(player.centery+math.sin(a)*28)),3)
    draw_game_hud()
    draw_game_footer()


def draw_chamber():
    screen.fill(BG)
    box(26,61,588,270,(24,31,50),7)
    for x in range(35,608,27):
        for y in range(72,319,27):
            pygame.draw.rect(screen,(42,54,76),(x,y,25,25),1)
    for x in range(30,612,27):
        box(x,65,24,11,(81,79,112)); box(x,318,24,11,(81,79,112))
    for y in range(77,319,25):
        box(27,y,10,23,(81,79,112)); box(603,y,10,23,(81,79,112))
    # A distinct room, with shelves, machinery, and a sealed chest.
    for x in (105,490):
        box(x,122,42,82,(43,54,78),5)
        box(x+5,129,32,10,(66,107,125)); box(x+5,148,32,10,(66,107,125))
        box(x+5,167,32,10,(66,107,125))
    box(300,205,40,32,(103,65,43),4)
    box(300,205,40,10,(202,143,62),3)
    box(318,211,5,11,GOLD)
    if not secret_chest_open:
        draw_text('SEALED' if secret_bugs else 'E: OPEN',293,185,GOLD,S)
    else: draw_text('EMPTY',301,185,GREEN,S)
    box(290,291,60,27,(46,122,105),4)
    draw_text('EXIT',305,297,WHITE,S)
    for e in secret_bugs:
        x,y=int(e['x']),int(e['y'])
        c=CYAN if e['kind']=='shooter' else PURPLE if e['kind']=='patrol' else GOLD
        pygame.draw.ellipse(screen,c,(x-12,y-9,24,20))
        pygame.draw.circle(screen,WHITE,(x-4,y-2),3)
        pygame.draw.circle(screen,WHITE,(x+5,y-2),3)
    for fx in hit_fx:
        x,y,life,damage_num=fx
        for k in range(6):
            a=k*math.pi/3+frame*.08; d=(15-life)*2
            pygame.draw.circle(screen,CYAN if k%2 else PINK,(int(x+math.cos(a)*d),int(y+math.sin(a)*d)),3)
        draw_text('-'+str(damage_num),x-8,y-25-(15-life),GOLD,F)
    for sh in shots:
        pygame.draw.circle(screen,RED if sh[4]=='enemy' else GOLD,(int(sh[0]),int(sh[1])),5)
    if secret_origin==2 and secret_index==0:
        draw_mentor('ECHO',450,253,MENTORS['ECHO']['color'])
    human()
    if overdrive_time:
        pygame.draw.circle(screen,[CYAN,GOLD,PINK,GREEN,PURPLE][frame//4%5],player.center,22+frame%5,3)
        for i in range(5):
            a=frame*.15+i*math.tau/5
            pygame.draw.circle(screen,GOLD,(int(player.centerx+math.cos(a)*28),int(player.centery+math.sin(a)*28)),3)
    draw_game_hud(chamber=True)
    draw_game_footer(chamber=True)


def update_chamber():
    global hp
    for e in secret_bugs[:]:
        if e.get('flash',0): e['flash']-=1
        if e.get('hurt',0): e['hurt']-=1; continue
        e['timer']-=1
        if e['timer']<=0:
            e['turn']=random.uniform(-math.pi,math.pi)
            e['timer']=random.randrange(55,120)
        if e['kind']=='patrol':
            e['x']+=e['vx']*1.35
            if e['x']<170 or e['x']>470: e['vx']*=-1
        elif e['kind']=='shooter':
            e['shot']-=1
            if e['shot']<=0:
                dx=player.centerx-e['x'];dy=player.centery-e['y']; mag=max(1,math.hypot(dx,dy))
                shots.append([e['x'],e['y'],dx/mag*2.4,dy/mag*2.4,'enemy'])
                e['shot']=120
        else:
            e['x']+=math.cos(e['turn'])*1.2; e['y']+=math.sin(e['turn'])*1.2
        e['x']=max(60,min(575,e['x']));e['y']=max(115,min(280,e['y']))
        if player.collidepoint(e['x'],e['y']): damage()
    for sh in shots[:]:
        sh[0]+=sh[2];sh[1]+=sh[3]
        if not AREA.collidepoint(sh[0],sh[1]): shots.remove(sh);continue
        if sh[4]=='enemy':
            if player.collidepoint(sh[0],sh[1]): damage(); shots.remove(sh)
        else:
            for e in secret_bugs[:]:
                if math.hypot(sh[0]-e['x'],sh[1]-e['y'])<17:
                    e['hp']-=1;shots.remove(sh)
                    if e['hp']<=0: secret_bugs.remove(e); stats['kills']+=1
                    break

def modal(title,subtitle):
    # A separate screen: do not draw the adventure HUD or its instructions behind menus.
    screen.fill(BG)
    box(0,0,640,53,(14,17,34))
    draw_text('GLITCH BUSTERS  /  '+hero_name(),22,17,CYAN,F)
    box(30,75,580,265,(13,19,37),9)
    pygame.draw.rect(screen,CYAN,(30,75,580,265),2,9)
    draw_text(title,48,92,GOLD,F)
    draw_text(subtitle,48,119,GRAY,S)

def question_screen():
    name,desc,code,opts,answer,*_=Q[active]
    modal('DEBUG TERMINAL // '+name,desc)
    box(47,143,546,66,(28,35,60),5)
    for i,line in enumerate(code): draw_text(line,62,150+i*24,GREEN,F)
    for i,opt in enumerate(opts):
        y=220+i*30
        box(47,y,546,27,(46,67,83) if i==selected else (29,34,55),4)
        draw_text(str(i+1)+'. '+opt,57,y+5,WHITE,S)
    draw_text('UP/DOWN + ENTER, 1-3, OR CLICK AN ANSWER',50,318,GOLD,S)

def lesson_screen():
    name,desc,code,opts,ans,why,ex1,ex2=Q[active]
    modal('DEBUG ASSISTANT // LEARNING MOMENT','Your answer was recorded. Read the explanation before trying again.')
    draw_text(why,52,153,WHITE,F)
    box(50,190,540,80,(30,40,59),5)
    draw_text(ex1,67,204,GREEN,F); draw_text(ex2,67,237,GREEN,F)
    draw_text('PRESS ENTER / SPACE / CLICK TO TRY AGAIN',52,304,GOLD,F)

def report_code():
    return ('GB2|R'+str(stats['runs'])+'|G'+str(stats['gameovers'])+'|D'+str(stats['damage'])+
        '|K'+str(stats['kills'])+'|W'+str(stats['wrong'])+'|Q'+'.'.join(map(str,stats['attempts']))+
        '|A'+''.join(str(i) for i in sorted(artifacts))+'|S'+''.join(str(i) for i in sorted(stats['rooms']))+
        '|V'+str(stats['victories'])+'|T'+str(int(stats['seconds']))+'|H'+str(stats['secrets'])+'|C'+str(stats['chests'])+'|DS'+str(stats['dashes'])+'|NPC'+str(stats['talks'])+'|J'+str(stats['lessons'])+'|P'+''.join(str(i) for i in sorted(puzzle_done))+'|PA'+'.'.join(map(str,puzzle_attempts))+'|ML'+''.join(str(sum((name,i) in mentor_checks_done for i in range(3))) for name in MAIN_MENTORS)+'|MA'+'.'.join(str(v) for name in MAIN_MENTORS for v in mentor_check_attempts[name])+'|NAME:'+hero_name().replace('|','').replace(' ','_')[:18]+'|EXP:'+player_experience.replace(' ','_')[:20]+
        '|PC'+str(crystal_total)+'|OD'+str(overdrive_earned)+'.'+str(overdrive_uses)+
        '|LG'+''.join(str(i) for i in sorted(legendary)) )

def copy_report():
    global copy_msg
    code=report_code()
    try:
        import js
        # Use the browser's native selectable text dialog as a reliable manual fallback.
        el=js.document.createElement('textarea'); el.value=code
        el.style.position='fixed'; el.style.top='0'; el.style.left='0'
        js.document.body.appendChild(el); el.focus(); el.select()
        ok=bool(js.document.execCommand('copy'))
        js.document.body.removeChild(el)
        if ok: copy_msg='COPIED! PASTE INTO THE GOOGLE FORM.'; return
        js.window.prompt('SELECT ALL (CTRL+A), COPY (CTRL+C), THEN PASTE INTO THE FORM:',code)
        copy_msg='USE CTRL+C IN THE POPUP, THEN CTRL+V IN THE FORM.'
    except Exception:
        copy_msg='BROWSER BLOCKED COPY. READ THE CODE BELOW.'

def report_screen():
    # Compact, fixed columns: the mission code is copied, not drawn over the stats.
    modal('MISSION INTELLIGENCE // LEVEL 2','Progress is information, not a penalty for mistakes.')
    box(43,137,554,120,(23,30,49),5)
    draw_text('RUNS '+str(stats['runs'])+'   GAME OVERS '+str(stats['gameovers'])+'   DAMAGE '+str(stats['damage']),53,145,WHITE,S)
    draw_text('BUGS '+str(stats['kills'])+'   ROOMS '+str(len(stats['rooms']))+'/5   ARTIFACTS '+str(len(artifacts))+'/3',53,165,WHITE,S)
    draw_text('SECRETS '+str(stats['secrets'])+'   WRONG '+str(stats['wrong'])+'   PUZZLES '+str(len(puzzle_done))+'/5',53,185,WHITE,S)
    draw_text('TIME '+str(int(stats['seconds']//60))+'m '+str(int(stats['seconds']%60))+'s   NPC '+str(stats['talks'])+'   WINS '+str(stats['victories']),53,205,WHITE,S)
    draw_text('LESSONS '+str(len(mentor_checks_done))+'/15   CRYSTALS '+str(crystal_total)+'   OVERDRIVE '+str(overdrive_uses),53,225,CYAN,S)
    draw_text('MISSION CODE FOR '+hero_name().upper()[:16],49,264,GOLD,S)
    draw_text('Use COPY CODE to submit your complete mission record.',49,285,GRAY,S)
    box(439,296,151,32,(39,107,102),5)
    draw_text('COPY CODE',462,303,WHITE,F)
    if copy_msg: draw_text(copy_msg[:43],49,309,GOLD,S)
    draw_text('R / BACKSPACE: RETURN',49,324,GRAY,S)

def distance(x,y): return math.hypot(player.centerx-x,player.centery-y)
def inspect_secret(mx=None,my=None):
    global potions,arrows,bombs,hp,speed_upgrade,sword_upgrade,secret_room,secret_origin,secret_index,secret_bugs,secret_chest_open
    for i,(x,y,kind,clue) in enumerate(SECRETS[room]):
        if (room,i) in secret_found: continue
        close=distance(x,y)<64
        clicked=mx is not None and math.hypot(mx-x,my-y)<22
        if not close or (mx is not None and not clicked): continue
        secret_found.add((room,i)); stats['secrets']+=1; play_sfx('unlock')
        secret_origin=room; secret_index=i; secret_room=True; secret_chest_open=False; shots.clear()
        secret_bugs=[bug(210,165,'patrol'),bug(430,210,'wander'),bug(320,250,'shooter')]
        player.topleft=(304,283)
        tell('A HIDDEN WALL OPENS! SEARCH THE CHAMBER, THEN USE THE EXIT.',230)
        return True
    return False

def interact():
    global active,selected,state,weapon,has_bow,arrows,bombs,potions,max_hp,hp,secret_room,secret_chest_open,room,speed_upgrade,sword_upgrade
    if secret_room:
        if secret_origin==2 and secret_index==0 and distance(450,253)<49:
            talk_to('ECHO'); return
        if distance(320,222)<52 and not secret_chest_open:
            if secret_bugs:
                tell('CHEST SEALED! CLEAR THE HIDDEN CHAMBER FIRST.',140); return
            secret_chest_open=True; play_sfx('treasure'); chamber_cleared.add((secret_origin,secret_index))
            grant_crystal('HIDDEN CHAMBER')
            n=secret_origin
            if secret_index==0 and n in ARTIFACTS and n not in artifacts:
                artifacts.add(n); tell('HIDDEN ARTIFACT FOUND: '+ARTIFACTS[n][2],220)
            elif n==1 and secret_index==0:
                potions+=2; tell('HIDDEN TREASURE: TWO HEALTH POTIONS!',220)
            elif n==4 and secret_index==0:
                hp=max_hp; tell('HIDDEN TREASURE: FULL HEALTH RESTORED!',220)
            elif n==0:
                speed_upgrade=True; tell('SECRET SPEED MODULE! MOVE FASTER!',220)
            elif n==2:
                sword_upgrade=True; tell('SECRET BLADE UPGRADE! STRONGER ATTACKS!',220)
            elif n==3:
                bombs+=3; tell('SECRET CACHE: THREE GLITCH BOMBS!',220)
            else:
                arrows+=8; tell('SECRET CACHE: EIGHT ARROWS!',220)
            return
        if distance(319,301)<48:
            secret_room=False; room=secret_origin; player.topleft=(100,115)
            tell('RETURNED TO '+ROOMS[room],150); return
        tell('DEFEAT THE GUARDS, OPEN THE CHEST, THEN RETURN THROUGH THE DOOR.',140); return
    if room in RESTRICTED and room not in legendary:
        title,reward,(gx,gy)=RESTRICTED[room]
        if distance(gx,gy)<65:
            start_gauntlet(room)
            return
    if room not in puzzle_done and distance(*PUZZLE_POS[room])<74:
        begin_puzzle(); return
    for name,data in MENTORS.items():
        if data['room']==room and distance(*data['pos'])<47:
            talk_to(name); return
    if inspect_secret(): return
    for x,y,q in STATIONS[room]:
        if q not in solved and distance(x,y)<44:
            active=q; selected=0; state='quiz'; return
    for x,y,name,clue in NPCS[room]:
        if distance(x,y)<48:
            if room not in npc_gifts:
                npc_gifts.add(room)
                if room==0: potions+=1; tell(name+': '+clue+' TAKE THIS POTION. LOOK FOR ODD WALL TILES.',280)
                elif room==1: potions+=1; tell(name+': '+clue+' HERE IS A POTION.',260)
                elif room==2: arrows+=5; tell(name+': '+clue+' TAKE FIVE ARROWS.',260)
                elif room==3: bombs+=2; tell(name+': '+clue+' TAKE TWO BOMBS.',260)
                else: potions+=1; tell(name+': '+clue+' TAKE A POTION.',260)
            else: tell(name+': '+clue+' LOOK FOR CRACKS AND ODD CABINETS.',260)
            return
    x,y,item=CHESTS[room]
    if room not in chests and distance(x,y)<47:
        if item=='armor' and len(artifacts)<3:
            tell('VAULT CHEST NEEDS ALL 3 ARTIFACTS!',160); return
        chests.add(room); stats['chests']+=1; play_sfx('treasure')
        if item=='sword': weapon='PIXEL SWORD'; tell('FOUND THE PIXEL SWORD! Z NOW DEALS MORE DAMAGE.',210)
        if item=='potion': potions+=2; tell('FOUND 2 HEALTH POTIONS! PRESS H TO USE.',210)
        if item=='bow': has_bow=True; arrows+=14; tell('DEBUG BOW UNLOCKED! PRESS C TO SHOOT.',210)
        if item=='bombs': bombs+=7; tell('GLITCH BOMBS UNLOCKED! PRESS B TO BLAST.',210)
        if item=='armor': max_hp=7; hp=7; tell('LEGENDARY ARMOR! MAX HEALTH INCREASED TO 7.',210)
        return

    tell('SEARCH FOR STATIONS, CHESTS, ARTIFACTS, OR NPCS.',100)

def submit_answer():
    global state,boss_open,boss_hacks,boss_quiz
    stats['attempts'][active]+=1
    if selected==Q[active][4]:
        state='world'
        if boss_quiz:
            boss_quiz=False; boss_open=540; boss_hacks+=1
            tell('SHIELD DOWN! MOVE CLOSE AND PRESS Z TO STRIKE!',240); play_sfx('unlock')
        else:
            solved.add(active); hp_restore(); play_sfx('repair')
            tell('REPAIR SUCCESSFUL! +1 HEART. '+Q[active][0],160)
    else:
        stats['wrong']+=1; state='lesson'

def hp_restore():
    global hp
    hp=min(max_hp,hp+1)

SFX_NAMES=('swing','hit','hurt','defeat','pickup','crystal','treasure','heal','repair','unlock','overdrive','bomb','victory')
sfx_bank={}
sfx_channels=[]
def play_sfx(name):
    if not music_enabled: return
    try:
        if not pygame.mixer.get_init(): return
        if name not in sfx_bank:
            sfx_bank[name]=pygame.mixer.Sound('sfx_'+name+'.ogg')
            sfx_bank[name].set_volume(.45)
        sfx_bank[name].play()
    except Exception:
        pass  # Never interrupt a lesson or gameplay for an audio failure.

def damage():
    global hp,lives,invuln,state
    if invuln or overdrive_time or state!='world': return
    hp-=1; stats['damage']+=1; invuln=80; play_sfx('hurt')
    if hp<=0:
        lives-=1; stats['lives']+=1
        if lives<=0:
            stats['gameovers']+=1; state='gameover'
        else:
            hp=max_hp; player.topleft=(65,283); invuln=130
            tell('LIFE LOST! '+str(lives)+' REMAINING.',140)

def hit_bug(e,amount,secret=False):
    e['hp']-=amount*(2 if 2 in legendary and weapon!='PUNCH' else 1); e['flash']=12; e['hurt']=12; play_sfx('hit')
    e['x']=max(55,min(582,e['x']+facing[0]*15))
    e['y']=max(107,min(300,e['y']+facing[1]*15))
    hit_fx.append([e['x'],e['y'],15,amount])
    if e['hp']<=0:
        play_sfx('defeat')
        if secret:
            if e in secret_bugs: secret_bugs.remove(e); stats['kills']+=1
        elif e in bugs: kill_bug(e)

def attack():
    global attack_time,attack_cd,boss_hp,boss,boss_open
    if attack_cd: return
    attack_cd=23 if weapon=='PUNCH' else 17; attack_time=11; play_sfx('swing')
    fx,fy=facing; reach=23 if weapon=='PUNCH' else 40
    target=pygame.Rect(player.centerx+fx*reach-17,player.centery+fy*reach-17,34,34)
    for e in (secret_bugs if secret_room else bugs)[:]:
        if target.collidepoint(e['x'],e['y']):
            hit_bug(e,1 if weapon=='PUNCH' else 3 if sword_upgrade else 2,secret_room)
    if not secret_room and boss and boss_open and math.hypot(target.centerx-boss['x'],target.centery-boss['y'])<53:
        boss_hp-=1; boss_open=0; boss_hacks_room[room]+=1; play_sfx('hit')
        hit_fx.append([boss['x'],boss['y'],15,1])
        tell('DIRECT HIT! GUARDIAN HAS '+str(boss_hp)+' HP LEFT.',100)
        if boss_hp<=0: defeat_boss()

def kill_bug(e):
    bugs.remove(e); stats['kills']+=1
    if random.random()<.22: pickups.append([e['x'],e['y'],360])

def defeat_boss():
    play_sfx('victory')
    global boss
    boss=None; rooms_done.add(room)
    tell('GUARDIAN DEFEATED! EXIT TO THE EAST IS OPEN!',230)

def shoot_bow():
    global arrows
    if not has_bow or arrows<=0: tell('FIND THE DEBUG BOW OR MORE ARROWS.',100); return
    arrows-=1; fx,fy=facing
    shots.append([float(player.centerx),float(player.centery),fx*5.5,fy*5.5,'arrow'])

def use_bomb():
    global bombs,boss_hp
    if bombs<=0: tell('NO BOMBS! FIND THEM IN THE FACTORY.',110); return
    bombs-=1; play_sfx('bomb'); x,y=player.center
    pygame.draw.circle(screen,GOLD,(x,y),55,4)
    for e in (secret_bugs if secret_room else bugs)[:]:
        if math.hypot(x-e['x'],y-e['y'])<82:
            if secret_room: secret_bugs.remove(e); stats['kills']+=1
            else: kill_bug(e)
    if not secret_room and boss and distance(boss['x'],boss['y'])<82 and boss_open:
        boss_hp-=1; boss_open=0; boss_hacks_room[room]+=1
        if boss_hp<=0: defeat_boss()
    tell('GLITCH BOMB DETONATED!',85)

def ready_exit():
    return all((MAIN_MENTORS[room],i) in mentor_checks_done for i in range(3)) and room in puzzle_done and all(q in solved for x,y,q in STATIONS[room]) and room in rooms_done and boss is None and not bugs

def update():
    global frame,invuln,attack_time,attack_cd,boss_open,boss_shot,spawn_cd,hp,state,boss,boss_hp,waves,dash_time,dash_cd,moving,reinforce_count,reinforce_timer
    frame+=1
    if state!='world': return
    stats['seconds']+=1/60
    global overdrive_time,gauntlet_cooldown,crystal_bank,overdrive_charges,overdrive_earned,crystal_total
    if invuln: invuln-=1
    if overdrive_time: overdrive_time-=1
    if gauntlet_cooldown: gauntlet_cooldown-=1
    if attack_time: attack_time-=1
    if attack_cd: attack_cd-=1
    if dash_cd: dash_cd-=1
    if dash_time: dash_time-=1
    msg_timer_update()
    keys=pygame.key.get_pressed(); dx=int(keys[pygame.K_RIGHT] or keys[pygame.K_d])-int(keys[pygame.K_LEFT] or keys[pygame.K_a]); dy=int(keys[pygame.K_DOWN] or keys[pygame.K_s])-int(keys[pygame.K_UP] or keys[pygame.K_w])
    global facing
    moving=bool(dx or dy)
    if dx or dy:
        if abs(dx)>abs(dy): facing=(1 if dx>0 else -1,0)
        else: facing=(0,1 if dy>0 else -1)
        scale=(7.4 if dash_time else 4.5 if overdrive_time else 3.25 if speed_upgrade else 2.95)/math.hypot(dx,dy)
        for axis,step in [('x',dx*scale),('y',dy*scale)]:
            old=player.copy()
            if axis=='x': player.x+=round(step)
            else: player.y+=round(step)
            if not secret_room and any(player.colliderect(w) for w in WALLS[room]): player.topleft=old.topleft
        player.clamp_ip(AREA)
    # Crystals persist after collection; returning to previous rooms is worthwhile.
    if not secret_room:
        for i,(cx,cy) in enumerate(CRYSTAL_SPOTS[room]):
            if (room,i) not in crystals and distance(cx,cy)<22 and crystal_bank<5:
                crystals.add((room,i)); grant_crystal('WORLD PICKUP')
                if crystal_bank==5:
                    tell('OVERDRIVE READY! PRESS V. OTHER CRYSTALS STAY UNTIL YOU USE IT.',190)
                else: tell('POWER CRYSTAL +1  |  '+str(crystal_bank)+'/5 TO OVERDRIVE',100)
    for fx in hit_fx[:]:
        fx[2]-=1
        if fx[2]<=0: hit_fx.remove(fx)
    if secret_room:
        update_chamber(); return
    if overdrive_time:
        for e in bugs[:]:
            if distance(e['x'],e['y'])<29:
                hit_bug(e,3)

    if room<4 and player.centerx>580 and 255<player.centery<306:
        if ready_exit():
            rooms_done.add(room); enter_room(room+1)
            return
        if frame%80==0:
            if not all((MAIN_MENTORS[room],i) in mentor_checks_done for i in range(3)):
                tell('EXIT LOCKED: TALK TO '+MAIN_MENTORS[room]+' AND PASS ALL 3 LESSON CHECKS.',140)
            else: tell('EXIT LOCKED: SOLVE THE PUZZLE, REPAIRS AND GUARDIAN.',100)
    if room>0 and player.centerx<57 and 255<player.centery<306:
        enter_room(room-1); player.topleft=(557,279); return
    for e in bugs[:]:
        if e.get('flash',0): e['flash']-=1
        if e.get('hurt',0):
            e['hurt']-=1
            continue
        e['timer']-=1
        if e['timer']<=0:
            e['turn']=random.uniform(-3.14,3.14)
            e['timer']=random.randrange(65,145)
            if e['kind']=='patrol': e['vx']*=-1
        dxp=player.centerx-e['x']; dyp=player.centery-e['y']
        angle=math.atan2(dyp,dxp)
        kind=e['kind']; speed=e['speed']
        if kind=='wander':
            angle=e['turn']; speed*=.8
        elif kind=='patrol':
            angle=0 if e['vx']>0 else math.pi; speed*=1.35
        elif kind=='hunter':
            angle+=math.sin(frame*.08+e['phase'])*.45; speed*=1.25
        elif kind=='shooter':
            # Keep distance; shoot rather than clustering around the hero.
            angle=angle+math.pi if math.hypot(dxp,dyp)<150 else e['turn']
            speed*=.65
            e['shot']-=1
            if e['shot']<=0:
                mag=max(1,math.hypot(dxp,dyp))
                shots.append([e['x'],e['y'],dxp/mag*2.7,dyp/mag*2.7,'enemy'])
                e['shot']=random.randrange(100,165)
        elif kind=='charger':
            if e['tell']>0:
                e['tell']-=1; speed=0
                if e['tell']==0: e['charge']=32; e['turn']=angle
            elif e['charge']>0:
                e['charge']-=1; angle=e['turn']; speed*=3.1
            elif math.hypot(dxp,dyp)<185 and e['timer']<40:
                e['tell']=35; speed=0
            else: angle=e['turn']; speed*=.55
        vx=math.cos(angle)*speed; vy=math.sin(angle)*speed
        for other in bugs:
            if other is e: continue
            dd=math.hypot(e['x']-other['x'],e['y']-other['y'])
            if 0<dd<54:
                vx+=(e['x']-other['x'])/dd*1.25
                vy+=(e['y']-other['y'])/dd*1.25
        e['x']=max(55,min(582,e['x']+vx)); e['y']=max(107,min(300,e['y']+vy))
        if player.collidepoint(e['x'],e['y']): damage()
    for p in pickups[:]:
        p[2]-=1
        if distance(p[0],p[1])<20:
            hp_restore(); play_sfx('pickup'); pickups.remove(p)
        elif p[2]<=0: pickups.remove(p)
    for sh in shots[:]:
        sh[0]+=sh[2]; sh[1]+=sh[3]
        if not AREA.collidepoint(sh[0],sh[1]): shots.remove(sh); continue
        if sh[4]=='enemy':
            if player.collidepoint(sh[0],sh[1]): damage(); shots.remove(sh)
        else:
            hit=False
            for e in bugs[:]:
                if math.hypot(sh[0]-e['x'],sh[1]-e['y'])<16:
                    hit_bug(e,1); hit=True
                    break
            if boss and boss_open and math.hypot(sh[0]-boss['x'],sh[1]-boss['y'])<43:
                boss_hp-=1; boss_open=0; boss_hacks_room[room]+=1; hit=True; play_sfx('hit'); hit_fx.append([boss['x'],boss['y'],15,1])
                if boss_hp<=0: defeat_boss()
            if hit: shots.remove(sh)
    if boss:
        # Guardians move in two dimensions, accelerate when wounded,
        # and summon a limited number of reinforcements after the first hit.
        if boss_hp<3 and reinforce_count<(2 if boss_hp==2 else 4):
            reinforce_timer-=1
            if reinforce_timer<=0:
                bx,by=random.choice([(110,160),(520,170),(170,275),(460,270)])
                bugs.append(bug(bx,by,['shooter','charger','hunter','patrol'][reinforce_count%4]))
                reinforce_count+=1; reinforce_timer=180 if boss_hp==1 else 280
                tell('GUARDIAN SUMMONED REINFORCEMENTS!',110)
        boss['x']+=math.sin(frame*.027)*(2.2 if boss_hp==1 else 1.6)
        boss['y']=135+math.sin(frame*.019+room)*48
        boss_shot-=1
        if boss_shot<=0:
            vx=player.centerx-boss['x']; vy=player.centery-boss['y']; mag=max(1,math.hypot(vx,vy))
            shots.append([boss['x'],boss['y'],vx/mag*2.5,vy/mag*2.5,'enemy'])
            boss_shot=90 if boss_hp>1 else 60
        if boss_open: boss_open-=1
        if distance(boss['x'],boss['y'])<37: damage()
    # Two additional finite waves per area. Guardians arrive only afterward.
    if not bugs and waves<3:
        waves+=1
        for i in range(3+room):
            bx=random.randint(125,510); by=random.randint(120,286)
            if math.hypot(bx-player.centerx,by-player.centery)<85: bx,by=500,135
            bugs.append(bug(bx,by,['wander','patrol','hunter','shooter','charger'][(i+waves+room)%5]))
        tell('GLITCH WAVE '+str(waves)+'/3! WATCH THE ENEMY PATTERNS.',140)
    if (waves>=3 and not bugs and boss is None and room not in rooms_done
        and all(q in solved for x,y,q in STATIONS[room])):
        boss={'x':315.,'y':110.,'dir':1,'timer':100,'phase':0}
        boss_hp=3
        boss_shot=90
        tell('WARNING: GUARDIAN EMERGING! GET CLOSE AND PRESS E TO HACK.',220)

def msg_timer_update():
    global msg_timer
    if msg_timer: msg_timer-=1
    return True

def try_boss_hack():
    global boss_open,boss_hacks,boss_quiz,active,selected,state
    if not boss: return False
    if distance(boss['x'],boss['y'])<165 and not boss_open:
        # One unique hack for each boss hit, no reused station questions.
        active=BOSS_Q[room][min(boss_hacks_room[room],2)]; selected=0
        boss_quiz=True; state='quiz'
        return True
    return False

def puzzle_note(msg):
    global puzzle_feedback,puzzle_feedback_timer
    puzzle_feedback=msg; puzzle_feedback_timer=210

# The six tiles form a snake-shaped route:
# START -> [1] [2] [3]
# EXIT  <- [4] [5] [6]
# Tiles 3 and 6 are elbows. Tiles 1,2,4,5 are straight.
# Check actual matching wire connections rather than a hardcoded orientation list.
CIRCUIT_SHAPES=('straight','straight','elbow','straight','straight','elbow')
CIRCUIT_START=[1,1,0,1,1,2]
CIRCUIT_PATH=[0,1,2,5,4,3]
CIRCUIT_DIRS={'N':(0,-1),'E':(1,0),'S':(0,1),'W':(-1,0)}
CIRCUIT_OPPOSITE={'N':'S','S':'N','E':'W','W':'E'}

def circuit_ports(index):
    turn=circuit_tiles[index]
    if CIRCUIT_SHAPES[index]=='straight':
        return {'E','W'} if turn%2==0 else {'N','S'}
    return [ {'N','E'}, {'E','S'}, {'S','W'}, {'W','N'} ][turn%4]

def circuit_powered():
    # Power enters tile 1 from the left and must leave tile 4 to the left.
    if 'W' not in circuit_ports(0):return set()
    powered={0}; pending=[0]
    while pending:
        i=pending.pop()
        x,y=i%3,i//3
        for d,(dx,dy) in CIRCUIT_DIRS.items():
            nx,ny=x+dx,y+dy
            if not (0<=nx<3 and 0<=ny<2):continue
            j=ny*3+nx
            if j not in powered and d in circuit_ports(i) and CIRCUIT_OPPOSITE[d] in circuit_ports(j):
                powered.add(j);pending.append(j)
    return powered

def circuit_solved():
    return len(circuit_powered())==6 and 'W' in circuit_ports(3)

def rotate_circuit(index):
    global circuit_selected
    circuit_selected=index
    circuit_tiles[index]=(circuit_tiles[index]+1)%(2 if CIRCUIT_SHAPES[index]=='straight' else 4)
    puzzle_attempts[0]+=1
    if circuit_solved():finish_puzzle()
    else:puzzle_note('TILE '+str(index+1)+' ROTATED. GREEN WIRES HAVE POWER.')

def circuit_click(mx,my):
    if room!=0:return
    for i in range(6):
        x=132+(i%3)*124;y=128+(i//3)*96
        if pygame.Rect(x,y,91,82).collidepoint(mx,my):
            rotate_circuit(i)
            return

def begin_puzzle():
    global state,puzzle_step,puzzle_switches,crate_player,crate_boxes,mirror_angles,mirror_selected,vault_input,conduits,conduit_selected,conduit_timer,conduit_damage,circuit_tiles,circuit_selected
    state='puzzle'; puzzle_step=0; puzzle_switches=[False]*3
    circuit_tiles=[1,1,0,1,1,2]; circuit_selected=0
    crate_player=[0,3]; crate_boxes={(1,1),(3,2)}
    mirror_angles=[0,0,0]; mirror_selected=0; vault_input=[]
    conduits=[0,0,0]; conduit_selected=0; conduit_timer=0; conduit_damage=0
    puzzle_note('Restore power to unlock the stage exit. H hint; BACKSPACE leaves.')

def finish_puzzle():
    global state,victory_kind,victory_countdown
    puzzle_done.add(room); stats['puzzles']+=1; play_sfx('victory')
    journal_add('PUZZLE SOLVED: '+PUZZLE_NAMES[room])
    grant_crystal('PUZZLE COMPLETE')
    victory_kind='puzzle'; victory_countdown=90
    state='celebrate'

def puzzle_key(key):
    global puzzle_step,puzzle_switches,crate_player,crate_boxes,mirror_selected,mirror_angles,vault_input,conduit_selected,conduits,conduit_timer,circuit_tiles,circuit_selected
    if key==pygame.K_BACKSPACE:
        return 'exit'
    if key==pygame.K_h:
        puzzle_hints[room]+=1; journal_add(PUZZLE_HINTS[room]); puzzle_note(PUZZLE_HINTS[room]); return
    if room==0:
        if key in (pygame.K_LEFT,pygame.K_a): circuit_selected=(circuit_selected-1)%6
        elif key in (pygame.K_RIGHT,pygame.K_d): circuit_selected=(circuit_selected+1)%6
        elif key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6):
            circuit_selected=key-pygame.K_1
            puzzle_note('TILE '+str(circuit_selected+1)+' SELECTED. PRESS SPACE TO ROTATE.')
        elif key in (pygame.K_SPACE,pygame.K_RETURN):rotate_circuit(circuit_selected)
        elif key==pygame.K_r:
            circuit_tiles[:]=CIRCUIT_START[:];circuit_selected=0
            puzzle_note('CIRCUIT RESET. GREEN WIRES HAVE POWER.')
    elif room==1:
        if key==pygame.K_r:
            crate_player=[0,3]; crate_boxes={(1,1),(3,2)}; puzzle_note('CRATES RESET.'); return
        moves={pygame.K_LEFT:(-1,0),pygame.K_RIGHT:(1,0),pygame.K_UP:(0,-1),pygame.K_DOWN:(0,1),pygame.K_a:(-1,0),pygame.K_d:(1,0),pygame.K_w:(0,-1),pygame.K_s:(0,1)}
        if key not in moves:return
        dx,dy=moves[key]; nx=crate_player[0]+dx; ny=crate_player[1]+dy
        if not (0<=nx<5 and 0<=ny<4):return
        if (nx,ny) in crate_boxes:
            bx,by=nx+dx,ny+dy
            if not (0<=bx<5 and 0<=by<4) or (bx,by) in crate_boxes:
                puzzle_note('BLOCKED! THINK ABOUT WHERE THE CRATE CAN GO.'); return
            crate_boxes.remove((nx,ny)); crate_boxes.add((bx,by)); puzzle_attempts[room]+=1
        crate_player=[nx,ny]
        if crate_boxes==crate_targets:finish_puzzle()
    elif room==2:
        if key in (pygame.K_LEFT,pygame.K_a):mirror_selected=(mirror_selected-1)%3
        elif key in (pygame.K_RIGHT,pygame.K_d):mirror_selected=(mirror_selected+1)%3
        elif key in (pygame.K_SPACE,pygame.K_RETURN):
            mirror_angles[mirror_selected]=(mirror_angles[mirror_selected]+1)%2; puzzle_attempts[room]+=1
            if mirror_angles==[1,0,1]:finish_puzzle()
            else:puzzle_note('MIRROR '+str(mirror_selected+1)+' ROTATED. FOLLOW THE LIGHT PATH.')
    elif room==3:
        keys={pygame.K_1:0,pygame.K_2:1,pygame.K_3:2,pygame.K_4:3}
        if key in keys:
            value=keys[key]; puzzle_attempts[room]+=1
            if value==vault_order[len(vault_input)]:
                vault_input.append(value); puzzle_note('SYMBOL ACCEPTED '+str(len(vault_input))+'/4')
                if len(vault_input)==4:finish_puzzle()
            else:
                vault_input=[]; puzzle_note('INCORRECT SYMBOL. THE VAULT RESETS.')
    elif room==4:
        if key in (pygame.K_LEFT,pygame.K_a):conduit_selected=(conduit_selected-1)%3
        elif key in (pygame.K_RIGHT,pygame.K_d):conduit_selected=(conduit_selected+1)%3
        elif key in (pygame.K_SPACE,pygame.K_RETURN,pygame.K_1,pygame.K_2,pygame.K_3):
            if key in (pygame.K_1,pygame.K_2,pygame.K_3):conduit_selected=key-pygame.K_1
            conduits[conduit_selected]=1; puzzle_attempts[room]+=1
            puzzle_note('CONDUIT '+str(conduit_selected+1)+' ONLINE! DEFEND THE POWER.')
    return None

def puzzle_update():
    global conduit_timer,conduit_damage,puzzle_feedback_timer
    stats['seconds']+=1/60
    if puzzle_feedback_timer:puzzle_feedback_timer-=1
    if room==4 and all(conduits):
        conduit_timer+=1
        # Incoming glitch pulses disrupt one conduit. Players must react and repair it.
        if conduit_timer in (120,250):
            i=0 if conduit_timer==120 else 2
            conduits[i]=0; conduit_damage+=1
            puzzle_note('GLITCH PULSE! CONDUIT '+str(i+1)+' IS OFFLINE!')
        if conduit_timer>=390:finish_puzzle()

def puzzle_screen():
    screen.fill(BG); box(24,60,592,273,(26,35,58),8)
    center('PUZZLE '+str(room+1)+': '+PUZZLE_NAMES[room],22,CYAN,L)
    draw_text('H: HINT     BACKSPACE: RETURN TO ADVENTURE',37,378,GOLD,S)
    if room==0:
        center('CONNECT POWER THROUGH ALL SIX WIRE TILES',74,WHITE,F)
        center('CLICK A TILE TO ROTATE IT. GREEN = POWERED.',97,GOLD,S)
        powered=circuit_powered()
        for i in range(6):
            col=i%3;row=i//3;x=132+col*124;y=128+row*96
            box(x,y,91,82,(58,68,96),7)
            if i==circuit_selected:
                pygame.draw.rect(screen,GOLD,(x-3,y-3,97,88),3,border_radius=7)
            pygame.draw.circle(screen,(35,43,63),(x+45,y+41),28)
            color=GREEN if i in powered else CYAN
            for direction in circuit_ports(i):
                dx,dy=CIRCUIT_DIRS[direction]
                pygame.draw.line(screen,color,(x+45,y+41),(x+45+dx*27,y+41+dy*27),8)
            pygame.draw.circle(screen,GOLD,(x+45,y+41),7)
            draw_text(str(i+1),x+42,y+67,WHITE,S)
        draw_text('START >',56,160,GREEN,S)
        draw_text('< EXIT',48,255,GREEN,S)
        box(28,316,584,56,(13,18,35),5)
        center('ARROWS: SELECT   SPACE: ROTATE   1-6: SELECT   R: RESET',324,GOLD,S)
        center('POWERED: '+str(len(powered))+'/6    |    TILES 3 AND 6 ARE ELBOWS',346,GRAY,S)
    elif room==1:
        center('PUSH BOTH CRATES ONTO THE BLUE TARGETS',76,WHITE,F)
        ox,oy=180,107; tile=52
        for y in range(4):
            for x in range(5):
                c=(49,66,88) if (x+y)%2 else (44,60,82)
                box(ox+x*tile,oy+y*tile,tile-3,tile-3,c,4)
                if (x,y) in crate_targets:
                    pygame.draw.rect(screen,CYAN,(ox+x*tile+9,oy+y*tile+9,tile-21,tile-21),3)
                if (x,y) in crate_boxes:box(ox+x*tile+7,oy+y*tile+7,35,35,(192,124,66),5)
                if [x,y]==crate_player:pygame.draw.circle(screen,GREEN,(ox+x*tile+25,oy+y*tile+24),13)
        center('ARROWS MOVE/PUSH   R RESET',324,GOLD,S)
    elif room==2:
        center('ROTATE THE MIRRORS TO GUIDE THE LASER',83,WHITE,F)
        for i in range(3):
            x=159+i*156; y=181
            pygame.draw.circle(screen,GOLD if mirror_selected==i else (83,95,124),(x,y),43,3)
            if mirror_angles[i]:pygame.draw.line(screen,CYAN,(x-22,y+22),(x+22,y-22),6)
            else:pygame.draw.line(screen,CYAN,(x-22,y-22),(x+22,y+22),6)
            draw_text('MIRROR '+str(i+1),x-37,239,WHITE,S)
        # A laser visibly advances only through correctly oriented mirrors.
        pygame.draw.line(screen,RED,(47,181),(117,181),4)
        if mirror_angles[0]==1:
            pygame.draw.line(screen,RED,(202,181),(273,181),4)
            if mirror_angles[1]==0:
                pygame.draw.line(screen,RED,(358,181),(429,181),4)
                if mirror_angles[2]==1:
                    pygame.draw.line(screen,GREEN,(514,181),(550,181),5)
        pygame.draw.circle(screen,GREEN if mirror_angles==[1,0,1] else PURPLE,(568,181),17,3)
        center('LEFT/RIGHT SELECT   SPACE ROTATE',293,GOLD,F)
    elif room==3:
        center('THE ARCHIVIST LEFT A FOUR-SYMBOL CODE',81,WHITE,F)
        names=['MOON','BOLT','STAR','GEAR']
        for i,name in enumerate(names):
            x=63+i*143
            box(x,154,120,62,(63,68,107),6)
            draw_text(str(i+1)+' '+name,x+13,174,GOLD,F)
        center('ENTER THE SYMBOLS IN ORDER USING 1-4',258,WHITE,F)
        center('ACCEPTED '+str(len(vault_input))+'/4',294,GREEN,F)
    else:
        center('POWER THREE CONDUITS AND DEFEND THEM',81,WHITE,F)
        for i in range(3):
            x=132+i*157
            box(x,145,106,84,GREEN if conduits[i] else (72,55,92),8)
            if conduit_selected==i:pygame.draw.rect(screen,GOLD,(x-4,141,114,92),3,border_radius=8)
            draw_text('CORE '+str(i+1),x+19,166,WHITE,F)
            draw_text('ON' if conduits[i] else 'OFF',x+36,195,WHITE,S)
        box(98,255,445,17,(57,61,84),5)
        box(98,255,445*min(390,conduit_timer)/390,17,CYAN,5)
        center('LEFT/RIGHT SELECT   SPACE REPAIR   1-3 DIRECT',294,GOLD,S)
    if puzzle_feedback_timer:
        box(33,365,574,27,(44,51,78),5)
        draw_text(puzzle_feedback[:82],42,372,GOLD,S)

def grant_crystal(reason):
    # A full meter never destroys a reward. World crystals remain on the map,
    # while one-time puzzle/chest rewards wait safely until the meter has space.
    global crystal_bank,crystal_total,pending_crystals,overdrive_earned
    if crystal_bank>=5:
        pending_crystals+=1
        journal_add('POWER CRYSTAL RESERVED: '+reason)
        tell('OVERDRIVE FULL! CRYSTAL REWARD SAVED FOR AFTER ACTIVATION.',160)
        return
    crystal_total+=1; crystal_bank+=1; play_sfx('crystal')
    journal_add('POWER CRYSTAL: '+reason)
    if crystal_bank==5:
        overdrive_earned+=1
        journal_add('OVERDRIVE READY: PRESS V TO ACTIVATE.')


def activate_overdrive():
    global overdrive_time,overdrive_uses,crystal_bank,pending_crystals
    if overdrive_time:
        tell('OVERDRIVE PROTOCOL ALREADY ACTIVE!',90)
    elif crystal_bank==5:
        crystal_bank=0; overdrive_uses+=1; play_sfx('overdrive')
        overdrive_time=(18 if 3 in legendary else 12)*60
        # Deliver reserved one-time rewards only after the full meter is spent.
        while pending_crystals and crystal_bank<5:
            pending_crystals-=1
            grant_crystal('SAVED REWARD')
        tell('OVERDRIVE ACTIVATED! '+str(crystal_bank)+'/5 CRYSTALS IN NEW METER.',190)
    else:
        tell('COLLECT FIVE POWER CRYSTALS TO CHARGE OVERDRIVE.',140)

def start_gauntlet(n):
    global state,gauntlet_room,gauntlet_x,gauntlet_y,gauntlet_hits,gauntlet_cooldown,gauntlet_return
    gauntlet_room=n; gauntlet_x=42; gauntlet_y=200; gauntlet_hits=0; gauntlet_cooldown=0
    gauntlet_return=player.topleft
    state='gauntlet'
    journal_add('RESTRICTED AREA DISCOVERED: '+RESTRICTED[n][0])

def finish_gauntlet():
    global state,max_hp,hp,sword_upgrade,overdrive_time,victory_kind,victory_countdown
    n=gauntlet_room
    if n in legendary: return
    legendary.add(n); play_sfx('victory')
    if n==1:
        max_hp+=2; hp=max_hp
    elif n==2:
        sword_upgrade=True
    elif n==3:
        # Root Access permanently lengthens Overdrive, including an active charge.
        if overdrive_time: overdrive_time+=6*60
    journal_add('LEGENDARY UPGRADE: '+RESTRICTED[n][1])
    victory_kind='legendary'; victory_countdown=105; state='celebrate'

def gauntlet_update():
    global frame,gauntlet_x,gauntlet_y,gauntlet_cooldown,gauntlet_hits,overdrive_time,hp
    frame+=1; stats['seconds']+=1/60
    if overdrive_time: overdrive_time-=1
    if gauntlet_cooldown: gauntlet_cooldown-=1
    keys=pygame.key.get_pressed()
    speed=5.8 if overdrive_time else 3.0
    gauntlet_x+=speed*(int(keys[pygame.K_RIGHT] or keys[pygame.K_d])-int(keys[pygame.K_LEFT] or keys[pygame.K_a]))
    gauntlet_y+=speed*(int(keys[pygame.K_DOWN] or keys[pygame.K_s])-int(keys[pygame.K_UP] or keys[pygame.K_w]))
    gauntlet_x=max(38,min(603,gauntlet_x)); gauntlet_y=max(112,min(290,gauntlet_y))
    for i,x in enumerate((157,243,329,415,501)):
        live=(frame//38+i)%3!=0
        if live and abs(gauntlet_x-x)<17 and not overdrive_time and not gauntlet_cooldown:
            gauntlet_hits+=1; gauntlet_cooldown=95; gauntlet_x=max(40,gauntlet_x-55)
            hp=max(1,hp-1); stats['damage']+=1
    if gauntlet_x>571: finish_gauntlet()

def gauntlet_screen():
    screen.fill(BG)
    n=gauntlet_room
    title,reward,_=RESTRICTED[n]
    center(title,21,CYAN,L)
    center('RESTRICTED ACCESS  //  REWARD: '+reward,60,GOLD,S)
    box(25,91,590,221,(25,35,59),7)
    for x in range(40,605,28):
        for y in range(104,300,28):
            pygame.draw.rect(screen,(44,57,80),(x,y,26,26),1)
    for i,x in enumerate((157,243,329,415,501)):
        live=(frame//38+i)%3!=0
        color=CYAN if live else (55,81,97)
        for j in range(6):
            yy=106+j*33
            pygame.draw.line(screen,color,(x+int(math.sin(frame*.25+j)*4),yy),(x-int(math.sin(frame*.25+j)*4),yy+31),5 if live else 2)
        draw_text('LIVE' if live else 'OFF',x-14,94,GOLD if live else GRAY,S)
    box(566,170,34,60,(53,144,99),5)
    draw_text('EXIT',568,153,WHITE,S)
    hero_color=[CYAN,PINK,GOLD,GREEN,PURPLE][frame//5%5] if overdrive_time else GREEN
    pygame.draw.circle(screen,hero_color,(int(gauntlet_x),int(gauntlet_y)),12)
    if overdrive_time:pygame.draw.circle(screen,GOLD,(int(gauntlet_x),int(gauntlet_y)),20,3)
    box(20,326,600,65,(16,23,42),5)
    draw_text('ARROWS: MOVE  |  V: OVERDRIVE  |  BACKSPACE: RETURN',34,336,WHITE,S)
    draw_text('TIME THE PULSES OR USE OVERDRIVE. THE EXIT IS ON THE RIGHT.',34,356,CYAN,S)
    draw_text('HEARTS '+str(hp)+'  HITS '+str(gauntlet_hits)+'  METER '+str(crystal_bank)+'/5'+'  ACTIVE '+str((overdrive_time+59)//60)+'s',34,374,GOLD,S)

def celebration_screen():
    global victory_countdown
    screen.fill((10,18,35))
    n=room if victory_kind=='puzzle' else gauntlet_room
    pulse=(frame//6)%5
    for i in range(7):
        pygame.draw.circle(screen,[CYAN,GREEN,GOLD,PURPLE,PINK][(i+pulse)%5],
            (320,174),28+i*21,2)
    if victory_kind=='puzzle':
        center('CIRCUIT RESTORED!' if n==0 else 'PUZZLE COMPLETE!',45,GREEN,L)
        center(PUZZLE_NAMES[n],98,CYAN,F)
        center('POWER CRYSTAL EARNED!',237,GOLD,L)
        center('EXIT SYSTEM RESTORED. WELL DONE, '+hero_name().upper()[:14]+'!',282,WHITE,S)
    else:
        center('LEGENDARY UPGRADE DISCOVERED!',45,GOLD,F)
        center(RESTRICTED[n][1],102,CYAN,L)
        explanation={1:'+2 MAX HEARTS  |  BLUE CAPACITOR ARMOR',
                     2:'DOUBLE SWORD DAMAGE  |  ELECTRIC BLADE',
                     3:'ROOT SCANNER  |  OVERDRIVE LASTS 18 SECONDS'}[n]
        center(explanation,252,GREEN,F)
        if len(legendary)==3: center('ALL THREE UPGRADES! MASTER ENDING UNLOCKED.',283,GOLD,S)
    if victory_countdown>0:
        center('ENERGY SURGE IN PROGRESS...',325,GRAY,S)
    else:
        center('PRESS ENTER OR CLICK TO CONTINUE',325,WHITE,F)

def draw_title():
    screen.fill(BG)
    for i in range(13):
        x=(i*53+frame//4)%W; y=(i*39+30)%H
        box(x,y,8,8,(45,55,99))
    center('GLITCH BUSTERS',85,CYAN,L)
    center('LEVEL 2: COORDINATE CHAOS',130,GOLD,F)
    center('FIVE AREAS  |  FIVE PUZZLES  |  HIDDEN SECRETS  |  NPCS',183,WHITE,S)
    center('WEEK 2 PYTHON: X/Y, MOVEMENT, BOUNDARIES, COINS, SCORE',207,GREEN,S)
    center('ENTER TO BEGIN THE ADVENTURE',265,GOLD,F)
    center('F11: FULLSCREEN   M: MUSIC ON/OFF   ESC: LEAVE FULLSCREEN',301,GRAY,S)

def draw_end(won):
    background(); box(54,103,530,194,(17,24,43),8)
    center('LEVEL 2 COMPLETE!' if won else 'GAME OVER',130,GREEN if won else RED,L)
    center('ARTIFACTS '+str(len(artifacts))+'/3   PUZZLES '+str(len(puzzle_done))+'/5',185,GOLD,F)
    if won and len(legendary)==3: center('MASTER GLITCH BUSTER ENDING UNLOCKED!',218,CYAN,F)
    center('R: MISSION REPORT     ENTER: RESTART',253,WHITE,F)


music_enabled=True
music_started=False
music_channel=None
music_tracks={}

def music_control(toggle=False):
    global music_enabled,music_started,music_channel
    if toggle: music_enabled=not music_enabled
    try:
        if not pygame.mixer.get_init(): pygame.mixer.init()
        if not music_tracks:
            for name in ('arcade','puzzle','boss','title'):
                music_tracks[name]=pygame.mixer.Sound('music_'+name+'.ogg')
        if not music_enabled:
            if music_channel: music_channel.stop()
            return
        desired='title' if state=='title' else 'puzzle' if state in ('puzzle','quiz','mentor_check','gauntlet') else 'boss' if state=='world' and boss else 'arcade'
        if not music_channel or not music_channel.get_busy() or music_started!=desired:
            if music_channel: music_channel.stop()
            music_channel=music_tracks[desired].play(loops=-1)
            if music_channel: music_channel.set_volume(.24)
            music_started=desired
    except Exception as err:
        # Some school browsers may disable audio; gameplay must still work.
        if not music_started: print('QuestForge audio unavailable:',err)
        music_started='unavailable'

async def game_loop():
    global state, chat_page, chat_selected, check_selected, dash_cd, dash_time
    global frame, hp, invuln, journal_page, player_name, potions
    global report_return, selected, victory_countdown
    running=True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                mx,my=event.pos
                if state=='world':
                    if secret_room:
                        if secret_origin==2 and secret_index==0 and math.hypot(mx-450,my-253)<28 and distance(450,253)<49:
                            talk_to('ECHO')
                        elif pygame.Rect(288,206,65,38).collidepoint(mx,my) or pygame.Rect(289,281,65,37).collidepoint(mx,my): interact()
                    else:
                        clicked_person=False
                        for name,data in MENTORS.items():
                            if data['room']==room:
                                x,y=data['pos']
                                if math.hypot(mx-x,my-y)<30 and distance(x,y)<47:
                                    talk_to(name); clicked_person=True; break
                        if not clicked_person:
                            if room not in puzzle_done and math.hypot(mx-PUZZLE_POS[room][0],my-PUZZLE_POS[room][1])<42 and distance(*PUZZLE_POS[room])<85:
                                begin_puzzle()
                            else: inspect_secret(mx,my)
                elif state=='quiz' and 220<=my<310:
                    i=(my-220)//30
                    if 0<=i<3: selected=i; submit_answer()
                elif state=='puzzle':
                    circuit_click(mx,my)
                elif state=='celebrate' and victory_countdown<=0:
                    state='world'
                    if victory_kind=='legendary':player.topleft=gauntlet_return
                elif state=='mentor_check' and 208<=my<307:
                    check_selected=(my-208)//33
                    if 0<=check_selected<3: answer_mentor_check()
                elif state in ('mentor_result','mentor_retry'):
                    if state=='mentor_result': state='dialogue'; chat_page='menu'
                    else: state='mentor_check'
                elif state=='dialogue':
                    if chat_page in ('menu','experience') and 213<=my<300:
                        chat_selected=max(0,min(2,(my-213)//29)); dialogue_advance()
                    elif pygame.Rect(48,303,544,29).collidepoint(mx,my): dialogue_advance()
                elif state=='lesson': state='quiz'
                elif state=='report' and pygame.Rect(445,301,143,30).collidepoint(mx,my): copy_report()
            if event.type!=pygame.KEYDOWN: continue
            if event.key==pygame.K_m:
                music_control(toggle=True)
                continue
            if state=='title':
                if event.key==pygame.K_RETURN: new_game(); music_control()
                elif event.key==pygame.K_r: report_return='title'; state='report'
            elif state=='world':
                if event.key==pygame.K_z: attack()
                elif event.key==pygame.K_x:
                    if not dash_cd:
                        dash_time=9; dash_cd=75; invuln=max(invuln,11); stats['dashes']+=1
                elif event.key==pygame.K_c: shoot_bow()
                elif event.key==pygame.K_b: use_bomb()
                elif event.key==pygame.K_h:
                    if potions and hp<max_hp: potions-=1; hp=min(max_hp,hp+3); play_sfx('heal'); tell('HEALTH RESTORED!')
                elif event.key==pygame.K_e:
                    if not try_boss_hack(): interact()
                elif event.key==pygame.K_r: report_return='world'; state='report'
                elif event.key==pygame.K_j: journal_page=0; state='journal'
                elif event.key==pygame.K_v: activate_overdrive()
            elif state=='puzzle':
                if puzzle_key(event.key)=='exit': state='world'
            elif state=='gauntlet':
                if event.key==pygame.K_BACKSPACE:
                    state='world'; player.topleft=gauntlet_return
                elif event.key==pygame.K_v: activate_overdrive()
            elif state=='celebrate':
                if victory_countdown<=0 and event.key in (pygame.K_RETURN,pygame.K_SPACE):
                    state='world'
                    if victory_kind=='legendary': player.topleft=gauntlet_return
            elif state=='dialogue':
                if chat_page=='name':
                    if event.key==pygame.K_RETURN: dialogue_advance()
                    elif event.key==pygame.K_BACKSPACE: player_name=player_name[:-1]
                    elif event.unicode and event.unicode.isprintable() and len(player_name)<18:
                        if event.unicode.isalpha() or event.unicode in (' ','-','_'):
                            player_name+=event.unicode
                elif event.key==pygame.K_BACKSPACE: state='world'
                elif chat_page in ('menu','experience'):
                    if event.key==pygame.K_UP: chat_selected=(chat_selected-1)%3
                    elif event.key==pygame.K_DOWN: chat_selected=(chat_selected+1)%3
                    elif event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                        chat_selected=event.key-pygame.K_1; dialogue_advance()
                    elif event.key in (pygame.K_RETURN,pygame.K_SPACE): dialogue_advance()
                elif event.key in (pygame.K_RETURN,pygame.K_SPACE): dialogue_advance()
            elif state=='mentor_check':
                if event.key==pygame.K_UP: check_selected=(check_selected-1)%3
                elif event.key==pygame.K_DOWN: check_selected=(check_selected+1)%3
                elif event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                    check_selected=event.key-pygame.K_1; answer_mentor_check()
                elif event.key in (pygame.K_RETURN,pygame.K_SPACE): answer_mentor_check()
            elif state in ('mentor_result','mentor_retry'):
                if event.key in (pygame.K_RETURN,pygame.K_SPACE):
                    if state=='mentor_result': state='dialogue'; chat_page='menu'
                    else: state='mentor_check'
            elif state=='journal':
                if event.key in (pygame.K_BACKSPACE,pygame.K_j): state='world'
                elif event.key in (pygame.K_RIGHT,pygame.K_DOWN): journal_page=min(max(0,(len(journal)-1)//6),journal_page+1)
                elif event.key in (pygame.K_LEFT,pygame.K_UP): journal_page=max(0,journal_page-1)
            elif state=='quiz':
                if event.key==pygame.K_UP: selected=(selected-1)%3
                elif event.key==pygame.K_DOWN: selected=(selected+1)%3
                elif event.key in (pygame.K_1,pygame.K_2,pygame.K_3): selected=event.key-pygame.K_1; submit_answer()
                elif event.key in (pygame.K_RETURN,pygame.K_SPACE): submit_answer()
            elif state=='lesson':
                if event.key in (pygame.K_RETURN,pygame.K_SPACE,pygame.K_BACKSPACE): state='quiz'
            elif state=='report':
                if event.key in (pygame.K_BACKSPACE,pygame.K_r): state=report_return
                elif event.key==pygame.K_c: copy_report()
            elif state in ('gameover','victory'):
                if event.key==pygame.K_r: report_return=state; state='report'
                elif event.key==pygame.K_RETURN: new_game(); music_control()
        if state=='title': frame+=1; draw_title()
        elif state=='world':
            update()
            if room==4 and ready_exit():
                stats['victories']+=1; state='victory'
            background()
            if not secret_room and boss and distance(boss['x'],boss['y'])<110:
                draw_text('Z: STRIKE NOW!' if boss_open else 'E: HACK SHIELD',215,309,GOLD,S)
        elif state=='puzzle': puzzle_update(); puzzle_screen() if state=='puzzle' else celebration_screen()
        elif state=='gauntlet': gauntlet_update(); gauntlet_screen() if state=='gauntlet' else celebration_screen()
        elif state=='celebrate':
            frame+=1
            if victory_countdown>0:victory_countdown-=1
            celebration_screen()
        elif state=='dialogue': dialogue_screen()
        elif state=='mentor_check': mentor_check_screen()
        elif state in ('mentor_result','mentor_retry'): mentor_result_screen()
        elif state=='journal': journal_screen()
        elif state=='quiz': question_screen()
        elif state=='lesson': lesson_screen()
        elif state=='report': report_screen()
        else: draw_end(state=='victory')
        if music_enabled: music_control()
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()

async def main():
    # Visible startup diagnostic: errors are displayed even when the console is quiet.
    try:
        screen.fill((12,15,31))
        screen.blit(L.render('QUESTFORGE BROWSER STARTING...', True, CYAN), (35,140))
        pygame.display.flip()
        await asyncio.sleep(0.2)
        await game_loop()
    except Exception:
        import traceback
        error=traceback.format_exc()
        print('QUESTFORGE STARTUP ERROR\n'+error,flush=True)
        lines=error.strip().splitlines()
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: return
            screen.fill((22,12,28))
            screen.blit(F.render('QUESTFORGE: BROWSER ERROR',True,(255,210,100)),(16,10))
            screen.blit(S.render('Send a photo of this screen.',True,(255,255,255)),(16,36))
            for i,line in enumerate(lines[-16:]):
                screen.blit(S.render(line[:100],True,(255,160,160)),(12,64+i*19))
            pygame.display.flip()
            await asyncio.sleep(0.05)

asyncio.run(main())
