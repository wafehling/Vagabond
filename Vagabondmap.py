"""This is the first major programming project I have undertaken. I started this project in late August 2011. 
Largely based off of a tutorial on Roguebasin by Jotaf."""


import libtcodpy as lbc, libtcodpy as libtcod
import math
from namegen import NameGen
import joblists
import textwrap
# # # # # # # # # # 
#Screen Orienting #
# # # # # # # # # #

#Window Sizes
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#Map sizes(smaller to accompany stat viewing, etc)
MAP_WIDTH = 250
MAP_HEIGHT = 200

BAR_WIDTH = 12
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MAX_ROOM_MONSTERS = 3
#colors for the current tiles
color_tree = lbc.Color(106, 52, 0)
color_dirt = lbc.Color(44, 124, 4)
color_light_wall_1 = lbc.Color(78, 78, 78)
color_light_wall_2 = lbc.Color(127, 123, 100)
color_light_wall_3 = lbc.Color(41, 41, 41)
color_light_wall_4 = lbc.Color(194, 194, 194)
color_light_wall_5 = lbc.Color(213, 195, 141)
color_light_wall_6 = lbc.Color(115, 37, 37)
color_sidewalk = lbc.Color(206, 206, 206)
color_floor = lbc.Color(104,104,104)
#Limits the screen refresh rate
LIMIT_FPS = 20

#Numbers to be used to renerate dungeon rooms
ROOM_MAX_SIZE = 4
ROOM_MIN_SIZE = 6
MAX_ROOMS = 125

FOV_LIGHT_WALLS = True
fov_recompute = True
torch_radius = SCREEN_WIDTH/1.5

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = color_light_wall_1
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = lbc.Color(137, 137, 137)

game_state = 'playing'
player_action = None

time_minute = float(0)
time_hour = 12 
am = False

#These lists handle announcements
ann_combatdeath = []
ann_combatd0 = []
ann_combatd1 = []
ann_dialog = []
ann_passive_actions = []
objects = []
total = []
newtotal = []

#Setup stuff for large map generation
map_bsp = lbc.bsp_new_with_size(0,0,MAP_WIDTH,MAP_HEIGHT)
min_h_size = int(MAP_HEIGHT/3.5)
min_v_size = int(MAP_WIDTH/3.5)
lbc.bsp_split_recursive(map_bsp, 0, 2, min_h_size, min_v_size, 0, 0)

can_attack = 1


display_width = 72
display_height = 40

startx = 0
starty = 0


def camera_move():
	global display_width, display_height, startx, starty
	print starty + display_height/1.5
	print "Less Than"
	print player.y
	print " "
	print starty
	print "Less Than"
	print MAP_HEIGHT - display_height - 1
	print "starty = " + str(starty)
	print "_____________________________"
	if(startx + display_width/3 > player.x):
		if startx > 0:
			startx = startx - 1
	if(starty + display_height/3 > player.y):
		if starty > 0:
			starty = starty - 1
	if startx + display_width/1.75 < player.x:
		if startx < MAP_WIDTH - display_width - 1:
			startx = startx + 1

	if starty + display_height/1.75 < player.y:
		if starty < MAP_HEIGHT - display_height - 1:
			starty = starty + 1


#####################################
#Map generation and object placement#
#####################################

class Tile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		#Tile blocks sight if it's blocked by default (will change later)
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

floor_tile = Tile(blocked = False, block_sight = None)

def create_room(room):
	global map
	#make walls of buildings
	for y in range(room.y1, room.y2):
		map[room.x1][y].blocked = True
		map[room.x1][y].block_sight = True
		map[room.x2-1][y].blocked = True
		map[room.x2-1][y].block_sight = True
	#Plase random "doors"
	doorsx = 2
	while doorsx > 0:
		doorposx = lbc.random_get_int(0, room.y1 + 1, room.y2 - 1)
		xside = lbc.random_get_int(0, 1, 2)
		if xside == 1:
			map[room.x1][doorposx].blocked = False
			map[room.x1][doorposx].block_sight = False
			doorsx = doorsx - 1
		elif xside == 2:
			map[room.x2-1][doorposx].blocked = False
			map[room.x2-1][doorposx].block_sight = False
			doorsx = doorsx - 1
	doorsy = 2
	while doorsy > 0:
		doorposy = lbc.random_get_int(0, room.x1 + 1, room.x2 - 1)
		yside = lbc.random_get_int(0, 1, 2)
		if yside == 1:
			map[doorposy][room.y1].blocked = False
			map[doorposy][room.y1].block_sight = False
			doorsy = doorsy - 1
		elif yside == 2:
			map[doorposy-1][room.y2].blocked = False
			map[doorposy-1][room.y2].block_sight = False
			doorsy = doorsy - 1
	for x in range(room.x1, room.x2):
		map[x][room.y1].blocked = True
		map[x][room.y1].block_sight = True
		map[x][room.y2].blocked = True
		map[x][room.y2].block_sight = True

