import os
from pathlib import Path


def edit_playlist(playlist, app_dir, use_gui=False, filedialog=None, tk=None):
    """
    Run a command based interface to edit existing playlists
    """

    playlist_filename = f"{playlist}.playlist"
    if playlist_filename not in os.listdir(app_dir):
        print(f"Playlist \"{playlist}\" not found.")
        return

    print(f"=== Edit playlist \"{playlist}\" ===")
    print(f"Enter \"help\" for a list of commands.")


    with open(os.path.join(app_dir, playlist_filename)) as f:
        full_paths = f.read().splitlines()

    # items are tuples of format (command, resulting list of absolute paths)
    history = [full_paths]


    ### COMMAND FUNCTIONS ###
    ### these should all return a boolean indicating whether to print out the playlist after execution

    def help():
        print("The following commands are available:\n")
        print("exit         --  exit the dialog")
        print("undo         --  undo the last command")
        print("save         --  save the changes you've made to disk")
        print("add", "      " if use_gui else "<path>", "  -- ", "add new files from a file prompt" if use_gui else "add a new file from the path specified")
        print("remove <#>   --  remove the item with the number specified")
        print("swap <#> <#> -- swap the two tracks with the numbers specified")
        print("reorder <#> <#> <#> ...")
        print("             --  define a new order for all the tracks")
        print("reverse      --  reverse the order of the tracks")
        print("show         --  show/print the playlist")
        print("help         --  show this message\n")
        return False

    def undo():
        if len(history) > 1:
            history.pop(-1)
            return True
        else:
            print("nothing to undo")
            return False

    def save():
        with open(os.path.join(app_dir, playlist_filename), "w") as f:
            f.write("\n".join(history[-1]))
        print("Succesfully saved.")
        return False

    def add(path=None):
        new_list = history[-1][:]
        if path:
            fullpath = str(Path.absolute(Path(path))).replace("\\", "/")
            new_list.append(fullpath)
        else:
            tk().withdraw()
            filenames = filedialog.askopenfilenames()
            if len(filenames) < 1: return
    
            for name in filenames:
                new_list.append(name.replace("\\", "/"))
            
        history.append(new_list)

        return True
    
    def remove(idx):
        if len(history[-1]) < 1:
            print("This playlist is already empty.")
            return False
        new_list = history[-1][:]
        new_list.pop(idx-1)
        history.append(new_list)
        return True

    def swap(i1, i2):
        idx1 = i1 - 1
        idx2 = i2 - 1
        new_list = history[-1][:]
        tmp = new_list[idx2]
        new_list[idx2] = new_list[idx1]
        new_list[idx1] = tmp
        history.append(new_list)
        return True

    def reorder(*indexes):
        if sorted(indexes) != [x+1 for x in range(len(history[-1]))]:
            print("You must include every track in the new order exactly once.")
            return False
        new_list = history[-1][:]
        for i, old_i in enumerate([x-1 for x in indexes]):
            new_list[i] = history[-1][old_i]
        history.append(new_list)
        return True
        
    
    def reverse():
        new_list = history[-1][::-1]
        history.append(new_list)
        return True
    
    def show():
        for i, item in enumerate(history[-1]):
            print(f"{i+1}.", os.path.split(item)[1])
        print() # extra newline
        return False

    commands = {
        "help": help,
        "undo": undo,
        "save": save,
        "add": add,
        "remove": remove,
        "swap": swap,
        "reorder": reorder,
        "reverse": reverse,
        "show": show
    }


    def rtfm():
        print("enter \"help\" for usage info")


    show()

    while True:
        command = input("acm> ")
        if command.lower() == "exit":
            break
        
        args = []

        if command.startswith("add") and not use_gui:
            try:
                args = [command.split(" ", 1)[1]]
            except:
                rtfm()
                continue
        elif command.startswith("remove"):
            try:
                args = [int(command.split(" ", 1)[1])]
            except:
                rtfm()
                continue
        elif command.startswith("swap"):
            try:
                args = [int(i) for i in command.split(" ")[1:3]]
            except:
                rtfm()
                continue
        elif command.startswith("reorder"):
            try:
                args = [int(i) for i in command.split(" ")[1:]]
                if len(args) != len(history[-1]):
                    print("You must include every track in the new ordering.")
                    raise Exception()
            except:
                rtfm()
                continue

        command_name = command.split(" ", 1)[0].lower()

        if command_name in commands:
            try:
                if commands[command_name](*args): # execute the command
                    show()
            except:
                rtfm()
        else:
            print("command not recognized")
        