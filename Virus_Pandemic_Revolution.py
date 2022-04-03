from turtle import *
import random
import time

start_speed = 1.5
virus_speed = start_speed
regular_speed = start_speed
colorIndex = 0
time_to_restore_lives = 0
title_font = ("Times New Roman", 80, "bold")
normal_font = ("Times New Roman", 20, "bold")
small_font = ("Times New Roman", 12, "normal")

game_duration = 60

city_lives = 5
score = 0
viruses_killed = 0
viruses_invaded = 0
foods_collected = 0
masks_collected = 0
bonus_lives = 0
city_population = 100000
shields = 0

game_is_on = True

Spawn_Points = [-100, 0, 100]
City_Colors = ['light green', '#cfea4f', 'dark red', '#7d327e', '#301330']
End_Display = ["Your score", "Viruses killed", "Viruses invaded", "Foods collected", "Masks collected", "Bonus Lives", "Population remaining"]
InGame_Display = ["Score", "Lives", "Shields"]
InGame_Info = [score, city_lives, shields]

Start_Display = [
"Welcome to Virus Pandemic Revolution!",
"The humanity is being threatened by viruses,",
"and your city is the last hope.",
"In this game, viruses, foods and masks",
"will charge towards your city.",
"VIRUSES : -1 Life, -20k Population",
"Obtain 3 FOODS : +1 Life, +20k Population",
"MASKS : prevents 1 Virus, reduces Speed",
"VICTORY : Hold until the Timer Ends.",
"Now, use LEFT, RIGHT Arrow Keys,",
"Block all Viruses and Collect the others!"
]

Viruses = []
Foods = []
Pens = [] 

def endGame():
    for p in Pens:
        p.clear()

# Display multi-lines of text.
def displayGameInfo(pen_list, pen, display_list, info_list, x, y, line_gap, loop_count, txt_font):
    for i in range(loop_count):
        if info_list != "None":
            if pen_list == "None":
                pen.goto(x, y)
                pen.write(f"{display_list[i]} : {info_list[i]}", move= False, align= "left", font= txt_font)
            elif pen == "None":
                pen_list[i].goto(x, y)
                pen_list[i].write(f"{display_list[i]} : {info_list[i]}", move= False, align= "left", font= txt_font)
        if info_list == "None":
            if pen_list == "None":
                pen.goto(x, y)
                pen.write(f"{display_list[i]}", move= False, align= "left", font= txt_font)
            elif pen == "None":
                pen_list[i].goto(x, y)
                pen_list[i].write(f"{display_list[i]}", move= False, align= "left", font= txt_font)
        y -= line_gap

# Player Movement
def moveRight():
    x = player.xcor()
    x += 100            # Keep the player on the road.
    if x > 100:
        x = 100
    player.setx(x)

def moveLeft():
    x = player.xcor()
    x -= 100
    if x < -100:
        x = -100
    player.setx(x)

# Set up the screen.
screen = Screen()
screen.setup(width= 750, height= 750)
screen.title("Virus Pandemic Revolution : The Final Fortress")
screen.bgpic("GameBG.gif")
screen.register_shape("Virus.gif")
screen.register_shape("Food.gif")
screen.register_shape("Mask.gif")
screen.register_shape("shield.gif")
screen.tracer(0)

game_duration = int(numinput("Set Game Duration", "How long do you wanna play? Please enter the amount of seconds. (min : 60, max : 500)", 100, 60, 500))

# Create pens.
for i in range(8):
    Pens.append(Turtle())

for p in Pens:
    p.hideturtle()
    p.speed(0)
    p.color('white')
    p.penup()

score_pen = Pens[0]
lives_pen = Pens[1]
shields_pen = Pens[2]
shields_pen.color('#31aae6')
population_pen = Pens[3]
timer_pen = Pens[4]
timer_pen.color('white')
ending_pen = Pens[5]
start_pen = Pens[6]
start_pen.color('black')
displayGameInfo("None", start_pen, Start_Display, "None", -130, 200, 30, 11, small_font)     # Start display

