#!/usr/bin/python

from markdown_images import find_notebooks_and_markdown_files, rename_file_references, rename_all_file_references


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
