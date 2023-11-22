from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 128

# overlay positions
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
	'seed': (100, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-20,20),
	'right': Vector2(20,20),
	'up': Vector2(0,-20),
	'down': Vector2(0,20)
}

LAYERS = {
	'water': 0,
    'water anim': 1,
	'ground': 2,
    'soil': 3,
	'soil water': 4,
	'rocks': 5,
	'rain floor': 6,
	'house bottom': 7,
	'ground_plant': 8,
    'trees': 9,
    'main': 10,
    'ground plant front': 11,
    'trees front': 12,
	'house top': 13,
	'fruit': 14,
	'rain drops': 15
}

FRUIT_POS = {
	'Apple': [(20,20), (15,50), (35,65), (84, 44), (70, 23), (64, 64)],
    'Peach': [(1,1)],
	'Birch': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}
