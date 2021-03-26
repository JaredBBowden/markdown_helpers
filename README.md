# markdown_helpers
A collection of functions that make working with markdown files easier (for me).

**Step one: setup**  
Pull the code  
`git clone git@github.com:JaredBBowden/markdown_helpers.git`  

Add module to the path of your conda envt
```
# Be sure to activate the relevant env first

# Add the DIRECTORY (emphasis here, _not_ the file)
conda-develop /path/to/module_DIRECTORY
```

**Step two: use it**  
I tend to work from within notebooks and interactive terminals. The following workflow reflects this. The second working assumption here is that _the most recent file_ within the specified source directory is the file you want to pull in.   Most of the work I do involves 1) screenshot from source, 2) add to markdown, 3) keep doing... Whatever it was that I was doing. 

_Working from the directory where you images to go_, import the module and run the `markdown_image` function.

You should then be prompted for a file name for your new image. Once this title is specified, the program should return the complete path where your new file has been moved (an `images` folder within your current working directory), and return a markdown formatted string (containing your new image path) to the clipboard. You can now paste this string to your markdown document. 

