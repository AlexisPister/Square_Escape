from Global import *


class Player:
	def __init__(self, col=RED, radius=int(WIDTH/40)):
		self.x = WIDTH/2
		self.y = HEIGHT/2
		self.color = col
		self.radius = radius
		
		
	def move(self, x, y):
		self.x = x
		self.y = y
	
	def draw(self, screen, alpha = 255):
		self.color.a = alpha
		#Draw the circle on surface
		self.surface = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA, 32)
		#pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius, 0)
		pygame.gfxdraw.aacircle(self.surface, self.radius, self.radius, self.radius-1, self.color)
		pygame.gfxdraw.filled_circle(self.surface, self.radius, self.radius, self.radius-1, self.color)
		#Draw the surface on screen
		screen.blit(self.surface, (self.x-self.radius, self.y-self.radius))
		
class Square:
	def __init__(self, col=BLUE):
		self.color = col
		self.width = WIDTH/20
		self.height = HEIGHT/20
		self.i = 0
		
		#Begin of trajectory
		rand = rn.randint(1,4)
		if rand == 1:
			x = -40
			y = rn.randint(1, HEIGHT)
		elif rand == 2:
			x = WIDTH + 40
			y = rn.randint(1, HEIGHT)
		elif rand == 3:
			x = rn.randint(1, WIDTH)
			y = -40
		elif rand == 4:
			x = rn.randint(1, WIDTH)
			y = HEIGHT + 40
			
		self.x = x
		self.y = y
			
		#End of trajectory
		choices = list(range(1,5))
		choices.remove(rand)
		rand2 = rn.choice(choices)
		
		if rand2 == 1:
			x = -20
			y = rn.randint(1, HEIGHT)
		elif rand2 == 2:
			x = WIDTH + 20
			y = rn.randint(1, HEIGHT)
		elif rand2 == 3:
			x = rn.randint(1, WIDTH)
			y = -20
		elif rand2 == 4:
			x = rn.randint(1, WIDTH)
			y = HEIGHT + 20
			
		self.x_end = x
		self.y_end = y
		
		#Difference of coordinates (=vector coordinates)
		self.Dx = self.x_end - self.x
		self.Dy = self.y_end - self.y
		
	def move(self):
		#One step of time
		dx = self.Dx / 100
		dy = self.Dy / 100
		#New posiion
		self.x = self.x + dx
		self.y = self.y + dy
		self. i += 1
	
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
		
		
		
		
class Game_handler:
	def __init__(self):
		self.object_list = []
		self.time_start = pygame.time.get_ticks()
		self.t0 = self.time_start
		self.t0_2 = self.time_start
		self.i = 0
		self.delay = DELAY[self.i]
		self.INV = False
		
	def update(self):
		t1 = pygame.time.get_ticks()
		#Baisse le delai entre chaque creation de square
		if self.delay > 50:
			if t1 - self.t0_2 > 500:
				self.i += 1
				self.delay = DELAY[self.i]
				self.t0_2 = pygame.time.get_ticks()
			
		#Cree un nouveau square si le temps passé est superieur au delai
		if t1 - self.t0 > self.delay:
			self.object_list.append(Square())
			self.t0 = pygame.time.get_ticks()
			
		#Refresh the coordinates and delete the out of screen squares
		for obj in self.object_list:
			if type(obj) == Square:
				if obj.i > 103:
					self.object_list.remove(obj)
				else :
					obj.move()
					
		t2 = pygame.time.get_ticks()
		if t2 - self.time_start > 20000:
			self.INV = True
				
		#print(self.delay)
		#print(len(self.object_list))
				
	def draw(self, screen):
		for obj in self.object_list:
			if type(obj) == Square:
				obj.draw(screen)