population_pen.goto(0, -220)
population_pen.write(f"City Population : {city_population}", move= False, align= "center", font= normal_font)
displayGameInfo(Pens, "None", InGame_Display, InGame_Info, -280, 200, 35, 3, normal_font)        

# Create a camera view.
camera_pen = Turtle()       
camera_pen.hideturtle()
camera_pen.speed(0)
camera_pen.color('black')
camera_pen.pensize(5)
camera_pen.penup()
camera_pen.goto(-300, -300)
camera_pen.pendown()
for i in range(4):
    camera_pen.forward(600) 
    camera_pen.left(90)

# Create player.
player = Turtle()
player.hideturtle()
player.speed(0)
player.shape("square")
player.color('black')
player.shapesize(stretch_wid= 0.5, stretch_len= 5)
player.penup()
player.goto(0, -135)
player.showturtle()

# Player movement
screen.onkeypress(moveRight, "Right")
screen.onkeypress(moveLeft, "Left")
screen.listen()

# Create city turtle.
city = Turtle()
city.hideturtle()
city.speed(0)
city.shape("square")
city.color(City_Colors[0])
city.shapesize(stretch_wid= 3, stretch_len= 20)
city.penup()
city.goto(0,-270)
city.showturtle()

# Create shield turtle.
shield = Turtle()
shield.hideturtle()
shield.speed(0)
shield.shape("shield.gif")
shield.penup()
shield.goto(0,-265)

# Create a mask.
mask = Turtle()
mask.hideturtle()
mask.speed(0)
mask.shape("Mask.gif")
mask.penup()
mask.goto(random.choice(Spawn_Points), random.randint(3000, 3300))

# Add Viruses.
for i in range(10):
    Viruses.append(Turtle())

for virus in Viruses:
    virus.hideturtle()
    virus.shape("Virus.gif")
    virus.speed(0)
    virus.penup()
    virus.goto(random.choice(Spawn_Points), random.randint(1500, 1800))

# Add Foods.
for i in range(3):
    Foods.append(Turtle())

for food in Foods:
    food.hideturtle()
    food.shape("Food.gif")
    food.speed(0)
    food.penup()        
    food.goto(random.choice(Spawn_Points), random.randint(1600, 1900))

start_time = time.time()

