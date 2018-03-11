# Creating the IMDb database
Because of restrictions on the use of IMDb data and the size of the IMDb data
files being too large for GitHub storages, use the following process to create
a local version of the IMDb database utilizing IMDbPy (a Python module that
provides Pythonic objects for interaction with local or online versions of the
IMDb database).

## Step 1: Download the IMDb data files
IMDb provides regularly updated versions of their dataset at
(http://www.imdb.com/interfaces/). Download the files and place them in the
`/imdb` directory in this repository. **Do not unzip them.**

## Step 2: Download IMDbPy
If you haven't already, you can download IMDbPy via `pip install imdbpy`. In
order to use it properly, you'll also need SQLalchemy (an interface adapter
module for common SQL frameworks; `pip install sqlalchemy`) and an SQLalchemy-
compatible SQL database program (I'm using SQLite3 here for convenience, which
is probably already installed with Python 3 on your system, especially if your
are running it via Anaconda).

## Step 3: Create a new SQL database
Open a new terminal window (I'm assuming you are on mac/linux here and using
SQLite3: **windows users take note and adapt accordingly**) and run this line of
code from the root of the project repository (this folder) to create a new db:

`sqlite3 ./imdb/imdb.db`

## Step 4: Run the s32imdbpy script to create a local instance of the IMDb database
In the same terminal window, run this line of code to have IMDbPy automatically
generate your local database from the compressed files:

`~/[PYTHON INSTALL PARENT]/bin/s32imdbpy.py ./imdb/ sqlite:///[FILE PATH]/ga-capstone/imdb/imdb.db`

where

* `[PYTHON INSTALL PARENT]` = the directory where your Python directory is
installed, and where pip installs your Python modules (for me this is
`anaconda3`) since I am running Python3 in Anacaonda.
and

* `[FILE PATH]` = the file path where this repo has been installed. SQLite3
needs the full path from wherever your user space is, which for me is just
`Documents`.

Putting it all together, my command looks like this:

`~/anaconda3/bin/s32imdbpy.py ./imdb/ sqlite:///documents/ga-capstone/imdb/imdb.db`

Or alternatively, to execute from an arbitrary directory in the terminal:

`~/anaconda3/bin/s32imdbpy.py ~/Documents/ga-capstone/imdb/ sqlite:///Documents/ga-capstone/imdb/imdb.db`

The program will take some time to execute (1-2 hours depending on your system) and will require several GBs of space on your local hard disk (4.28 GB on my system).
Once installed, you can use the `imdb('s3','sqlite:///documents/ga-capstone/imdb/imdb.db')`
method to query the local database.

## Having trouble?

Alternatively IMDbPy let's you query the remote database (but where's the fun in
that?). Check the IMDbPy documentation for details.
