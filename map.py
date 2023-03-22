import libtcodpy as lbc 
import libtcodpy as libtcod
import overmap
import objects, items


#Map sizes(smaller to accompany stat viewing, etc)
map_width = 57
map_height = 55

startx = 0
starty = 0

#Map tiles
color_missing = lbc.Color(100,1,90)
color_tree = lbc.Color(106, 52, 0)
color_dirt = lbc.Color(90, 56, 27)
color_light_wall_1 = lbc.Color(78, 78, 78)
color_light_wall_2 = lbc.Color(127, 123, 100)
color_light_wall_3 = lbc.Color(41, 41, 41)
color_light_wall_4 = lbc.Color(194, 194, 194)
color_light_wall_5 = lbc.Color(213, 195, 141)
color_trash_1 = lbc.Color(135, 103, 66)
color_trash_2 = lbc.Color(95, 75, 51)
color_trash_3 = lbc.Color(28, 55, 56)
color_trash_4 = lbc.Color(176, 61, 32)
color_trash_5 = lbc.Color(110, 134, 135)
color_sidewalk = lbc.Color(160, 160, 160)
color_floor = lbc.Color(104,104,104)
color_grass = lbc.Color(16,119,4)
color_street = lbc.Color(60,60,60)
color_lookie = lbc.Color(0,34,0)

color_office_building = lbc.Color(128, 128, 128)
color_apartments_rich = lbc.Color(0, 0, 128)
color_apartments_poor = lbc.Color(0, 128, 128)
color_park = lbc.Color(0, 128, 0)
color_scrap_heap = lbc.Color(0, 128, 0)
color_factory = lbc.Color(128, 0, 128)
color_warehouse = lbc.Color(128, 128, 128)
color_home_rich = lbc.Color(0, 0, 128)
color_home_poor = lbc.Color(0, 128, 128)
color_stores = lbc.Color(128, 0, 65)
color_pier = lbc.Color(0, 64, 64)
color_warehouse = lbc.Color(128, 64, 0)
color_street = lbc.Color(128,128,128)
color_water_back = lbc.Color(0, 0, 128)
color_water_front = lbc.Color(0, 128, 192)
color_missing = lbc.Color(100,1,90)

class Tile:
	def __init__(self, blocked, chara = 'X', color_front = color_missing, color_back = color_missing,  block_sight = None, searchable = False, name = 'test', num = 0):
		self.blocked = blocked
		self.color_back = color_back
		self.color_front = color_front
		self.chara = chara
		self.block_sight = block_sight
		self.searchable = searchable
		self.name = name
		self.num = num
		
def initialize_fov():
	global fov_recompute, fov_map
	fov_recompute = True
	libtcod.console_clear(0)
	fov_map = libtcod.map_new(map_width, map_height)
	for y in xrange(map_height):
		for x in xrange(map_width):
			libtcod.map_set_properties(fov_map, x, y, not map_map[x][y].blocked, not map_map[x][y].block_sight)

class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = w
        self.y2 = h
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        self.center_x = center_x
        self.center_y = center_y
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(room, floor, wall):
    global map
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1, room.x2):
        for y in range(room.y1, room.y2):
            map_map[x][y] = floor
	for x in xrange(room.x1, room.x2 + 1):
		map_map[x][room.y1] = wall
		map_map[x][room.y2] = wall
	for y in xrange(room.y1, room.y2 + 1):
		map_map[room.x1][y] = wall
		map_map[room.x2][y] = wall
	

def is_blocked(x, y):
	if map_map[x][y].blocked:
		return True
	
	for object in items.objects_list:
		if object.blocks and object.x == x and object.y == y:
			return True
			
	return False
	
	