#Makes rectangles. Even I get how this one works.		
class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
 
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
			
def place_objects(room):
	#choose random number of monsters
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
	jobs = [joblists.beggar, joblists.thief, joblists.day_laborer, joblists.business_worker, joblists.construction_worker, joblists.punk, joblists.gang_member, joblists.transient, joblists.bank_teller, joblists.retail_worker, joblists.shop_owner, joblists.janitor]
	for i in range(num_monsters):
		#choose random spot for this monster
			x = libtcod.random_get_int(0, room.x1, room.x2)
			y = libtcod.random_get_int(0, room.y1, room.y2)
	
			job = libtcod.random_get_int(0, 0, len(jobs)-1)
			active_job = jobs[job]
			job_name = active_job[0]
			job_color = active_job[1]
			if not is_blocked(x, y):
				#create a person
				ai_person = BasicMonster()
				person_power = lbc.random_get_int(0, 1, 4)
				person_defense = lbc.random_get_int(0, 1, 4)
				person_spee = lbc.random_get_int(0, 75, 105)
				person_speed = float(person_spee)/100
				fighter_person = Fighter(body = "body_def", hp = 10, defense = person_defense, power = person_power, speed = person_speed, death_function=monster_death)
				monster = Object(x, y, 'H', job_name, job_color, blocks=True, fighter=fighter_person, ai=ai_person)
				objects.append(monster)
				
#Makes horizontal tunnels.
def create_h_tunnel(x1, x2, y):
	xswitch1 = 0
	xswitch2 = 0
	if x1 > x2:
		xswitch1 = x1
		xswitch2 = x2
		x1 = xswitch2
		x2 = xswitch1
	global map
	for x in range(x1, x2):
		map[x][y].blocked = False
		map[x][y].block_sight = False
#makes vertical tunnels.
def create_v_tunnel(y1, y2, x):
	yswitch1 = 0
	yswitch2 = 0
	if y1 > y2:
		yswitch1 = y1
		yswitch2 = y2
		y1 = yswitch2
		y2 = yswitch1
	global map
	for y in range(y1, y2):
		map[x][y].blocked = False
		map[x][y].block_sight = False
def is_blocked(x, y):
	if map[x][y].blocked:
		return True
	
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True
			
	return False
		
#Generates the map. Rather complex and cryptic, no idea how it works fully.
def make_map():
	global map, player
	
    #fill map with "unblocked" tiles
	map = [[ Tile(blocked = False, block_sight = False)
		for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
 
	rooms = []
	num_rooms = 0
 
	for r in range(MAX_ROOMS):
		#random width and height
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#random position without going out of the boundaries of the map
		x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
	
		new_room = Rect(x, y, w, h)
	#Uses some sort of witchcraft to check whether the rooms intersect or not
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
	#new_room is an instance of the Rect class, if you get confused again.
		if not failed:
			create_room(new_room)
			place_objects(new_room)
		(new_x, new_y) = new_room.center()
		if num_rooms == 0:
			player.x = new_x
			player.y = new_y
		else:
			(prev_x, prev_y) = rooms[num_rooms - 1].center()
		rooms.append(new_room)
		num_rooms += 1

########################
#Object and combat info#
########################

class Object:
	#Generic Object, anything represented by the screen
	def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None):
		self.name = name
		self.blocks = blocks
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.fighter = fighter
		if self.fighter:  #let the fighter component know who owns it
			self.fighter.owner = self
 
		self.ai = ai
		if self.ai:  #let the AI component know who owns it
			self.ai.owner = self
		
	def send_to_back(self):
		#This brings all the objects in play to the function.
		global objects
		objects.remove(self)
		objects.insert(0, self)
	
	def move(self, dx, dy):
	    if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
		
	def draw(self):
		if lbc.map_is_in_fov(fov_map, self.x, self.y):
			if self.x > startx:
				if self.x < display_width+startx:
					if self.y > starty:
						if self.y < display_height+starty:
							lbc.console_set_foreground_color(con, self.color)
							lbc.console_put_char(con, self.x-startx, self.y-starty, self.char, lbc.BKGND_NONE)
		
	def clear(self):
		if self.x > startx:
			if self.x < display_width+startx:
				if self.y > starty:
					if self.y < display_height+starty:
						lbc.console_put_char(con, self.x-startx, self.y-starty, ' ', lbc.BKGND_NONE)
		
	def move_towards(self, target_x, target_y):
		#vector
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)
		#make it 1 tile length distance and make it an integer ot keep it on the map grid
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		self.move(dx, dy)
	
	def distance_to(self, other):
		#vector
		dx = other.x - self.x
		dy = other.y - self.y
		return(math.sqrt(dx ** 2 + dy ** 2))

