import tkinter as tk
import random

# Set up the game window
root = tk.Tk()
root.title("Snake Game")

# Constants for the game
GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_SIZE = 20
SNAKE_SPEED = 100  # Speed in milliseconds (lower value means faster)
INITIAL_SNAKE_LENGTH = 3

# Create a canvas for the game area
canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg="black")
canvas.pack()

# Initialize variables
snake = [(100, 100), (80, 100), (60, 100)]  # Snake body parts
snake_direction = "Right"
food_position = (random.randint(0, (GAME_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
                 random.randint(0, (GAME_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)
score = 0
game_over = False

# Display the score
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 14), bg="black", fg="white")
score_label.pack()

# Functions to control the snake's movement
def change_direction(new_direction):
    global snake_direction
    # Prevent the snake from moving in the opposite direction
    if (new_direction == "Left" and snake_direction != "Right") or \
       (new_direction == "Right" and snake_direction != "Left") or \
       (new_direction == "Up" and snake_direction != "Down") or \
       (new_direction == "Down" and snake_direction != "Up"):
        snake_direction = new_direction

def move_snake():
    global snake, food_position, score, game_over

    if game_over:
        return

    head_x, head_y = snake[0]

    if snake_direction == "Right":
        new_head = (head_x + SNAKE_SIZE, head_y)
    elif snake_direction == "Left":
        new_head = (head_x - SNAKE_SIZE, head_y)
    elif snake_direction == "Up":
        new_head = (head_x, head_y - SNAKE_SIZE)
    elif snake_direction == "Down":
        new_head = (head_x, head_y + SNAKE_SIZE)

    # Check for collisions with walls
    if (new_head[0] < 0 or new_head[0] >= GAME_WIDTH or
        new_head[1] < 0 or new_head[1] >= GAME_HEIGHT):
        game_over = True
        canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, fill="red", font="Arial 24 bold",
                           text="GAME OVER!")
        return

    # Check for collisions with itself
    if new_head in snake:
        game_over = True
        canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, fill="red", font="Arial 24 bold",
                           text="GAME OVER!")
        return

    # Add the new head to the snake
    snake = [new_head] + snake

    # Check if snake has eaten the food
    if new_head == food_position:
        score += 1
        update_score()
        spawn_food()  # Spawn new food
    else:
        snake.pop()  # Remove the tail (moving effect)

    # Update the game display
    update_snake_display()
    root.after(SNAKE_SPEED, move_snake)

# Function to update the displayed snake on the canvas
def update_snake_display():
    canvas.delete("snake")  # Clear previous snake display
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE, fill="green", tag="snake")

# Function to spawn food at a random position
def spawn_food():
    global food_position
    food_position = (random.randint(0, (GAME_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
                     random.randint(0, (GAME_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)
    canvas.delete("food")
    canvas.create_oval(food_position[0], food_position[1], food_position[0] + SNAKE_SIZE, food_position[1] + SNAKE_SIZE, fill="red", tag="food")

# Function to update the score display
def update_score():
    score_label.config(text=f"Score: {score}")

# Key bindings for controlling the snake
root.bind("<Up>", lambda event: change_direction("Up"))
root.bind("<Down>", lambda event: change_direction("Down"))
root.bind("<Left>", lambda event: change_direction("Left"))
root.bind("<Right>", lambda event: change_direction("Right"))

# Start the game
spawn_food()
move_snake()

# Start the Tkinter main loop
root.mainloop()
