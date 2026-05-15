# Gamerunner's Breakout Program
# Last Edited 3/4/2026

# ------- Imported Libraries -------

import math
import turtle
import turtle as paddle
import random
import math as m

# ------- Game Variables -------

game_active = True
check_loss = False

# Color list for bricks
colors_list = [
    "red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta",
    "brown", "gray", "gold", "silver", "navy", "lime", "teal", "maroon", "violet",
    "turquoise", "coral", "salmon", "plum", "khaki", "lavender", "indigo", "crimson",
    "tan", "chocolate"
]

# ------- Screen Set-Up -------

screen = paddle.Screen()
screen.bgcolor("black")
screen.setup(width=600, height=800)
screen.title("Gamerunner's Breakout")

WIDTH = screen.window_width() - 20
HEIGHT = screen.window_height()

screen.tracer(0)

limit_right = WIDTH / 2 - 60
limit_left = -WIDTH / 2 + 60
limit_top = HEIGHT / 2

# ------- Paddle Settings -------

paddle.shapesize(stretch_len=4, stretch_wid=0.6)
paddle.pencolor("white")
paddle.fillcolor("white")
paddle.shape("square")
paddle.penup()
paddle.goto(0, -270)
paddle.speed(10)
move_value = 20

# Input States
left_down = False
right_down = False

# Paddle Movement Functions

def check_wall():
    x = paddle.xcor()
    if x > limit_right:
        paddle.setx(limit_right + 5)
    elif x < limit_left:
        paddle.setx(limit_left - 15)

def update_paddle():
    global left_down, right_down

    if right_down and not left_down:
        paddle.setx(paddle.xcor() + move_value)
    elif left_down and not right_down:
        paddle.setx(paddle.xcor() - move_value)

    check_wall()

# Key Functions

def press_right():
    global right_down
    right_down = True

def release_right():
    global right_down
    right_down = False

def press_left():
    global left_down
    left_down = True

def release_left():
    global left_down
    left_down = False

def pause():
    global game_active
    if game_active == True:
        game_active = False
        draw_shadow()
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write("Paused", align="center", font=(font, 48, "bold"))
    elif game_active == False:
        score_display.goto(-220, 360)
        game_active = True
        update_score()
        tick()

# Paddle Movement Keybinds

screen.listen()
screen.onkeypress(press_right, "d")
screen.onkeyrelease(release_right, "d")
screen.onkeypress(press_left, "a")
screen.onkeyrelease(release_left, "a")
screen.onkeypress(pause, "t")

# ------- Ball Movement and Collisions -------

ball = turtle.Turtle()
ball.color("white")
ball.pensize(1)
ball.shape("circle")
SPEED = 0
ball.speed(SPEED)
ball.penup()
ball.left(45)
ball.pensize(5)
ball.goto(random.randint(-120, 120), 0)

def check_horizontal_walls(ball_mx):
    ball_x = ball.xcor()
    if ball_x > (limit_right + 50) or ball_x < (limit_left - 50):
        return -ball_mx
    return ball_mx

def check_vertical_walls(ball_my):
    ball_y = ball.ycor()
    if ball_y > (limit_top - 20):
        return -ball_my
    return ball_my

ball_speed = 5
ball_mx = ball_speed
ball_my = ball_speed

def ball_move():
    ball.sety(ball.ycor() + ball_my)
    ball.setx(ball.xcor() + ball_mx)

def clamp(val, lo, hi):
    return max(lo, min(val, hi))

def paddle_collision(paddle_obj, ball_obj):
    ball_x, ball_y = ball_obj.xcor(), ball_obj.ycor()
    paddle_x, paddle_y = paddle_obj.xcor(), paddle_obj.ycor()
    paddle_stretch_len = 4
    paddle_half_w = 10 * paddle_stretch_len
    paddle_half_h = 10 * 0.6
    ball_r = 10

    hit_x = (paddle_x - paddle_half_w - ball_r) <= ball_x <= (paddle_x + paddle_half_w + ball_r)
    hit_y = (paddle_y - paddle_half_h - ball_r) <= ball_y <= (paddle_y + paddle_half_h + ball_r)

    return hit_x and hit_y and (ball_y >= paddle_y)

# ------- Brick Settings and Collision -------

requested_bricks = 121

def create_bricks():
    brick_dict = {}
    total_bricks = requested_bricks
    starting_x = -255
    brick_move_y = 360
    row_filled = 0
    bricks_generated = 0

    for brick in range(1, total_bricks + 1):
        if bricks_generated % 11 == 0:
            brick_move_y -= 30
            row_filled = 0

        new_brick = turtle.Turtle()
        bricks_generated += 1
        row_filled += 1

        new_brick.shape("square")
        new_brick.shapesize(stretch_len=2, stretch_wid=0.6)
        new_brick.penup()
        new_brick.color(random.choice(colors_list))

        brick_move_x = starting_x + (row_filled - 1) * 50
        new_brick.goto(brick_move_x, brick_move_y)
        brick_name = f"brick_{brick}"
        brick_dict[brick_name] = new_brick

    return brick_dict