class Fighter:
	def __init__(self, defense, power, speed, hp, head_hp=0, torso_hp=0, lArm_hp=0, rArm_hp=0, lLeg_hp=0, rLeg_hp=0, can_attack = 0, sprint = False, death_function=None, attack_mode_stat = None, body=' '):
		self.max_hp = hp
		self.hp = hp
		self.body = body
		self.defense = defense
		self.power = power
		self.death_function = death_function
		self.attack_mode_stat = attack_mode_stat
		self.speed = speed
		self.reg_speed = speed
		self.can_attack = can_attack
		self.sprint = sprint
		self.head_hp = [int(self.max_hp*.8), int(self.max_hp*.8)]
		self.torso_hp = [int(self.max_hp*1.5), int(self.max_hp*1.5)]
		self.lArm_hp = [int(self.max_hp*1), int(self.max_hp*1)]
		self.rArm_hp = [int(self.max_hp*1), int(self.max_hp*1)]
		self.lLeg_hp = [int(self.max_hp*1.2), int(self.max_hp*1.2)]
		self.rLeg_hp = [int(self.max_hp*1.2), int(self.max_hp*1.2)]

		
	def take_damage(self, damage, part):
		if part[0] > 0:
			part[0] = part[0] - damage
			if self.torso_hp[0] <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)
			if self.head_hp[0] <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)
	#Checks for and activates a death function if your HP drops below 0.
	
	def attack(self, target):
		global ann_combat
		damage = self.power - target.fighter.defense
		#Cause the target damage
		if damage > 0:
			#Not sure how self.owner.name works right now, don't know if I ever will. As far as I can tell, it is a way to find the 
			#name of the object currently acting in this class.
			human_parts = (target.fighter.head_hp, target.fighter.head_hp, target.fighter.torso_hp, target.fighter.torso_hp, target.fighter.torso_hp, target.fighter.lArm_hp, target.fighter.rArm_hp, target.fighter.lLeg_hp, target.fighter.rLeg_hp)
			human_parts_name = ("head", "head", "torso", "torso", "torso", "left arm", "right arm", "left leg", "right leg")
			body_part_number = lbc.random_get_int(0, 0, 8)
			body_part = human_parts[body_part_number]
			target.fighter.take_damage(damage, body_part)
			ann_combatd1.append(self.owner.name.capitalize() + " Attacks " + target.name.capitalize() + "'s " + human_parts_name[body_part_number] + ' for ' + str(damage) + " damage!")
			#The way this is set up goes as follows: target (the target being attacked by the fighter) fighter (the subclass where
			#take_damage is located) (damage) the damage done to the target.
		if damage <= 0:
			ann_combatd0.append(self.owner.name.capitalize() + " Attacks " + target.name.capitalize() + ', but they are not harmed!')
			
def player_death(player):
	global game_state
	ann_combatdeath.append('You died!')
	game_state = 'dead'
		
	player.char = '%'
	player.color = lbc.dark_red	

def monster_death(monster):
	ann_combatdeath.append(monster.name.capitalize() + ' is dead!')
	monster.char = '%'
	monster.color = lbc.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = monster.name + " corpse"
	monster.send_to_back()

