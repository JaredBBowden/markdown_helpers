#!/usr/bin/python

# TODO more imports are required
from markdown_images import find_notebooks_and_markdown_files


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

        with open(source_file_path, 'r') as file:
            filedata = file.read()

        # Find and replace the target strings
        filedata = filedata.replace('./images', new_path)

        # Write the file out again
        with open(source_file_path, 'w') as file:
            file.write(filedata)
    else:
        print("File not found: ", source_file_path)


# TODO let's make a function to do this over all images in a directory,
# then move this to the script file.

# I think that move markdown still has a place, particularly for when files
# need to move to a totally new path (ie we want to move the file AND images)


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
    print("Found: ", len(file_paths))

    for one_file in file_paths:
        print("Running:", one_file)
        rename_file_references(os.path.basename(one_file), new_path)


# Let's do this right.
if __name__ == "__main__":

    check_mode = input("Run on single file (y/n)?: ")

    if check_mode == "y":
        print("Single file mode")

        the_file = input("Enter current path to the file: ")
        the_new_path = input("Enter _new_ relative path to images: ")

        rename_file_references(the_file, the_new_path)

    elif check_mode == "n":
        print("Directory mode mode")

        the_base_directory_path = input("Enter path to base_directory: ")
        the_new_path = input("Enter _new_ relative path to images: ")

        rename_all_file_references(the_base_directory_path, the_new_path)

    else:
        print("Please enter y or n")


# TODO I would prefer to _import_ these functions from the helper file.
# Note that the same goes for the md_image_script file, too

# I think that this will also allow us to avoid all these imports...

# Also, the more I look around here, the more I see that there are more
# _internal_ functions that I have to pull in, too.



