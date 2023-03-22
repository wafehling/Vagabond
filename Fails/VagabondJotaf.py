"""This is the first major programming project I have undertaken. I started this project in late August 2011. 
Largely based off of a tutorial on Roguebasin by Jotaf.
Written by Rarenth.
I'd like to thank Nalan Hikari, my one and only, for motivating and inspiring me on this project."""


import libtcodpy as lbc, libtcodpy as libtcod
import math
# # # # # # # # # # 
#Screen Orienting #
# # # # # # # # # #

#Window Sizes
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#Map sizes(smaller to accompany stat viewing, etc)
MAP_WIDTH = 80
MAP_HEIGHT = 75

camerax = 0
cameray = 0

MAX_ROOM_MONSTERS = 0
#colors for the current tiles
color_tree = lbc.Color(106, 52, 0)
color_light_ground = lbc.Color(44, 124, 4)

#Limits the screen refresh rate
LIMIT_FPS = 20

#Numbers to be used to renerate dungeon rooms
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
fov_recompute = True

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = color_tree
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = color_light_ground

game_state = 'playing'
player_action = None




#####################################
#Map generation and object placement#
#####################################

class Tile:
	def __init__(self, blocked, explored = False, block_sight = None):
		self.blocked = blocked
		self.explored = explored
		#Tile blocks sight if it's blocked by default (will change later)
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

