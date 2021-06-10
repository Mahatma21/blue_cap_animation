import pygame
from pygame import mixer


def redraw_game_window():
    global spriteCount
    # Draw background img
    win.blit(bg, (0, 0))

    # Draw info text
    win.blit(info1, (20, 20))
    win.blit(info2, (20, 60))
    win.blit(info3, (20, 100))

    # Reset spriteCount on its limit (game FPS)
    if spriteCount >= GAME_FPS:
        spriteCount = 0

    # Sprite count for animation
    drawSpriteCount = spriteCount // FRAME_PER_SPRITE

    # Jump animation
    if isGameClose:
        if playerDir == L:
            imgToDraw = leftDead
        else:
            imgToDraw = rightDead
    elif isJump:
        if playerDir == L:
            imgToDraw = leftJump
        else:
            imgToDraw = rightJump
    # Run animation
    elif spriteCond == 'run':
        if playerDir == L:
            imgToDraw = leftRun
        else:
            imgToDraw = rightRun
    # Walk animation
    elif spriteCond == 'walk':
        if playerDir == L:
            imgToDraw = leftWalk
        else:
            imgToDraw = rightWalk
    # Idle animation
    else:  # If spriteCond == 'idle'
        if playerDir == L:
            imgToDraw = leftIdle
        else:
            imgToDraw = rightIdle

    # Draw sprite
    win.blit(imgToDraw[drawSpriteCount], (playerX, playerY))

    # Sound effects play
    if spriteCond in ('walk', 'run'):
        if spriteCount in (3, 21, 45):
                if spriteCount in (3, 45):
                    step_sound_l.play()
                elif spriteCount == 21:
                    step_sound_r.play()

    spriteCount += 1

    pygame.display.update()


# Init
pygame.init()
mixer.init(48000)

# Cinema ration = 2.35 : 1
WIN_WIDTH = 1410
WIN_HEIGHT = 600
PLAYER_WIDTH = 256
PLAYER_HEIGHT = 256
JUMP_VEL = 17
PLAYER_WALK_VEL = 3
PLAYER_WALK_JUMP_VEL = 5
PLAYER_RUN_VEL = 8
JUMP_DELAY = 9  # 3 Sprite images * 3 FPS per sprite image
GAME_FPS = 45
FRAME_PER_SPRITE = 3

# Move directions
L = 'left'
R = 'right'

# Font
GLOBAL_FONT = "assets/caramel_sweets.ttf"
INFO_FONT = pygame.font.Font(GLOBAL_FONT, 32)

# Import player animation with resize
rightWalk = []
rightJump = []
rightIdle = []
rightRun = []
rightDead = []

leftWalk = []
leftJump = []
leftIdle = []
leftRun = []
leftDead = []

# Import player sprite images
for i in range(1, 16):
    rightWalk.append(
        pygame.transform.smoothscale(
            pygame.image.load(f'assets/Walk ({i}).png'),
            (PLAYER_WIDTH, PLAYER_HEIGHT)))
    rightJump.append(
        pygame.transform.smoothscale(
            pygame.image.load(f'assets/Jump ({i}).png'),
            (PLAYER_WIDTH, PLAYER_HEIGHT)))
    rightIdle.append(
        pygame.transform.smoothscale(
            pygame.image.load(f'assets/Idle ({i}).png'),
            (PLAYER_WIDTH, PLAYER_HEIGHT)))
    rightRun.append(
        pygame.transform.smoothscale(
            pygame.image.load(f'assets/Run ({i}).png'),
            (PLAYER_WIDTH, PLAYER_HEIGHT)))
    rightDead.append(
        pygame.transform.smoothscale(
            pygame.image.load(f'assets/Dead ({i}).png'),
            (PLAYER_WIDTH, PLAYER_HEIGHT)))

    leftWalk.append(pygame.transform.flip(rightWalk[-1], True, False))
    leftJump.append(pygame.transform.flip(rightJump[-1], True, False))
    leftIdle.append(pygame.transform.flip(rightIdle[-1], True, False))
    leftRun.append(pygame.transform.flip(rightRun[-1], True, False))
    leftDead.append(pygame.transform.flip(rightDead[-1], True, False))

# Import background image
bg = pygame.transform.smoothscale(
    pygame.image.load('assets/bg.jpg'),
    (WIN_WIDTH, WIN_HEIGHT))