def check_brick_collision(bricks, ball):
    for name, brick in list(bricks.items()):
        ball_x, ball_y = ball.xcor(), ball.ycor()
        brick_x, brick_y = brick.xcor(), brick.ycor()

        brick_wid = 20
        brick_height = 6
        ball_r = 10

        hit_x = (brick_x - brick_wid - ball_r) <= ball_x <= (brick_x + brick_wid + ball_r)
        hit_y = (brick_y - brick_height - ball_r) <= ball_y <= (brick_y + brick_height + ball_r)

        if hit_x and hit_y:
            return name
    return None

# ------- Score Display -------

score_display = turtle.Turtle()
score_display.penup()
score_display.hideturtle()
score_display.color("white")
score_display.goto(-220, 360)
font = "Trebuchet MS"
score_display.write("Score: 0", align="center", font=(font, 24, "bold"))

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=(font, 24, "bold"))

# ------- Defeat Screen -------

def check_defeat():
    return ball.ycor() < -380

shadow_overlay = turtle.Turtle()
shadow_overlay.penup()
shadow_overlay.hideturtle()
shadow_overlay.speed(0)

def draw_shadow():
    shadow_overlay.goto(-WIDTH / 2, -HEIGHT / 2)
    shadow_overlay.color("black")
    shadow_overlay.begin_fill()

    for num in range(2):
        shadow_overlay.forward(WIDTH)
        shadow_overlay.left(90)
        shadow_overlay.forward(HEIGHT)
        shadow_overlay.left(90)

    shadow_overlay.end_fill()

def check_victory():
    global requested_bricks
    if score == requested_bricks:
        return True

# ------- Game Settings -------

brick_dict = create_bricks()
game_speed = 16
score = 0
print("Controls: Use 'A' and 'D' to move the paddle left and right, use 'T' to pause and unpause the game.")

def tick():
    global game_active, ball_mx, ball_my, score, game_speed, ball_speed, screen, requested_bricks

    if not game_active:
        screen.listen()
        screen.onkeypress(pause, "t")
        return

    update_paddle()
    ball_move()

    ball_mx = check_horizontal_walls(ball_mx)
    ball_my = check_vertical_walls(ball_my)

    if paddle_collision(paddle, ball) and ball_my < 0:
        ball_x, ball_y = ball.xcor(), ball.ycor()
        paddle_x, paddle_y = paddle.xcor(), paddle.ycor()

        hit_pos = (ball_x - paddle_x) / 40
        hit_pos = clamp(hit_pos, -1, 1)

        max_bounce = 60
        angle = 90 - (hit_pos * max_bounce)
        angle = clamp(angle, 30, 150)

        rad = angle * (m.pi / 180)
        ball_mx = ball_speed * m.cos(rad)
        ball_my = ball_speed * m.sin(rad)
        ball.sety(paddle_y + 20)

    brick_hit = check_brick_collision(brick_dict, ball)
    if brick_hit:
        ball_x, ball_y = ball.xcor(), ball.ycor()
        brick_x, brick_y = brick_dict[brick_hit].xcor(), brick_dict[brick_hit].ycor()
        brick_half_w = 20
        brick_half_h = 6
        ball_r = 10

        brick_dict[brick_hit].hideturtle()
        del brick_dict[brick_hit]

        dx = abs(ball_x - brick_x)
        dy = abs(ball_y - brick_y)

        overlap_x = (brick_half_w + ball_r) - abs(dx)
        overlap_y = (brick_half_h + ball_r) - abs(dy)

        if overlap_y < overlap_x:
            ball_my *= -1
            if ball_my > 0:
                ball.sety(brick_y + brick_half_h + ball_r + 1)
            else:
                ball.sety(brick_y - brick_half_h - ball_r - 1)
        else:
            ball_mx *= -1
            if ball_mx > 0:
                ball.setx(brick_x + brick_half_w + ball_r + 1)
            else:
                ball.setx(brick_x - brick_half_w - ball_r - 1)

        score += 1
        if score % 3 == 0:
            ball_speed *= 1.06

            if ball_mx > 0:
                ball_mx = ball_speed
            else:
                ball_mx = -ball_speed
            if ball_my > 0:
                ball_my = ball_speed
            else:
                ball_my = -ball_speed

    if check_defeat():
        game_active = False
        draw_shadow()
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write("Game Over", align="center", font=(font, 48, "bold"))
        print(f"Game Over \nFinal Score: {score}")
        return

    if check_victory():
        game_active = False
        draw_shadow()
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write("You Win", align="center", font=(font, 48, "bold"))
        print(f"You Win \nFinal Score: {score}")
        return

    update_score()
    screen.update()
    screen.ontimer(tick, game_speed)

tick()
screen.mainloop()
