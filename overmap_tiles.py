import libtcodpy as lbc 
import libtcodpy as libtcod
import math

screen_width = 100
screen_height = 65
overmap_width = 57
overmap_height = 55
lbc.console_set_custom_font('prestige12x12_gs_tc.png', lbc.FONT_TYPE_GREYSCALE | lbc.FONT_LAYOUT_TCOD)
libtcod.console_init_root(screen_width, screen_height, 'overmap testing', False)

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

class Overmap_Tile:
	def __init__(self, chara = 'X', color_front = color_missing, color_back = color_missing):
		self.color_back = color_back
		self.color_front = color_front
		self.chara = chara
Overmap_Tile_missing = Overmap_Tile()
Overmap_Tile_office_building = Overmap_Tile(chara = '#', color_front = color_office_building, color_back = lbc.black)
Overmap_Tile_water = Overmap_Tile(chara = '~', color_front = color_water_front, color_back = color_water_back)
Overmap_Tile_asphalt_lot = Overmap_Tile(chara = chr(176), color_front = color_street, color_back = lbc.dark_grey)
Overmap_Tile_pier = Overmap_Tile(chara = '+', color_front = color_pier, color_back = lbc.darker_blue)
Overmap_Tile_warehouse = Overmap_Tile(chara = 'X', color_front = color_warehouse, color_back = lbc.black)
Overmap_Tile_apartments_rich = Overmap_Tile(chara = '0', color_front = color_apartments_rich, color_back = lbc.black)
Overmap_Tile_park = Overmap_Tile(chara = '%', color_front = color_park, color_back = lbc.black)
Overmap_Tile_scrap_heap = Overmap_Tile(chara = '*', color_front = color_scrap_heap, color_back = lbc.black)
Overmap_Tile_factory = Overmap_Tile('&', color_front = color_factory, color_back = lbc.black)
Overmap_Tile_apartments_poor = Overmap_Tile('0', color_front = color_apartments_poor, color_back = lbc.black)
Overmap_Tile_stores = Overmap_Tile('#', color_front = color_stores, color_back = lbc.black)
Overmap_Tile_forest = Overmap_Tile('1', color_front = lbc.dark_green, color_back = lbc.black)
Overmap_Tile_field = Overmap_Tile('.', color_front = lbc.dark_green, color_back = lbc.black)
def handle_keys():

	key = libtcod.console_wait_for_keypress(True)  #turn-based

	if key.vk == libtcod.KEY_ESCAPE:
		return True  #exit game

def make_overmap():
	global map, district_diameter
	x1 = 0
	y1 = 0
	x2 = 1
	y2 = 0
	watery = 0
	piery = 0
	warehousey = 0
	map = [[ Overmap_Tile_asphalt_lot
		for y in xrange(overmap_height) ]
			for x in xrange(overmap_width) ]