dirt_tile = Tile(blocked = False, chara = ' ', color_front = color_dirt, color_back = color_dirt, block_sight = None, num = 0, name = "Dirt")
grass_tile = Tile(blocked = False, chara = '.', color_front = color_grass, color_back = color_dirt, block_sight = None, num = 1, name = "Grass")
small_tree_tile = Tile(blocked = True, chara = chr(179), color_front = lbc.dark_green, color_back = color_dirt, block_sight = True, num = 2)
flower_red_tile = Tile(blocked = False, chara = '*', color_front = lbc.dark_red, color_back = color_dirt, block_sight = False, num = 3)
flower_yellow_tile = Tile(blocked = False, chara = '*', color_front = lbc.dark_yellow, color_back = color_dirt, block_sight = False, num = 4)
water_tile = Tile(blocked = False, chara = '~', color_front = color_water_front, color_back = color_water_back, block_sight = False, num = 5)
scrap_small_tile = Tile(blocked = False, chara = '&', color_front = color_scrap_heap, color_back = color_dirt, block_sight = None, searchable = True, num = 6)
scrap_large_tile = Tile(blocked = True, chara = '&', color_front = color_scrap_heap, color_back = lbc.Color(76, 46, 29), block_sight = True,  searchable = True, num = 7)
street_tile = Tile(blocked = False, chara = chr(176), color_front = lbc.dark_grey, color_back = lbc.dark_grey, block_sight = None, num = 8, name = "Street")
sidewalk_tile = Tile(blocked = False, chara = chr(178), color_front = color_sidewalk, color_back = color_sidewalk, block_sight = None, num = 9, name = "Sidewalk")
chain_fence_tile = Tile(blocked = True, chara = '#', color_front = lbc.grey, color_back = lbc.dark_grey, block_sight = False, num = 10)
dock_tile = Tile(blocked = False, chara = '=', color_front = lbc.Color(163, 100, 37), color_back = lbc.Color(100, 61, 21), block_sight = False, num = 11)
door_tile = Tile(blocked = False, chara = '+', color_front = lbc.darker_orange, color_back = lbc.grey, block_sight = None, num = 12)
office_building_floor_tile = Tile(blocked = False, chara = chr(177), color_front = lbc.grey, color_back = lbc.grey, block_sight = False, num = 13)
office_building_wall_tile = Tile(blocked = True, chara = ' ', color_front = None, color_back = lbc.grey, block_sight = True, num = 14)
raw_mats_tile = Tile(blocked = True, chara = '%', color_front = lbc.grey, color_back = lbc.Color(100, 61, 21), block_sight = False, num = 15)
goods_tile = Tile(blocked = True, chara = 'X', color_front = lbc.Color(82, 45, 9), color_back = lbc.Color(100, 61, 21), block_sight = False, num = 16)
belt_tile = Tile(blocked = True, chara = '=', color_front = lbc.grey, color_back = lbc.dark_grey, block_sight = False, num = 17)
machinery_tile = Tile(blocked = True, chara = '&', color_front = lbc.grey, color_back = lbc.dark_grey, block_sight = True, num = 18)
shelf_tile = Tile(blocked = True, chara = '}', color_front = lbc.light_grey, color_back = lbc.grey, block_sight = True, num = 19)
freezer_tile = Tile(blocked = True, chara = '}', color_front = lbc.blue, color_back = lbc.grey, block_sight = True, num = 20)