class BasicMonster:
	#Super basic AI
	def take_turn(self):
		global ann_dialog
		monster = self.owner
		if lbc.map_is_in_fov(fov_map, monster.x, monster.y):
			#generates a random number between 1 and 15. If the number is 6, this dialog is spoken. The same applies for later dialog,
			#with correspoding numbers.
			max_number = 25 * player.fighter.speed
			dialog = lbc.random_get_int(0, 1, int(max_number))
			if dialog == 2:

				ann_dialog.append('The ' + self.owner.name + ' yells "HR is gonna hear about this!"')
			if dialog == 3:

				ann_dialog.append('The ' + self.owner.name + ' yells "This is not good for morale!"')
			if dialog == 4:

				ann_dialog.append('The ' + self.owner.name + ' yells "Son of a biscuit!"')
			if dialog == 5:

				ann_dialog.append('The ' + self.owner.name + ' yells "MOO!"')
			if dialog == 6:

				ann_dialog.append('The ' + self.owner.name + ' yells "Drop it, you hobo!"')
			if dialog == 7:

				ann_dialog.append('The ' + self.owner.name + ' yells "You! Stop!"')
			if dialog == 8:

				ann_dialog.append('The ' + self.owner.name + ' yells "Gimme back my wallet, you bum!"')
			if dialog == 9:

				ann_dialog.append('The ' + self.owner.name + ' yells "Hey, get back here!"')
			if dialog == 10:

				ann_dialog.append('The ' + self.owner.name + ' yells "HEY!"')
			#Controls whether a monster can move during a turn based on their speed.
			#Calculates the multipliers based on the player's chosen movement speed.
			if player.fighter.sprint == 0:
				player.fighter.speed = .5
			elif player.fighter.sprint == 1:
				player.fighter.speed = 1
			elif player.fighter.sprint == 2:
				player.fighter.speed = 1.5
			elif player.fighter.sprint == 3:
				player.fighter.speed = 2.25
			if monster.distance_to(player) >= 2:
				while self.owner.fighter.can_attack >= 1:
					monster.move_towards(player.x, player.y)
					self.owner.fighter.can_attack = self.owner.fighter.can_attack - 1
				if self.owner.fighter.can_attack < 1:
					self.owner.fighter.can_attack = self.owner.fighter.can_attack + (self.owner.fighter.speed/player.fighter.speed)
			elif player.fighter.torso_hp[0] > 0:
				while self.owner.fighter.can_attack >= 1:
					monster.fighter.attack(player)
					self.owner.fighter.can_attack = self.owner.fighter.can_attack - 1
				if self.owner.fighter.can_attack < 1:
					self.owner.fighter.can_attack = self.owner.fighter.can_attack + (self.owner.fighter.speed/player.fighter.speed)



###########################		
#Movement and key controls#
###########################
	
	
def player_move_or_attack(dx, dy):
	global fov_recompute
	global attack_mode_stat
	x = player.x + dx
	y = player.y + dy
	
	target = None
	for object in objects:
		if player.fighter.attack_mode_stat == True:
			if object.fighter and object.x == x and object.y == y: 
				target = object
				break
	if target is not None:
		if target is not player:
			fov_recompute = True
			player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True	
		
