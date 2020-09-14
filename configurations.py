###############################################################################
# Configurations
###############################################################################
timer = 15 # time in seconds
filename = "testcsv.csv" #csv file to append the data to
snake_speed = 10 # relative speed of the game
num_food = 100 # number of resources that are dispersed
num_clusters = 4
num_per_cluster = 20
size_cluster = 55


# colors
blue = (68, 109, 212)
light_blue = (168, 210, 240)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# locations and dimensions
play_width = 600
play_height = 600  # not actually needed, just makes things easier to read on the bottom loop
sidebar_width = 300
# sidebar and play rectangle
play = [0, 0, play_width, play_height]
sidebar = [play_width, 0, sidebar_width, play_height]
userIDline = [10, int(play_height/2), int(play_width - 50), 30]
# dis is the entire window
dis_width = play_width + sidebar_width
dis_height = play_height

snake_block = 10  # size of one "block", the width/height of the snake as well as the food

