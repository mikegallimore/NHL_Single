## NHL_Single

### Purpose
This is a script for scraping and parsing the play-by-play, roster and shift files available for an NHL game in order to generate tabular and visualized data.

### Prerequisites
This script requires Python (3.0 at minimum, 3.6+ is recommended) in order to run the script. If you don't already have Python on your machine, the simplest remedy is to install the <a href="https://www.anaconda.com/distribution/">Anaconda Distribution</a>. 

If you intend on taking advantage of the script's Twitter functionality, you need to create a <a href="https://apps.twitter.com/app/new">Twitter application</a> and request its Access Token.

### Installation

### Usage

Standard<br>
To use the script, you need to be in your interactive Python shell (i.e. command line interface). If you installed the Anaconda Distribution, this is the Anaconda Prompt program. 

At minimum, you must indicate the season and the particular game's 5-digit identifier. For example:<br>
<code>python run_game.py 20182019 20001</code>

Modified<br>
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
