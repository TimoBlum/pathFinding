import pygame, random
pygame.init()

xy = 500
rows = 20
spacebtwn = 25
win = pygame.display.set_mode((xy, xy))
clock = pygame.time.Clock()
started = False
run = True
frames = 0
wayfinderIterations = 1
world = []
start = ()
end = ()
absDistance = 0
ways = []


def drawCube(color, position):
    pygame.draw.rect(win, color, (position[0], position[1], 25, 25))


def drawGrid():
    global win, xy
    x = 0
    y = 0
    for l in range(rows):
        pygame.draw.line(win, (230, 230, 230), (x, 0), (x, xy))
        pygame.draw.line(win, (230, 230, 230), (0, y), (xy, y))

        x = x + spacebtwn
        y = y + spacebtwn


def placeStartEnd():
    global start, end, absDistance
    start = (random.randrange(1, 19), random.randrange(1, 19))
    end = (random.randrange(1, 19), random.randrange(1, 19))
    absDistance = (abs(end[1] - start[1]) + abs(end[0] - start[0]))
    print(absDistance)
    world[start[0]][start[1]] = 2
    world[end[0]][end[1]] = 3


def drawWorld():
    rowcounter = 0
    for row in world:
        tilecounter = 0
        for tile in row:
            if tile == 1:
                drawCube((0, 0, 0), (tilecounter * 25, rowcounter * 25))
            if tile == 2:
                drawCube((255, 0, 0), (tilecounter * 25, rowcounter * 25))
            if tile == 3:
                drawCube((0, 255, 0), (tilecounter * 25, rowcounter * 25))
            tilecounter += 1
        rowcounter += 1


def makeWorld():
    for row in range(0, rows):
        world.append([])
        for tile in range(0, rows):
            if row == 0 or row == rows - 1:
                world[row].append(1)
            elif tile == 0 or tile == rows - 1:
                world[row].append(1)
            else:
                world[row].append(0)


def drawAtWill():
    mpos = pygame.mouse.get_pos()
    mpress = pygame.mouse.get_pressed(3)
    if mpress[0] and world[int(mpos[1]/25)][int(mpos[0]/25)] == 0:
        world[int(mpos[1]/25)][int(mpos[0]/25)] = 1


def checkForStart():
    # sets started to True if the user wishes to start finding the way
    global started
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        started = True


def showBestWay():
    ways.sort(key=lambda x: x[1])
    if ways != []:
        for node in ways[0][0]:
            drawCube((128, 0, 128), (node[1]*25, node[0]*25))


def wayFinder():
    global ways
    visited = []
    steps = 0
    crashed = 0
    endnode = start
    while endnode != end:
        # moving up, down, left or right
        upwards = random.randrange(-1, 2)
        if upwards == 0:
            sidewards = random.randrange(-1, 2, 2)
        else:
            sidewards = 0

        # checking if new node is possible and abandoning way if too inefficient
        if crashed > 5:
            break
        if (endnode[0] + upwards, endnode[1] + sidewards) in visited:
            crashed += 1
            continue
        elif world[endnode[0] + upwards][endnode[1] + sidewards] == 1:
            crashed += 1
            continue
        crashed = 0

        endnode = (endnode[0] + upwards, endnode[1] + sidewards)
        visited.append(endnode)
        steps += 1
        if steps > absDistance*10:
            break
        if endnode == end:
            print("FOUND A WAY WITH " + str(steps) + " STEPS")
            ways.append((visited, steps))


def redrawWin():
    global wayfinderIterations
    win.fill((255, 255, 255))
    drawGrid()
    drawAtWill()
    if started:
        wayFinder()
        print("looked at " + str(wayfinderIterations) + ' different ways by now')
        wayfinderIterations += 1
        showBestWay()
    drawWorld()
    checkForStart()
    pygame.display.update()


def main():
    global run
    while run:
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if run:
            redrawWin()


makeWorld()
placeStartEnd()
print(start, end)
main()
