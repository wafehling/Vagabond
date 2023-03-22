import libtcodpy as lbc 
import libtcodpy as libtcod
import joblists
import overmap
import objects
import map
import items
import objects
import con_info

ann_dialog = []

class Peaceful_outside:
	#Just minding their own buisness
	def take_turn(self):
		global ann_dialog
		monster = self.owner
		#All dialog stuff
		dialog = lbc.random_get_int(0, 1, 75)
		pre = ('The ' + self.owner.name + ' says ')
		if lbc.map_is_in_fov(map.fov_map, monster.x, monster.y):
			if dialog == 1:
				ann_dialog.append(pre + '"Man, I am so late..."')
			if dialog == 2:
				ann_dialog.append(pre + '"Ugh..."')
			if dialog == 3:
				ann_dialog.append(pre + '"Stay away from me."')
			if dialog == 4:
				ann_dialog.append(pre + '"Saying 4"')
			if dialog == 5:
				ann_dialog.append(pre + '"Saying 5"')
			if dialog == 6:
				ann_dialog.append(pre + '"Saying 6"')
		self_pos = map.map_map[self.x][self.y]
class Robbed:
	#Agreesive AI
	def take_turn(self):
		global ann_dialog
		monster = self.owner
		if lbc.map_is_in_fov(map.fov_map, monster.x, monster.y):
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
	player.color_front = lbc.dark_red	

def monster_death(monster):
	ann_combatdeath.append(monster.name.capitalize() + ' is dead!')
	monster.char = '%'
	monster.color_front = lbc.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = monster.name + " corpse"
	monster.send_to_back()



def place_npcs(overmapx, overmapy):
	#choose random number of monsters
	jobs = [joblists.beggar, joblists.thief, joblists.day_laborer, joblists.business_worker, joblists.construction_worker, joblists.punk, joblists.gang_member, joblists.transient, joblists.bank_teller, joblists.retail_worker, joblists.shop_owner, joblists.janitor]
	job = libtcod.random_get_int(0, 0, len(jobs)-1)
	active_job = jobs[job]
	job_name = active_job[0]
	job_color = active_job[1]
	if overmap.overmap_map[overmapx][overmapy].empty == False:
		#create a person
		ai_person = Peaceful_outside()
		person_power = lbc.random_get_int(0, 1, 4)
		person_defense = lbc.random_get_int(0, 1, 4)
		person_spee = lbc.random_get_int(0, 75, 105)
		person_speed = float(person_spee)/100
		fighter_person = Fighter(body = "body_def", hp = 10, defense = person_defense, power = person_power, speed = person_speed, death_function=monster_death)
		q = 0
		while q == 0:
			x = lbc.random_get_int(0, 1, map.map_width - 1)
			y = lbc.random_get_int(0, 1, map.map_height - 1)

			if map.map_map[x][y].name == "Street" or map.map_map[x][y].name == "Sidewalk" or map.map_map[x][y].name == "Grass" or map.map_map[x][y].name == "Dirt":
				q = 1
			
		NPC = items.Object(x, y, 'H', job_name, job_color, blocks=True, fighter=fighter_person, ai=ai_person)
		items.objects_list.append(NPC)
