from microbit import *
import random

# Define constants
# they modify the way the game behaves
directions = [(1,0), (0,1), (-1,0), (0,-1)]
FOOD_BRIGHT = 9
SNAKE_BRIGHT = 5
MAX_X = 4
MAX_Y = 4
# modify DIFFICULTY and START_SLEEP_TIME 
# to set your challenge
DIFFICULTY = 0.1
START_SLEEP_TIME = 1000
SKULL = Image("55555:"
              "59595:"
              "05550:"
              "00000:"
              "05550")


# define functions
def draw():
    display.clear()
    for pos in snake:
        display.set_pixel(pos[0], pos[1], SNAKE_BRIGHT)
    display.set_pixel(food[0], food[1], FOOD_BRIGHT)
    for pos in others:
        display.set_pixel(pos[0], pos[1], 6)

def compute_next_head():
    next_head_x = snake[0][0] + directions[current_direction][0]
    next_head_y = snake[0][1] + directions[current_direction][1]
    # allow to roll to the other side
    next_head_x %= (MAX_X + 1)
    next_head_y %= (MAX_Y + 1)
    if next_head_x == -1:
        next_head_x = MAX_X
    if next_head_y == -1:
        next_head_y = MAX_Y
    return (next_head_x, next_head_y)

def colision(head):
    col = False
    # check if head is in bounds
    x, y = head
    if x < 0 or x > MAX_X:
        col = True
    if y < 0 or y > MAX_Y:
        col = True
    
    # check if colision with snake
    if head in snake[:-1]:
        col = True
    return col

def compute_next_food():
    food = snake[0]
    while food in snake:
        food = (random.randint(0, MAX_X), random.randint(0, MAX_Y))
    return food

# define variables
snake = [(2,3),(2,4)]
others = []
food = compute_next_food()
sleep_time = START_SLEEP_TIME
current_direction = 3
speed_up = (1.0 - DIFFICULTY)
points = 0

gameOn = True
while gameOn:
    draw()
    sleep(sleep_time)
    # capture user inputs
    if button_a.is_pressed():
        current_direction -= 1
    elif button_b.is_pressed():
        current_direction += 1
    current_direction = current_direction % 4

    # compute next snake
    next_head = compute_next_head()
    if colision(next_head):
        gameOn = False
    
    new_snake = []
    new_snake.append(next_head)
    for e in snake[:-1]:
        new_snake.append(e)
    # check if we ate food    
    if next_head == food:
        new_snake.append(snake[-1])
        food = compute_next_food()
        sleep_time *= speed_up
        points += 1
    
    # draw new frame    
    snake = new_snake
    

while True:
    display.show(SKULL)
    sleep(2000)
    display.scroll(points)
