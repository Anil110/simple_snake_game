'''
Created on May 24, 2018

@author: Anil
'''
import pygame
import sys
import random


board_size = 30             # Size of the board, in block
block_size = 20             # Size of 1 block, in pixel
snake_head_color = (0, 100, 0)    
snake_body_color = (0, 200, 0)    
food_color = (200, 0, 0)   
speed = 10             # Game speed (Normal = 10), The bigger, the faster

class Snake():
    def __init__(self):
        self.head = [int(board_size/4), int(board_size/4)]
        self.body = [[self.head[0], self.head[1]],
                     [self.head[0]-1, self.head[1]],
                     [self.head[0]-2, self.head[1]]
                    ]
        self.direction = "RIGHT"
        

    def change_direction_toward(self, dir):
        if dir == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"


    def move(self, food_position):
        ''' Move the snake to the desired direction by adding the head to that direction
            and remove the tail if the snake does not eat food
        '''
        if self.direction == "RIGHT":
            self.head[0] += 1
        if self.direction == "LEFT":
            self.head[0] -= 1
        if self.direction == "UP":
            self.head[1] -= 1
        if self.direction == "DOWN":
            self.head[1] += 1
            
        self.body.insert(0, list(self.head))
        if self.head == food_position:
            return 1
        else:
            self.body.pop()
            return 0
        

    def check_for_collision(self):
        # Check if the head collides with the edges of the board
        if self.head[0] >= board_size or self.head[0] < 0:
            return 1
        elif self.head[1] > board_size or self.head[1] < 0:
            return 1
        # Check if the head collides with the body
        for body in self.body[1:]:
            if self.head == body:
                return 1
        return 0


    def get_body(self):
        return self.body


class FoodGenerater():
    def __init__(self):
        self.head = [random.randrange(1, board_size), random.randrange(1, board_size)]
        self.is_food_on_screen = True


    def generate_food(self):
        if self.is_food_on_screen == False:
            self.head = [random.randrange(1, board_size), random.randrange(1, board_size)]
            self.is_food_on_screen = True
        return self.head


    def set_food_on_screen(self, bool_value):
        self.is_food_on_screen = bool_value


# Game Initialization
window = pygame.display.set_mode((board_size*block_size, board_size*block_size))
pygame.display.set_caption("SNAKE GAME")
fps = pygame.time.Clock()

score = 0

# Initialize snake and food
snake = Snake()
food_generater = FoodGenerater()

def game_start():
    for i in range(3):
        pygame.display.set_caption("SNAKE GAME  |  Game starts in " + str(3-i) + " second(s) ...")
        pygame.time.wait(1000)

        
def game_over():
    pygame.display.set_caption("SNAKE GAME  |  Score: " + str(score) + "  |  GAME OVER. Press any key to quit ...")
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            break
    pygame.quit()
    sys.exit()


game_start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction_toward("RIGHT")
            if event.key == pygame.K_UP:
                snake.change_direction_toward("UP")
            if event.key == pygame.K_DOWN:
                snake.change_direction_toward("DOWN")
            if event.key == pygame.K_LEFT:
                snake.change_direction_toward("LEFT")
    food_position = food_generater.generate_food()
    if snake.move(food_position) == 1:
        score += 1
        food_generater.set_food_on_screen(False)

    window.fill(pygame.Color(225, 225, 225))
    # Draw snake
    head = 1
    for pos in snake.get_body():
        if head == 1:
            pygame.draw.rect(window, snake_head_color, pygame.Rect(pos[0]*block_size, pos[1]*block_size, block_size, block_size))
            head = 0
        else:
            pygame.draw.rect(window, snake_body_color, pygame.Rect(pos[0]*block_size, pos[1]*block_size, block_size, block_size))

    # Draw food
    pygame.draw.rect(window, food_color, pygame.Rect(food_position[0]*block_size, food_position[1]*block_size, block_size, block_size))
        
    if snake.check_for_collision() == 1:
        game_over()

    pygame.display.set_caption("SNAKE GAME  |  Speed: " + str(speed) + "  |  Score: " + str(score))
    pygame.display.flip()
    fps.tick(speed)