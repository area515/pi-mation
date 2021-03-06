#!/usr/bin/env python

# Pi-Mation v0.5
# Stop motion animation for the Raspberry Pi and camera module
# Russell Barnes - 12 Nov 2013 for Linux User magazine issue 134 
# www.linuxuser.co.uk

import pygame, picamera, os, sys, time, dropbox, RPi.GPIO as GPIO, datetime, json, glob

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP) # OK
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Not_OK
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Not used
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Done

# global variables
pics_taken = 0
current_alpha, next_alpha = 128, 255
animation_done = 0
trigger = 0
width = 2592
height = 1944

# Get your app key and secret from the Dropbox developer website
app_key = 'INSERT_APP_KEY'
app_secret = 'INSERT_APP_SECRET'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# set your desired fps (~5 for beginners, 10+ for advanced users)
fps = 4

# set max pics
max_pics = 40

# Initialise Pygame, start screen and camera
pygame.init()
res = pygame.display.list_modes() # return the best resolution for your monitor
width, height = res[0] # Having trouble getting the right resolution? Manually set with: 'width, height = 1650, 1050' (where the numbers match your monitor)
print ("Reported resolution is:" +str(width) + "x" + str(height))

#Intro (splash) screen pic
intro_pic = pygame.image.load(os.path.join('data', 'intro_screen.jpg'))
intro_pic_fix = pygame.transform.scale(intro_pic, (width, height))

# intro custome screen
start_pic_custom = pygame.image.load(os.path.join('/home/pi/animation/data', 'Opening_Screen.jpg'))
start_pic_fix_custom = pygame.transform.scale(start_pic_custom, (width, height))

#Banner screen pic
banner_custom = pygame.image.load(os.path.join('data', 'banner_custom.jpg'))
#banner_fix_custom = pygame.transform.scale(start_pic_custom, (width, height/10))

#Help screen pic
help_pic = pygame.image.load(os.path.join('data', 'help_screen.jpg'))
help_pic_fix = pygame.transform.scale(help_pic, (width, height))

#Animate screen pic
animate_pic = pygame.image.load(os.path.join('data', 'animate_screen.jpg'))
animate_pic_fix = pygame.transform.scale(animate_pic, (width, height))

#Video processing screen pic
video_pic = pygame.image.load(os.path.join('data', 'video_processing_screen.jpg'))
video_pic_fix = pygame.transform.scale(video_pic, (width, height))

# Finished processing screen pic
finished_pic = pygame.image.load(os.path.join('data', 'finished_screen.jpg'))
finished_pic_fix = pygame.transform.scale(finished_pic, (width, height))

screen = pygame.display.set_mode([width, height])
pygame.display.toggle_fullscreen()
pygame.mouse.set_visible = False
play_clock = pygame.time.Clock()
camera = picamera.PiCamera()
camera.resolution = (width, height)
#camera.resolution = (640,380)
camera.vflip = True
camera.hflip = True

# sanity check
print ("Width")
print (pygame.display.Info().current_w)
print (width)
print ("Height")
print (pygame.display.Info().current_h)
print (height)

