#!/usr/bin/env python
"""
If you filled right path into config.json but powershell cannot
find config.xlaunch, try PROGRA~1 instead of Program Files.

And please use \\ instead of \ and /,
or run this script to avoid this problem.
"""
import json


def main():
    with open("config.json", "r") as f:
        config = json.load(f)


    class Path:
        """
        Stores Path variables. More paths in future.
        """
        xlaunch = config["path"]["xlaunch"]


    def set_xlaunch_path():
        new_path = input(
            f"Now: {Path.xlaunch} \n"
            "Return nothing for cancel\n"
            "path of config.xlaunch?\n")
        
        if new_path:
            Path.xlaunch = new_path
        else:
            pass


    answer = input(
        "[0] Cancel\n"
        "[1] Set path of config.xlaunch"
        "(config that checked 'Disable Accessing Control')\n")
    
    def bye():
        print("Bye")

    switch = {
        "0": bye,
        "1": set_xlaunch_path,
    }

    switch.get(answer, bye)()

    """
    TODO: try other data structure like ordered dict if too many keys and values.
    """
    config["path"]["xlaunch"] = Path.xlaunch

    with open("config.json", "w") as f: 
        json.dump(config, f, indent=4)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print(
            "Cannot find 'config.json'!\n"
            f"Please check you working directory is {__file__[:-9]}.")