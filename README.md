## NHL_Single

### Purpose
This is a script for scraping and parsing the play-by-play, roster and shift files available for an NHL game in order to generate tabular and visualized data.

### Prerequisites
This script requires Python (3.0 at minimum, 3.6+ is recommended) in order to run the script. If you don't already have Python on your machine, the simplest remedy is to install the <a href="https://www.anaconda.com/distribution/">Anaconda Distribution</a>. 

If you intend on taking advantage of the script's Twitter functionality, you need to create a <a href="https://apps.twitter.com/app/new">Twitter application</a> and request its Access Token.

### Setup
Clone this Git package and then install its dependencies:

If you have the Anaconda Distribution or Miniconda, create a new environment with all the requirements as follows:<br>
<code>conda create --name environment_name --file requirements_conda.txt</code><br>

### Usage
You need to be in your machine's interactive Python shell (if you installed the Anaconda Distribution or Miniconda, this is Anaconda Prompt) in order to execute command lines.

At minimum, you must indicate two positional arguments, which are the particular season and the 5-digit game number:<br>
<code>python run_game.py 20182019 20001</code>

There are optional arguments available for you to tack onto the basic structure as well:<br>
<code>--extent full</code><br>
<code>--images show</code><br>
<code>--fetch skip</code><br>
<code>--parse skip</code><br>
<code>--players skip</code><br>
<code>--teams skip</code><br>
<code>--tweet no</code><br>
<code>--units skip</code><br>

So, if you wanted, for example, to use the script without scraping and parsing the game files and without tweeting out generated visualizations, you'd enter:<br>
<code>python run_game.py 20182019 20001 --fetch skip --parse skip --tweet no</code>

You can always reference the required and optional arguments in the shell by typing the following:<br>
<code>python run_game.py -h</code>

### Acknowledgements