def take_pic():
    """Grabs an image and load it for the alpha preview and 
    appends the name to the animation preview list"""
    background = pygame.Surface([width, height])
    background = background.convert()
    background.fill((0,0,0))
    screen.fill((0,0,0))
    global pics_taken, prev_pic
    pics_taken += 1
    camera.capture(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'), use_video_port = True)
    prev_pic = pygame.image.load(os.path.join('pics', 'image_' + str(pics_taken) + '.jpg'))
    if(pics_taken > max_pics):
        print ("maximum picture limit has been reached")
        print ("making movie")
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
    global animation_done, repeat_loop
    camera.stop_preview()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    screen.fill((0,0,0))
    for pic in range(1, pics_taken):
        anim = pygame.image.load(os.path.join('pics', 'image_' + str(pic) + '.jpg'))
        screen.blit(anim, (0, 0))
        #screen.blit(anim, (600, 350))
        play_clock.tick(fps)
        pygame.display.flip()
    play_clock.tick(fps)
    screen.blit(animate_pic_fix, (0, 0))
    pygame.display.update()
     #camera.start_preview()
    animate_again=0
"""    while animate_again == 0:
        time.sleep(0.10)
        if GPIO.input(17) == 0:
            animate_again = 1
        elif GPIO.input(22) == 0:
            repeat_loop = 1 # break the loop after animate
            animate_again = 1
        elif GPIO.input(18) == 0:
            restart_app()
    animation_done = 1"""

def animate_repeat():
    global repeat
    animation_done = 0
    animate()
    repeat += repeat

def update_display():
    """Blit the screen (behind the camera preview) with the last picture taken"""
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    screen.fill((0,0,0))
    global pic_loop
    if pics_taken > 0:
        screen.blit(prev_pic, (0, 0))
        screen.blit(banner_custom, (100,750))
    play_clock.tick(30)
    print ("Picture Number " + str(pics_taken) + " of " + str(max_pics))
    #display the total pics taken
    main_surface=pygame.display.get_surface()
    font=pygame.font.Font(None,30)
    frame_number=font.render("Picture Number " + str(pics_taken) + " of " + str(max_pics), 1, (255,255,0))
    main_surface.blit(frame_number, (100, 100))
    pygame.display.update()
    pygame.display.flip()
    keep_pic=0
    while keep_pic == 0:
        time.sleep(0.10)
        if GPIO.input(17) == 0:
            keep_pic = 1
        elif GPIO.input(22) == 0:
            delete_pic()
            keep_pic = 1
        elif GPIO.input(18) == 0:
            #restart_app()
            pic_loop = 1
            keep_pic = 1
    debounce_input = 1
    while debounce_input:
        if GPIO.input(17) == 1:
            debounce_input = 0

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
    print ("You've taken " + str(pics_taken) + " pictures. Don't forget to back them up (or they'll be overwritten next time)")
    sys.exit(410)

def quit_app():
    """Cleanly closes the camera and the application"""
    camera.close()
    pygame.quit()
    print ("You've taken " + str(pics_taken) + " pictures. Don't forget to back them up (or they'll be overwritten next time)")
    sys.exit(0)

def help_screen():
    """Application starts on the help screen. User can exit 
    or start Pi-Mation proper from here"""
    intro = True
    while intro:
        time.sleep(0.10)
        if GPIO.input(18) == 0:
            restart_app()
        elif GPIO.input(17) == 0:
            camera.start_preview()
            intro = False
        screen.blit(help_pic_fix, (0, 0))
        pygame.display.update()
        background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    screen.fill((0,0,0))
    time.sleep(0.20)

def intro_screen():
    """Application starts on a custom splash screen.  User can exit
    or start Pi-mation proper from here"""
    intro = True
    screen.blit(intro_pic_fix, (0, 0))
    pygame.display.update()
    while intro:
        time.sleep(0.10)
        if GPIO.input(18) == 0:
            restart_app()
        elif GPIO.input(17) == 0:
            intro = False
    debounce_input = 1
    while debounce_input:
        if GPIO.input(17) == 1:
            debounce_input = 0

def video_screen():
    """Application displays while compiling movie. User can exit 
    from here"""
    screen.blit(video_pic_fix, (0, 0))
    pygame.display.update()
    time.sleep(5)

def all_done_screen():
    """Application displays while compiling movie. User can exit 
    from here"""
    screen.blit(finished_pic_fix, (0, 0))
    pygame.display.update()
    time.sleep(5)

def animate_screen():
    """Application displays while compiling movie. User can exit 
    from here"""
    screen.blit(animate_pic_fix, (0, 0))
    pygame.display.update()

def dropbox_upload():
    """Following the creation of a movie and user approval, movie will
    be uploaded to Dropbox with time/date stamp"""

    #f = open(os.path.join('video_' + str(vid) + '.mp4', 'rb')
    #response = client.put_file(os.path.join('video_' + str(vid) + '.mp4', f))
    #print ("Uploaded:", response)
    if (3,0) <= sys.version_info < (4,0):
        import http.client as httplib
    elif (2,6) <= sys.version_info < (3,0):
        import httplib

    headers = {
        "Authorization": "Bearer zacin5fBx2AAAAAAAAAADvIh9LlKb9R25LK072jFD3DTZp8UOWAX32tF5HIyCK9R",
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": "{\"path\":\"/home/pi/animation\",\"mode\":{\".tag\":\"add\"},\"autorename\":true,\"mute\":false}"
    }
    
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    movie_name=str('pimation_' + timestamp + '.mp4')
    os.rename("video.mp4",movie_name)
    data = open(movie_name, "rb")
    
    c = httplib.HTTPSConnection("content.dropboxapi.com")
    c.request("POST", "/2/files/upload", data, headers)
    r = c.getresponse()
    print(r)

def make_movie():
    """Quit out of the application 
    and create a movie with your pics"""
    camera.stop_preview()
    # display the video processing screen
    screen.blit(video_pic_fix, (0, 0))
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    print ("\nQuitting Pi-Mation to transcode your video.\nWarning: this may take a long time!")
    print ("\nOnce complete, write 'omxplayer video.mp4' in the terminal to play your video.\n")
    #os.system("avconv -y -r " + str(fps) + " -i " + str(os.path.join('pics', 'image_%d.jpg')) + " -vcodec libx264 video.mp4")
    os.system("avconv -y -r " + str(fps) + " -i " + str((os.path.join('pics', 'image_%d.jpg'))) + " -vcodec libx264 video.mp4")
    #os.system("./upload-stage.sh video.mp4 ../upload/")
    #pygame.quit()
    print ("\nMade movie\n")
    #sys.exit(410)
    files = glob.glob('/home/pi/animation/pics/*')
    for f in files:
        os.remove(f)
    dropbox_upload()
    #os._ext(0)

def main():
    while True:
        status = 1
        print("GPIO 17 = " + str(GPIO.input(17)))
        intro_screen()
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0,0,0))
        screen.fill((0,0,0))
        time.sleep(0.50)
        camera.start_preview()
        #help_screen()
        pic_loop = 0
        pics_done = 1
        time.sleep(0.50)
        while (pics_taken < max_pics) and pic_loop == 0:
            time.sleep(0.10)
            if GPIO.input(17) == 0:
                take_pic()
                time.sleep(0.10)
                camera.stop_preview()
                time.sleep(0.10)
                update_display()
                camera.start_preview()
                time.sleep(0.20)
                debounce_input = 1
                while debounce_input:
                    if GPIO.input(17) == 1:
                        debounce_input = 0
                    elif (GPIO.input(18) == 0):
                        debounce_input = 1
                while debounce_input:
                    if GPIO.input(18) == 1:
                        debounce_input = 0
                pic_loop = 1
        camera.stop_preview()
        #screen.blit(finished_pic_fix, (0, 0))
        pygame.display.update()
        animation_done = 0
        time.sleep(0.20)
        animate_repeat = 1
        animate()
        repeat_loop = 0
        time.sleep(0.20)
        while (animate_repeat < 3) and repeat_loop == 0:
            time.sleep(0.10)
            if GPIO.input(17) == 0:
                debounce_input = 1
                time.sleep(0.20)
                while debounce_input:
                    time.sleep(0.10)
                    if GPIO.input(17) == 1:
                        debounce_input = 0
                    elif GPIO.input(18) == 0:
                        debounce_input = 0
                animate()
                animate_repeat += 1
                time.sleep(0.20)
            elif (GPIO.input(18) == 0) or (GPIO.input(22) == 0):
                repeat_loop = 1
        #GPIO.cleanup()
        #restart_app()
        
        # future stuff for when on the network
        while pics_done:
            time.sleep(0.10)
            all_done = 1
            while all_done:
                make_movie()
                all_done = 0
                pics_done = 0

if __name__ == '__main__':
    main()