# Import sound
jump_sound = mixer.Sound('assets/sfx_jump_HM_BTN.wav')
jump_sound.set_volume(0.7)
step_sound_l = mixer.Sound('assets/sfx_step_grass_l.flac')
step_sound_l.set_volume(0.6)
step_sound_r = mixer.Sound('assets/sfx_step_grass_r.flac')
step_sound_r.set_volume(0.6)
backsound = mixer.music.load('assets/backsound.wav')

# Play background music
mixer.music.set_volume(0.15)  # Reduce backsound volume
mixer.music.play(-1)

# Create main window
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Sprite Animation")
pygame.display.set_icon(pygame.image.load("assets/logo_py.png"))
# Game clock
clock = pygame.time.Clock()

# Info text
info1 = INFO_FONT.render(
    "- ARROW KEYS to walk", True, (0, 0, 0))
info2 = INFO_FONT.render(
    "- LSHIFT + ARROW KEYS to run", True, (0, 0, 0))
info3 = INFO_FONT.render("- SPACE to jump", True, (0, 0, 0))

# Player starting point
playerX = (WIN_WIDTH / 2) - PLAYER_WIDTH
playerY = WIN_HEIGHT - PLAYER_HEIGHT - 20
playerVel = 0
spriteCount = 0
prevSprite = 'idle'
spriteCond = 'idle'
# Player sprite
playerDir = R  # Player direction
jumpCount = JUMP_VEL
isJump = False
isJumpDelay = False
jumpDelayCount = 0
isGameClose = False

# Mainloop
running = True
while running:
    # The game framerate
    clock.tick(GAME_FPS)

    if not isGameClose:
        # Quiting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if playerDir == L:
                    playerX -= 90
                else:
                    playerX += 90

                mixer.music.stop()  # Stop background music
                spriteCount = 0  # For dead animation
                spriteCond = 'dead'
                isGameClose = True

        # Take the pressed keys from user
        keys = pygame.key.get_pressed()
        # Player
        # Idle when L and R clicked or both is not clicked
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] 
            or not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])):
            # Make the sprite idle
            spriteCond = 'idle'
        # Walk if L or R clicked
        else:
            if keys[pygame.K_LEFT]:  # Left key pressed
                playerDir = L
            elif keys[pygame.K_RIGHT]:  # Right key pressed
                playerDir = R
            # Change sprite condition
            spriteCond = 'walk'

        # Player vel
        if spriteCond != 'idle' and not isJumpDelay:
            if keys[pygame.K_LSHIFT]:  # If player running
                spriteCond = 'run'
                playerVel = PLAYER_RUN_VEL
            else:  # If player not running
                if isJump:
                    playerVel = PLAYER_WALK_JUMP_VEL
                else:
                    playerVel = PLAYER_WALK_VEL
            # Player move direction
            if playerDir == L:
                playerVel = -playerVel
            else:
                playerVel = playerVel
            # Moving player sprite
            playerX += playerVel

        # Player jump
        if not isJump:
            if keys[pygame.K_SPACE]:
                spriteCount = 0  # Reset sprite count for jump animation
                isJump = True
                isJumpDelay = True
        else:  # If isJump
            spriteCond = 'jump'
            if not isJumpDelay:
                if jumpCount >= -JUMP_VEL:
                    playerY -= (jumpCount / 2)
                    jumpCount -= 1
                else:
                    jumpCount = JUMP_VEL  # Reset jumpCount for next jump
                    spriteCount = 0  # Reset spriteCount for next animation
                    isJump = False  # Stop jump
            else:  # If jumpDelay
                if jumpDelayCount >= JUMP_DELAY:
                    jump_sound.play()  # Play jump sound effect
                    isJumpDelay = False  # Stop jump delay
                    jumpDelayCount = 0  # Reset jumpDelayCount for next jump
                else:
                    jumpDelayCount += 1

        # Reset spriteCount if player condition is different
        if prevSprite != spriteCond:
            prevSprite = spriteCond
            spriteCount = 0

    else:
        if spriteCount + 1 >= GAME_FPS:
            running = False

    # Game Border
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIN_WIDTH - PLAYER_WIDTH:
        playerX = WIN_WIDTH - PLAYER_WIDTH

    redraw_game_window()
