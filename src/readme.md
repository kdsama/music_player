### Dev Environment in MacOS
> Use only if you don't want to install too many dependencies on your MacOS system.

- Install and Open [XQuartz X11](https://www.xquartz.org/)
- XQuartz Settings - Safety - Allow from network clients ✓
```
# step1: build image
cd music_player
docker build -t musicplayer .

# step2: set X11 support
xhost 127.0.0.1
export DISPLAY=:0

# step3: run app
docker run -e DISPLAY=host.docker.internal:0 -it musicplayer
```