def make_map(overmapx, overmapy):
	global map_map, player, overmappyx, overmappyy
	overmappyx = overmapx
	overmappyy = overmapy
	def make_doors(x1, y1, x2, y2):
		if x2 == 'repeat':
			x2 = x1
		if y2 == 'repeat':
			y2 = y1
		for x in xrange(x1, x2+1):
			for y in xrange(y1, y2+1):
				map_map[x][y] = door_tile
	def make_wall(x1, y1, x2, y2):
		if x2 == 'repeat':
			x2 = x1
		if y2 == 'repeat':
			y2 = y1
		for x in xrange(x1, x2+1):
			for y in xrange(y1, y2+1):
				map_map[x][y] = office_building_wall_tile
	def make_floor(x1, y1, x2, y2):
		for x in xrange(x1, x2+1):
			for y in xrange(y1, y2+1):
				map_map[x][y] = office_building_floor_tile
	def make_gen_area(x1, y1, x2, y2, tile_type):
		for x in xrange(x1, x2+1):
			for y in xrange(y1, y2+1):
				map_map[x][y] = tile_type
	def make_gen_tile(x, y, tile_type):
		map_map[x][y] = tile_type
	#fill map with "unblocked" tiles
	map_map = [[ Tile(blocked = False, block_sight = False)
		for y in xrange(map_height) ]
			for x in xrange(map_width) ]
	for y in xrange(map_height):
		for x in xrange(map_width):
			grass_num = lbc.random_get_int(0,1,4)
			if grass_num == 1:
				grass_char = chr(59)
			if grass_num == 2:
				grass_char = chr(46)
			if grass_num == 3:
				grass_char = chr(44)
			if grass_num == 4:
				grass_char = chr(39)
			grass_tile = Tile(blocked = False, chara = grass_char, color_front = color_grass, color_back = color_dirt, block_sight = None, num = 1)
			color_number = lbc.random_get_int(0, 1, 4)
			if color_number != 1:
				map_map[x][y] = grass_tile
			else:
				map_map[x][y] = dirt_tile
	def make_chain_fence():
		for why in xrange(7, map_height - 7):
				map_map[map_width - 8][why] = chain_fence_tile
				map_map[7][why] = chain_fence_tile
				
		for x in xrange(7, map_width - 7):
				map_map[x][map_height - 8] = chain_fence_tile
				map_map[x][7] = chain_fence_tile
		for x in xrange(map_width/2-1, map_width/2+2):
			map_map[x][7] = dirt_tile
			map_map[x][map_height-8] = dirt_tile
		for y in xrange(map_height/2-1, map_height/2+2):
			map_map[7][y] = dirt_tile
			map_map[map_width-8][y] = dirt_tile
	def make_scrap():
		for x in xrange(8, map_width - 8):
			for y in xrange(8, map_height - 8):
				scrap_colo = lbc.random_get_int(0, 1, 5)
				if scrap_colo == 1:
					scrap_color = color_trash_1
				if scrap_colo == 2:
					scrap_color = color_trash_2
				if scrap_colo == 3:
					scrap_color = color_trash_3
				if scrap_colo == 4:
					scrap_color = color_trash_4
				if scrap_colo == 5:
					scrap_color = color_trash_5
				scrap_small_tile = Tile(blocked = False, chara = '&', color_front = scrap_color, color_back = color_dirt, block_sight = None, searchable = True, num = 6)
				map_map[x][y] = scrap_small_tile
		
	def make_scrap_heaps():
		scrap_heaps = lbc.random_get_int(0, 25, 30)
		while scrap_heaps >= 1:
			scrap_colo = lbc.random_get_int(0, 1, 5)
			if scrap_colo == 1:
				scrap_color = color_trash_1
			if scrap_colo == 2:
				scrap_color = color_trash_2
			if scrap_colo == 3:
				scrap_color = color_trash_3
			if scrap_colo == 4:
				scrap_color = color_trash_4
			if scrap_colo == 5:
				scrap_color = color_trash_5
			scrap_large_tile = Tile(blocked = True, chara = '&', color_front = scrap_color, color_back = lbc.Color(76, 46, 29), block_sight = True,  searchable = True, num = 7)
			x = lbc.random_get_int(0, 9, map_width-9)
			y = lbc.random_get_int(0, 9, map_height-9)
			chaos_x_1 = lbc.random_get_int(0, -1, 1) 
			chaos_x_2 = lbc.random_get_int(0, -1, 1) 
			chaos_y_1 = lbc.random_get_int(0, -1, 1) 
			chaos_y_2 = lbc.random_get_int(0, -1, 1) 
			map_map[x][y] = scrap_large_tile
			map_map[x+chaos_x_1][y] = scrap_large_tile
			map_map[x+chaos_x_2][y] = scrap_large_tile
			map_map[x][y+chaos_y_1] = scrap_large_tile
			map_map[x][y+chaos_y_2] = scrap_large_tile
			map_map[x+chaos_x_1][y+chaos_y_1] = scrap_large_tile
			map_map[x+chaos_x_2][y+chaos_y_2] = scrap_large_tile
			scrap_heaps = scrap_heaps - 1
	def make_dirt_path():
		for x in xrange(8, map_width-8):
			path_middle = lbc.random_get_int(0, map_height/2-1, map_height/2+1)
			for y in xrange(path_middle-1, path_middle+2):
				map_map[x][y] = dirt_tile
		for y in xrange(7, map_width-9):
			path_middle = path_middle = lbc.random_get_int(0, map_width/2-1, map_width/2+1)
			for x in xrange(path_middle-1, path_middle+2):
				map_map[x][y] = dirt_tile
	def make_sidewalk():
		x = 0
		y = 0
		y2 = 0
		x2 = 0
		while x2 < map_width:
			x2 = x2 + 39
			for why in xrange(5, map_height - 5):
				map_map[map_width - 6][why] = sidewalk_tile
				map_map[map_width - 7][why] = sidewalk_tile
				map_map[5][why] = sidewalk_tile
				map_map[6][why] = sidewalk_tile
		x2 = 0
		while y < map_height:
			y = y + 39
			for x in xrange(5, map_width - 5):
				map_map[x][map_height - 6] = sidewalk_tile
				map_map[x][map_height - 7] = sidewalk_tile
				map_map[x][5] = sidewalk_tile
				map_map[x][6] = sidewalk_tile
		y = 0
		while y < map_height:
			y = y + 39
			for x in xrange(map_width):
				for why in xrange(0,5):
					map_map[x][why] = street_tile
				for why in xrange(map_height-5, map_height):
					map_map[x][why] = street_tile
		while x2 < map_width:
			x2 = x2 + 39
			for why in xrange(map_height):
				for ex in xrange(0,5):
					map_map[ex][why] = street_tile
				for ex in xrange(map_width-5, map_width):
					map_map[ex][why] = street_tile
		
	def pave_over():
		for x in xrange(6, map_width - 6):
			for y in xrange(6, map_height - 6):
				map_map[x][y] = sidewalk_tile
	def make_park():
		for x in xrange(0, map_width):
			for y in xrange(0, map_height):
				tile_type = lbc.random_get_int(0, 1, 35)
				if tile_type <= 27:
					map_map[x][y] = grass_tile
				elif tile_type <= 32:
					map_map[x][y] = dirt_tile
				elif tile_type == 33:
					map_map[x][y] = flower_red_tile
				elif tile_type == 34:
					map_map[x][y] = flower_yellow_tile
				elif tile_type == 35:
					map_map[x][y] = small_tree_tile
	def make_big_trees():
		for x in xrange(0, map_width):
			for y in xrange(0, map_height):
				tree_true = lbc.random_get_int(0, 1, 15)
				if tree_true == 15:
					for x in xrange(x-1, x+1):
						for y in xrange(y-1, y+1):
							map_map[x][y] = small_tree_tile
	def make_ocean():
		for x in xrange(7, map_width):
			for y in xrange(0, map_height):
				map_map[x][y] = water_tile
		for x in xrange(5, 7):
			for y in xrange(0, map_height):
				map_map[x][y] = sidewalk_tile
	def make_dock():
		dock_length = lbc.random_get_int(0, 35, 45)
		dock_pos = lbc.random_get_int(0, map_height/2-15, map_height/2+15)
		for x in xrange(5, dock_length):
			for y in xrange(dock_pos - 3, dock_pos + 2):
				map_map[x][y] = dock_tile
	def make_building():
		global random_x, random_y, wall_color, office_type, x_or_y, office_building_wall_tile, left_wall, right_wall, top_wall, bottom_wall, bldg_height, bldg_width
		#These control the wall positions
		random_x = 10
		random_y = 10
		wall_colo = lbc.random_get_int(0, 1, 5)
		office_type = 1
		top_wall = random_y
		bottom_wall = map_height - random_y - 1
		left_wall = random_x
		right_wall = map_width - random_x - 1
		bldg_height = bottom_wall - top_wall
		bldg_width = right_wall - left_wall
		#This decides whether the main hallway goes along the x or y axis
		x_or_y = lbc.random_get_int(0, 1, 2)
		if wall_colo == 1:
			wall_color = color_light_wall_1
		if wall_colo == 2:
			wall_color = color_light_wall_2
		if wall_colo == 3:
			wall_color = color_light_wall_3
		if wall_colo == 4:
			wall_color = color_light_wall_4
		if wall_colo == 5:
			wall_color = color_light_wall_5
		office_building_wall_tile = Tile(blocked = True, chara = ' ', color_front = None, color_back = wall_color, block_sight = True, num = 8)
		
		main = Rect(left_wall, top_wall, right_wall, bottom_wall)
		create_room(main, floor = office_building_floor_tile, wall = office_building_wall_tile)
		
	#These are new code mappings needed for drawing thin (cubicle) walls.
	
	lbc.console_map_ascii_code_to_font(150, 25, 2)
	lbc.console_map_ascii_codes_to_font(151, 10, 15, 1)
	
	cubicle_none = Tile(blocked = True, chara = chr(150), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")

	cubicle_vert = Tile(blocked = True, chara = chr(150), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_vert_left = Tile(blocked = True, chara = chr(153), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_vert_right = Tile(blocked = True, chara = chr(155), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")

	cubicle_horiz = Tile(blocked = True, chara = chr(151), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_horiz_up = Tile(blocked = True, chara = chr(154), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_horiz_down = Tile(blocked = True, chara = chr(156), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")

	cubicle_all = Tile(blocked = True, chara = chr(152), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")

	cubicle_ne = Tile(blocked = True, chara = chr(157), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_nw = Tile(blocked = True, chara = chr(160), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_se = Tile(blocked = True, chara = chr(158), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	cubicle_sw = Tile(blocked = True, chara = chr(159), color_front = lbc.dark_grey, color_back = lbc.grey, block_sight = True, name = "Cubicle Wall")
	
	
	
	def make_office():
		global random_x, random_y
		#here are some wall variables
		x_alt_l = map_width/2-2
		x_alt_2 = map_width/2+1
		x_main_1 = map_width/2-2
		x_main_2 = map_width/2+2
		y_alt_1 = map_height/2-2
		y_alt_2 = map_height/2+1
		y_main_1 = map_height/2-2
		y_main_2 = map_height/2+2
		
		if office_type == 1:
			#This is for when the main hallway is horizontal
			if x_or_y == 1:
				#This makes the doors for the hallway
				make_doors(left_wall, y_alt_1, left_wall, y_alt_2)
				make_doors(right_wall, y_alt_1, right_wall, y_alt_2)

				room1 = Rect(left_wall, random_y, x_alt_l, y_main_1)
				room2 = Rect(x_alt_2, random_y, right_wall, y_main_1)
				room3 = Rect(left_wall, y_main_2, x_alt_l, bottom_wall)
				room4 = Rect(x_alt_2, y_main_2, right_wall, bottom_wall)
				create_room(room1, floor = office_building_floor_tile, wall = office_building_wall_tile)
				create_room(room2, floor = office_building_floor_tile, wall = office_building_wall_tile)
				create_room(room3, floor = office_building_floor_tile, wall = office_building_wall_tile)
				create_room(room4, floor = office_building_floor_tile, wall = office_building_wall_tile)

				#This makes the doors in the main(horizontal) hallway walls
				door_ran = lbc.random_get_int(0, -3, 3)
				make_doors(map_width/4+3+door_ran, y_main_2, map_width/4+3+door_ran, y_main_2)
				make_doors(map_width/4+3+door_ran, y_main_1, map_width/4+3+door_ran, y_main_1)
				door_ran = lbc.random_get_int(0, -3, 3)
				make_doors(map_width/2+8+door_ran, y_main_2, map_width/2+8+door_ran, y_main_2)
				make_doors(map_width/2+8+door_ran, y_main_1, map_width/2+8+door_ran, y_main_1)
				#This makes the doors in the alternate(vertical) hallway walls
				door_ran = lbc.random_get_int(0, -3, 3)
				make_gen_tile(x_alt_2, map_height/4+3+door_ran, door_tile)
				make_gen_tile(x_alt_l, map_height/4+3+door_ran, door_tile)
				door_ran = lbc.random_get_int(0, -3, 3)
				make_gen_tile(x_alt_2, map_height/2+8+door_ran, door_tile)
				make_gen_tile(x_alt_l, map_height/2+8+door_ran, door_tile)
				
			#This is for when the main hallway is vertical
			if x_or_y == 2:
				#This makes the doors for the hallway
				make_doors(map_width/2-1, random_y, map_width/2+1, random_y)
				make_doors(map_width/2-1, bottom_wall, map_width/2+1, bottom_wall)
				#This makes the walls for the main hallway
				room1 = Rect(left_wall, top_wall, x_main_1, y_alt_1)
				room2 = Rect(x_main_2, top_wall, right_wall, y_alt_1)
				room3 = Rect(left_wall, y_alt_2, x_main_1, bottom_wall)
				room4 = Rect(x_main_2, y_alt_2, right_wall, bottom_wall)
				create_room(room1, floor = office_building_floor_tile, wall = office_building_wall_tile)
				create_room(room2, floor = office_building_floor_tile, wall = office_building_wall_tile)
				create_room(room3, floor = office_building_floor_tile, wall = office_building_wall_tile)
				create_room(room4, floor = office_building_floor_tile, wall = office_building_wall_tile)
				#This makes the doors in the main(vertical) hallway walls
				door_ran = lbc.random_get_int(0, -3, 3)
				make_gen_tile(x_main_2, map_height/4+3+door_ran, door_tile)
				make_gen_tile(x_main_1, map_height/4+3+door_ran, door_tile)
				door_ran = lbc.random_get_int(0, -3, 3)
				make_gen_tile(x_main_2, map_height/2+8+door_ran, door_tile)
				make_gen_tile(x_main_1, map_height/2+8+door_ran, door_tile)
				#This makes the doors in the alternate(horizontal) hallway walls
				door_ran = lbc.random_get_int(0, -3, 3)
				make_gen_tile(map_width/4+3+door_ran, y_alt_2, door_tile)
				make_gen_tile(map_width/4+3+door_ran, y_alt_1, door_tile)
				door_ran = lbc.random_get_int(0, -3, 3)
				make_gen_tile(map_width/2+8+door_ran, y_alt_2, door_tile)
				make_gen_tile(map_width/2+8+door_ran, y_alt_1, door_tile)
			#Cubicles
			rooms = [room1, room2, room3, room4]
			
			for room in rooms:
				place = 0
				cenx = room.center_x
				ceny = room.center_y
				for y in xrange(ceny - 2, ceny + 3):
					place = 0
					for x in xrange(cenx - 5, cenx + 5):
						if place == 0:
							map_map[x][y] = cubicle_none
						place += 1
						if place == 3:
							place = 0
				for x in xrange(cenx - 5, cenx + 5):
					map_map[x][ceny] = cubicle_none
			def check_align(x,y):
				global n,e,s,w
				n = False
				e = False
				s = False
				w = False
				t = "Cubicle Wall"
				def decide(n1, e1, s1, w1):
					global n,e,s,w
					if (map_map[x][y-1].name == t) == n1:
						if (map_map[x+1][y].name == t) == e1:
							if (map_map[x][y+1].name == t) == s1:
								if (map_map[x-1][y].name == t) == w1:
									return True
					else:
						return False
				if decide(False, False, False, False) == True:
					map_map[x][y] = cubicle_none
				elif decide(False, False, False, True) == True:
					map_map[x][y] = cubicle_horiz
				elif decide(False, False, True, False) == True:
					map_map[x][y] = cubicle_vert
				elif decide(False, True, False, False) == True:
					map_map[x][y] = cubicle_horiz
				elif decide(True, False, False, False) == True:
					map_map[x][y] = cubicle_vert
					
				elif decide(False, False, True, True) == True:
					map_map[x][y] = cubicle_sw
				elif decide(False, True, True, False) == True:
					map_map[x][y] = cubicle_se
				elif decide(True, True, False, False) == True:
					map_map[x][y] = cubicle_ne
				elif decide(True, False, False, True) == True:
					map_map[x][y] = cubicle_nw
					
				elif decide(True, False, True, False) == True:
					map_map[x][y] = cubicle_vert
				elif decide(False, True, False, True) == True:
					map_map[x][y] = cubicle_horiz
					
				elif decide(True, True, True, False) == True:
					map_map[x][y] = cubicle_vert_right
				elif decide(False, True, True, True) == True:
					map_map[x][y] = cubicle_horiz_down
				elif decide(True, False, True, True) == True:
					map_map[x][y] = cubicle_vert_left
				elif decide(True, True, False, True) == True:
					map_map[x][y] = cubicle_horiz_up
				
				elif decide(True, True, True, True) == True:
					map_map[x][y] = cubicle_all
			
			for x in xrange(0, map_width):
				for y in xrange(0, map_height):
					if map_map[x][y].name == "Cubicle Wall":
						check_align(x, y)
			
			

			
			
	def make_factory():
		
		x_or_y = 2
		x_or_y2 = 1
		l_or_r = lbc.random_get_int(0, 1, 2)
		num_piles = 2
		pos = 1
		workable_area_x = (map_width - random_x) - random_x
		workable_area_y = (map_height - random_y) - random_y
		
		#This makes the belts and the machinery
		if x_or_y2 == 1:
			while workable_area_y >= 9:
				workable_area_y -= 3
				pos = 1
				for x in xrange(random_x + 3, (map_width - random_x - 3)):
					if pos != 4:
						pos += 1
						map_map[x][map_height - random_y - workable_area_y + 3] = belt_tile
					elif pos == 4:
						pos = 1
						map_map[x][map_height - random_y - workable_area_y + 3] = machinery_tile
		#This makes an office
		corner = lbc.random_get_int(0, 1, 4)
		if corner == 1:
			for x in xrange(random_x, random_x + 6):
				map_map[x][random_y + 4] = office_building_wall_tile
			for y in xrange(random_y, random_y + 5):
				map_map[random_x+6][y] = office_building_wall_tile
			map_map[random_x+4][random_y+4] = door_tile
		if corner == 2:
			for x in xrange(map_width - random_x-6, map_width -  random_x):
				map_map[x][random_y + 4] = office_building_wall_tile
			for y in xrange(random_y, random_y+5):
				map_map[map_width - random_x-6][y] = office_building_wall_tile
			map_map[map_width - random_x-4][random_y+4] = door_tile
		if corner == 3:
			#This prevents door blockage
			for y in xrange(map_height - random_y - 7, map_height - random_y):
				for x in xrange(random_x+1, random_x + 9):
					map_map[x][y] = office_building_floor_tile
			for x in xrange(random_x, random_x + 6):
				map_map[x][map_height - random_y - 4] = office_building_wall_tile
			for y in xrange(map_height - random_y - 4, map_height - random_y):
				map_map[random_x+5][y] = office_building_wall_tile
			map_map[random_x + 3][map_height - random_y-4] = door_tile
		if corner == 4:
			#This prevents door blockage
			for y in xrange(map_height - random_y - 7, map_height - random_y):
				for x in xrange(map_width - random_x - 8, map_width - random_x):
					map_map[x][y] = office_building_floor_tile
			for y in xrange(map_height - random_y - 4, map_height - random_y):
				map_map[map_height - random_y-5][y] = office_building_wall_tile
			for x in xrange(map_width - random_y-6, map_width -  random_y):
				map_map[x][map_width - random_y - 6] = office_building_wall_tile
			map_map[map_width - random_x-4][map_height - random_y-4] = door_tile
		
		#This is for the goods piles
		while num_piles > 0:
			r_or_g = lbc.random_get_int(0, 1, 2)
			wall_pos = lbc.random_get_int(0, 20, 37)
			if x_or_y == 1:
				x_or_y = 2
			elif x_or_y == 2:
				x_or_y = 1
			if r_or_g == 2:
				r_or_g = 1
			elif r_or_g == 1:
				r_or_g = 2
			if x_or_y == 1:
				#Makes doors
				map_map[random_x][map_height/2-1] = door_tile
				map_map[random_x][map_height/2] = door_tile
				map_map[random_x][map_height/2+1] = door_tile
				map_map[map_width - random_x][map_height/2-1] = door_tile
				map_map[map_width - random_x][map_height/2] = door_tile
				map_map[map_width - random_x][map_height/2+1] = door_tile
				#This generates the piles of goods and supplies
				for y in xrange(wall_pos-4, wall_pos + 6):
					length = lbc.random_get_int(0, 2, 4)
					if l_or_r == 1:
						for x in xrange(random_x+1, random_x+1+length):
							if r_or_g == 1:
								map_map[x][y] = raw_mats_tile
							if r_or_g == 2:
								map_map[x][y] = goods_tile
						for x in xrange(random_x+1+length, random_x+1+6):
							if r_or_g == 1:
								map_map[x][y] = office_building_floor_tile
							if r_or_g == 2:
								map_map[x][y] = office_building_floor_tile
					if l_or_r == 2:
						for x in xrange(map_width - random_x-length, map_width - random_x):
							if r_or_g == 1:
								map_map[x][y] = raw_mats_tile
							if r_or_g == 2:
								map_map[x][y] = goods_tile
						for x in xrange(map_width - random_x-6, map_width - random_x-length):
							if r_or_g == 1:
								map_map[x][y] = office_building_floor_tile
							if r_or_g == 2:
								map_map[x][y] = office_building_floor_tile
				
				#Prevents door blockage
				for y in xrange(map_height/2-1, map_height/2+2):
					for x in xrange(random_x+1, map_width - random_x):
						map_map[x][y] = office_building_floor_tile
			if x_or_y == 2:
				#Makes doors
				map_map[map_width/2-1][random_y] = door_tile
				map_map[map_width/2][random_y] = door_tile
				map_map[map_width/2+1][random_y] = door_tile
				map_map[map_width/2-1][map_height - random_y] = door_tile
				map_map[map_width/2][map_height - random_y] = door_tile
				map_map[map_width/2+1][map_height - random_y] = door_tile
				#This generates the piles of goods and supplies
				for x in xrange(wall_pos-4, wall_pos + 6):
					length = lbc.random_get_int(0, 2, 4)
					if l_or_r == 1:
						for y in xrange(random_y+1, random_y+length+1):
							if r_or_g == 1:
								map_map[x][y] = raw_mats_tile
							if r_or_g == 2:
								map_map[x][y] = goods_tile
						for y in xrange(random_y+length+1, random_y+6+1):
							if r_or_g == 1:
								map_map[x][y] = office_building_floor_tile
							if r_or_g == 2:
								map_map[x][y] = office_building_floor_tile
					if l_or_r == 2:
						for y in xrange(map_height - random_y-length, map_height - random_y):
							if r_or_g == 1:
								map_map[x][y] = raw_mats_tile
							if r_or_g == 2:
								map_map[x][y] = goods_tile
						for y in xrange(map_height - random_y-6, map_height - random_y-length):
							if r_or_g == 1:
								map_map[x][y] = office_building_floor_tile
							if r_or_g == 2:
								map_map[x][y] = office_building_floor_tile
				#This prevents the doors from getting blocked
				for x in xrange(map_width/2-1, map_width/2+2):
					for y in xrange(random_y+1, map_height - random_y):
						map_map[x][y] = office_building_floor_tile
			num_piles = num_piles - 1
	def make_store():
		
		side = 1
		if side == 1:
			dist = random_x + 2
			dist2 = random_x + 1
			for x in xrange(random_x + 5, random_x + 7):
				map_map[x][random_y] = door_tile
			for x in xrange(map_width - random_x - 8, map_width - random_x - 6):
				map_map[x][random_y] = door_tile
			while dist < map_width - random_x - 8:
				dist += 4
				dist2 += 4
				for y in xrange(random_y+8 , map_height - 8 - random_y):
					map_map[dist][y] = shelf_tile
					map_map[dist2][y] = shelf_tile
				for y in xrange(random_y + 3, random_y + 6):
					map_map[dist][y] = shelf_tile
					map_map[dist2][y] = shelf_tile
				map_map[dist2][random_y+4] = office_building_floor_tile
				map_map[dist2][random_y+3] = office_building_floor_tile
				for y in xrange(map_height - random_y - 5, map_height - random_y - 3):
					map_map[dist][y] = shelf_tile
					map_map[dist2][y] = shelf_tile
			for y in xrange(random_y+4 , map_height - 4 - random_y):
				map_map[random_x + 1][y] = freezer_tile 
				map_map[map_width - random_x - 1][y] = freezer_tile
			for x in xrange(random_x + 4, map_width - random_x - 4):
				map_map[x][map_height - random_y - 1] = freezer_tile
	def make_apartments():
		chaosx = lbc.random_get_int(0, -1, 1)
		chaosy = lbc.random_get_int(0, -1, 1)
		#Horizontal
		x_or_y = 1
		if x_or_y == 1:
		#This makes the doors for the hallway
			make_doors(random_x, map_height/2-1, random_x, map_height/2+1)
			make_doors(map_width - random_x, map_height/2-1, map_width - random_x, map_height/2+1)
			#This makes the walls for the main hallway
			make_wall(random_x, map_height/2-2, x2 = map_height - random_x + 1, y2 = map_height/2-2)
			make_wall(random_x, map_height/2+2, x2 = map_height - random_x + 1, y2 = map_height/2+2)
			#Interior walls
			#Top
			make_wall(left_wall, top_wall + bldg_width/4  - 3+ chaosx, right_wall,'repeat')
			#Bottom
			make_wall(left_wall, top_wall + int(bldg_width/1.3) - chaosx, right_wall, 'repeat')
			
			for y in xrange(1, 4):
				make_wall(left_wall+(bldg_width*y)/3,top_wall, 'repeat', bottom_wall)
				make_gen_tile(left_wall+(bldg_width*y+1)/3 - (bldg_width)/6, map_height/2-2, door_tile)
				make_gen_tile(left_wall+(bldg_width*y+1)/3 - (bldg_width)/6, map_height/2+2, door_tile)
				#Interior walls
				make_wall(left_wall + int(bldg_width)*y/3 - 4 + chaosx, top_wall, 'repeat', top_wall + bldg_width/4  - 3+ chaosx)
				make_gen_tile(left_wall + int(bldg_width)*y/3 - 4 + chaosx, top_wall + 3, door_tile)
				
				make_wall(left_wall + int(bldg_width)*y/3 - 4 + chaosx, top_wall + int(bldg_width/1.3) - chaosx, 'repeat', bottom_wall)
				make_gen_tile(left_wall + int(bldg_width)*y/3 - 4 + chaosx, top_wall + int(bldg_width/1.3) - chaosx + 3, door_tile)
				make_gen_tile(left_wall + int(bldg_width)*y/3 - 7 + chaosx, top_wall + bldg_width/4  - 3+ chaosx, door_tile)
				make_gen_tile(left_wall + int(bldg_width)*y/3 - 7 + chaosx, top_wall + int(bldg_width/1.3) - chaosx, door_tile)
			make_floor(random_x+1, map_height/2-1, map_width - random_x-1, map_height/2+1)
		#Vertical
		if x_or_y == 2:
			#This makes the doors for the hallway
			make_doors(map_width/2-1, random_y, map_width/2+1, random_y)
			make_doors(map_width/2-1, map_height - random_y, map_width/2+1, map_height - random_y)
			#This makes the walls for the main hallway
			make_wall(map_width/2-2, random_y, map_width/2-2, map_width - random_y-2)
			make_wall(map_width/2+2, random_y, map_width/2+2, map_width - random_y-2)
			#This makes the interior walls
			#Left
			make_wall(left_wall + bldg_width/4 + chaosx, top_wall, 'repeat', bottom_wall)
			#Right
			make_wall(left_wall + int(bldg_width/1.3) + chaosx, top_wall, 'repeat', bottom_wall)
			for x in xrange(1, 4):
				make_wall(left_wall, top_wall+(bldg_height*x)/3, right_wall, 'repeat')
				#Entrance Doors
				make_gen_tile(map_width/2-2, top_wall+(bldg_height*x+1)/3 - (bldg_height)/6, door_tile)
				make_gen_tile(map_width/2+2, top_wall+(bldg_height*x+1)/3 - (bldg_height)/6, door_tile)
				#Interior interior walls
				make_wall(left_wall, top_wall+(bldg_height*(x-1))/3+4 + chaosy, left_wall + bldg_width/4 + chaosx, 'repeat')
				make_wall(left_wall + int(bldg_width/1.3) + chaosx, top_wall+(bldg_height*(x-1))/3+4 + chaosy, right_wall, 'repeat')
				#Interior Doors
				make_gen_tile(left_wall + bldg_width/4 + chaosx, top_wall+(bldg_height*(x-1))/3+6 + chaosy, door_tile)
				make_gen_tile(left_wall + int(bldg_width/1.3) + chaosx, top_wall+(bldg_height*(x-1))/3+6 + chaosy, door_tile)
				make_gen_tile(left_wall + 2, top_wall+(bldg_height*(x-1))/3+4 + chaosy, door_tile)
				make_gen_tile(right_wall - 2, top_wall+(bldg_height*(x-1))/3+4 + chaosy, door_tile)
			make_floor(map_width/2-1, random_y + 1, map_width/2+1, map_height - random_y-1)
			
	def make_warehouse():
		dist = random_x 
		dist2 = random_x -1
		map_map[map_width/2-1][random_y] = door_tile
		map_map[map_width/2][random_y] = door_tile
		map_map[map_width/2+1][random_y] = door_tile
		map_map[map_width/2-1][map_height - random_y] = door_tile
		map_map[map_width/2][map_height - random_y] = door_tile
		map_map[map_width/2+1][map_height - random_y] = door_tile
		while dist < map_width - random_x - 5:
				dist += 4
				dist2 += 4
				for y in xrange(random_y+2 , map_height - 2 - random_y):
					map_map[dist][y] = goods_tile
					map_map[dist2][y] = goods_tile

#Office
	if overmap.overmap_map[overmapx][overmapy].num == 10:
		make_sidewalk()
		pave_over()
		make_building()
		make_office()
		items.place_junk(tiles = [8,9])
#Factory
	if overmap.overmap_map[overmapx][overmapy].num == 14:
		pave_over()
		make_sidewalk()
		make_building()
		make_factory()
		items.place_junk(tiles = [8,9])
#Dock/Pier
	if overmap.overmap_map[overmapx][overmapy].num == 9:
		make_sidewalk()
		make_ocean()
		make_dock()
		items.place_junk(tiles = [8,9,11])
#Ocean
	if overmap.overmap_map[overmapx][overmapy].num == 3:
		make_sidewalk()
		make_ocean()
		items.place_junk(tiles = [8,9])
#Park
	if overmap.overmap_map[overmapx][overmapy].num == 7:
		make_park()
		make_big_trees()
		make_sidewalk()
		make_dirt_path()
		items.place_junk(tiles = [8,9,0,1])
#Scrap Yard
	if overmap.overmap_map[overmapx][overmapy].num == 8:
		make_sidewalk()
		make_scrap()
		make_scrap_heaps()
		make_dirt_path()
		make_chain_fence()
		items.place_junk(tiles = [8,9,0])

#Forest
	if overmap.overmap_map[overmapx][overmapy].num == 5:
		make_big_trees()
		items.place_junk(tiles = [0,1])
#Store
	if overmap.overmap_map[overmapx][overmapy].num == 15:
		pave_over()
		make_sidewalk()
		make_building()
		make_store()
		items.place_junk(tiles = [8,9])
#Rich Apartments
	if overmap.overmap_map[overmapx][overmapy].num == 13:
		pave_over()
		make_sidewalk()
		make_building()
		make_apartments()
		items.place_junk(tiles = [8,9])
#Warehouse
	if overmap.overmap_map[overmapx][overmapy].num == 11:
		pave_over()
		make_sidewalk()
		make_building()
		make_warehouse()
		items.place_junk(tiles = [8,9])
#Poor Apartments
	if overmap.overmap_map[overmapx][overmapy].num == 12:
		pave_over()
		make_sidewalk()
		make_building()
		make_apartments()
		items.place_junk(tiles = [8,9])
