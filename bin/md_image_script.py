#!/home/jared/anaconda3/bin/python3

import os
import platform
import glob
from datetime import datetime
import sys


"""
# TODO 
* this could really use some documentation... What is the convention for 
something like a scipt? 

The first argument appears to be the number of files to pull. The second 
argument is the path where the files are going.

* I think that the files that are being pulled here are not really working. 

I was getting some older images... and more than one. 

* I would also like to add some code to accept relative paths.

* Also, I would like to add this to the path... and then add some instruction 
to ensure that this... Are we getting to a point where this could use more 
documentation than a readme? Could be an interesting exercise. 


https://fishshell.com/docs/current/cmds/fish_add_path.html#
"""


# Adjust the source path according to the detected OS
if platform.system() == "Darwin":
    source_path = "~/Desktop/"
    system_OS = "Mac"
elif platform.system() == "Linux":
    source_path = "~/Pictures/"
    system_OS = "Linux"

# Find recent screenshots in OS-specific location
list_of_files = sorted(
    glob.glob(os.path.expanduser(source_path) + '*.png'),
    key=os.path.getmtime)

# Subset to pull the specified range of files that should be moved.
# TODO presumably here is a better way to set defaults for sys.argv
n_files = int(sys.argv[1])

if n_files < 1:
    n_files = 1

subset_file_list = list_of_files[n_files * -1:]

# Create a `images` file path for the new file(s)
try:
    # If the base path exists...
    os.path.exists(sys.argv[2])

    # Providing the base is there, let's check for an images dir, and add it
    # if it's not
    new_path = sys.argv[2] + "/images/"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
except:
    print("Base path not found")

# Note that this is now a loop: starting to build in functionality to
# accept multiple files
markdown_return = []

for file_name in subset_file_list:

    # Add an (optimistically) more informative title, and transform to replace
    # spaces with underscores

    # For a script -- it would appear we have to make some adjustments to this
    # use of input
    new_file_name = str(input("File name: "))
    new_file_name = datetime.now().strftime("%d-%m-%Y %H %M %S") + " " + new_file_name + ".png"
    new_file_name = new_file_name.replace(" ", "_")

    new_file_path = new_path + new_file_name

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
        os.system("echo " + "'" + markdown_return[0] + "'" + " | xclip -sel clip")
    else:
        several_markdown_values = "\n".join(str(e) for e in markdown_return)
        os.system("printf " + "'" + several_markdown_values + "'" +
                " | xclip -sel clip")
