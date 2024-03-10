import pygame
from pygame import mixer
import csv
import button
from Setting import*
from Bullet import Bullet
from Decoration import Decoration
from Exit import Exit
from Explosion import Explosion
from Grenade import Grenade
from HealthBar import HealthBar
from ItemBox import ItemBox
from ScreenFade import ScreenFade
from Soldier import Soldier
from Water import Water
from World import World

mixer.init()
pygame.init()



#function to reset level
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)
	return data



#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)


#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 180, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 60, exit_img, 1)
choose_player = button.Button(SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 + 50, choose_img, 2)
choose_player2 = button.Button(SCREEN_WIDTH - 245, 30, choose_img, 0.8)

frog_btn = button.Button(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 60, frog_icon, 2)
guy_btn = button.Button(SCREEN_WIDTH // 2 + 160, SCREEN_HEIGHT // 2 - 160, guy_icon, 2)
player_btn = button.Button(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 160, player_icon, 2)
mask_btn = button.Button(SCREEN_WIDTH // 2 + 160, SCREEN_HEIGHT // 2 + 60, mask_icon, 2)

restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

loa_btn = button.Button(SCREEN_WIDTH - 80, 30, loa_img, 1)

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data, water_group, decoration_group, enemy_group, item_box_group, exit_group, main_Character)

def choose_maincr():
	global chse_player, player, main_Character
	dx, dy = player.rect.x, player.rect.y
	screen.fill(BG)
	if frog_btn.draw(screen):
		main_Character = 'NinjaFrog'
		player = Soldier('NinjaFrog', dx, dy, 1.65, 5, 20, 5)
		chse_player = False
	if guy_btn.draw(screen):
		main_Character = 'VirtualGuy'
		player = Soldier('VirtualGuy', dx, dy, 1.65, 5, 20, 5)
		chse_player = False
	if player_btn.draw(screen):
		main_Character = 'player'
		player = Soldier('player', dx, dy, 1.65, 5, 20, 5)
		chse_player = False
	if mask_btn.draw(screen):
		main_Character = 'MaskDude'
		player = Soldier('MaskDude', dx, dy, 1.65, 5, 20, 5)
		chse_player = False
	draw_text('SIEU NHAN CUONG', font3, PINK, 160, 250)
	draw_text('PHONG', font3, PINK, 230, 280)

	draw_text('CHU ECH NHI NHANH', font3, PINK, 160, 470)
	draw_text('Tho Dan Than Thien', font3, PINK, 480, 470)
	draw_text('Chien', font3, PINK, 570, 500)
	draw_text('Shin cau be but chi', font3, PINK, 480, 250)


run = True
while run:
	clock.tick(FPS)

	if chse_player == True:
		choose_maincr()
	else:
		if start_game == False:
			#draw menu
			screen.fill(BG)

			if chse_player == False:
				#add buttons
				if start_button.draw(screen):
					start_game = True
					start_intro = True
				if exit_button.draw(screen):
					run = False
				if choose_player.draw(screen):
					chse_player = True
		else:
			#update background
			draw_bg()
			#draw world map
			world.draw(screen, screen_scroll )
			#show player health
			health_bar.draw(screen, player.health)
			#show ammo
			draw_text('AMMO: ', font, WHITE, 10, 35)
			for x in range(player.ammo):
				screen.blit(bullet_img, (90 + (x * 10), 40))
			#show grenades
			draw_text('GRENADES: ', font, WHITE, 10, 60)
			for x in range(player.grenades):
				screen.blit(grenade_img, (135 + (x * 15), 60))


			player.update()
			player.draw(screen)
			if choose_player2.draw(screen):
					chse_player = True

			for enemy in enemy_group:
				enemy.ai(player, world, water_group, exit_group, screen_scroll, bg_scroll, bullet_group)
				enemy.update()
				enemy.draw(screen)

			#update and draw groups
			bullet_group.update(world, player, bullet_group, enemy_group, screen_scroll)
			grenade_group.update(world, explosion_group, player, enemy_group, screen_scroll)
			explosion_group.update(screen_scroll)
			item_box_group.update(player, screen_scroll)
			decoration_group.update(screen_scroll)
			water_group.update(screen_scroll)
			exit_group.update(screen_scroll)
			bullet_group.draw(screen)
			grenade_group.draw(screen)
			explosion_group.draw(screen)
			item_box_group.draw(screen)
			decoration_group.draw(screen)
			water_group.draw(screen)
			exit_group.draw(screen)

			#show intro
			if start_intro == True:
				if intro_fade.fade(screen):
					start_intro = False
					intro_fade.fade_counter = 0


			#update player actions
			if player.alive:
				#shoot bullets
				if shoot:
					player.shoot(bullet_group)
				#throw grenades
				elif grenade and grenade_thrown == False and player.grenades > 0:
					grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
								player.rect.top, player.direction)
					grenade_group.add(grenade)
					#reduce grenades
					player.grenades -= 1
					grenade_thrown = True
				if player.in_air:
					player.update_action(2)#2: jump
				elif moving_left or moving_right:
					player.update_action(1)#1: run
				else:
					player.update_action(0)#0: idle
				screen_scroll, level_complete = player.move(moving_left, moving_right, world, water_group, exit_group, bg_scroll, enemy_group)
				bg_scroll -= screen_scroll
				#check if player has completed the level
				if level_complete:
					start_intro = True
					level += 1
					bg_scroll = 0
					world_data = reset_level()
					if level <= MAX_LEVELS:
						#load in level data and create world
						with open(f'level{level}_data.csv', newline='') as csvfile:
							reader = csv.reader(csvfile, delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y] = int(tile)
						world = World()
						player, health_bar = world.process_data(world_data, water_group, decoration_group, enemy_group, item_box_group, exit_group, main_Character)
			else:
				screen_scroll = 0
				if death_fade.fade(screen):
					if restart_button.draw(screen):
						death_fade.fade_counter = 0
						start_intro = True
						bg_scroll = 0
						world_data = reset_level()
						#load in level data and create world
						with open(f'level{level}_data.csv', newline='') as csvfile:
							reader = csv.reader(csvfile, delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y] = int(tile)
						print(main_Character)
						world = World()
						player, health_bar = world.process_data(world_data, water_group, decoration_group, enemy_group, item_box_group, exit_group, main_Character)
						
	# turn on/off the music
	if is_playing_msc == True:
		if loa_btn.draw(screen):
			pygame.mixer.music.stop()
			is_playing_msc = False
	else:
		if loa_btn.draw(screen):
			pygame.mixer.music.play(-1, 0.0, 5000)
			is_playing_msc = True

	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_DOWN:
				grenade = True
			if event.key == pygame.K_UP and player.alive:
				player.jump = True
				jump_fx.play()
			if event.key == pygame.K_ESCAPE:
				run = False


		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False
			if event.key == pygame.K_DOWN:
				grenade = False
				grenade_thrown = False


	pygame.display.update()

pygame.quit()