def handle_keys():
	global playerx, playery
	global fov_recompute
	global attack_mode
	global attack_mode_stat

	key = libtcod.console_wait_for_keypress(True)
	
	if key.vk == lbc.KEY_ENTER and lbc.KEY_ALT:
		lbc.console_set_fullscreen(not lbc.console_is_fullscreen())
	
	elif key.vk == lbc.KEY_ESCAPE:
		return 'exit'
		
	elif key.vk == lbc.KEY_F6:
		game_state == 'didnt_take_turn'
		fov_recompute = True
		player.fighter.attack_mode_stat = not player.fighter.attack_mode_stat
		if player.fighter.attack_mode_stat == True:
			ann_passive_actions.append("You prepare yourself, moving into a fighting stance.")
			fov_recompute = True
		elif player.fighter.attack_mode_stat == False:
			ann_passive_actions.append("You relax, assuming a regular stance.")
			fov_recompute = True
	elif key.vk == lbc.KEY_F5:
		
		if player.fighter.sprint <= 3:
			player.fighter.sprint = player.fighter.sprint + 1
		if player.fighter.sprint == 1:
			ann_passive_actions.append("You pick up the pace, moving at a light jog.")
			fov_recompute = True
		if player.fighter.sprint == 2:
			ann_passive_actions.append("You move quickly, breathing raggedly as you run.")
			fov_recompute = True
		if player.fighter.sprint == 3:
			ann_passive_actions.append("You bolt madly, your feet flying along the ground.")
			fov_recompute = True
		if player.fighter.sprint > 3:
			player.fighter.sprint = 0
			ann_passive_actions.append("You walk at a steady, slow pace.")
			fov_recompute = True
		
		
	
	#Movement Keys
	if game_state == 'playing':
        #movement keys
		if lbc.console_is_key_pressed(lbc.KEY_KP8):
			player_move_or_attack(0,-1)
			
		elif lbc.console_is_key_pressed(lbc.KEY_UP):
			player_move_or_attack(0,-1)
	 
		elif lbc.console_is_key_pressed(lbc.KEY_KP2):
			player_move_or_attack(0,1)
			
		elif lbc.console_is_key_pressed(lbc.KEY_DOWN):
			player_move_or_attack(0,1)
	 
		elif lbc.console_is_key_pressed(lbc.KEY_KP4):
			player_move_or_attack(-1,0)
			
		elif lbc.console_is_key_pressed(lbc.KEY_LEFT):
			player_move_or_attack(-1,0)
	 
		elif lbc.console_is_key_pressed(lbc.KEY_KP6):
			player_move_or_attack(1,0)
			
		elif lbc.console_is_key_pressed(lbc.KEY_RIGHT):
			player_move_or_attack(1,0)
		
		elif lbc.console_is_key_pressed(lbc.KEY_KP1):
			player_move_or_attack(-1,1)
			
		elif lbc.console_is_key_pressed(lbc.KEY_KP3):
			player_move_or_attack(1,1)
			
		elif lbc.console_is_key_pressed(lbc.KEY_KP7):
			player_move_or_attack(-1,-1)
			
		elif lbc.console_is_key_pressed(lbc.KEY_KP9):
			player_move_or_attack(1,-1)
			
		elif lbc.console_is_key_pressed(lbc.KEY_KP5):
			player_move_or_attack(0, 0) 
			fov_recompute = True
		else:
			return 'didnt-take-turn'

def render_all():
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute
    global startx, starty
    screen_gui_limit_y = 0
    screen_gui_limit_x = 0
    
    if MAP_HEIGHT > SCREEN_HEIGHT - 10:
        screen_gui_limit_y = SCREEN_HEIGHT - 10 - MAP_HEIGHT
    if MAP_WIDTH > SCREEN_WIDTH - 8:
        screen_gui_limit_x = SCREEN_WIDTH - 8 - MAP_WIDTH

    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, (player.x), (player.y), int(torch_radius), FOV_LIGHT_WALLS, 1)
 
        #go through all tiles, and set their background color according to the FOV
        for y in range(starty, display_height+starty):
            for x in range(startx, display_width+startx):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    #it's out of the player's FOV
					if wall:
						libtcod.console_set_back(con, x-startx, y-starty, color_dark_wall, libtcod.BKGND_SET)
					else:
						libtcod.console_set_back(con, x-startx, y-starty, color_dark_ground, libtcod.BKGND_SET)
					
                else:
                    #it's visible
					if wall:
						libtcod.console_set_back(con, x-startx, y-starty, color_light_wall, libtcod.BKGND_SET )
					else:
						libtcod.console_set_back(con, x-startx, y-starty, color_light_ground, libtcod.BKGND_SET )
					
    #draw all objects in the list
	for object in objects:
		if object != player:
			object.draw()
		player.draw()
    #blit the contents of "con" to the root console
	libtcod.console_blit(con, 0, 0, display_width, display_height, 0, 0, 0)

def clock_move():
	global time_minute, time_hour, am, torch_radius, speed
	time_minute = time_minute + .25/player.fighter.speed
	if time_minute == 60:
		time_hour = time_hour + 1
		time_minute = 0
	if time_hour == 12:
		if time_minute == 0:
			am = not am
	if time_hour > 12:
		time_hour = 1
		time_minute = 0
	if am == True:
		if time_hour >= 6:
			if time_hour < 12:
				torch_radius = torch_radius + 1.5 * player.fighter.speed
	if am == False:
		if time_hour >= 8:
			if time_hour < 12:
				if torch_radius >= 4:
					torch_radius = torch_radius - 1.5 * player.fighter.speed

