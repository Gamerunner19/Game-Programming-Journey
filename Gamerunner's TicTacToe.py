import tkinter as t

#                               ------- Variables -------

# Define variables
player_1 = True
player_2 = False
can_draw = True
turns = 0

# The score table the detects if there is a line
score = [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "]]

#                             ------- Main Functions -------

# Check for a line in the game
def check_line():
    global turns
    # ------- Player 1 Wins -------
    # If a row is filled with X
    if score[0][0] == 'X' and score[0][1] == 'X' and score[0][2] == 'X':
        p1_victory()
    elif score[1][0] == 'X' and score[1][1] == 'X' and score[1][2] == 'X':
        p1_victory()
    elif score[2][0] == 'X' and score[2][1] == 'X' and score[2][2] == 'X':
        p1_victory()
    # If a column is filled with X
    elif score[0][0] == 'X' and score[1][0] == 'X' and score[2][0] == 'X':
        p1_victory()
    elif score[0][1] == 'X' and score[1][1] == 'X' and score[2][1] == 'X':
        p1_victory()
    elif score[0][2] == 'X' and score[1][2] == 'X' and score[2][2] == 'X':
        p1_victory()
    # Check the Cross
    elif score[0][0] == 'X' and score[1][1] == 'X' and score[2][2] == 'X':
        p1_victory()
    elif score[0][2] == 'X' and score[1][1] == 'X' and score[2][0] == 'X':
        p1_victory()
    # ------- Player 2 -------
    # Check if a row is filled with O
    elif score[0][0] == 'O' and score[0][1] == 'O' and score[0][2] == 'O':
        p2_victory()
    elif score[1][0] == 'O' and score[1][1] == 'O' and score[1][2] == 'O':
        p2_victory()
    elif score[2][0] == 'O' and score[2][1] == 'O' and score[2][2] == 'O':
        p2_victory()
    # If a column is filled with O
    elif score[0][0] == 'O' and score[1][0] == 'O' and score[2][0] == 'O':
        p2_victory()
    elif score[0][1] == 'O' and score[1][1] == 'O' and score[2][1] == 'O':
        p2_victory()
    elif score[0][2] == 'O' and score[1][2] == 'O' and score[2][2] == 'O':
        p2_victory()
    # Check the Cross
    elif score[0][0] == 'O' and score[1][1] == 'O' and score[2][2] == 'O':
        p2_victory()
    elif score[0][2] == 'O' and score[1][1] == 'O' and score[2][0] == 'O':
        p2_victory()
    # Checks if the board is filled or not
    if can_draw:
        turns += 1
        if turns >= 9:
            tie_game()

# Swap Player Turns
def swap_player(player_1, player_2):
    if player_1 == True:
        player_2 = True
        player_1 = False
        canvas.itemconfig(turn_label, text="Player 2 (O)")
        return player_1, player_2
    else:
        player_2 = False
        player_1 = True
        canvas.itemconfig(turn_label, text="Player 1 (X)")
        return player_1, player_2


# X and O drawing settings
def draw_shape(x, y, size, p1, p2):
    # Draw an X
    if p1 == True:
        offset = size / 2
        canvas.create_line(x - offset, y - offset, x + offset, y + offset, fill="red", width=4)
        canvas.create_line(x - offset, y + offset, x + offset, y - offset, fill="red", width=4)
    # Draw an O
    elif p2 == True:
        offset = size / 2
        canvas.create_oval(x - offset, y - offset, x + offset, y + offset, width=4)

# Handles the drawing of X or O depending on whose turn it is
def handle_click(click):
    global player_1, player_2
    col = int(click.x // 166)
    row = int(click.y // 166)

    # Check if the clicked box is empty
    def is_occupied():
        if score[row][col] == " ":
            return False
        else:
            return True

    # Draw the shapes
    if can_draw:
        # First Column Shapes
        if row == 0 and col == 0 and is_occupied() == False:
            x, y = 85, 85
            size = 100
            draw_shape(x, y, size, player_1, player_2)
        elif row == 1 and col == 0 and is_occupied() == False:
            x, y = 85, 250
            size = 100
            draw_shape(x, y, size, player_1, player_2)
        elif row == 2 and col == 0 and is_occupied() == False:
            x, y = 85, 415
            size = 100
            draw_shape(x, y, size, player_1, player_2)

        # Middle Column Shapes
        if row == 0 and col == 1 and is_occupied() == False:
            x, y = 250, 85
            size = 100
            draw_shape(x, y, size, player_1, player_2)
        elif row == 1 and col == 1 and is_occupied() == False:
            x, y = 250, 250
            size = 100
            draw_shape(x, y, size, player_1, player_2)
        elif row == 2 and col == 1 and is_occupied() == False:
            x, y = 250, 415
            size = 100
            draw_shape(x, y, size, player_1, player_2)

        # Last Column Shapes
        if row == 0 and col == 2 and is_occupied() == False:
            x, y = 415, 85
            size = 100
            draw_shape(x, y, size, player_1, player_2)
        elif row == 1 and col == 2 and is_occupied() == False:
            x, y = 415, 250
            size = 100
            draw_shape(x, y, size, player_1, player_2)
        elif row == 2 and col == 2 and is_occupied() == False:
            x, y = 415, 415
            size = 100
            draw_shape(x, y, size, player_1, player_2)

        # Update the score table
        if not is_occupied():
            if player_1:
                score[row][col] = "X"
            else:
                score[row][col] = "O"
            check_line()

            # Swap the player's turn if the round is still going
            if can_draw:
                player_1, player_2 = swap_player(player_1, player_2)
            # If the round is ended, restart the game after
            elif not can_draw:
                root.after(3000, restart_game)


# Runs if Player 1 won
def p1_victory():
    global can_draw
    canvas.itemconfig(turn_label, text="Player 1 Wins")
    can_draw = False

# Runs if Player 2 won
def p2_victory():
    global can_draw
    canvas.itemconfig(turn_label, text="Player 2 Wins")
    can_draw = False

# Runs if there is a tie game
def tie_game():
    global can_draw
    canvas.itemconfig(turn_label, text="Tie")
    can_draw = False


# Restarts the game after a completed round
def restart_game():
    global score, can_draw, turns, player_1, player_2

    canvas.delete("all")

    draw_game()
    score = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]
    can_draw = True
    turns = 0
    player_1, player_2 = swap_player(player_1, player_2)
#                            ------- Game Setup -------
# Set up the window
root = t.Tk()
canvas = t.Canvas(root, width=500, height=525)
turn_label = canvas.create_text(250, 500, text=" ", font=("Arial", 16))
canvas.bind("<Button-1>", handle_click)
root.title("Gamerunner's Tic-Tac-Toe")
canvas.pack()


def draw_game():
    global turn_label
    turn_label = canvas.create_text(250, 500, text=" ", font=("Arial", 16))

    # X lines
    canvas.create_line(25, 166, 475, 166, fill="black", width=2)
    canvas.create_line(25, 333, 475, 333, fill="black", width=2)
    # Y lines
    canvas.create_line(166, 25, 166, 475, fill="black", width=2)
    canvas.create_line(333, 25, 333, 475, fill="black", width=2)

# Initially Draws the Game
draw_game()
root.mainloop()