#makes rectangles in the ground that are passable	
def create_room(room):
	global map
	#make passable rectangles
	for x in range(room.x1, room.x2):
		for y in range(room.y1, room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False
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
 
    for i in range(num_monsters):
		#choose random spot for this monster
			x = libtcod.random_get_int(0, room.x1, room.x2)
			y = libtcod.random_get_int(0, room.y1, room.y2)
	 
			if libtcod.random_get_int(0, 0, 100) < 80:  #80% chance of getting an orc
				if not is_blocked(x, y):
					#create a businessman
					ai_businessman = BasicMonster()
					businessman_defense = lbc.random_get_int(0, 1, 3)
					businessman_power = lbc.random_get_int(0, 1, 4)
					fighter_businessman = Fighter(hp = 10, defense = businessman_defense, power = businessman_power, death_function=monster_death)
					monster = Object(x, y, 'B', 'Businessman', lbc.dark_blue, blocks=True, fighter=fighter_businessman, ai=ai_businessman)
					objects.append(monster)
			else:
				if not is_blocked(x, y):
					#create a businesswoman
					ai_businesswoman = BasicMonster()
					businesswoman_defense = lbc.random_get_int(0, 1, 4)
					businesswoman_power = lbc.random_get_int(0, 1, 3)
					fighter_businesswoman = Fighter(hp = 10, defense = businesswoman_defense, power = businesswoman_power, death_function=monster_death)
					monster = Object(x, y, 'B', 'Businesswoman', lbc.grey, blocks=True, fighter=fighter_businesswoman, ai=ai_businesswoman)
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
	
    #fill map with "blocked" tiles
	map = [[ Tile(True)
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
			player.x = new_x+camerax
			player.y = new_y+cameray
		else:
			(prev_x, prev_y) = rooms[num_rooms - 1].center()
			create_h_tunnel(prev_x, new_x, prev_y)
			create_v_tunnel(prev_y, new_y, prev_x)
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
			lbc.console_set_foreground_color(con, self.color)
			lbc.console_put_char(con, self.x, self.y, self.char, lbc.BKGND_NONE)
		
	def clear(self):
		lbc.console_put_char(con, self.x, self.y, ' ', lbc.BKGND_NONE)
		
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
	def __init__(self, hp, defense, power, death_function=None, attack_mode_stat = None):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power
		self.death_function = death_function
		self.attack_mode_stat = attack_mode_stat
	def take_damage(self, damage):
		if self.hp > 0:
			self.hp = self.hp - damage
			if self.hp <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)
	#Checks for and activates a death function if your HP drops below 0.
	
	def attack(self, target):
		damage = self.power - target.fighter.defense
		#Cause the target damage
		if damage > 0:
			#Not sure how self.owner.name works right now, don't know if I ever will. As far as I can tell, it is a way to find the 
			#name of the object currently acting in this class.
			print self.owner.name.capitalize() + " Attacks " + target.name.capitalize() + ' for ' + str(damage) + " damage!"
			#The way this is set up goes as follows: target (the target being attacked by the fighter) fighter (the subclass where
			#take_damage is located) (damage) the damage done to the target.
			target.fighter.take_damage(damage)
		if damage <= 0:
			print self.owner.name.capitalize() + " Attacks " + target.name.capitalize() + ', but the attack is deflected!'		
			
def player_death(player):
	global game_state
	print 'You died!'
	game_state = 'dead'
		
	player.char = '%'
	player.color = lbc.dark_red	

def monster_death(monster):
	print monster.name.capitalize() + ' is dead!'
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
		monster = self.owner
		if lbc.map_is_in_fov(fov_map, monster.x, monster.y):
			#generates a random number between 1 and 15. If the number is 6, this dialog is spoken. The same applies for later dialog,
			#with correspoding numbers.
			dialog = lbc.random_get_int(0, 1, 25)
			if dialog == 2:
				print 'The ' + self.owner.name + ' yells "HR is gonna hear about this!"'
			if dialog == 3:
				print 'The ' + self.owner.name + ' yells "This is not good for morale!"'
			if dialog == 4:
				print 'The ' + self.owner.name + ' yells "Son of a biscuit!"'
			if dialog == 5:
				print 'The ' + self.owner.name + ' yells "MOO!"'
			if dialog == 6:
				print 'The ' + self.owner.name + ' yells "Drop it, you hobo!"'
			if dialog == 7:
				print 'The ' + self.owner.name + ' yells "You! Stop!"'
			if dialog == 8:
				print 'The ' + self.owner.name + ' yells "Gimme back my wallet, you bum!"'
			if dialog == 9:
				print 'The ' + self.owner.name + ' yells "Hey, get back here!"'
			if dialog == 10:
				print 'The ' + self.owner.name + ' yells "HEY!"'
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)
				
			elif player.fighter.hp > 0:
				monster.fighter.attack(player)

###########################		
#Movement and key controls#
###########################
	
def camera_chase():
	global camerax, cameray
	if camerax + SCREEN_WIDTH > player.x and camerax > 0:
		camerax = camerax + 1
	if (cameray + SCREEN_HEIGHT > player.y and cameray > 0):
		cameray = cameray + 1
	if (camerax + SCREEN_WIDTH/2 < player.x and camerax < MAP_WIDTH - SCREEN_WIDTH - 1):
		camerax = camerax - 1
	if (cameray + SCREEN_HEIGHT/2 < player.y and cameray < MAP_HEIGHT - SCREEN_HEIGHT - 1):
		cameray = cameray - 1

def player_move_or_attack(dx, dy):
	global camerax, cameray, SCREEN_WIDTH, SCREEN_HEIGHT
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
		player.fighter.attack_mode_stat = not player.fighter.attack_mode_stat
		if player.fighter.attack_mode_stat == True:
			print "You prepare yourself, moving into a fighting stance."
		elif player.fighter.attack_mode_stat == False:
			print "You relax, assuming a regular stance."
			
		
	
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
		else:
			return 'didnt-take-turn'
 
def render_all():
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute

 
    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, 12)
 
        #go through all tiles, and set their background color according to the FOV
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x+camerax, y+cameray)
                wall = map[x+camerax][y+cameray].block_sight
                if not visible:
                    #it's out of the player's FOV
					if map[x+camerax][y+cameray].explored:
						if wall:
							libtcod.console_set_back(con, x, y, color_dark_wall, libtcod.BKGND_SET)
						else:
							libtcod.console_set_back(con, x, y, color_dark_ground, libtcod.BKGND_SET)
						
                else:
                    #it's visible
						map[x+camerax][y+cameray].explored = True
						if wall:
							libtcod.console_set_back(con, x, y, color_light_wall, libtcod.BKGND_SET )
						else:
							libtcod.console_set_back(con, x, y, color_light_ground, libtcod.BKGND_SET )
					
    #draw all objects in the list
	for object in objects:
		if object != player:
			object.draw()
		player.draw()
    #blit the contents of "con" to the root console
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
###########
#GUI Stuff#
###########
def render_gui():
	global attack_mode_stat_string
	attack_mode_stat_string = ' '
	#Health Bar
	libtcod.console_set_foreground_color(0, libtcod.light_red)
	libtcod.console_print_left(0, 0, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, 'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))
	#Attack Mode Indicator
	if player.fighter.attack_mode_stat == True:
		attack_mode_stat_string = 'On '
	elif player.fighter.attack_mode_stat == False:
		attack_mode_stat_string = 'Off'
	libtcod.console_set_foreground_color(0, libtcod.light_blue)
	lbc.console_print_left(0, SCREEN_WIDTH - 16, SCREEN_HEIGHT - 1, lbc.BKGND_NONE, 'Attack mode: ' + str(attack_mode_stat_string))

def console_clear():
	for y in range(SCREEN_HEIGHT):
		for x in range(SCREEN_WIDTH):
			libtcod.console_set_back(con, x, y, lbc.black, libtcod.BKGND_SET)
			libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
 

# # # # # # # # #
#Initialization #
# # # # # # # # #	

lbc.console_set_custom_font('prestige12x12_gs_tc.png', lbc.FONT_TYPE_GREYSCALE | lbc.FONT_LAYOUT_TCOD)
lbc.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Vagabond', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
lbc.sys_set_fps(LIMIT_FPS)


fighter_player = Fighter(hp=55, defense=6, power=6, death_function=player_death, attack_mode_stat = True)
player = Object(0, 0, '@', 'Player', libtcod.white, blocks = True, fighter=fighter_player)



objects = [player]
make_map()

fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].blocked, not map[x][y].block_sight)

while not lbc.console_is_window_closed():
	console_clear()
	camera_chase()
	render_all()
	render_gui()
	
	lbc.console_flush()
	print ("cameras: " + str(camerax) + " " + str(cameray))
	print ("camerax + SCREEN_WIDTH/2 VS player.x: " + str(camerax + SCREEN_WIDTH/2) + ' ' + str(player.x))
	print ("cameray + SCREEN_HEIGHT/2 VS player.y: " + str(cameray + SCREEN_HEIGHT/2) + ' ' + str(player.y))
	for Object in objects:
		Object.clear()
	
	player_action = handle_keys()
	if player_action == 'exit':
		break
		
	if game_state == 'playing' and player_action != 'didnt-take-turn':
		for object in objects:
			if object.ai:
				object.ai.take_turn()