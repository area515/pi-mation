#!/usr/bin/python3

import picamera
import time
import RPi.GPIO as GPIO
import os
import pygame.image
import pygame.display
import pygame
from PIL import Image

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Take picture
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Accept image
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Reject image
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Done
pygame.init()
max_frames = 40

#camera = picamera.PiCamera()
#camera.capture('image.jpg')

#camera.start_preview()
#camera.vflip = False
#camera.hflip = False
#camera.brightness = 60

ratio = 1. * 80 / 50

def texts(frame_count):
   font=pygame.font.Font(None,30)
   frm_number=font.render("Picture Number " + str(frame) + "of 20", 1, (255,255,255))
   screen = pygame.display.get_surface()
   screen.blit(frm_number, (500, 457))

# Display the opening screen
picture = pygame.image.load('/home/pi/animation/Opening_Screen.jpg')
picture.get_size()
pygame.display.set_mode(picture.get_size())
main_surface = pygame.display.get_surface()
main_surface.blit(picture, (0, 0))
pygame.display.update()
GPIO.wait_for_edge(17, GPIO.RISING)
time.sleep(0.50)
GPIO.remove_event_detect(17)

with picamera.PiCamera() as camera:
    YupIAmDone = 0
    time.sleep(2)
    frame = 1
    dummyVariable = 0
    while (frame <= max_frames) :
        camera.start_preview()
        camera.resolution = (1392, 868)
        def iAmDone(channel):
            global YupIAmDone
            YupIAmDone = 1
        GPIO.add_event_detect(18, GPIO.RISING, callback=iAmDone, bouncetime=500)
        def takePicture(channel):
            global dummyVariable
            dummyVariable = 1
        GPIO.add_event_detect(17, GPIO.RISING, callback=takePicture, bouncetime=500)

        while (frame <= 20) and (GPIO.event_detected(17) == False) or (GPIO.event_detected(18) == False):
            time.sleep(0.50)
            if (dummyVariable == 1) or (YupIAmDone == 1):
                break
        print("Taking picture")
        print(frame)
        GPIO.remove_event_detect(18)
        GPIO.remove_event_detect(17)
        camera.capture('/home/pi/animation/frame%03d.jpg' % frame)
        time.sleep(.05)
        camera.stop_preview()
        picture = pygame.image.load('/home/pi/animation/frame%03d.jpg' % frame)
        picture.get_size()
        pygame.display.set_mode(picture.get_size())
        main_surface = pygame.display.get_surface()
        main_surface.blit(picture, (0, 0))
        pygame.display.update()
        #texts(frame)
        font=pygame.font.Font(None,30)
        frame_number=font.render("Picture Number " + str(frame) + " of " + str(max_frames), 1, (255,255,0))
        main_surface.blit(frame_number, (100, 700))
        message=font.render("Press Yes to use this image or No to replace it", 1, (255,255,0))
        main_surface.blit(message, (100, 750))
        pygame.display.update()
        UseImage = 0
        DummyValue = 0
        def imageOK(channel):
            global frame
            UseImage = 1
            if frames < max_frames:
               frame += 1
        GPIO.add_event_detect(17, GPIO.RISING, callback=imageOK, bouncetime=500)
        def imageNotOK(channel):
            UseImage = 2
        GPIO.add_event_detect(22, GPIO.RISING, callback=imageNotOK, bouncetime=500)

        while (GPIO.event_detected(17) == False) and (GPIO.event_detected(22) == False) and (GPIO.event_detected(18) == False):
            time.sleep(0.50)
            if (UseImage == 1) or (YupIAmDone == 1):
                #frame += 1
                break
            if YupIAmDone == 1:
                dummyVariable == 1
                break
        """#Image resizing
        im = Image.open('/home/pi/animation/frame%03d.jpg' % frame)
        (width, height) = im.size   # get size of latest picture
        if width > height * ratio:
           newwidth = int(height * ratio)
           left = width / 2 - newwidth / 2
           right = left + newwidth
           top = 0
           bottom = height
        elif width < height * ratio:
           newheight = int(width * ratio)
           top = height / 2 - newheight / 2
           bottom = top + newheight
           left = 0
           right = width
        if width != height * ratio:
           im = im.crop((left, top, right, bottom))

        im = im.resize((50, 80), Image.ANTIALIAS)
        im.save(fout, "jpeg", quality = 80)
        fout.close()"""

        #Image Resizing
        image = Image.open('/home/pi/animation/frame%03d.jpg' % frame)
        image.thumbnail((400, 640), Image.ANTIALIAS)
        image.save('/home/pi/animation/frame%03d.jpg' % frame, 'JPEG', quality = 80)

        #GPIO.cleanup()
        GPIO.remove_event_detect(27)
        GPIO.remove_event_detect(22)
        GPIO.remove_event_detect(18)
        GPIO.remove_event_detect(17)
        dummyVariable = 0
        if YupIAmDone == 1:
            break


#pygame.display.quit()
picture = pygame.image.load('/home/pi/animation/frame%03d.jpg' % frame)
picture.get_size()
pygame.display.set_mode(picture.get_size())
main_surface = pygame.display.get_surface()
main_surface.blit(picture, (0, 0))
pygame.display.update()


os.remove("timelapse.mp4")
os.system("avconv -r 6 -i /home/pi/animation/frame%03d.jpg -r 6 -vcodec libx264 -crf 20 -g 15 timelapse.mp4")
os.system("omxplayer timelapse.mp4")

