import random
from configurations import play_width, play_height, snake_block, num_food, num_clusters, num_per_cluster, size_cluster

xbound1 = 10
xbound2 = play_width - 10 - snake_block
ybound1 = 10
ybound2 = play_height - 10 - snake_block


def dist(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] + pos2[1]) ** 2) ** .5


def create_food(clumpy):
    food = set()

    if clumpy:
        # choose clusters
        clusters = set()
        while len(clusters) < num_clusters:
            x = round(random.randrange(xbound1 + size_cluster, xbound2 - size_cluster) / 10) * 10
            y = round(random.randrange(ybound1 + size_cluster, ybound2 - size_cluster) / 10) * 10
            # check if clusters are too close
            far_enough = True
            for cluster in clusters:
                if dist((x,y), cluster) <= 6 * size_cluster:
                    far_enough = False
                    break
            if far_enough:
                clusters.add((x, y))

        # distribute near clusters
        for cluster in clusters:
            cluster_food = set()
            while len(cluster_food) < num_per_cluster:
                # currently a square cluster
                x = round(random.randrange(cluster[0] - size_cluster, cluster[0] + size_cluster) / 10) * 10
                y = round(random.randrange(cluster[1] - size_cluster, cluster[1] + size_cluster) / 10) * 10
                cluster_food.add((x,y))
            food = food | cluster_food

    # distribute remaining pellets randomly (or all for diffuse case)
    while len(food) < num_food:
        x = round(random.randrange(xbound1, xbound2) / 10) * 10
        y = round(random.randrange(xbound1, xbound2) / 10) * 10
        food.add((x, y))

    return food
