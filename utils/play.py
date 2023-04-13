import pygame
import json
import sqlite3
import os
from mutagen.mp3 import MP3
from time import sleep


class MusicPlayer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Music Player")
        self.font = pygame.font.SysFont(None, 36)
        self.music_list = self.get_music_list()
        self.current_music_index = 0
        self.MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../music/')
        self.current_music = self.MUSIC_DIR + self.music_list[self.current_music_index]
        pygame.mixer.music.load(self.current_music)
        self.START_VOLUME = 0.5
        self.VOLUME_CHANGE = 0.1
        pygame.mixer.music.set_volume(self.START_VOLUME)
        pygame.mixer.music.play()
        self.FAST_FORWARD_OFFSET = 10000
        self.change_time = 0

    def get_music_list(self):
        conn = sqlite3.connect("music.db")
        c = conn.cursor()
        c.execute("SELECT * FROM music")
        music_list = [row[1] for row in c.fetchall()]
        conn.close()
        return music_list

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toggle_playback()
                elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.volume_down()
                elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.volume_up()
                elif event.key == pygame.K_LEFT:
                    self.rewind()
                elif event.key == pygame.K_RIGHT:
                    self.fast_forward()
                elif event.key == pygame.K_UP:
                    self.previous_song()
                elif event.key == pygame.K_DOWN:
                    self.next_song()

    def toggle_playback(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def rewind(self):
        self.change_time -= self.FAST_FORWARD_OFFSET
        new_time = pygame.mixer.music.get_pos() + self.change_time
        pygame.mixer.music.set_pos(new_time / 1000)

    def fast_forward(self):
        self.change_time += self.FAST_FORWARD_OFFSET
        new_time = pygame.mixer.music.get_pos() + self.change_time
        pygame.mixer.music.set_pos(new_time / 1000)

    def previous_song(self):
        self.change_time = 0
        pygame.mixer.music.stop()
        self.current_music_index = (self.current_music_index - 1) % len(self.music_list)
        self.current_music = self.MUSIC_DIR + self.music_list[self.current_music_index]
        pygame.mixer.music.load(self.current_music)
        pygame.mixer.music.play()

    def next_song(self):
        self.change_time = 0
        pygame.mixer.music.stop()
        self.current_music_index= (self.current_music_index + 1) % len(self.music_list)
        self.current_music = self.MUSIC_DIR + self.music_list[self.current_music_index]
        pygame.mixer.music.load(self.current_music)
        pygame.mixer.music.play()

    def display_time(self):
        current_time = (pygame.mixer.music.get_pos() + self.change_time) / 1000
        audio = MP3(self.current_music)
        music_length = audio.info.length
        current_time_str = f"{int(current_time // 60):02}:{int(current_time % 60):02}"
        music_length_str = f"{int(music_length // 60):02}:{int(music_length % 60):02}"
        self.screen.fill((0, 0, 0))
        current_time_text = self.font.render(current_time_str, True, (255, 255, 255))
        music_length_text = self.font.render(music_length_str, True, (255, 255, 255))
        self.screen.blit(current_time_text, (10, 10))
        self.screen.blit(music_length_text, (500, 10))

    # write current song into music_info.json
    # def save_music_info(self):
    #     current_time = pygame.mixer.music.get_pos() // 1000
    #     music_info = {"current_music": self.current_music}
    #     with open("music_info.json", "w") as f:
    #         json.dump(music_info, f)

    def quit(self):
        pygame.mixer.music.stop()
        pygame.quit()
        exit()

    def run(self):
        while True:
            self.handle_events()
            self.display_time()
            # self.save_music_info()
            pygame.display.update()
            sleep(0.1)

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def volume_down(self):
        self.START_VOLUME -= self.VOLUME_CHANGE
        pygame.mixer.music.set_volume(self.START_VOLUME)

    def volume_up(self):
        self.START_VOLUME += self.VOLUME_CHANGE
        pygame.mixer.music.set_volume(self.START_VOLUME)


if __name__ == "__main__":
    player = MusicPlayer()
    player.run()