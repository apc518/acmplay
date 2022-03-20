"""
acmusicplayer by Andy Chamberlain
"""

import os
import argparse
import random
from pathlib import Path

import playsound

APP_DIRECTORY = os.path.join(Path.home(), ".acmusicplayer")


def list_music():
    for item in os.listdir(APP_DIRECTORY):
        print(item.rsplit(".", 1)[0])
        with open(os.path.join(APP_DIRECTORY, item), "r") as f:
            lines = f.read().splitlines()
            f.close()
        for audio_file in lines:
            print("\t", os.path.split(audio_file)[1], sep="")


def add_one_filename(playlist, in_filename):
    playlist_filepath = os.path.join(APP_DIRECTORY, f"{playlist}.playlist")
    if not os.path.isfile(playlist_filepath):
        with open(playlist_filepath, "w") as f:
            f.write(in_filename)
    else:
        with open(playlist_filepath, "r") as f:
            old_content = f.read()
        
        with open(playlist_filepath, "w") as f:
            f.write(f"{old_content}\n{in_filename}")


def create_playlist(name):
    filename = f"{name}.playlist"
    if filename not in os.listdir(APP_DIRECTORY):
        open(os.path.join(APP_DIRECTORY, filename), "w")
        print(f"New playlist \"{name}\" successfully created")
    else:
        print(f"Playlist \"{name}\" already exists")



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


def add_music(filedialog=None, tk=None):
    if filedialog:
        tk().withdraw()
        filenames = filedialog.askopenfilenames()
        if len(filenames) < 1: return

        in_playlist = input("Playlist (if it does not exist a new one will be created): ")
        for name in filenames:
            add_one_filename(in_playlist, name)
    else:
        # add it through the command line
        in_filename = input("Enter the path to a file you'd like to add: ")
        if not os.path.isfile(in_filename):
            print(f"Could not find file \"{in_filename}\"")
            return
        in_filename = str(Path.absolute(Path(in_filename))).replace("\\", "/")

        in_playlist = input("Playlist (if it does not exist a new one will be created): ")
        
        add_one_filename(in_playlist, in_filename)

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
        print(f"No such playlist \"{playlist_name}\"")


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
    parser.add_argument("-p", "--playlist", type=str, help="name of the playlist to be played")
    parser.add_argument("-i", "--inpath", type=str, help="path to an audio file or folder of audio files to be played")
    parser.add_argument("-c", "--create", type=str, help="create a new playlist with the given name")
    parser.add_argument("-l", "--library", action="store_true", help="list the playlists and tracks in your library")
    parser.add_argument("-s", "--shuffle", action="store_true", help="shuffle the tracks in a playlist; has no effect for playing a single track")
    parser.add_argument("-n", "--nogui", action="store_true", help="do not try to use a file dialog GUI")
    parser.add_argument("-a", "--add", action="store_true", help="add files to your library")
    parser.add_argument("-r", "--remove", type=str, help="remove a playlist")
    args = parser.parse_args()

    try:
        from tkinter import filedialog, Tk
        use_gui = True
    except:
        use_gui = False

    if args.add:
        # do stuff
        if use_gui and not args.nogui:
            add_music(filedialog=filedialog, tk=Tk)
        else:
            add_music()
    elif args.library:
        list_music()
    elif args.remove:
        remove_playlist(args.remove)
    elif args.create:
        create_playlist(args.create)
    else:
        if not os.path.isdir(APP_DIRECTORY):
            try:
                os.mkdir(APP_DIRECTORY)
            except:
                print("Could not make application directory.")
                exit(1)

        if args.shuffle:
            print("shuffle play enabled")
        
        if args.playlist:
            play_playlist(args.playlist, shuffle=args.shuffle)
        elif args.inpath:
            if os.path.isdir(args.inpath):
                play_directory(args.inpath, shuffle=args.shuffle)
            else:
                play_file(args.inpath)
        else:
            print("No arguments given. Use `acmplayer -h` to see options.")


if __name__ == "__main__":
    main()