class Game:
	def __init__(self):
		#Initialization
		pygame.init()
		self.clock = pygame.time.Clock()
		pygame.display.set_caption(GAME_NAME) #title of screen
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32) #screen
		pygame.mouse.set_visible(False)
		#Fonts
		self.FONT = pygame.font.SysFont("monospace", 27) #Police des scores
		self.FONT2 = pygame.font.SysFont("freesans", 30) #Police des scores
		#Sounds
		self.music = pygame.mixer.music.load("Pygame01.mp3")
		pygame.mixer.music.play(-1)

		#Objects
		self.player = Player()
		self.alpha = 255 #transparency of player
		
		#time where invisibility start
		self.INV_time = 0
   
			
	##############
	#####MENU#####
	##############
	def events_menu(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			#Quitte le menu
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					self.main_loop()
	
	def display_menu(self):
		#Fond
		self.screen.fill(GRAY_BLUE)
		
		#Display the game title and text
		text_title = self.FONT2.render(GAME_NAME,1,RED)
		self.screen.blit(text_title,  (WIDTH/2 - text_title.get_width()/2, 4 * HEIGHT/20))
		text_enter = self.FONT2.render("Appuyer sur entrer pour jouer", 1, BLACK)
		self.screen.blit(text_enter,  (WIDTH/2 - text_enter.get_width()/2, 6 * HEIGHT/20))
		
		#Display the highest scores
		hght = 11
		for score in HIGH_SCORES:
			text_score = self.FONT.render(str(score),1,BLACK)
			self.screen.blit(text_score, (WIDTH/2 - text_score.get_width()/2, hght * HEIGHT/20))
			hght += 1
			
		pygame.display.flip()
		
	def menu_loop(self):
		while True:
			self.events_menu()
			self.display_menu()
	
	##############
	#####MAIN#####
	##############
	def update_main(self):
		#Move the player
		x, y = pygame.mouse.get_pos()
		self.player.move(x, y)
		#Move objetcs
		self.Game_handler.update()
		
		#Detect if collision
		for rect in self.Game_handler.object_list:
			if type(rect == Square):
				if collision(x, y, self.player.radius, rect.x, rect.y, rect.width, rect.height):
					self.game_over()
	
	
	def events_main(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == SCOREEVENT:
				self.score +=10
			
			if event.type == INVEVENT:
				self.INV_time = pygame.time.get_ticks()
				
	
	def display_main(self):
		#Fond
		self.screen.fill(GRAY_BLUE)
		#Player
		t1 = pygame.time.get_ticks()
		if t1 - self.INV_time < 1500:
			self.player.draw(self.screen, self.alpha)
			self.alpha -= 25
			if self.alpha < 0:
				self.alpha = 0
		else:
			self.alpha = 255
			self.player.draw(self.screen, alpha = 255)
			
		
		
		#objects
		self.Game_handler.draw(self.screen)
		#Score
		TEXT_SCORE = self.FONT.render(str(self.score),1,BLACK)
		self.screen.blit(TEXT_SCORE, (11 * WIDTH/13, HEIGHT/40))
		#Refresh
		pygame.display.flip()
		
	def game_over(self):
		global HIGH_SCORES
		#Rajoute le score dans la liste si il est assez grand
		if self.score > min(HIGH_SCORES):
			HIGH_SCORES.append(self.score)
			HIGH_SCORES.sort(reverse=True)
			HIGH_SCORES = HIGH_SCORES[:-1]
		with open(path_Scores, 'w') as f:
			f.write(str(HIGH_SCORES))
		self.menu_loop()
		
	
	def main_loop(self):
		#Initialization of the main loop screen
		self.Game_handler = Game_handler()
		self.score = 0
		pygame.time.set_timer(INVEVENT, 0)
		pygame.time.set_timer(SCOREEVENT, 1000)
		a = 0
		
		#loop
		while True:
			#Start the invisible event
			if a == 0 and self.Game_handler.INV == True:
				pygame.time.set_timer(INVEVENT, 10000)
				a = 1
				
			self.clock.tick(60) #Never more that 60 frames per second
			self.update_main()
			self.events_main()
			self.display_main()


if __name__ == '__main__':
	game = Game()
	game.menu_loop()
	
	
