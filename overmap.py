import libtcodpy as lbc 
import libtcodpy as libtcod
import math

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

overmap_width = 58
overmap_height = 56

abandoned_map = []


noise = libtcod.noise_new(2, lbc.random_get_int(0, 0, 999999))

class Overmap_Tile:
	def __init__(self, chara = 'X', color_front = color_missing, color_back = color_missing, num = 0, occupy = False, empty = True):
		self.color_back = color_back
		self.color_front = color_front
		self.chara = chara
		self.num = num
		self.occupy = occupy
		self.empty = empty
		if occupy is True:
			self.empty = False


Overmap_Tile_missing = Overmap_Tile()
Overmap_Tile_blank = Overmap_Tile(' ', color_front = None, color_back = None, num = 1)
Overmap_Tile_abandoned = Overmap_Tile(' ', color_front = lbc.grey, color_back = None, num = 2)
Overmap_Tile_water = Overmap_Tile(chara = '~', color_front = color_water_front, color_back = color_water_back, num = 3) #Done
Overmap_Tile_field = Overmap_Tile('.', color_front = lbc.dark_green, color_back = lbc.black, num = 4) #Done
Overmap_Tile_forest = Overmap_Tile('1', color_front = lbc.dark_green, color_back = lbc.black, num = 5) #Done
Overmap_Tile_asphalt_lot = Overmap_Tile(chara = chr(176), color_front = color_street, color_back = lbc.dark_grey, num = 6, empty = False) 
Overmap_Tile_park = Overmap_Tile(chara = '%', color_front = color_park, color_back = lbc.black, num = 7, occupy = True, empty = False) #Done
Overmap_Tile_scrap_heap = Overmap_Tile(chara = '*', color_front = color_scrap_heap, color_back = lbc.black, num = 8, empty = False) #Done
Overmap_Tile_pier = Overmap_Tile(chara = '+', color_front = color_pier, color_back = lbc.darker_blue, num = 9, empty = False) #Done
Overmap_Tile_office_building = Overmap_Tile(chara = '#', color_front = color_office_building, color_back = lbc.black, num = 10, occupy = True) #Done (for now)
Overmap_Tile_warehouse = Overmap_Tile(chara = 'X', color_front = color_warehouse, color_back = lbc.black, num = 11, occupy = True) #Done (for now)
Overmap_Tile_apartments_rich = Overmap_Tile(chara = '0', color_front = color_apartments_rich, color_back = lbc.black, num = 12, occupy = True) #Done (for now)
Overmap_Tile_apartments_poor = Overmap_Tile('0', color_front = color_apartments_poor, color_back = lbc.black, num = 13, occupy = True) #Done (for now)
Overmap_Tile_factory = Overmap_Tile('&', color_front = color_factory, color_back = lbc.black, num = 14, occupy = True) #Done
Overmap_Tile_stores = Overmap_Tile('#', color_front = color_stores, color_back = lbc.black, num = 15, occupy = True) #1 of 4 sides done






def make_overmap():
	global overmap_map, district_diameter, abandoned_map
	
	x1 = 0
	y1 = 0
	x2 = 1
	y2 = 0
	perx = 0
	pery = 0
	watery = 0
	piery = 0
	warehousey = 0
	overmap_map = [[ Overmap_Tile_missing
		for y in xrange(overmap_height) ]
			for x in xrange(overmap_width) ]
	abandoned_map = [[False
		for y in xrange(overmap_height) ]
			for x in xrange(overmap_width) ]
