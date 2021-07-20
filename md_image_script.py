#!/usr/bin/python

import os
import platform
import glob
from datetime import datetime
import sys

# Adjust the source path according to the detected OS
if platform.system() == "Darwin":
    source_path = "~/Desktop/"
    system_OS = "Mac"
elif platform.system() == "Linux":
    source_path = "~/Pictures/"
    system_OS = "Linux"

# Let's try a different approach to this. Note that we need some adjustment to the path to account
# for globs apparent inability to work with tilde characters
list_of_files = sorted(
    glob.glob(os.path.expanduser(source_path) + '*.png'),
    key=os.path.getmtime)

# Find the most recent n files in the source directory.
subset_file_list = list_of_files[int(sys.argv[1]) * -1:]

# Create a file path for the new file. Note that here were are going to
# assume there is an 'images' directory in the current location
new_path = sys.argv[2] + "/images/"
if not os.path.exists(new_path):
    os.makedirs(new_path)

# Here, we're going to just move a single file

# Note that this is now a loop: starting to build in functionality to
# accept multiple files
markdown_return = []

for file_name in subset_file_list:

    # Add an (optimistically) more informative title, and transform to replace
    # spaces with underscores
    new_file_name = input("File name: ")
    new_file_name = datetime.now().strftime("%d-%m-%Y %H %M %S") + \
        " " + new_file_name + ".png"
    new_file_name = new_file_name.replace(" ", "_")

    new_file_path = os.getcwd() + "/images/" + new_file_name

    # Move the file and confirm to the user where this file has been moved
    os.system("cp " + "'" + file_name + "' " + new_file_path)
    print("Saved new file to: " + new_file_path)

    # Note here that it's best to insert images with relative paths
    abs_path = sys.argv[2]
    cut_it = abs_path.split("/")[-1]
    relative_path = "./images/" + new_file_name

    # Reformat this thing to markdown, and return to a new list
    markdown_return.append("![](" + relative_path + ")")

# Save the new filepath to the clipboard
# TODO has this multiple markdown functionality been tested?
if system_OS == "Mac":
    if len(markdown_return) == 1:
        os.system("echo " + "'" + markdown_return[0] + "'" + " | pbcopy")
    else:
        several_markdown_values = "\n".join(str(e) for e in markdown_return)
        os.system("printf " + "'" + several_markdown_values + "'" +
                  " | pbcopy")
elif system_OS == 'Linux':
    if len(markdown_return) == 1:
        os.system("echo " + "'" +
                  markdown_return[0] + "'" + " | xclip -sel clip")
    else:
        several_markdown_values = "\n".join(str(e) for e in markdown_return)
        os.system("printf " + "'" + several_markdown_values + "'" +
                  " | xclip -sel clip")


# TODO I would prefer to _import_ these functions from the helper file.
