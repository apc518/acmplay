"""
acmusicplayer by Andy Chamberlain
"""

import os
import argparse
import random
from pathlib import Path
from tkinter import filedialog

import playsound

from .editplaylist import edit_playlist

APP_DIRECTORY = os.path.join(Path.home(), ".acmusicplayer")


def create_playlist(name):
    filename = f"{name}.playlist"
    if filename not in os.listdir(APP_DIRECTORY):
        open(os.path.join(APP_DIRECTORY, filename), "w")
        print(f"New playlist \"{name}\" successfully created")
    else:
        print(f"Playlist \"{name}\" already exists")


def show_playlists():
    for item in os.listdir(APP_DIRECTORY):
        print(item.rsplit(".", 1)[0])
        with open(os.path.join(APP_DIRECTORY, item), "r") as f:
            lines = f.read().splitlines()
            f.close()
        for audio_file in lines:
            print("\t", os.path.split(audio_file)[1], sep="")


def remove_playlist(playlist):
    playlist_filename = f"{playlist}.playlist"
    if playlist_filename in os.listdir(APP_DIRECTORY):
        confirmation = input(f"Are you sure you want to remove playlist \"{playlist}\"?\nThis action cannot be undone. (Y/n) ")
        if confirmation == "Y":
            os.remove(os.path.join(APP_DIRECTORY, playlist_filename))
            print(f"Removed \"{playlist}\"")
        else:
            print(f"No action taken")
    else:
        print(f"No playlist named \"{playlist}\"\nList all playlists with `acmplay -l`")


def play_playlist(playlist_name, shuffle=False):
    fname = f"{playlist_name.lower()}.playlist"
    if fname in os.listdir(APP_DIRECTORY):
        with open(os.path.join(APP_DIRECTORY, fname), "r") as f:
            lines = f.read().splitlines()
            f.close()
        
        if shuffle:
            random.shuffle(lines)
        
        play_items(lines, playlist_name)
    else:
        print(f"Playlist \"{playlist_name}\" not found.")


def play_directory(dirpath, shuffle=False):
    if not os.path.isdir(dirpath):
        print(f"{dirpath} is not a directory.")
        return

    paths = [os.path.join(dirpath, item) for item in os.listdir(dirpath)]
    
    if shuffle:
        random.shuffle(paths)

    play_items(paths, os.path.basename(str(Path(dirpath).resolve().parent)))


def play_items(list, list_name):
    for item in list:
        play_file(item, origin=list_name)


def play_file(filepath, origin=None):
    try:
        print(f"Now playing \"{os.path.basename(filepath)}\"", f" from \"{origin}\"" if origin else "", "...", sep="")
        playsound.playsound(filepath)
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            print("KeyboardInterrupt, exiting.")
            exit(0)
        
        print(f"Error: {filepath} was not playable.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-p", "--play", metavar="PLAYLIST_NAME_OR_PATH", type=str, help="play the specified playlist, or a file or folder at the specified path")
    parser.add_argument("-i", "--inpath", type=str, help="path to an audio file or folder of audio files to be played")
    parser.add_argument("-c", "--create", metavar="PLAYLIST", type=str, help="create a new playlist with the given name")
    parser.add_argument("-l", "--library", action="store_true", help="list the playlists and tracks in your library")
    parser.add_argument("-e", "--edit", metavar="PLAYLIST", type=str, help="edit a playlist")
    parser.add_argument("-r", "--remove", metavar="PLAYLIST", type=str, help="remove a playlist")
    parser.add_argument("-s", "--shuffle", action="store_true", help="shuffle playback if there are multiple tracks")
    parser.add_argument("-n", "--nogui", action="store_true", help="do not try to use a file dialog GUI")
    args = parser.parse_args()

    try:
        from tkinter import filedialog, Tk
        use_gui = True and not args.nogui
    except:
        use_gui = False

    if not os.path.isdir(APP_DIRECTORY):
        try:
            os.mkdir(APP_DIRECTORY)
        except:
            print("Could not make application directory.")
            exit(1)

    if args.create:
        create_playlist(args.create)
    elif args.library:
        show_playlists()
    elif args.edit:
        if use_gui:
            edit_playlist(args.edit, APP_DIRECTORY, use_gui=use_gui, filedialog=filedialog, tk=Tk)
        else:
            edit_playlist(args.edit, APP_DIRECTORY)
    elif args.remove:
        remove_playlist(args.remove)
    else:
        if args.shuffle:
            print("shuffle play enabled")
        
        if args.play:
            play_playlist(args.play, shuffle=args.shuffle)
        elif args.inpath:
            if os.path.isdir(args.inpath):
                play_directory(args.inpath, shuffle=args.shuffle)
            else:
                play_file(args.inpath)
        else:
            print("No arguments given. Use `acmplayer -h` to see options.")


if __name__ == "__main__":
    main()