import os
import platform
import glob
from datetime import datetime
import re


# TODO Well... [gestures broadly] there's a lot. Base functionality is there
# remaining updates are tagged. I should really have a develop branch for this
# project, but that's not how we're doing things.


def markdown_image(n_files=1):
    """    
    Pull the n most recent screenshots, re-title, move a destination of your choosing,
    and copy a formatted markdown snippet to the system clipboard.

    n_files: the number of files you want to move

    Dependencies
    * xclip: to copy path to clipboard
    """

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
    subset_file_list = list_of_files[n_files * -1:]

    # Create a file path for the new file. Note that here were are going to
    # assume there is an 'images' directory in the current location
    new_path = os.getcwd() + "/images/"
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    markdown_return = []

    for file_name in subset_file_list:

        # Add an (optimistically) more informative title, and transform to replace
        # spaces with underscores
        new_file_name = input("File name: ")
        new_file_name = datetime.now().strftime("%d-%m-%Y %H %M %S") + " " + new_file_name + ".png"
        new_file_name = new_file_name.replace(" ", "_")

        new_file_path = os.getcwd() + "/images/" + new_file_name

        # Move the file and confirm to the user where this file has been moved
        os.system("cp " + "'" + file_name + "' " + new_file_path)
        print("Saved new file to: " + new_file_path)

        # Note here that it's best to insert images with relative paths
        abs_path = os.getcwd()
        cut_it = abs_path.split("/")[-1]
        relative_path = "./images/" + new_file_name

        # Reformat this thing to markdown, and return to a new list
        markdown_return.append("![](" + relative_path + ")")

    # Save the new filepath to the clipboard
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


def notebook_to_markdown(notebook_directory_name):
    """Find notebooks, convert to markdown, push to a "mirrored" version of the 
    repo, populated _only_ with markdown versions of files. 

    Args:
        notebook_directory_name ([type]): [description]
    
    TODO 
    * This is starter code only. 
    """    

    # Find all .ipynb suffix files and their FULL path
    notebook_paths = glob.glob("./**/*.ipynb", recursive=True)

    for path in notebook_paths:

        path_list = path.split("/")

        # Adjust path to the new notebook location
        path_list[1] = notebook_directory_name

        # Join list to create the new path
        new_path = "/".join(path_list)

        # Convert, and save the new file
        jupyter nbconvert --to html mynotebook.ipynb
        os.system()


        # I think we need some control flow to ensure that, under cases where the
        # directory structure is not present, it is created.

    # Loop through these files, apply the converstion to a new file structure
    # that specifies the new notebook method.


def find_images_in_markdown(markdown_file_path):
    """Look at a markdown file, return all image names

    Args:
        markdown_file_path ([type]): [description]

    Returns:
        [type]: [description]
    TODO
    * I could really make better use of these regex objects. For now, I'm 
    parsing things in a way that is... "not great". 
    """
    regex = re.compile("(?:!\[(.*?)\]\((.*?)\))")

    matches = []

    with open(markdown_file_path) as f:
        for line in f:
            result = regex.search(line)
            if result != None:
                # This is about to be some garbage code
                first = str(result).split("[")
                image_only = first[1].split("]")[0]
                matches.append(image_only)

    return matches


def move_file(image_name, source, destination):
    """Move an image from the source location to a specified destination 
    location

    Args:
        image_name ([type]): [description]
        source ([type]): [description]
        destination ([type]): [description]
    TODO 
    * This function could be used in a number of other locations, above. This 
    would require a refactor... That I don't really feel like doing right now.
    """
    # The original location
    file_name = source + image_name

    # Where it's going
    new_file_path = destination + image_name

    # Move the file
    os.system("cp " + "'" + file_name + "' " + new_file_path)


def move_markdown(markdown_file_path, source, destination):
    """
    Stuff

    Args:
        markdown_file_path ([type]): [description]
        source ([type]): [description]
        destination ([type]): [description]

    TODO
    * Need to move the original file, too 
    """
    # Find images in the file
    images_names = find_images_in_markdown(markdown_file_path)

    # Move the files
    for image_name in images_names:
        move_file(image_name, source, destination)
