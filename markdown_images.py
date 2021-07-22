import os
import platform
import glob
from datetime import datetime
import re


# TODO Well... [gestures broadly] there's a lot. Base functionality is there
# remaining updates are tagged. I should really have a develop branch for this
# project, but that's not how we're doing things.

def system_image_path():
    """Find the path to the system image directory
    
    Returns: string, path to the system image directory
    """
    if platform.system() == "Darwin":
        image_path = "~/Desktop/"
        system_OS = "Mac"
    elif platform.system() == "Linux":
        image_path = "~/Pictures/"
        system_OS = "Linux"

    return image_path, system_OS


def string_to_clipboard(the_string, system_OS):
    """send a string to the clipboard

    Args:
        the_string (string): the sting you want to send to the clipboard
        system_OS (string): string describing the system OS you're using
    """    
    if system_OS == "Mac":
        os.system("echo " + "'" + the_string + "'" + " | pbcopy")
        
    elif system_OS == 'Linux':
        os.system("echo " + "'" +
                  the_string + "'" + " | xclip -sel clip")


def markdown_image(file_destination_path):
    """    
    Pull the n most recent screenshots, re-title, move a destination of your choosing,
    and copy a formatted markdown snippet to the system clipboard.

    n_files: the number of files you want to move

    Dependencies
    * xclip: to copy path to clipboard
    """

    # Adjust the source path according to the detected OS
    image_path, system_OS = system_image_path()

    list_of_files = sorted(
        glob.glob(os.path.expanduser(image_path) + '*.png'),
        key=os.path.getmtime)

    # Find the most recent file in the source directory.
    original_image = list_of_files[-1]

    # Create a file path for the new file. Note that here were are going to
    # assume there is an 'images' directory in the current location
    file_destination_path = os.path.normpath(file_destination_path)
    
    new_path = file_destination_path + "/images/"
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Add an (optimistically) more informative title, and transform to replace
    # spaces with underscores
    new_file_name = input("File name: ")
    new_file_name = datetime.now().strftime("%d-%m-%Y %H %M %S") + \
        " " + new_file_name + ".png"
    new_file_name = new_file_name.replace(" ", "_")

    # Move the file
    new_file_path = new_path + new_file_name

    # TODO: this is probably a better approach to this. Kill the other function.
    os.replace(original_image, new_file_path)
    print("Moved image to:", new_file_path)

    # Now we need the path to the image 
    relative_path = "./images/" + os.path.basename(new_file_path)

    # Now let's format this for markdown
    markdown_path = "![](" + relative_path + ")"

    # Copy to the clipboard
    string_to_clipboard(markdown_path, system_OS)


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
        # jupyter nbconvert --to html mynotebook.ipynb
        # os.system()

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
    # TODO review: want this to find local file paths, _not_ external links.
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
                image_path = a_match[a_match.find(
                    "(")+1:a_match.find(")")].replace('"', "")
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
        for one_image_path in image_paths:

            # TODO I don't love how verbose this is, but this is a much better
            # way to work with paths. Change this elsewhere...
            one_image_path = os.path.dirname(
                source_file_path) + "/" + one_image_path

            move_file(one_image_path, new_image_path)

    # Move the original file
    move_file(source_file_path, destination_dir_path)


def find_notebooks_and_markdown_files(base_path):
    """Find all notbook and markdown files in a specified directory, and 
    return paths

    Args:
        base_path (string): string to the path where you want to look or files
    """
    base_path = os.path.abspath(base_path)

    file_paths = glob.glob(base_path + "/*.md") + \
        glob.glob(base_path + "/*.ipynb")

    print("Found: ", len(file_paths), "files")

    return file_paths


def image_dir_cleanup(base_directory):
    """
    Let's make another function, adding a hidden directory for each file, to 
    contain all of the images embedded within... That was a dramatic way 
    to put that.

    base_directory: the starting point for finding all of the files that 
    you want to create specific image directories for
    """
    # Find all the file paths in the local environment. Let's ensure that
    # this is done recursively, as some files are now in nested directories
    file_path = find_notebooks_and_markdown_files(base_directory)

    # Loop through paths
    for file_path in file_paths:

        # For each path, make a new hidden directory with a new "images"
        # desination at the end... Now that I think about it, I suspect
        # we should check to see if the directory exists, and only make it
        # if we _need_ it.
        new_image_dir_path = "." + \
            os.path.split(file_path)[1].split(".")[0] + "_images"

        if not os.path.exists(new_image_dir_path):
            os.makedirs(new_image_dir_path)

        # Find all of the image links in the file
        image_paths = find_images_in_markdown(file_path)

        # Move all of the image files that were in the grouped image file
        # to the new file-specific directory
        for one_image_path in image_paths:
            move_file(one_image_path, new_image_dir_path)

        # FIXME well, I just realized late in this process that
        # (of course) we're also going to need to modify the path
        # references in the original file.

        # I'm not sure this is functional... Pull this out, make a function
        # test, and then move things back.

        with open(file_path, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('./images', "./" + new_image_dir_path)

        # Write the file out again
        with open(file_path, 'w') as file:
            file.write(filedata)


def rename_file_references(source_file_path, new_path):
    """Open a file, find all markdown references, replace with the new path. 

    Args:
        source_file (str): the full path to the file that you want to replace
        new_path (str): the path to the new file to be used as a reference. 
        don't include the final slash.
    """

    source_file_path = os.path.normpath(source_file_path)
    new_path = os.path.normpath(new_path)

    if os.path.exists(source_file_path) == True:

        print("Found file: ", source_file_path)

        with open(source_file_path, 'r') as file:
            filedata = file.read()

        # Find and replace the target strings
        filedata = filedata.replace('./images', new_path)

        # Write the file out again
        with open(source_file_path, 'w') as file:
            file.write(filedata)
    else:
        print("File not found: ", source_file_path)


def rename_all_file_references(base_directory_path, new_path):
    """Run `rename_file_references` on all files within a specified directory

    Args:
        base_directory (string): string to path containing files that you want
        to replace
        new_path (string): string to the preferred image directory
    """

    # Path normalization
    base_directory_path = os.path.normpath(base_directory_path)
    new_path = os.path.normpath(new_path)

    file_paths = find_notebooks_and_markdown_files(base_directory_path)

    for one_file in file_paths:
        print("Running:", one_file)
        rename_file_references(os.path.abspath(one_file), new_path)
