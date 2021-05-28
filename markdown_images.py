import os
import platform
import glob
from datetime import datetime
import re
import pdb


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

    # Note that this is now a loop: starting to build in functionality to 
    # accept multiple files
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
        #jupyter nbconvert --to html mynotebook.ipynb
        #os.system()


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
                # For posterity, there is a better way to access the results 
                # of re matches -- as follows
                a_match = result.group(0)

                # All we really care about is the image stuff (between parentheses)
                image_path = a_match[a_match.find("(")+1:a_match.find(")")].replace('"', "")
                matches.append(image_path)

    # TODO what happens if there are no matches? What do we want to return 
    # from this? None? 
    print("Found", len(matches), "image links")
    
    return matches


def move_file(source_file_path, destination_dir_path):
    """Simple wrapper function for a system command to move a file from the 
    source location to a specified destination location. 

    Args:
        source_file_path ([type]): the path (including file name) of the file to
        move
        destination_dir_path ([type]): the path to the directory where the file 
        should be moved. 
    
    TODO 
    * This function could be used in a number of other locations, above. This 
    would require a refactor... That I don't really feel like doing right now.
    * There are some new changes to argument names in here that need to be 
    propagated. 
    """

    # Move the file
    os.system("mv " + "'" + source_file_path + "' " + destination_dir_path)

    print("Moved", source_file_path, "to", destination_dir_path)


def move_markdown(source_file_path, destination_dir_path):
    """Move a markdown file from one directory to another. If there are image
    files to move, move those too (and confirm that they are going into an 
    `images` directory in the new destination)

    Args:
        source_file_path ([type]): the path (including file name) of the file to
        move
        destination_dir_path ([type]): the path to the directory where the file 
        should be moved.  

    Let's assume there are some regular patterns here. 
    1. Images are always going to be located in the same directory as the 
    markdown file (titled `images`)
    
    TODO I should write another function that confirms that the files have been
    moved
    """    

    # Find images in the file
    image_paths = find_images_in_markdown(source_file_path)

    if len(image_paths) > 0:

        # I'm tired for forgetting this slash, so here we go
        if destination_dir_path[-1] != "/":
            destination_dir_path = destination_dir_path + "/"

        # Confirm that the new destination has an images directory 
        new_image_path = destination_dir_path + "images/"
        if not os.path.exists(new_image_path):
            os.makedirs(new_image_path)

        # Move image files files

        # FIXME wait. These are all going to be relative image paths. 
        # This is going to be a huge pain to work with if I'm running this
        # from literally anywhere else but the source 

        # FIXME I also kind think that I'm not moving files to a location path, 
        # but a file path... And that is going to require some additional 
        # review. No... Let's debug this now. No, still don't get this. 
        # Fix the first issue and see if this is still a problem
        for one_image_path in image_paths:
            
            # I don't love how verbose this is, but this is a much better 
            # way to work with paths. 
            one_image_path = os.path.dirname(
                source_file_path) + "/" + one_image_path
            
            move_file(one_image_path, new_image_path)

    # Move the original file
    move_file(source_file_path, destination_dir_path)