# main game loop
while game_is_on:
    screen.update()
    
    # Game Timer
    elapsed_time = time.time() - start_time
    count_down = game_duration - int(elapsed_time)
    timer_pen.clear()
    timer_pen.goto(-280, 250)
    timer_pen.write(f"Duration : {count_down}", move= False, align= "left", font= normal_font)
    
    # Victory
    if elapsed_time > game_duration and city_lives > 0:  
        endGame()
        mask.hideturtle()
        ending_pen.color('yellow')
        ending_pen.goto(0, 150)
        ending_pen.write("Victory!", move= False, align= "center", font= title_font)
        
        End_Info = [score, viruses_killed, viruses_invaded, foods_collected, masks_collected, bonus_lives, city_population]
        ending_pen.color('black')
        displayGameInfo("None", ending_pen, End_Display, End_Info, -145, 95, 35, 7, normal_font)
        
        game_is_on = False

    for virus in Viruses:
        # Virus movement
        y = virus.ycor()    
        y -= virus_speed
        virus.sety(y)
    
        # Virus Collision Detection
        if virus.ycor() < -200:     # Collision with City
            virus.hideturtle()                              
            virus.goto(random.choice(Spawn_Points), random.randint(400, 700))
            if shields > 0:
                shields -= 1
                shields_pen.clear()
                shields_pen.goto(-280, 130)
                shields_pen.write(f"Shields : {shields}", move= False, align= "left", font= normal_font)
                if shields == 0:
                    shield.hideturtle()
            else:
                city_lives -= 1
                lives_pen.clear()
                lives_pen.goto(-280, 165)
                lives_pen.write(f"Lives : {city_lives}", move= False, align= "left", font= normal_font)                
                score -= 20
                if score < 0:
                    score = 0
                score_pen.clear()
                score_pen.goto(-280, 200)
                score_pen.write(f"Score : {score}", move= False, align= "left", font= normal_font)         
                city_population -= 20000
                population_pen.clear()
                population_pen.goto(0, -220)
                population_pen.write(f"City Population : {city_population}", move= False, align= "center", font= normal_font)
                viruses_invaded += 1
                colorIndex += 1
                
                # Defeat
                if city_lives <= 0:  
                    endGame()
                    ending_pen.color('dark red')
                    ending_pen.goto(0, 150)
                    ending_pen.write("Game Over!", move= False, align= "center", font= title_font) 
            
                    End_Info = [score, viruses_killed, viruses_invaded, foods_collected, masks_collected, bonus_lives, city_population]
                    ending_pen.color('black')
                    displayGameInfo("None", ending_pen, End_Display, End_Info, -145, 95, 35, 7, normal_font)
                    game_is_on = False
                elif colorIndex <= 4: 
                    city.color(City_Colors[colorIndex])
                    virus_speed += 0.4
                    
        elif virus.distance(player) < 30:   # Destroyed by Player
            score += 10
            score_pen.clear()
            score_pen.goto(-280, 200)
            score_pen.write(f"Score : {score}", move= False, align= "left", font= normal_font) 
            viruses_killed += 1
            virus.hideturtle()
            virus.goto(random.choice(Spawn_Points), random.randint(400, 700))
        
        elif virus.ycor() < 260:            # Virus wiil appear only inside the camera.
            virus.showturtle()
            start_pen.clear()
        else :
            virus.hideturtle()
        
    for food in Foods:
        # Food movement
        y = food.ycor()    
        y -= regular_speed
        food.sety(y)
    
        # Food Collision Detection
        if food.ycor() < -200:     # Collision with City
            foods_collected += 1
            time_to_restore_lives += 1
            score += 10
            score_pen.clear()
            score_pen.goto(-280, 200)
            score_pen.write(f"Score : {score}", move= False, align= "left", font= normal_font)
            food.hideturtle()                              
            food.goto(random.choice(Spawn_Points), random.randint(500, 800))
            
            if time_to_restore_lives >= 3:  # Add 1 Bonus Life.
                if colorIndex > 0:
                    colorIndex -= 1
                    city.color(City_Colors[colorIndex])
                city_lives += 1
                lives_pen.clear()
                lives_pen.goto(-280, 165)
                lives_pen.write(f"Lives : {city_lives}", move= False, align= "left", font= normal_font)
                bonus_lives += 1
                city_population += 20000
                population_pen.clear()
                population_pen.goto(0, -220)
                population_pen.write(f"City Population : {city_population}", move= False, align= "center", font= normal_font)
                time_to_restore_lives = 0

        elif food.distance(player) < 30:   # Destroyed by Player
            food.hideturtle()
            food.goto(random.choice(Spawn_Points), random.randint(500, 800))
        
        elif food.ycor() < 260:            # Food wiil appear only inside the camera.
            food.showturtle()
            start_pen.clear()
        else :
            food.hideturtle()

    # Mask movement
    y = mask.ycor()    
    y -= regular_speed
    mask.sety(y)
    
    # Mask Collision Detection
    if mask.ycor() < -200:              # Collision with City
        if virus_speed > start_speed:
            virus_speed -= 0.4
        shield.showturtle()
        shields += 1
        shields_pen.clear()
        shields_pen.goto(-280, 130)
        shields_pen.write(f"Shields : {shields}", move= False, align= "left", font= normal_font)
        masks_collected += 1
        score += 30
        score_pen.clear()
        score_pen.goto(-280, 200)
        score_pen.write(f"Score : {score}", move= False, align= "left", font= normal_font)
        mask.hideturtle()
        mask.goto(random.choice(Spawn_Points), random.randint(1000, 1200))
    
    elif mask.distance(player) < 30:   # Destroyed by Player
        mask.hideturtle()
        mask.goto(random.choice(Spawn_Points), random.randint(1000, 1200))
        
    elif mask.ycor() < 260:            # Mask wiil appear only inside the camera.
        mask.showturtle()
        start_pen.clear()
    else :
        mask.hideturtle()

screen.exitonclick()