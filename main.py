import pygame
import datetime
import csv

from configurations import *
import clumpy_diffuse

pygame.init()

#font
font = pygame.font.SysFont(None, 25)

clock = pygame.time.Clock()

###############################################################################
# Function definitions
###############################################################################

def message(msg, x, y): # displays a message anywhere on dis
    mesg = font.render(msg, True, black)
    return dis.blit(mesg, [int(x), int(y)])

def print_timer(time):
    mesg = font.render("Time elapsed: " + str(time), True, blue)
    return dis.blit(mesg, [play_width + 10, 10])

def print_score(score):
    mesg = font.render("Score: " + str(score), True, blue)
    return dis.blit(mesg, [play_width + 10, 50])

def print_userid(userid):
    mesg = font.render("User ID: " + userid, True, black)
    return dis.blit(mesg, [userIDline[0], userIDline[1]])

def print_to_csv(userid, score):
    with open(filename, 'a', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M")
        # writing the data rows
        csvwriter.writerow([timestamp, userid, score])

def gameLoop():

    game_over = False
    game_close = False
    start = False
    userIDentered = False


    x1 = int(play_width/2)
    y1 = int(play_height/2)
    x1_change = 0
    y1_change = 0

    clumpy = True # TODO make it based off userID

    food = clumpy_diffuse.create_food(clumpy)

    score = 0
    userid = "";

    dis.fill(white, play)
    dis.fill(light_blue, sidebar)
    print_userid(userid)
    print_timer(0)
    print_score(0)
    pygame.display.flip()

    # enter the userID
    while not userIDentered and not game_close:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    userIDentered = True
                elif event.unicode.isalpha():
                    userid += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    userid = userid[:-1]
            if event.type == pygame.QUIT:
                game_close = True

        pygame.draw.rect(dis, white, userIDline)
        print_userid(userid)
        pygame.display.update(userIDline)

    dis.fill(white, userIDline)
    message("Press Enter to start.", 10, play_height / 2)
    pygame.display.update(play)

    # waiting for user to start game
    while not start and not game_close:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                start = True
            if event.type == pygame.QUIT:
                game_close = True

    start_ticks = pygame.time.get_ticks()

    dis.fill(white, play)
    dis.fill(light_blue, sidebar)
    pygame.display.flip()

    # the actual playing of the game
    while not game_over and not game_close:

        # update the sidebar
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > timer:
            game_over = True

        dis.fill(light_blue, sidebar)
        pygame.display.update([print_timer(seconds), print_score(score)])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block


        #only move the snake if it's not going to go out of bounds
        rect1 = pygame.draw.rect(dis, white, [x1, y1, snake_block, snake_block]) #paints over the old one

        if x1 >= play_width - 10 and x1_change > 0:
            x1 = play_width - 10
        elif x1 <= 0 and x1_change < 0:
            x1 = 0
        else:
            x1 += x1_change
        if y1 >= play_height - 10 and y1_change > 0:
            y1 = play_height - 10
        elif y1 <= 0 and y1_change < 0:
            y1 = 0
        else:
            y1 += y1_change

        rect2 = pygame.draw.rect(dis, blue, [x1, y1, snake_block, snake_block])
        pygame.display.update(play) #TODO be more specific so it's faster

        # draw all the food
        for f in food:
            pygame.draw.rect(dis, black, [f[0], f[1], snake_block, snake_block])

        # update if found a food
        for f in food:
            if (x1, y1) == (f[0], f[1]):
                score += 1
                food.remove(f)
                break

        clock.tick(snake_speed)

    # once the timer is over
    print_to_csv(userid, score)
    while not game_close:
        dis.fill(light_blue, sidebar)
        pygame.display.update(message("Score: " + str(score), play_width, int(play_height / 2)))
        pygame.display.update(message("Press Enter to start again.", play_width, play_height / 2 + 60))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
            if event.type == pygame.QUIT:
                game_close = True


    pygame.quit()
    quit()

###########################################################################################
# Things actually happen here
###########################################################################################

#initialize the display window
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Spatial Foraging Task")

# calling the main function
gameLoop()