#Make the street layout
	district_num = int(overmap_width * overmap_height)
	forest_num = int(overmap_width * overmap_height/750)
	while x1 <= overmap_height-8:
		map[x1][y1] = Overmap_Tile_asphalt_lot
		x1 = x1 + 2
	while x2 <= overmap_height-8:
		map[x2][y1] = Overmap_Tile_asphalt_lot
		x2 = x2 + 2
	while district_num > 0:
		district_diameter = lbc.random_get_int(0, 1, 2)
		district_x = lbc.random_get_int(0, 0, overmap_width)
		district_y = lbc.random_get_int(0, 0, overmap_height)
		district_num = district_num - 1
		Overmap_Tile_num = lbc.random_get_int(0, 1, 32)
		if Overmap_Tile_num == 1:
			Overmap_Tile_choice = Overmap_Tile_office_building
		if Overmap_Tile_num == 2:
			Overmap_Tile_choice = Overmap_Tile_office_building
		if Overmap_Tile_num == 3:
			Overmap_Tile_choice = Overmap_Tile_office_building
		if Overmap_Tile_num == 4:
			Overmap_Tile_choice = Overmap_Tile_office_building
		if Overmap_Tile_num == 5:
			Overmap_Tile_choice = Overmap_Tile_office_building
		if Overmap_Tile_num == 6:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 7:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 8:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 9:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 10:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 11:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 12:
			Overmap_Tile_choice = Overmap_Tile_factory
		if Overmap_Tile_num == 13:
			Overmap_Tile_choice = Overmap_Tile_warehouse
		if Overmap_Tile_num == 14:
			Overmap_Tile_choice = Overmap_Tile_warehouse
		if Overmap_Tile_num == 15:
			Overmap_Tile_choice = Overmap_Tile_apartments_rich
		if Overmap_Tile_num == 16:
			Overmap_Tile_choice = Overmap_Tile_apartments_rich
		if Overmap_Tile_num == 17:
			Overmap_Tile_choice = Overmap_Tile_park
		if Overmap_Tile_num == 18:
			Overmap_Tile_choice = Overmap_Tile_park
		if Overmap_Tile_num == 19:
			Overmap_Tile_choice = Overmap_Tile_park
		if Overmap_Tile_num == 20:
			Overmap_Tile_choice = Overmap_Tile_scrap_heap
		if Overmap_Tile_num == 21:
			Overmap_Tile_choice = Overmap_Tile_scrap_heap
		if Overmap_Tile_num == 22:
			Overmap_Tile_choice = Overmap_Tile_scrap_heap
		if Overmap_Tile_num == 23:
			Overmap_Tile_choice = Overmap_Tile_scrap_heap
		if Overmap_Tile_num == 24:
			Overmap_Tile_choice = Overmap_Tile_scrap_heap
		if Overmap_Tile_num == 25:
			Overmap_Tile_choice = Overmap_Tile_apartments_poor
		if Overmap_Tile_num == 26:
			Overmap_Tile_choice = Overmap_Tile_apartments_poor
		if Overmap_Tile_num == 27:
			Overmap_Tile_choice = Overmap_Tile_apartments_poor
		if Overmap_Tile_num == 28:
			Overmap_Tile_choice = Overmap_Tile_apartments_poor
		if Overmap_Tile_num == 29:
			Overmap_Tile_choice = Overmap_Tile_apartments_poor
		if Overmap_Tile_num == 30:
			Overmap_Tile_choice = Overmap_Tile_stores
		if Overmap_Tile_num == 31:
			Overmap_Tile_choice = Overmap_Tile_stores
		if Overmap_Tile_num == 32:
			Overmap_Tile_choice = Overmap_Tile_stores
		for x in range(district_x - district_diameter, district_x + district_diameter):
			for y in range(district_y - district_diameter, district_y + district_diameter):
				if x <= overmap_width-1:
					if y <= overmap_height-1:
						if y >= 0:
							if x >= 0:
								map[x][y] = Overmap_Tile_choice
	while forest_num > 0:
		forest_diameter = lbc.random_get_int(0, 3, 5)
		forest_x = lbc.random_get_int(0, 0, overmap_width)
		forest_y = lbc.random_get_int(0, 0, overmap_height)
		forest_num = forest_num - 1

		for x in range(forest_x - forest_diameter, forest_x + forest_diameter):
			for y in range(forest_y - forest_diameter, forest_y + forest_diameter):
				if x <= overmap_width-2:
					if y <= overmap_height-2:
						if y >= 1:
							if x >= 1:
								forest_or_field = lbc.random_get_int(0, 1, 5)
								chaosx = lbc.random_get_int(0, -1, 1)
								chaosy = lbc.random_get_int(0, -1, 1)
								if forest_or_field != 5:
									map[x][y] = Overmap_Tile_forest
									map[x+chaosx][y+chaosy] = Overmap_Tile_forest
								elif forest_or_field == 5:
									map[x][y] = Overmap_Tile_field
									map[x+chaosx][y+chaosy] = Overmap_Tile_field
	while piery <= overmap_height-1:
		pierx = overmap_width - 6
		for x in xrange(pierx, overmap_width-5):
			map[x][piery] = Overmap_Tile_pier
		piery = piery + 1
	while warehousey <= overmap_height-1:
		warehousex = lbc.random_get_int(0, overmap_width - 8, overmap_width - 7)
		for x in xrange(warehousex, overmap_width-6):
			map[x][warehousey] = Overmap_Tile_warehouse
		warehousey = warehousey + 1
	while watery <= overmap_height-1:
		waterx = lbc.random_get_int(0, overmap_width - 6, overmap_width - 5)
		for x in xrange(waterx, overmap_width):
			map[x][watery] = Overmap_Tile_water
		watery = watery + 1
	

def render_all():
	global map
	for y in xrange(overmap_height):
		for x in xrange(overmap_width):
			lbc.console_set_fore(0, x, y, map[x][y].color_front)
			lbc.console_set_back(0, x, y, map[x][y].color_back)
			lbc.console_set_char(0, x, y, map[x][y].chara)

make_overmap()
while not libtcod.console_is_window_closed():
	render_all()
	libtcod.console_flush()
	exit = handle_keys()
	if exit:
		break