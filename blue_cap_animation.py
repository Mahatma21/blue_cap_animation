import sys
import pygame
from pygame import mixer
import concurrent.futures


def redraw_game_window():
    global spriteCount

    # Reset spriteCount on its limit (game FPS)
    if spriteCount >= GAME_FPS:
        spriteCount = 0

    # Sprite count for animation
    drawSpriteCount = spriteCount // FRAME_PER_SPRITE
    # Jump animation
    if isJump:
        if playerDir == L:
            imgToDraw = leftJump
        else:
            imgToDraw = rightJump
    # Run animation
    elif curSprite == 'run':
        if playerDir == L:
            imgToDraw = leftRun
        else:
            imgToDraw = rightRun
    # Walk animation
    elif curSprite == 'walk':
        if playerDir == L:
            imgToDraw = leftWalk
        else:
            imgToDraw = rightWalk
    # Idle animation
    else:  # If curSprite == 'idle'
        if playerDir == L:
            imgToDraw = leftIdle
        else:
            imgToDraw = rightIdle

    # Sound effects play
    if curSprite in ('walk', 'run'):
        if spriteCount in (3, 21, 45):
            if spriteCount in (3, 45):
                step_sound_l.play()
            elif spriteCount == 21:
                step_sound_r.play()

    # Draw background and info text
    draw_bg_n_info()
    # Draw sprite
    win.blit(imgToDraw[drawSpriteCount], (playerX, playerY))

    # Increase draw index
    spriteCount += 1

    pygame.display.update()


def import_right_sprite(img_name: str) -> pygame.Surface:
    return pygame.transform.smoothscale(
        pygame.image.load(img_name),
        PLAYER_SIZE)


def flip_right_sprite(sprite):
    return pygame.transform.flip(
        sprite, 1, 0)


def close_game():
    global playerX

    mixer.music.stop()  # Stop background music

    if playerDir == L:
        playerX -= 90
        imgToDraw = leftDead
    else:
        playerX += 90
        imgToDraw = rightDead

    for spriteCount in range(GAME_FPS):
        # Limit loop speed
        clock.tick(GAME_FPS)
        # Set index for sprite
        drawSpriteCount = spriteCount // FRAME_PER_SPRITE

        # Draw background and info text
        draw_bg_n_info()
        # Draw dead animation
        win.blit(imgToDraw[drawSpriteCount], (playerX, playerY))

        pygame.display.update()

    # Closing game
    sys.exit()


def draw_bg_n_info():
    # Draw background img
    win.blit(bg, (0, 0))

    # Draw info text
    win.blit(info1, (20, 20))
    win.blit(info2, (20, 60))
    win.blit(info3, (20, 100))


# Init
pygame.init()
mixer.init(48000)

# Cinema ration = 2.35 : 1
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 1410, 600
WIN_CAPTION = "Blue Cap Animation"
WIN_ICON = "assets/icon.png"
PLAYER_SIZE = PLAYER_WIDTH, PLAYER_HEIGHT = 256, 256
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
info_font = pygame.font.Font(GLOBAL_FONT, 32)

# Set sprite imgs names
walk_img_names = [f"assets/Walk ({i}).png" for i in range(1, 16)]
jump_img_names = [f"assets/Jump ({i}).png" for i in range(1, 16)]
idle_img_names = [f"assets/Idle ({i}).png" for i in range(1, 16)]
run_img_names = [f"assets/Run ({i}).png" for i in range(1, 16)]
dead_img_names = [f"assets/Dead ({i}).png" for i in range(1, 16)]

# Set sfx names
sfx_names = ('assets/sfx_jump_HM_BTN.wav',
             'assets/sfx_step_grass_l.flac',
             'assets/sfx_step_grass_r.flac')

# Import player sprite with resize using Thread
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Import sprite imgs
    rightWalk = tuple(executor.map(import_right_sprite, walk_img_names))
    rightJump = tuple(executor.map(import_right_sprite, jump_img_names))
    rightIdle = tuple(executor.map(import_right_sprite, idle_img_names))
    rightRun = tuple(executor.map(import_right_sprite, run_img_names))
    rightDead = tuple(executor.map(import_right_sprite, dead_img_names))

    # Flip sprite imgs
    leftWalk = tuple(executor.map(flip_right_sprite, rightWalk))
    leftJump = tuple(executor.map(flip_right_sprite, rightJump))
    leftIdle = tuple(executor.map(flip_right_sprite, rightIdle))
    leftRun = tuple(executor.map(flip_right_sprite, rightRun))
    leftDead = tuple(executor.map(flip_right_sprite, rightDead))

    # Import sfx
    jump_sound, step_sound_l, step_sound_r = tuple(
        executor.map(mixer.Sound, sfx_names))

