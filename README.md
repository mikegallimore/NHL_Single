## NHL_Single

### Purpose
This is a script for scraping and parsing the play-by-play, roster and shift files available for an NHL game in order to generate tabular and visualized data.

### Prerequisites
This script requires Python (3.0 at minimum, 3.6+ is recommended) in order to run the script. If you don't already have Python on your machine, the simplest remedy is to install the <a href="https://www.anaconda.com/distribution/">Anaconda Distribution</a>. 

If you intend on taking advantage of the script's Twitter functionality, you need to create a <a href="https://apps.twitter.com/app/new">Twitter application</a> and request its Access Token.

### Installation

### Standard Usage
To use the script, you need to be in your interactive Python shell (i.e. command line interface). If you installed the Anaconda Distribution, this is the Anaconda Prompt program. 

At minimum, you must indicate the season and the particular game's 5-digit identifier. For example:<br>
<code>python run_game.py 20182019 20001</code>

### Modified Usage
There are optional arguments available for you to tack onto the basic structure as well. Following are some examples:
<code>python run_game.py 20182019 20001 --tweet no</code>



You can always reference the required and optional arguments in the shell by typing the following:
<code>python run_game.py -h</code>


### Acknowledgements
