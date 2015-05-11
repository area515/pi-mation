#!/usr/bin/env python

# Pi-Mation v0.5
# Stop motion animation for the Raspberry Pi and camera module
# Russell Barnes - 12 Nov 2013 for Linux User magazine issue 134 
# www.linuxuser.co.uk

import pygame, picamera, os, sys

# global variables
pics_taken = 0
current_alpha, next_alpha = 128, 255

# set your desired fps (~5 for beginners, 10+ for advanced users)
fps = 5

# set max pics
max_pics = 40

# Initialise Pygame, start screen and camera
pygame.init()
res = pygame.display.list_modes() # return the best resolution for your monitor
width, height = res[0] # Having trouble getting the right resolution? Manually set with: 'width, height = 1650, 1050' (where the numbers match your monitor)
print "Reported resolution is:", width, "x", height

#Intro (splash) screen pic
intro_pic = pygame.image.load(os.path.join('data', 'intro_screen.jpg'))
intro_pic_fix = pygame.transform.scale(intro_pic, (width, height))

#Banner screen pic
#banner_custom = pygame.image.load(os.path.join('data', 'banner_custom.jpg'))
#banner_fix_custom = pygame.transform.scale(start_pic_custom, (width, height/10))

#Help screen pic
help_pic = pygame.image.load(os.path.join('data', 'help_screen.jpg'))
help_pic_fix = pygame.transform.scale(help_pic, (width, height))

#Video processing screen pic
video_pic = pygame.image.load(os.path.join('data', 'video_processing_screen.jpg'))
video_pic_fix = pygame.transform.scale(video_pic, (width, height))

screen = pygame.display.set_mode([width, height])
pygame.display.toggle_fullscreen()
pygame.mouse.set_visible = False
play_clock = pygame.time.Clock()
camera = picamera.PiCamera()
camera.resolution = (width, height)

# sanity check
print "Width"
print pygame.display.Info().current_w
print "Height"
print pygame.display.Info().current_h

def take_pic():
    """Grabs an image and load it for the alpha preview and 
    appends the name to the animation preview list"""
    global pics_taken, prev_pic
    pics_taken += 1
    camera.capture(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'), use_video_port = True)
    prev_pic = pygame.image.load(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'))
    if(pics_taken > max_pics):
        print "maximum picture limit has been reached"
        print "making movie"
        make_movie()


def delete_pic():
    """Doesn't actually delete the last picture, but the preview will 
    update and it will be successfully overwritten the next time you take a shot"""
    global pics_taken, prev_pic
    if pics_taken > 0:
        pics_taken -= 1
	if pics_taken >= 1:
	    prev_pic = pygame.image.load(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'))
        
def animate():
    """Do a quick live preview animation of 
    all current pictures taken"""
    camera.stop_preview()
    for pic in range(1, pics_taken):
        anim = pygame.image.load(os.path.join('pics', 'image_' + str(pic) + '.jpg'))
        screen.blit(anim, (0, 0))
        play_clock.tick(fps)
        pygame.display.flip()
    play_clock.tick(fps)
    camera.start_preview()

def update_display():
    """Blit the screen (behind the camera preview) with the last picture taken"""
    screen.fill((0,0,0))
    if pics_taken > 0:
        screen.blit(prev_pic, (0, 0))
        #screen.blit(banner_fix_custom, (0,0))
    play_clock.tick(30)
    print "Picture Number " + str(pics_taken) + " of " + str(max_pics)
    #display the total pics taken
    main_surface=pygame.display.get_surface()
    font=pygame.font.Font(None,30)
    frame_number=font.render("Picture Number " + str(pics_taken) + " of " + str(max_pics), 1, (255,255,0))
    main_surface.blit(frame_number, (100, 700))
    pygame.display.update()
    pygame.display.flip()

def make_movie():
    """Quit out of the application 
    and create a movie with your pics"""
    camera.stop_preview()
    # display the video processing screen
    screen.blit(video_pic_fix, (0, 0))
    pygame.display.update()
    #pygame.quit()
    print "\nQuitting Pi-Mation to transcode your video.\nWarning: this will take a long time!"
    print "\nOnce complete, write 'omxplayer video.mp4' in the terminal to play your video.\n"
    os.system("avconv -y -r " + str(fps) + " -i " + str((os.path.join('pics', 'image_%d.jpg'))) + " -vcodec libx264 video.mp4")
    pygame.quit()
    print "\nMade movie -- debug.\n"
    sys.exit(410)
    
def change_alpha():
    """Toggle's camera preview optimacy between half and full."""
    global current_alpha, next_alpha
    camera.stop_preview()
    current_alpha, next_alpha = next_alpha, current_alpha
    return next_alpha
    
def restart_app():
    """Cleanly closes the camera and the application"""
    camera.close()
    pygame.quit()
    print "You've taken", pics_taken, " pictures. Don't forget to back them up (or they'll be overwritten next time)"
    sys.exit(410)

def quit_app():
    """Cleanly closes the camera and the application"""
    camera.close()
    pygame.quit()
    print "You've taken", pics_taken, " pictures. Don't forget to back them up (or they'll be overwritten next time)"
    sys.exit(0)

def help_screen():
    """Application starts on the help screen. User can exit 
    or start Pi-Mation proper from here"""
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_app()
                elif event.key == pygame.K_r:
                    restart_app()
                elif event.key == pygame.K_F1:
                    camera.start_preview()
                    intro = False
        screen.blit(help_pic_fix, (0, 0))
        pygame.display.update()

def intro_screen():
    """Application starts on a custom splash screen.  User can exit
    or start Pi-mation proper from here"""
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_app()
                elif event.key == pygame.K_r:
                    restart_app()
                elif event.key == pygame.K_F1:
                    camera.start_preview()
                    intro = False
        screen.blit(intro_pic_fix, (0, 0))
        pygame.display.update()


def main():
    """Begins on the help screen before the main application loop starts"""
    intro_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_app()
                elif event.key == pygame.K_SPACE:
                    take_pic()
                elif event.key == pygame.K_BACKSPACE:
                    delete_pic()
                elif event.key == pygame.K_RETURN:
                    make_movie()
                elif event.key == pygame.K_TAB:
                    camera.preview_alpha = change_alpha()
                    camera.start_preview()
                elif event.key == pygame.K_F1:
                    camera.stop_preview()
                    help_screen()
                elif event.key == pygame.K_r:
                    restart_app()
                elif event.key == pygame.K_p:
                    if pics_taken > 1:
                        animate()
        update_display()

if __name__ == '__main__':
    main()
