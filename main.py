
from service.song import SongService


if __name__ == '__main__':
    song = SongService("test_music/Westlife - Nothing's Gonna Change My Love For You.mp3")
    song.play()
    song.wait(5)
    song.pause()
    song.wait(5)
    song.resume()

