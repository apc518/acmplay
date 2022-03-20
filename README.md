# acmusicplayer

by Andy Chamberlain

## Setup

Python and the playsound module must be installed. You can install python at https://python.org/downloads

Once python is installed, use `pip install playsound` to install the playsound module.

Tkinter will make adding songs to your library easier. If you kept the checkbox checked when installing python, it should already be on your system. On linux you may have to use `sudo apt-get install python3-tk`.


## Usage

### Adding songs

The following will prompt you to select audio files to add.

```sh
acmplay -a
```

Then you'll be prompted as to whether the selected files should go into a playlist

### Playing songs

```sh
acmplay -s -l myplaylist # shuffle play a playlist you've created
acmplay -d newalbum # play all audio files in a directory
acmplay -f workinprogress.mp3 # play an audio file
```