#Make the street layout
	district_num = int(overmap_width * overmap_height)
	forest_num = int(overmap_width * overmap_height/750)
	while district_num > 0:
		district_diameter = lbc.random_get_int(0, 1, 2)
		district_x = lbc.random_get_int(0, 0, overmap_width)
		district_y = lbc.random_get_int(0, 0, overmap_height)
		district_num = district_num - 1
		Overmap_Tile_num = lbc.random_get_int(0, 1, 35)
		if Overmap_Tile_num <= 5:
			Overmap_Tile_choice = Overmap_Tile_office_building
		elif Overmap_Tile_num <= 12:
			Overmap_Tile_choice = Overmap_Tile_factory
		elif Overmap_Tile_num <= 14:
			Overmap_Tile_choice = Overmap_Tile_warehouse
		elif Overmap_Tile_num <= 17:
			Overmap_Tile_choice = Overmap_Tile_apartments_rich
		elif Overmap_Tile_num <= 22:
			Overmap_Tile_choice = Overmap_Tile_scrap_heap
		elif Overmap_Tile_num <= 29:
			Overmap_Tile_choice = Overmap_Tile_apartments_poor
		elif Overmap_Tile_num <= 32:
			Overmap_Tile_choice = Overmap_Tile_stores
		elif Overmap_Tile_num <= 35:
			Overmap_Tile_choice = Overmap_Tile_park
		for x in xrange(district_x - district_diameter, district_x + district_diameter):
			for y in xrange(district_y - district_diameter, district_y + district_diameter):
				perx = float(float(x)/float(overmap_width))*100
				pery = float(float(y)/float(overmap_height))*100
				if x <= overmap_width-1:
					if y <= overmap_height-1:
						if y >= 0:
							if x >= 0:
								if libtcod.noise_fbm_simplex(noise,[perx, pery], 4.0) > 0:
									overmap_map[x][y] = Overmap_Tile_choice
									abandoned_map[x][y] = True
								elif libtcod.noise_fbm_simplex(noise,[perx, pery], 4.0) <= 0:
									overmap_map[x][y] = Overmap_Tile_choice
	while forest_num > 0:
		forest_diameter = lbc.random_get_int(0, 3, 5)
		forest_x = lbc.random_get_int(0, 0, overmap_width)
		forest_y = lbc.random_get_int(0, 0, overmap_height)
		forest_num = forest_num - 1

		for x in xrange(forest_x - forest_diameter, forest_x + forest_diameter):
			for y in xrange(forest_y - forest_diameter, forest_y + forest_diameter):
				if x <= overmap_width-2:
					if y <= overmap_height-2:
						if y >= 1:
							if x >= 1:
								forest_or_field = lbc.random_get_int(0, 1, 5)
								chaosx = lbc.random_get_int(0, -1, 1)
								chaosy = lbc.random_get_int(0, -1, 1)
								if forest_or_field != 5:
									overmap_map[x][y] = Overmap_Tile_forest
									overmap_map[x+chaosx][y+chaosy] = Overmap_Tile_forest
									abandoned_map[x][y] = False
									abandoned_map[x+chaosx][y+chaosy] = False
								elif forest_or_field == 5:
									overmap_map[x][y] = Overmap_Tile_field
									overmap_map[x+chaosx][y+chaosy] = Overmap_Tile_field
									abandoned_map[x][y] = False
									abandoned_map[x+chaosx][y+chaosy] = False
	while piery <= overmap_height-1:
		pierx = overmap_width - 6
		for x in xrange(pierx, overmap_width-5):
			overmap_map[x][piery] = Overmap_Tile_pier
			abandoned_map[x][piery] = False
		piery = piery + 1
	while warehousey <= overmap_height-1:
		warehousex = lbc.random_get_int(0, overmap_width - 8, overmap_width - 7)
		for x in xrange(warehousex, overmap_width-6):
			if libtcod.noise_fbm_simplex(noise,[x,warehousey], 4.0) <= 0:
				overmap_map[x][warehousey] = Overmap_Tile_warehouse
				abandoned_map[x][warehousey] = False
			elif libtcod.noise_fbm_simplex(noise,[x,warehousey], 4.0) > 0:
				overmap_map[x][warehousey] = Overmap_Tile_warehouse
				abandoned_map[x][warehousey] = Overmap_Tile_abandoned
		warehousey = warehousey + 1
	while watery <= overmap_height-1:
		waterx = lbc.random_get_int(0, overmap_width - 6, overmap_width - 5)
		for x in xrange(waterx, overmap_width):
			overmap_map[x][watery] = Overmap_Tile_water
			abandoned_map[x][watery] = False
		watery = watery + 1