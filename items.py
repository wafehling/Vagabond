import libtcodpy as lbc 
import libtcodpy as libtcod
import overmap
import objects
import map
import items
import objects
import con_info

objects_list = []
inventory = []
ann_item_actions = []


class Object:
	#Generic Object, anything represented by the screen
	def __init__(self, x, y, char, name, color_front=None, color_back = None, overmapx = 0, overmapy = 0, blocks=False, fighter=None, ai=None, item = None):
		self.name = name
		self.blocks = blocks
		self.x = x
		self.y = y
		self.overmapx = overmapx
		self.overmapy = overmapy
		self.char = char
		self.color_front = color_front
		self.color_back = color_back
		self.fighter = fighter
		self.item = item
		if self.item:  #let the Item component know who owns it
			self.item.owner = self
		if self.fighter:  #let the fighter component know who owns it
			self.fighter.owner = self
 
		self.ai = ai
		if self.ai:  #let the AI component know who owns it
			self.ai.owner = self
		
	def send_to_back(self):
		#This brings all the objects in play to the function.
		global objects
		items.objects_list.remove(self)
		items.objects_list.insert(0, self)
	
	def move(self, dx, dy):
	    if not map.is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
	def move_noblock(self, dx, dy):
		self.x += dx
		self.y += dy
		
	def draw(self):
		if lbc.map_is_in_fov(map.fov_map, self.x, self.y):
			if self.x >= map.startx:
				if self.x < con_info.display_width+map.startx:
					if self.y >= map.starty:
						if self.y < con_info.display_height+map.starty:
							lbc.console_set_foreground_color(con_info.con, self.color_front)
							lbc.console_set_background_color(con_info.con, self.color_back)
							lbc.console_put_char(con_info.con, self.x-map.startx, self.y-map.starty, self.char, lbc.BKGND_NONE)
		
	def clear(self):
		if self.x >= map.startx:
			if self.x < con_info.display_width+map.startx:
				if self.y > map.starty:
					if self.y < con_info.display_height+map.starty:
						lbc.console_put_char(con_info.con, self.x-map.startx, self.y-map.starty, map.map_map[self.x][self.y].chara, lbc.BKGND_NONE)
						lbc.console_set_foreground_color(con_info.con, map.map_map[self.x][self.y].color_front)
						lbc.console_set_background_color(con_info.con, map.map_map[self.x][self.y].color_back)
		
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
	
	def describe():
		print self.name


class Item:
	def __init__(self, weight = 1, volume = 1, container = False):
		self.weight = weight
		self.volume = volume
		self.container = container
	#an item that can be picked up and used.
	def pick_up(self):
		#add to the player's inventory and remove from the map
		inventory.append(self.owner)
		items.objects_list.remove(self.owner)
		ann_item_actions.append('You picked up a ' + self.owner.name + '.')
	def drop(self):
		items.objects_list.append(self.owner)
		inventory.remove(self.owner)
		ann_item_actions.append('You dropped a ' + self.owner.name + '.')
#Item Types
item_large_cardboard_box = [10, 50,True]
item_small_cardboard_box = [2, 4, True]
item_cardboard_piece = [2, 8, False]
item_newspaper_sheet = [1, 1, False]
item_small_container = [1, 1, True]

#Trash Items
large_cardboard_box = ['U', 'large cardboard box', lbc.Color(150, 100, 0), None, False, item_large_cardboard_box]
small_cardboard_box = ['u', 'small cardboard box', lbc.Color(150, 100, 0), None, False, item_small_cardboard_box]
newspaper_sheet = ['^', 'newspaper sheet', lbc.light_grey, None, False, item_newspaper_sheet]
cardboard_piece = ['[', 'cardboard piece', lbc.Color(150, 100, 0), None, False, item_cardboard_piece]
aluminum_can = ['u', 'aluminum can', lbc.grey, None, False, item_small_container]
paper_bag = ['c', 'paper bag', lbc.Color(172, 89, 0), None, False, item_small_container]
plastic_bottle = ['u', 'plastic bottle', lbc.white, None, False, item_small_container]
plastic_bag = ['c', 'plastic bag', lbc.white, None, False, item_small_container]
glass_bottle = ['u', 'glass bottle', lbc.Color(119, 119, 255), None, False, item_small_container]

"""#Furniture Items
wooden_chair
easy_chair
metal_chair
wooden_table
metal_table
filing_cabinet
"""

def place_junk(junk_items = 25, tiles = []):
	#Create random junk
	global overmappyx, overmappyy, junk_items_alpha
	junk_items_alpha = junk_items
	def make_junk(junk_items_alpha):
		global overmapx, overmapy, junk_items
		item_type = Item(item_type_weight, item_type_volume, item_type_container)
		item = Object(x = x_val, y = y_val, char = item_char, name = item_name, color_front = item_color_front, color_back = item_color_back, blocks = item_blocked, item = item_type)
		items.objects_list.append(item)
		

	if overmap.abandoned_map[map.overmappyx][map.overmappyy] == True:
		junk_items = junk_items * 2
	while junk_items > 0:
		x_val = lbc.random_get_int(0, 1, map.map_width - 1)
		y_val = lbc.random_get_int(0, 1, map.map_height - 1)
		
		#This chooses the item and pulls the info from the list of items store in items.py
		item_choice = lbc.random_get_int(0, 0, 14)
		
		
		if item_choice == 0:
			active_item = large_cardboard_box
			active_item_item = item_large_cardboard_box
		elif item_choice <= 4:
			active_item = newspaper_sheet
			active_item_item = item_newspaper_sheet
		elif item_choice <= 5:
			active_item = cardboard_piece
			active_item_item = item_cardboard_piece
		elif item_choice <= 7:
			active_item = aluminum_can
			active_item_item = item_small_container
		elif item_choice <= 8:
			active_item = paper_bag
			active_item_item = item_small_container
		elif item_choice <= 10:
			active_item = plastic_bottle
			active_item_item = item_small_container
		elif item_choice <= 13:
			active_item = plastic_bag
			active_item_item = item_small_container
		elif item_choice <= 14:
			active_item = glass_bottle
			active_item_item = item_small_container
		item_char = active_item[0]
		item_name = active_item[1]
		item_color_front = active_item[2]
		item_color_back = active_item[3]
		item_blocked = active_item[4]
		
		item_type_weight = active_item_item[0]
		item_type_volume = active_item_item[1]
		item_type_container = active_item_item[2]
		
		junk_items -= 1
		if not map.is_blocked(x_val, y_val):
			for x in tiles:
				if map.map_map[x_val][y_val].num == x:
					make_junk(junk_items)

		