###########
#GUI Stuff#
###########
panel = lbc.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	bar_width = int(float(value) / maximum * total_width)
	
	lbc.console_set_background_color(panel, back_color)
	lbc.console_rect(panel, x, y, total_width, 1, False)
	
	lbc.console_set_background_color(panel, bar_color)
	if bar_width > 0:
		lbc.console_rect(panel, x, y, bar_width, 1, False)
	lbc.console_set_background_color(panel, lbc.white)
	lbc.console_set_print_center(panel, x + total_width / 2, y, lbc.BKGND_NONE, name)
def render_gui():
	global attack_mode_stat_string
	attack_mode_stat_string = ' '
	#Health Display Internals 
	
	#Health Display
	def name_hp(part):
		if part[0] >= part[1]:
			status = 'Fine'
			return status
		if part[0] < part[1]:
			if part[0] >= part[1]*.75:
				status = 'Good'
				return status
			if part[0] >= part[1]*.5:
				if part[0] < part[1]*.75:
					status = 'Okay'
					return status
			if part[0] >= part[1]*.25:
				if part[0] < part[1]*.5:
					status = 'Poor'
					return status
			if part[0] < part[1]*.25:
				if part[0] > 0:
					status = 'DANG'
					return status
			if part[0] <= 0:
				status = 'Lost'
				return status
	libtcod.console_set_foreground_color(0, libtcod.light_orange)
	libtcod.console_print_right(0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 10, libtcod.BKGND_NONE, 'Head Body lArm rArm lLeg rLeg')
	libtcod.console_set_foreground_color(0, libtcod.green)
	libtcod.console_print_right(0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 9, libtcod.BKGND_NONE,  str(name_hp(player.fighter.head_hp)) + ' ' + str(name_hp(player.fighter.torso_hp)) + ' ' + str(name_hp(player.fighter.lArm_hp)) + ' ' + str(name_hp(player.fighter.rArm_hp)) + ' ' + str(name_hp(player.fighter.lLeg_hp)) + ' ' + str(name_hp(player.fighter.rLeg_hp)))
	#Attack Mode Indicator
	if player.fighter.attack_mode_stat == True:
		attack_mode_stat_string = 'On '
	elif player.fighter.attack_mode_stat == False:
		attack_mode_stat_string = 'Off'
	libtcod.console_set_foreground_color(0, libtcod.light_blue)
	lbc.console_print_left(0, SCREEN_WIDTH - 13, SCREEN_HEIGHT - 3, lbc.BKGND_NONE, 'Atk mode:' + str(attack_mode_stat_string))
	#Targeting Indicator
	lbc.console_print_left(0, SCREEN_WIDTH - 13, SCREEN_HEIGHT -7, lbc.BKGND_NONE, '           o ')
	lbc.console_print_left(0, SCREEN_WIDTH - 13, SCREEN_HEIGHT -6, lbc.BKGND_NONE, 'Targeted: /@''\\')
	lbc.console_print_left(0, SCREEN_WIDTH - 13, SCREEN_HEIGHT -5, lbc.BKGND_NONE, '          / \\' )
	#Sprint Indicator
	if player.fighter.sprint == 0:
		sprint_string = ' Walk.'
	elif player.fighter.sprint == 1:
		sprint_string = ' Run. '
	elif player.fighter.sprint == 2:
		sprint_string = ' RUN. '
	elif player.fighter.sprint == 3:
		sprint_string = ' RUN! '
	libtcod.console_set_foreground_color(0, libtcod.light_green)
	lbc.console_print_left(0, SCREEN_WIDTH - 13, SCREEN_HEIGHT - 2, lbc.BKGND_NONE, 'Speed:' + str(sprint_string))
	#Clock
	libtcod.console_set_foreground_color(0, libtcod.light_grey)
	if time_minute >= 10: 
		if am == True:
			lbc.console_print_right(0, SCREEN_WIDTH - 1, 0, lbc. BKGND_NONE, str(time_hour) + ":" + str(int(time_minute)) + " AM")
		if am == False:
			lbc.console_print_right(0, SCREEN_WIDTH - 1, 0, lbc. BKGND_NONE, str(time_hour) + ":" + str(int(time_minute)) + " PM")
	elif time_minute < 10: 
		if am == True:
			lbc.console_print_right(0, SCREEN_WIDTH - 1, 0, lbc. BKGND_NONE, str(time_hour) + ":" + "0" + str(int(time_minute)) + " AM")
		if am == False:
			lbc.console_print_right(0, SCREEN_WIDTH - 1, 0, lbc. BKGND_NONE, str(time_hour) + ":" + "0" + str(int(time_minute)) + " PM")

