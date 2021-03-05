import os
import platform
import glob
from datetime import datetime

# TODO function to move markdown file (and all associated images) to new location
# TODO make a list of all images that are not used in markdown files


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


"""
def notebook_to_markdown(notebook_directory_name):

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


    from sklearn.datasets import load_diabetes
    from sklearn.datasets import make_moons

    data = load_diabetes()
    data = make_moons()

"""

def move_markdown(target_file, destination_location):
    """
    Note that this is going to assume that all images are linked from a 
    directory in the same location as the file

    Args:
        target_file ([type]): [description]
        destination_location ([type]): [description]
    """

    # This is the link describing regex used to parse image links
    # https://gist.github.com/ttscoff/dbf4737b04e1635e1d20
