import pygame, sys
from settings import *
from level import Level
from button import Button

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		# set title
		pygame.display.set_caption('RPG_Game_Pog')
		# set icon
		new_icon = pygame.image.load("../graphics/overlay/axe.png")
		pygame.display.set_icon(new_icon)

		self.font = pygame.font.Font(None, 36)
		self.play_flag = False
		self.intro_flag = True

		self.clock = pygame.time.Clock()
		self.level = Level()

	def intro(self):
		self.screen.fill((140,140,220))
		text = self.font.render("Press PLAY to start", True, 'White')
		text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
		self.screen.blit(text, text_rect)

		# Intro buttons
		start_img = pygame.image.load('../graphics/buttons/play.png').convert_alpha()
		exit_img = pygame.image.load('../graphics/buttons/quit.png').convert_alpha()
		button_scaling = 3
		button_x = SCREEN_WIDTH//2 - (button_scaling*32)
		start_button = Button(button_x, 200, start_img, button_scaling)
		exit_button = Button(button_x, 400, exit_img, button_scaling)

		# intro button interactions
		if start_button.draw(self.screen):
			self.play_flag = True
			self.intro_flag = False
		if exit_button.draw(self.screen):
			pygame.quit()
			sys.exit()

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	def run(self):
		while True:
			# intro call
			if self.intro_flag:
				self.intro()

			# game loop
			elif self.play_flag:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				dt = self.clock.tick() / 1000
				self.level.run(dt)
				pygame.display.update()

if __name__ == '__main__':
	# Game Init
	game = Game()
	# Game Loop
	game.run()