def print_announcements():
	top = len(ann_dialog) + len(ann_combatd1) + len(ann_combatd0) + len(ann_passive_actions) + len(ann_combatdeath)
	#While there are more than 8 things in the list, remove the latest ones... AHA, GOTCHA YA FUCKERS
	x = 0
	while len(total)+top > 8:
		x = x + 1
		total.pop(x - 1)
	#If there are one or more things to be printed...
	if len(total) >= 1:
		#For the range of however many things there are to be printed...
		for x in range(len(total)):
			libtcod.console_set_foreground_color(0, libtcod.grey)
			lbc.console_print_left(0, 0, SCREEN_HEIGHT - len(total) + x - top, lbc.BKGND_NONE, total[x])
	while len(ann_passive_actions) >= 1:
		libtcod.console_set_foreground_color(0, libtcod.light_blue)
		newline = ann_passive_actions.pop()
		total.append(newline)
		lbc.console_print_left(0, 0, SCREEN_HEIGHT - top, lbc.BKGND_NONE, str(newline))
		top = top - 1
	while len(ann_dialog) >= 1:
		libtcod.console_set_foreground_color(0, libtcod.light_green)
		newline = ann_dialog.pop()
		lbc.console_print_left(0, 0, SCREEN_HEIGHT - top, lbc.BKGND_NONE, str(newline))
		total.append(newline)
		top = top - 1
	while len(ann_combatd1) >= 1:
		libtcod.console_set_foreground_color(0, libtcod.red)
		newline = ann_combatd1.pop()
		lbc.console_print_left(0, 0, SCREEN_HEIGHT - top, lbc.BKGND_NONE, str(newline))
		total.append(newline)
		top = top - 1
	while len(ann_combatd0) >= 1:
		libtcod.console_set_foreground_color(0, libtcod.light_red)
		newline = ann_combatd0.pop()
		lbc.console_print_left(0, 0, SCREEN_HEIGHT - top, lbc.BKGND_NONE, str(newline))
		total.append(newline)
		top = top - 1
	while len(ann_combatdeath) >= 1:
		libtcod.console_set_foreground_color(0, libtcod.light_violet)
		newline = ann_combatdeath.pop()
		lbc.console_print_left(0, 0, SCREEN_HEIGHT - top, lbc.BKGND_NONE, str(newline))
		total.append(newline)
		top = top - 1



# # # # # # # # #
#Initialization #
# # # # # # # # #

lbc.console_set_custom_font('prestige12x12_gs_tc.png', lbc.FONT_TYPE_GREYSCALE | lbc.FONT_LAYOUT_TCOD)
lbc.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Vagabond', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
lbc.sys_set_fps(LIMIT_FPS)

fighter_player = Fighter(body = "body_def", hp=55, defense=6, power=6, speed = 1, sprint = 0, death_function=player_death, attack_mode_stat = True)
player = Object(0, 0, '@', 'Player', libtcod.white, blocks = True, fighter=fighter_player)

objects = [player]
make_map()

startx = MAP_WIDTH/2 - display_width/2
starty = MAP_HEIGHT/2 - display_height/2

player.x = MAP_WIDTH/2
player.y = MAP_HEIGHT/2


fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].blocked, not map[x][y].block_sight)

while not lbc.console_is_window_closed():
	clock_move()
	camera_move()
	render_all()
	render_gui()
	print_announcements()
	for object in objects:
		object.draw()
	lbc.console_flush()


	for Object in objects:
		Object.clear()
	
	player_action = handle_keys()
	if player_action == 'exit':
		break
		
	if game_state == 'playing' and player_action != 'didnt-take-turn':
		for object in objects:
			if object.ai:
				object.ai.take_turn()