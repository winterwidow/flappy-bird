# import modules
import os
from pathlib import Path
import random 
import sys 
import pygame 
from pygame.locals import *

# Global Variables for the game 
window_width = 600
window_height = 499

# set height and width of window 
window = pygame.display.set_mode((window_width, window_height)) 
elevation = window_height * 0.8
game_images = {}	 
framepersecond = 32

#load images
pipeimage = Path('C:/Users/naija/Coding/flappy-bird/images/pipe.png')
background_image = 'C:/Users/naija/Coding/flappy-bird/images/background.jpg'
birdplayer_image = 'C:/Users/naija/Coding/flappy-bird/images/bird.png'
sealevel_image = 'C:/Users/naija/Coding/flappy-bird/images/base.jfif'

#load score images

zero=Path('C:/Users/naija/Coding/flappy-bird/images/0.png')
one=Path('C:/Users/naija/Coding/flappy-bird/images/1.png')
two=Path('C:/Users/naija/Coding/flappy-bird/images/2.png')
three=Path('C:/Users/naija/Coding/flappy-bird/images/3.png')
four=Path('C:/Users/naija/Coding/flappy-bird/images/4.png')
five=Path('C:/Users/naija/Coding/flappy-bird/images/5.png')
six=Path('C:/Users/naija/Coding/flappy-bird/images/6.png')
seven=Path('C:/Users/naija/Coding/flappy-bird/images/7.png')
eight=Path('C:/Users/naija/Coding/flappy-bird/images/8.png')
nine=Path('C:/Users/naija/Coding/flappy-bird/images/9.png')


#----------------------------------------------------------------------------------------------------------------------------------------------------------

#defining the pipes location

def createPipe(): 
	offset = window_height/3
	pipeHeight = game_images['pipeimage'][0].get_height() 
	
	# generating random height of pipes 
	y2 = offset + random.randrange( 
	0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset)) 
	pipeX = window_width + 10
	y1 = pipeHeight - y2 + offset 
	pipe = [ 
		
		# upper Pipe 
		{'x': pipeX, 'y': -y1}, 
		
		# lower Pipe 
		{'x': pipeX, 'y': y2} 
	] 
	return pipe


#flappy game function

def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100

	# Generating two pipes for blitting on window 
    first_pipe = createPipe()
    second_pipe = createPipe()

	# List containing lower pipes 
    down_pipes = [
        {'x': window_width+300-mytempheight, 'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2), 'y': second_pipe[1]['y']},
    ]

	# List containing upper pipes 
    up_pipes = [
        {'x': window_width+300-mytempheight, 'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2), 'y': second_pipe[0]['y']},
    ]

	
    pipeVelX = -4 #pipe velocity along x 

    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
    
	# velocity while flapping 
    bird_flap_velocity = -8
    
	# It is true only when the bird is flapping 
    bird_flapped = False

    while True:
        
		# Handling the key pressing events 
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

		# This function will return true if the flappybird is crashed 
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        
        if game_over:
            return

		# check for score 
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        
        for pipe in up_pipes:
            
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                
				# Printing the score
                your_score += 1
                print(f"Your score is {your_score}")

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False

        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)
        
		# move pipes to the left

        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

		# Add a new pipe when the first is about to cross the leftmost part of the screen 
        
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
            
		# if the pipe is out of the screen, remove it 	

        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
            
		# blit game images now

        window.blit(game_images['background'], (0, 0))
        
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

		# Fetching the digits of score
        
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
        
		# finding the width of score images from numbers

        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1

		# Blitting the images on the window

        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

		# Refreshing the game window and displaying the score. 
        pygame.display.update()
        
		# Set the framepersecond 
        framepersecond_clock.tick(framepersecond)



#to check if the game is over

def isGameOver(horizontal, vertical, up_pipes, down_pipes):

    if vertical > elevation - 25 or vertical < 0:
        return True
    
	#checking if bird hits the upper pipe or not
    for pipe in up_pipes:

        pipeHeight = game_images['pipeimage'][0].get_height()

        if vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    
	#checking if bird hits the upper pipe or not
    for pipe in down_pipes:

        if vertical + game_images['flappybird'].get_height() > pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True

    return False

		   
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# program where the game starts 
if __name__ == "__main__":		 
	
	# For initializing modules of pygame library 
	pygame.init() 
	framepersecond_clock = pygame.time.Clock() 
	
	# Sets the title on top of game window 
	pygame.display.set_caption('Flappy Bird Game')	 

	# Load all the images which we will use in the game 
	# images for displaying score

	game_images['scoreimages'] = (
                pygame.image.load(zero).convert_alpha(),
		
                pygame.image.load(one).convert_alpha(),
                pygame.image.load(two).convert_alpha(),
                pygame.image.load(three).convert_alpha(),
                pygame.image.load(four).convert_alpha(),
                pygame.image.load(five).convert_alpha(),
                pygame.image.load(six).convert_alpha(),
                pygame.image.load(seven).convert_alpha(),
                pygame.image.load(eight).convert_alpha(),
                pygame.image.load(nine).convert_alpha(),
                )
	#print("works")
	
	game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()				 
	game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha() 
	game_images['background'] = pygame.image.load(background_image).convert_alpha() 
	game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(),180), pygame.image.load(pipeimage).convert_alpha()) 

	print("WELCOME TO THE FLAPPY BIRD GAME") 
	print("Press space or enter to start the game") 


#infinite loop till user stops 
#MAIN GAME

while True: 
  
        # sets the coordinates of flappy bird 
  
        horizontal = int(window_width/5) 
        vertical = int( 
            (window_height - game_images['flappybird'].get_height())/2) 
        ground = 0
        while True: 
            for event in pygame.event.get(): 
  
                # if user clicks on cross button, close the game 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                    pygame.quit() 
                    sys.exit() 
  
                # If the user presses space or 
                # up key, start the game for them 
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                    flappygame() 
  
                # if user doesn't press anykey Nothing happen 
                else: 
                    window.blit(game_images['background'], (0, 0)) 
                    window.blit(game_images['flappybird'], 
                                (horizontal, vertical)) 
                    window.blit(game_images['sea_level'], (ground, elevation)) 
                    pygame.display.update() 
                    framepersecond_clock.tick(framepersecond)


#----------------------------------------------------------------------------------------------------------------------------------------------------------