# Remove unused sprite imgs names
del walk_img_names
del jump_img_names
del idle_img_names
del run_img_names
del dead_img_names

# Import background image
bg = pygame.transform.smoothscale(
    pygame.image.load('assets/bg.jpg'),
    WIN_SIZE)
# Set sfx volume
jump_sound.set_volume(0.7)
step_sound_l.set_volume(0.6)
step_sound_r.set_volume(0.6)
# Import backsound
backsound = mixer.music.load('assets/backsound.wav')

# Play background music
mixer.music.set_volume(0.15)  # Reduce backsound volume
mixer.music.play(-1)

# Create main window
win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption(WIN_CAPTION)
pygame.display.set_icon(pygame.image.load(WIN_ICON))
# Game clock
clock = pygame.time.Clock()

# Info text
info1 = info_font.render(
    "- ARROW KEYS to walk", 1, (0, 0, 0))
info2 = info_font.render(
    "- LSHIFT + ARROW KEYS to run", 1, (0, 0, 0))
info3 = info_font.render("- SPACE to jump", 1, (0, 0, 0))

# Player starting point
playerX = (WIN_WIDTH / 2) - PLAYER_WIDTH
playerY = WIN_HEIGHT - PLAYER_HEIGHT - 20
playerVel = 0
spriteCount = 0
prevSprite = 'idle'
curSprite = 'idle'
# Player sprite
playerDir = R  # Player direction
jumpCount = JUMP_VEL
isJump = 0
isJumpDelay = 0
jumpDelayCount = 0
isGameClose = 0

# Mainloop
while 1:
    # The game framerate
    clock.tick(GAME_FPS)

    # Quiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game()

    # Take the pressed keys from user
    keys = pygame.key.get_pressed()
    # Idle when L and R clicked or both is not clicked
    if not (keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]):  # If L and R not pressed
        # Make the sprite idle
        curSprite = 'idle'
    # Walk if L or R clicked
    else:
        if keys[pygame.K_LEFT]:  # Left key pressed
            playerDir = L
        elif keys[pygame.K_RIGHT]:  # Right key pressed
            playerDir = R
        # Change sprite condition
        curSprite = 'walk'

    # Player vel
    # Not moving if player idle or jump delay
    if curSprite == 'idle' or isJumpDelay:
        playerVel = 0
    # If player jumping
    elif isJump:
        playerVel = jumpVel
    # If player running
    elif keys[pygame.K_LSHIFT]:
        curSprite = 'run'
        playerVel = PLAYER_RUN_VEL
    else:  # If player == 'walk'
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
            isJump = 1
            isJumpDelay = 1
            # Determine jump velocity
            if curSprite == 'idle':
                jumpVel = 0
            elif keys[pygame.K_LSHIFT]:
                jumpVel = PLAYER_RUN_VEL
            else:
                jumpVel = PLAYER_WALK_JUMP_VEL
    else:  # If isJump
        curSprite = 'jump'
        if not isJumpDelay:
            if jumpCount >= -JUMP_VEL:
                playerY -= (jumpCount / 2)
                jumpCount -= 1
            else:
                jumpCount = JUMP_VEL  # Reset jumpCount for next jump
                spriteCount = 0  # Reset spriteCount for next animation
                isJump = 0  # Stop jump
        else:  # If jumpDelay
            if jumpDelayCount >= JUMP_DELAY:
                jump_sound.play()  # Play jump sound effect
                isJumpDelay = 0  # Stop jump delay
                jumpDelayCount = 0  # Reset jumpDelayCount for next jump
            else:
                jumpDelayCount += 1

    # Reset spriteCount if player condition is different
    if prevSprite != curSprite:
        # Play landed sfx after jump
        if prevSprite == 'jump' and curSprite == 'idle':
            step_sound_r.play()

        prevSprite = curSprite
        spriteCount = 0

    # Game Border
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIN_WIDTH - PLAYER_WIDTH:
        playerX = WIN_WIDTH - PLAYER_WIDTH

    redraw_game_window()
