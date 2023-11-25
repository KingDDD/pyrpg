import pygame, sys
from settings import *
from level import Level

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
		self.screen.fill('Black')
		text = self.font.render("Press SPACE to start", True, 'White')
		text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
		self.screen.blit(text, text_rect)

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.play_flag = True
				self.intro_flag = False

	def run(self):
		while True:
			if self.intro_flag:
				self.intro()
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
