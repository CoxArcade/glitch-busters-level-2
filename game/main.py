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
# Week 2-only debugging bank: 21 unique stations, 15 unique guardian hacks.
Q = [('UP IS DOWN', 'UP key sends the hero downward.', ['if keyboard.up:', '    y = y + speed'], ['Use y = y - speed', 'Use x = x + speed', 'Use y = y + speed'], 0, 'Screen y decreases when you move up.', 'if keyboard.up:', '    y = y - speed'), ('FROZEN Y', 'Hero moves vertically, but drawing stays fixed.', ['y = y - 3', 'draw_hero(x, 200)'], ['Use draw_hero(200, y)', 'Use draw_hero(x, y)', 'Change speed to 0'], 1, 'Both coordinates must use the live variables.', 'y = y - 3', 'draw_hero(x, y)'), ('WRONG AXIS', 'RIGHT key moves the hero down.', ['if keyboard.right:', '    y = y + speed'], ['Use y = y - speed', 'Use x = x - speed', 'Use x = x + speed'], 2, 'Right changes x, not y.', 'if keyboard.right:', '    x = x + speed'), ('TELEPORT PAD', 'Pad should appear at (120, 80).', ['pad_x = 120', 'pad_y = 80'], ['draw_pad(pad_x, pad_y)', 'draw_pad(pad_y, pad_x)', 'draw_pad(80, 120)'], 0, 'Draw using x first, then y.', 'pad_x = 120', 'draw_pad(pad_x, pad_y)'), ('LEFT WALL LEAK', 'Hero slips past the left edge.', ['if x < 0:', '    x = -10'], ['Set y = 0', 'Set x = 0', 'Set x = -20'], 1, 'Clamp x to the minimum allowed position.', 'if x < 0:', '    x = 0'), ('RIGHT WALL LEAK', 'Hero crosses a 600-pixel right boundary.', ['if x > 600:', '    x = 650'], ['Set x = 650', 'Set y = 600', 'Set x = 600'], 2, 'Keep x at the rightmost permitted value.', 'if x > 600:', '    x = 600'), ('TOP EDGE', 'Hero escapes through the top of the screen.', ['if y < 0:', '    y = -5'], ['Set y = 0', 'Set x = 0', 'Set y = 400'], 0, 'Top of screen is y = 0.', 'if y < 0:', '    y = 0'), ('COIN AT A DISTANCE', 'A coin is collected when only one coordinate is close. Fix the condition.', ['if abs(x - coin_x) < 20 or', '   abs(y - coin_y) < 20:'], ['Use or', 'Use and', 'Remove both checks'], 1, 'Both x and y must be close to the coin.', 'if abs(x - coin_x) < 20 and', '   abs(y - coin_y) < 20:'), ('COIN NOT MOVING', 'After a coin is collected, it should appear at a different, preset location.', ['coin_x = 150', 'coin_y = 100'], ['Delete coin_y', 'Set score = 0', 'Change the next coin position'], 2, 'Move the coin to a new known position after pickup.', 'coin_x = 300', 'coin_y = 220'), ('PICKUP RADIUS', 'The player and coin are 15 pixels apart on x. The pickup range should be 20 pixels.', ['abs(x - coin_x) < 10', 'x = 85; coin_x = 100'], ['Use a distance limit of 20', 'Use a distance limit of 5', 'Set x = 0'], 0, 'Fifteen is inside 20, but not inside 10.', 'abs(x - coin_x) < 20', 'score = score + 1'), ('VECTOR SWITCH', 'DOWN key moves the platform upward.', ['if keyboard.down:', '    y = y - speed'], ['Decrease x', 'Increase y', 'Increase x'], 1, 'Moving down increases y.', 'if keyboard.down:', '    y = y + speed'), ('TWO-AXIS SENSOR', 'Door checks x but ignores y.', ['if abs(x - door_x) < 15:', '    open_door()'], ['Use x only', 'Use y only', 'Check both x and y'], 2, 'A two-dimensional target needs both coordinates.', 'if abs(x-door_x)<15 and', '   abs(y-door_y)<15:'), ('SPEED BOOST', 'Player should move 4 pixels per key press.', ['speed = 2', 'x = x + speed'], ['Set speed = 4', 'Set x = 4', 'Set speed = 0'], 0, 'speed determines the amount of movement.', 'speed = 4', 'x = x + speed'), ('SCORE RESET BUG', 'Collecting a coin resets the score.', ['score = 6', '# coin collected: score = 0'], ['score = score - 1', 'score = score + 1', 'score = 0'], 1, 'Increase the current score by one.', 'score = 6', 'score = score + 1'), ('DOUBLE REWARD', 'A single coin should award one point.', ['score = 4', 'score = score + 2'], ['score = 0', 'score = score - 2', 'score = score + 1'], 2, 'One coin means one extra point.', 'score = 4', 'score = score + 1'), ('FINAL SCORE', 'Player has 7 coins, collects one more.', ['score = 7', '# another coin is collected'], ['score = score + 1', 'score = score - 1', 'score = 7'], 0, 'Seven plus one is eight.', 'score = 7', 'score = score + 1'), ('GUARDIAN: UP', 'UP key must reduce y.', ['if keyboard.up:', '    y = y + 2'], ['y = y - 2', 'x = x - 2', 'y = y + 2'], 0, 'Up means a smaller y.', 'if keyboard.up:', '    y = y - 2'), ('GUARDIAN: DOWN', 'DOWN key must increase y.', ['if keyboard.down:', '    y = y - 2'], ['x = x + 2', 'y = y + 2', 'y = y - 2'], 1, 'Down means a larger y.', 'if keyboard.down:', '    y = y + 2'), ('GUARDIAN: LEFT', 'LEFT key should change which coordinate?', ['if keyboard.left:', '    y = y - 2'], ['y', 'score', 'x'], 2, 'Left and right change x.', 'if keyboard.left:', '    x = x - 2'), ('GUARDIAN: CLAMP X', 'At x = -3, what is a safe x?', ['x = -3', 'if x < 0:'], ['x = 0', 'x = -6', 'x = 900'], 0, 'Clamp negative x to zero.', 'if x < 0:', '    x = 0'), ('GUARDIAN: CLAMP Y', 'At y = -7, what is a safe y?', ['y = -7', 'if y < 0:'], ['y = -7', 'y = 0', 'x = 0'], 1, 'Clamp negative y to zero.', 'if y < 0:', '    y = 0'), ('GUARDIAN: RIGHT EDGE', 'Right boundary is 600.', ['x = 630', 'if x > 600:'], ['x = 630', 'x = 700', 'x = 600'], 2, 'Set x to the maximum of 600.', 'if x > 600:', '    x = 600'), ('GUARDIAN: COIN X', 'Hero x=80, coin x=90; limit=15.', ['abs(80 - 90) < 15', ''], ['X is close enough', 'X is too far', 'Coin moves itself'], 0, 'Difference is 10, inside 15.', 'abs(80 - 90) < 15', 'score = score + 1'), ('GUARDIAN: COIN Y', 'Hero y=20, coin y=70; limit=15.', ['abs(20 - 70) < 15', ''], ['Y is close enough', 'Y is too far', 'Score doubles'], 1, 'Difference is 50, outside 15.', 'abs(20 - 70) < 15', ''), ('GUARDIAN: BOTH AXES', 'What joins two required proximity checks?', ['close_x = True', 'close_y = True'], ['or', '=', 'and'], 2, 'Both conditions must be true.', 'if close_x and close_y:', '    score = score + 1'), ('GUARDIAN: SPEED', 'At speed 3, what does y = y - speed do?', ['y = 60', 'speed = 3'], ['Moves up to y=57', 'Moves down to y=63', 'Stays at y=60'], 0, 'Subtracting three from y moves up.', 'speed = 3', 'y = 57'), ('GUARDIAN: DRAW', 'What makes the platform follow both axes?', ['x = 30; y = 40', 'draw_platform(30, 40)'], ['draw_platform(30,40)', 'draw_platform(x,y)', 'draw_platform(y,y)'], 1, 'Use both live coordinates.', 'x = 30; y = 40', 'draw_platform(x,y)'), ('GUARDIAN: SPEED FIX', 'Moving too fast? speed is 9.', ['speed = 9', 'x = x + speed'], ['Set speed = 20', 'Set x = 9', 'Set speed = 3'], 2, 'Lower speed makes smaller steps.', 'speed = 3', 'x = x + speed'), ('GUARDIAN: SCORE', 'Score starts at 3 and gains 1.', ['score = 3', 'score = score + 1'], ['Score becomes 4', 'Score becomes 2', 'Score becomes 0'], 0, 'Three plus one is four.', 'score = 3', 'score = 4'), ('GUARDIAN: NO PICKUP', 'A coin is collected only if BOTH distance checks pass. What must be true?', ['abs(x-coin_x)<10', 'abs(y-coin_y)<10'], ['Only x must be close', 'Both must be close', 'Only y must be close'], 1, 'Both coordinate distances must be close.', 'if abs(x-coin_x)<10 and', '   abs(y-coin_y)<10:'), ('GUARDIAN: COIN RESET', 'After pickup, move coin to (300,180).', ['coin_x = 50', 'coin_y = 50'], ['coin_x = 50; coin_y = 50', 'coin_x = 180; coin_y = 300', 'coin_x = 300; coin_y = 180'], 2, 'x is horizontal, y is vertical.', 'coin_x = 300', 'coin_y = 180'), ('Y AXIS MIXUP', 'What does y = y + 5 do?', ['y = 100', 'y = y + 5'], ['Moves right', 'Moves down', 'Moves up'], 1, 'Increasing y moves downward.', 'y = 100', 'y = 105'), ('BOTTOM EDGE', 'Bottom boundary is y=320.', ['y = 345', 'if y > 320:'], ['y = 320', 'y = 345', 'x = 320'], 0, 'Clamp y to 320.', 'if y > 320:', '    y = 320'), ('COIN CHECK', 'Hero and coin must be near on both axes.', ['close_x = True', 'close_y = False'], ['Use or', 'Use +', 'Use and'], 2, 'Both checks must be true to collect.', 'if close_x and close_y:', '    score = score + 1'), ('DIAGONAL MOVE', 'UP and RIGHT are held together.', ['x = 50; y = 50', 'speed = 2'], ['x=48, y=52', 'x=52, y=48', 'x=52, y=52'], 1, 'Right increases x; up decreases y.', 'x = 52', 'y = 48'), ('SCORE DISPLAY', 'After collecting a coin, what updates?', ['score = 9', 'score = score + 1'], ['score becomes 10', 'score becomes 8', 'score stays 9'], 0, 'Add one to the existing score.', 'score = 9', 'score = 10')]
BOSS_Q={r:[16+r*3+i for i in range(3)] for r in range(5)}
STATIONS={
 0:[(110,142,0),(494,144,1),(490,285,2),(105,218,3),(300,205,31)],
 1:[(168,135,4),(463,258,5),(507,194,6),(280,265,32)],
 2:[(156,133,7),(480,267,8),(147,285,9),(310,194,33)],
 3:[(167,145,10),(464,260,11),(505,197,12),(290,270,34)],
 4:[(176,145,13),(460,264,14),(105,220,15),(295,195,35)]
}
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
               ('How do I move in four directions?', 'Use left and right to change x, and up and down to change y. Keep both within the screen.', 'TIP: LEFT/RIGHT CHANGE X; UP/DOWN CHANGE Y.'),
               ('Any advice about the arcade?', 'The COORDINATE PANEL is near the southeast wall, away from GUIDE. Follow the numbered coordinate beacons to power the exit. Look north for a secret seam.', 'CLUE: The southeast coordinate panel restores power; search the north wall for a secret.')],
     'gift':('potion',1)},
  'SPROCKET': {'room':1,'pos':(465,133),'color':(240,120,82),
     'intro':'A mechanic who fixes arcade machines.',
     'topics':[('How do boundaries work?', 'If x becomes less than zero, set x back to zero. Do the same for y at the top edge.', 'TIP: CLAMP X TO THE LEFT AND RIGHT EDGES.'),
               ('Why does the player leave the screen?', 'Check the boundary conditions. Keep x and y between the screen edges.', 'TIP: CLAMP Y TO THE TOP AND BOTTOM EDGES.'),
               ('Where are the spare parts?', 'One panel in the north wall sounds hollow. Try examining the masonry closely.', 'CLUE: A north wall panel hides supplies.')],
     'gift':('potion',1)},
  'ARCHIVIST': {'room':3,'pos':(463,132),'color':(179,119,232),
     'intro':'A quiet keeper of forgotten arcade secrets.',
     'topics':[('Tell me about the artifacts.', 'Three lost artifacts are concealed in secret chambers. Finding all three unlocks the vault armor.', 'LORE: Three artifacts unlock legendary armor.'),
               ('Where should I search?', 'Look north in the arcade and maze. In the factory, investigate the southern wall. The factory navigation panel uses numbered waypoints.', 'CLUE: North in arcade/maze; south in factory. Follow numbered waypoints.'),
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
PUZZLE_NAMES=['COORDINATE TELEPORT','BOUNDARY REPAIR','COIN COLLECTOR LAB','FOUR-WAY NAVIGATION','SCORE RECONSTRUCTION']
PUZZLE_POS=[(397,284),(528,287),(535,205),(530,286),(530,286)]
puzzle_done=set(); puzzle_attempts=[0]*5; puzzle_hints=[0]*5
puzzle_step=0; puzzle_switches=[False]*3
# Each room has its own player-operated simulation rather than a reused Level 1 puzzle.
grid_cursor=[0,0]; grid_targets=[(2,1),(4,3),(1,2)]
boundary_cursor=[2,2]; boundary_route=[(4,2),(4,0),(0,0),(0,3)]
coin_cursor=[0,0]; coin_positions=[(2,1),(4,3),(1,3),(3,0)]
vector_cursor=[0,0]; vector_route=[(3,0),(3,2),(1,2),(1,4),(4,4)]
score_cursor=[0,0]; score_positions=[(1,1),(4,1),(2,3),(0,4),(4,4)]
puzzle_feedback=''; puzzle_feedback_timer=0
PUZZLE_HINTS=[
 'TELEPORT: Read each target as (x, y). RIGHT adds to x; DOWN adds to y. Visit each gold beacon.',
 'BOUNDARIES: Stay inside the 5 by 4 grid. Reach the blue checkpoints in order without leaving the screen.',
 'COINS: Move onto each gold coin in order. Both your x AND y must match its position to collect it.',
 'NAVIGATION: Follow the numbered waypoints. Use all four arrow keys; avoid overshooting a turn.',
 'SCORE: Collect all five coins. Each pickup increases score by one; the last coin unlocks the exit.'
]

# Mandatory guided learning: three topics and a comprehension check per main-stage mentor.
MAIN_MENTORS=['PROFESSOR PIXEL','SPROCKET','RANGER ARROW','ARCHIVIST','KEEPER']
# The Keeper is a main-stage mentor; Echo remains a bonus secret contact.
MENTORS['KEEPER']={'room':4,'pos':(460,125),'color':(236,198,96),
 'intro':'Guardian of the final arcade restoration.',
 'topics':[('How do functions begin?', 'Write def draw(): with a colon. Put instructions on the next indented line.', 'TIP: def draw(): starts a function.'),
           ('What changes the game?', 'update() changes x or other variables; draw() displays objects using those values.', 'TIP: update changes values; draw displays.'),
           ('How can if help with score?', 'An if statement can check whether the player is near a coin, then add one to score.', 'TIP: SCORE INCREASES WHEN BOTH COORDINATES ARE CLOSE.')],
 'gift':('potion',1)}
LESSON_CHECKS={'PROFESSOR PIXEL': [('Which coordinate must change when the hero moves UP?', ['x', 'y', 'score'], 1, 'Up and down change y.'), ('If y is 40 and UP subtracts 3, what is y?', ['37', '43', '40'], 0, '40 minus 3 is 37.'), ('Which drawing call uses both changing coordinates?', ['draw_hero(x, y)', 'draw_hero(x, 90)', 'draw_hero(30, 90)'], 0, 'Both x and y must update.')], 'SPROCKET': [('What keeps x from becoming negative?', ['if x < 0: x = 0', 'if x > 0: x = -5', 'y = 0'], 0, 'Clamp x at the left edge.'), ('What should happen if y > 320?', ['y = 400', 'y = 320', 'x = 320'], 1, 'Keep y at its maximum.'), ('At x=600, pressing RIGHT should do what?', ['Go past 600', 'Change y', 'Stay within the boundary'], 2, 'The right boundary stops movement.')], 'RANGER ARROW': [('Which check requires BOTH x and y to be close?', ['close_x or close_y', 'close_x and close_y', 'score = 0'], 1, 'Both conditions must be true.'), ('What happens to score when one coin is collected?', ['score = score + 1', 'score = 0', 'score = score - 1'], 0, 'Add one to score.'), ('Where is (200, 100) compared to (100, 200)?', ['Left and down', 'Same location', 'Right and up'], 2, 'x increases right; y decreases up.')], 'ARCHIVIST': [('Which direction decreases y?', ['DOWN', 'UP', 'RIGHT'], 1, 'Up decreases y.'), ('The player can move left and right, but not up and down. What needs to be added?', ['Y movement controls', 'A new background', 'A new name'], 0, 'Add up and down y movement.'), ('Why does draw_hero(x, 100) ignore up/down?', ['x is wrong', 'speed is wrong', '100 is a fixed y'], 2, 'Use the changing y variable.')], 'KEEPER': [('Score is 5; collect a coin. New score?', ['4', '6', '5'], 1, 'One coin adds one point.'), ('Why is OR wrong for coin collision?', ['Only one axis may be close', 'It is too slow', 'It makes x negative'], 0, 'Both x and y must be close.'), ('After a pickup, which variables position the next coin?', ['speed and score', 'player_x only', 'coin_x and coin_y'], 2, 'A coin has an x and a y position.')]}
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
secret_lock_solved=set(); secret_lock_selected=0
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
            'phase':random.random()*7,'turn':random.uniform(-3,3),'timer':random.randrange(55,145),'speed':.82+room*.14,'vx':random.choice([-1,1]),'shot':random.randrange(70,140),'charge':0,'tell':0,'base_x':float(x),'base_y':float(y),'max_hp':3 if kind=='charger' else 2 if room>1 else 2,'flash':0,'hurt':0}

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
    global secret_lock_solved,secret_lock_selected
    global rooms_done,solved,chests,artifacts,opened,boss_hacks,boss_quiz,secret_found,npc_gifts,boss_hacks_room,dash_cd,dash_time,speed_upgrade,sword_upgrade,secret_room,secret_origin,secret_index,chamber_cleared,secret_bugs,secret_chest_open,mentor_met,mentor_gifts,journal,journal_page,puzzle_done,puzzle_attempts,puzzle_hints,mentor_topics_done,mentor_checks_done,mentor_check_attempts,player_name,player_experience
    stats['runs']+=1; hp=5; max_hp=5; lives=3; weapon='PUNCH'; has_bow=False
    bombs=0; arrows=12; potions=0; invuln=0; boss_hacks=0; boss_quiz=False
    secret_lock_solved=set();secret_lock_selected=0
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
    draw_text('ART '+str(len(artifacts))+'/3' + ('' if chamber else '   FIX '+str(len(solved))+'/21'),495,10,GOLD,S)
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
        notice='EXIT LOCKED: SOLVE THE '+('COORDINATES' if room==0 else 'PUZZLE')+' TO ADVANCE'
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
        draw_text('COORDINATE PANEL' if room==0 else 'PUZZLE PANEL',px-47,py+27,GOLD,S)
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
        secret_bugs=[bug(210,165,'patrol'),bug(430,210,'wander'),bug(320,250,'shooter'),bug(330,133,'patrol')]
        player.topleft=(304,283)
        tell('A HIDDEN WALL OPENS! SEARCH THE CHAMBER, THEN USE THE EXIT.',230)
        return True
    return False

# Secret chest security questions. One distinct coordinate challenge per hidden chamber.
SECRET_LOCKS=[
 ('You are at (3, 2). Move UP once. New position?', ['(3, 1)','(4, 2)','(3, 3)'],0),
 ('Which coordinate changes when you move RIGHT?', ['y','x','score'],1),
 ('From (4, 1), move LEFT twice. New position?', ['(4, 3)','(3, 1)','(2, 1)'],2),
 ('Your x is -1. The left boundary is 0. Fix x.', ['x = 0','x = -2','y = 0'],0),
 ('From (2, 2), which move reaches the coin at (2, 3)?', ['UP','DOWN','LEFT'],1),
 ('Coin and player share x, but y is far apart. Collect?', ['Yes','Always','No'],2),
 ('From (3, 4), which move reaches (4, 4)?', ['RIGHT','UP','DOWN'],0),
 ('Score is 3. Collect two coins. New score?', ['4','5','6'],1),
 ('At y = 0, which move would cross the top edge?', ['DOWN','RIGHT','UP'],2),
 ('Which coordinates place a coin at x=2 and y=4?', ['(2, 4)','(4, 2)','(2, 2)'],0)]
def secret_lock_screen():
    screen.fill(BG);box(38,70,564,268,(25,38,60),10)
    n=secret_origin*2+secret_index
    question,choices,answer=SECRET_LOCKS[n]
    center('SECRET VAULT: COORDINATE LOCK',54,GOLD,L)
    center('Solve this lock to open the hidden treasure.',105,CYAN,F)
    center(question,148,WHITE,F)
    for j,choice in enumerate(choices):
        box(110,181+j*42,420,34,(52,96,122) if j==secret_lock_selected else (38,49,73),5)
        draw_text(str(j+1)+'. '+choice,128,189+j*42,WHITE,F)
    center('1-3: CHOOSE   UP/DOWN: SELECT   ENTER: CONFIRM   BACKSPACE: RETURN',366,GOLD,S)
def secret_lock_key(key):
    global secret_lock_selected,state
    if key==pygame.K_BACKSPACE:state='world';return
    if key in (pygame.K_1,pygame.K_2,pygame.K_3):
        secret_lock_selected=key-pygame.K_1
    elif key==pygame.K_UP:
        secret_lock_selected=(secret_lock_selected-1)%3;return
    elif key==pygame.K_DOWN:
        secret_lock_selected=(secret_lock_selected+1)%3;return
    elif key!=pygame.K_RETURN:return
    if secret_lock_selected==SECRET_LOCKS[secret_origin*2+secret_index][2]:
        secret_lock_solved.add((secret_origin,secret_index));state='world'
        tell('SECURITY LOCK DISABLED! OPEN THE CHEST TO CLAIM YOUR REWARD.',170)
    else:tell('INCORRECT COORDINATES. TRY AGAIN.',150)

def interact():
    global active,selected,state,weapon,has_bow,arrows,bombs,potions,max_hp,hp,secret_room,secret_chest_open,room,speed_upgrade,sword_upgrade
    if secret_room:
        if secret_origin==2 and secret_index==0 and distance(450,253)<49:
            talk_to('ECHO'); return
        if distance(320,222)<52 and not secret_chest_open:
            if secret_bugs:
                tell('CHEST SEALED! CLEAR THE HIDDEN CHAMBER FIRST.',140); return
            if (secret_origin,secret_index) not in secret_lock_solved:
                global secret_lock_selected
                secret_lock_selected=0;state='secret_lock';return
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

def begin_puzzle():
    global state,grid_cursor,boundary_cursor,coin_cursor,vector_cursor,score_cursor,puzzle_step
    state='puzzle';puzzle_step=0
    grid_cursor=[0,0];boundary_cursor=[2,2];coin_cursor=[0,0];vector_cursor=[0,0];score_cursor=[0,0]
    puzzle_note('Use the arrow keys to move on the coordinate grid. H gives a hint; BACKSPACE returns.')

def finish_puzzle():
    global state,victory_kind,victory_countdown
    puzzle_done.add(room);stats['puzzles']+=1;play_sfx('victory')
    journal_add('PUZZLE SOLVED: '+PUZZLE_NAMES[room])
    grant_crystal('PUZZLE COMPLETE')
    victory_kind='puzzle';victory_countdown=90;state='celebrate'

def puzzle_key(key):
    global puzzle_step
    if key==pygame.K_BACKSPACE:return 'exit'
    if key==pygame.K_h:
        puzzle_hints[room]+=1;journal_add(PUZZLE_HINTS[room]);puzzle_note(PUZZLE_HINTS[room]);return
    if key==pygame.K_r:
        begin_puzzle();return
    moves={pygame.K_LEFT:(-1,0),pygame.K_RIGHT:(1,0),pygame.K_UP:(0,-1),pygame.K_DOWN:(0,1),
           pygame.K_a:(-1,0),pygame.K_d:(1,0),pygame.K_w:(0,-1),pygame.K_s:(0,1)}
    if key not in moves:return
    dx,dy=moves[key]
    cursors=[grid_cursor,boundary_cursor,coin_cursor,vector_cursor,score_cursor]
    routes=[grid_targets,boundary_route,coin_positions,vector_route,score_positions]
    widths=[5,5,5,5,5];heights=[4,4,4,5,5]
    cur=cursors[room];nx=cur[0]+dx;ny=cur[1]+dy
    puzzle_attempts[room]+=1
    if not (0<=nx<widths[room] and 0<=ny<heights[room]):
        puzzle_note('BOUNDARY ALERT: That move leaves the grid. Try a different direction.')
        return
    cur[:]=[nx,ny]
    target=routes[room][puzzle_step]
    if (nx,ny)==target:
        puzzle_step+=1
        if puzzle_step==len(routes[room]):
            finish_puzzle()
        else:
            if room in (2,4):play_sfx('pickup')
            puzzle_note(('COIN COLLECTED! ' if room in (2,4) else 'CHECKPOINT REACHED! ')+
                        str(puzzle_step)+'/'+str(len(routes[room]))+'. NEXT TARGET: '+str(routes[room][puzzle_step]))
    elif room==1:
        puzzle_note('POSITION: ('+str(nx)+', '+str(ny)+'). Stay inside the grid.')

def puzzle_update():
    global puzzle_feedback_timer
    stats['seconds']+=1/60
    if puzzle_feedback_timer:puzzle_feedback_timer-=1

def puzzle_screen():
    screen.fill(BG);box(24,60,592,273,(26,35,58),8)
    center('PUZZLE '+str(room+1)+': '+PUZZLE_NAMES[room],22,CYAN,L)
    routes=[grid_targets,boundary_route,coin_positions,vector_route,score_positions]
    cursors=[grid_cursor,boundary_cursor,coin_cursor,vector_cursor,score_cursor]
    route=routes[room];cur=cursors[room]
    descriptions=[
      'TELEPORT: MOVE TO EACH COORDINATE IN ORDER.',
      'BOUNDARY REPAIR: VISIT THE CHECKPOINTS WITHOUT LEAVING THE GRID.',
      'COIN COLLECTOR: STAND ON EACH COIN TO PICK IT UP.',
      'NAVIGATION: TRACE THE WAYPOINTS IN THE CORRECT ORDER.',
      'SCORE VAULT: COLLECT FIVE COINS TO RESTORE THE SCORE.'
    ]
    center(descriptions[room],73,WHITE,F)
    nrows=4 if room<3 else 5
    tile=43;ox=210;oy=113
    for y in range(nrows):
        for x in range(5):
            xx=ox+x*tile;yy=oy+y*tile
            box(xx,yy,tile-3,tile-3,(42,58,83) if (x+y)%2 else (48,67,92),4)
            draw_text(str(x)+','+str(y),xx+5,yy+5,GRAY,S)
    for i,(x,y) in enumerate(route):
        if i<puzzle_step:continue
        xx=ox+x*tile+tile//2;yy=oy+y*tile+tile//2
        pygame.draw.circle(screen,GOLD if i==puzzle_step else (98,113,140),(xx,yy),11)
        center_label=str(i+1)
        draw_text(center_label,xx-4,yy-8,BG,S)
    pygame.draw.circle(screen,CYAN,(ox+cur[0]*tile+tile//2,oy+cur[1]*tile+tile//2),8)
    draw_text('YOU: ('+str(cur[0])+', '+str(cur[1])+')',32,124,WHITE,F)
    draw_text('NEXT: '+str(route[puzzle_step]),32,154,GOLD,F)
    draw_text('DONE: '+str(puzzle_step)+'/'+str(len(route)),32,184,GREEN,F)
    if room==4:draw_text('SCORE: '+str(puzzle_step),32,215,GOLD,F)
    center('ARROWS / WASD: MOVE     R: RESET',338,GOLD,S)
    draw_text('H: HINT     BACKSPACE: RETURN',37,378,GOLD,S)
    if puzzle_feedback_timer>0:
        # Wrap long hints so they stay within the panel.
        msg=puzzle_feedback
        for i,line in enumerate([msg[j:j+75] for j in range(0,min(len(msg),225),75)]):
            draw_text(line,35,300+i*12,WHITE,S)

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
        center('TELEPORTER RESTORED!' if n==0 else 'PUZZLE COMPLETE!',45,GREEN,L)
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
    global report_return, selected, victory_countdown, secret_lock_selected
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
                elif state=='secret_lock' and 181<=my<307:
                    secret_lock_selected=max(0,min(2,(my-181)//42));secret_lock_key(pygame.K_RETURN)
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
            elif state=='secret_lock':
                secret_lock_key(event.key)
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
        elif state=='secret_lock': secret_lock_screen()
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
