
from service.song import SongService
from service.playlist import PlaylistService


if __name__ == '__main__':
    song = SongService(["test_music/Westlife - Nothing's Gonna Change My Love For You.mp3",])
    # play the song. The song will be played and you cant do anything till song_length + 100 ms 
    song.play()
    song.wait(5)
    # song.pause()
    # song.wait(5)
    # song.resume()

