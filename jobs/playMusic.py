import pygame
import json
import sqlite3
from mutagen.mp3 import MP3
from time import sleep

# Initialize pygame
pygame.init()

# Connect to the database
conn = sqlite3.connect("music_database.db")
c = conn.cursor()

# query music list
c.execute("SELECT * FROM music")
music_list = [row[1] for row in c.fetchall()]
music_name = [row[2] for row in c.fetchall()]
music_artist = [row[3] for row in c.fetchall()]

# Get the first song in the music list
current_music_index = 0
current_music = music_list[current_music_index]

# create window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Music Player")

# set font
font = pygame.font.SysFont(None, 36)

# load music files
pygame.mixer.music.load(current_music)

# set volume
pygame.mixer.music.set_volume(0.5)

#10 seconds
FAST_FORWARD_OFFSET = 10000

#Used for fast forward
change_time = 0

# play music
pygame.mixer.music.play()

# Enter the event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exit the program
            pygame.mixer.music.stop()
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # pause/resume playback
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_LEFT:
                # rewind
                current_time = pygame.mixer.music.get_pos()
                pygame.mixer.music.rewind()
                new_time = current_time - FAST_FORWARD_OFFSET
                pygame.mixer.music.play(0, new_time // 1000)
            elif event.key == pygame.K_RIGHT:
                # fast forward
                change_time += 10000
                current_time = pygame.mixer.music.get_pos() + change_time
                new_time = current_time + FAST_FORWARD_OFFSET
                pygame.mixer.music.set_pos(new_time/1000)
            elif event.key == pygame.K_UP:
                # previous song
                pygame.mixer.music.stop()
                current_music_index = (current_music_index - 1) % len(music_list)
                current_music = music_list[current_music_index]
                pygame.mixer.music.load(current_music)
                pygame.mixer.music.play()
            elif event.key == pygame.K_DOWN:
                # next song
                pygame.mixer.music.stop()
                current_music_index = (current_music_index + 1) % len(music_list)
                current_music = music_list[current_music_index]
                pygame.mixer.music.load(current_music)
                pygame.mixer.music.play()
    
    #Update once every 0.1 second
    sleep(0.1)
    # Get the current playing time
    current_time = (pygame.mixer.music.get_pos() + change_time) / 1000

    # Format time as minutes:seconds
    audio = MP3(current_music)
    music_length = audio.info.length
    current_time_str = f"{int(current_time // 60):02}:{int(current_time % 60):02}"
    music_length_str = f"{int(music_length // 60):02}:{int(music_length % 60):02}"

    # Display current time , music length and song name
    screen.fill((0, 0, 0))
    current_time_text = font.render(current_time_str, True, (255, 255, 255))
    music_length_text = font.render(music_length_str, True, (255, 255, 255))
    current_music_text = font.render(current_music[:len(current_music)-4], True, (255, 255, 255))

    screen.blit(current_time_text, (10, 30))
    screen.blit(music_length_text, (500, 30))
    screen.blit(current_music_text, (10, 100))

    # Store play information in a json file
    music_info = {"current_music": current_music}
    with open("music_info.json", "w") as f:
        json.dump(music_info, f)

    # refresh window
    pygame.display.update()

    # close database connection
    conn.close()
