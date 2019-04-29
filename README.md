## NHL_Single

### Purpose
This is a script for scraping and parsing the play-by-play, roster and shift files available for an NHL game in order to generate tabular and visualized data.

### Prerequisites
This script requires Python3 (written with 3.6.5; tested with 3.6.8). If you don't already have Python on your machine, the simplest remedy is to install the <a href="https://www.anaconda.com/distribution/">Anaconda Distribution</a> or, alternatively, <a href="https://docs.conda.io/en/latest/miniconda.html">Miniconda</a>. 

### Setup
1. Clone/Download the NHL_Single files
2. Move the folder containing the NHL_Single files wherever you want them stored on your machine
3. Using your machine's interactive Python shell (for Anaconda or Miniconda, this is Anaconda Prompt), change the working directory to the NHL_Single folder and install dependencies after creating a new environment:
  
   ##### Anaconda / Miniconda
   <code>conda create -n environment_name -f environment.yml</code><br>
   
   ##### Pipenv
   <code>pipenv install</code><br>
   <code>pip install -r requirements.txt</code><br>      

4. If you intend on using the script's Twitter functionality, you need to create a <a href="https://apps.twitter.com/app/new">Twitter application</a> and request its Access Token, then rename <code>twitter_credentials_sample.py</code> to <code>twitter_credentials.py</code> and input your own APP_KEY, APP_SECRET, OAUTH_TOKEN and OAUTH_TOKEN_SECRET

### Usage
You need to be in your machine's interactive Python shell (if you installed the Anaconda Distribution or Miniconda, this is Anaconda Prompt) in order to execute command lines.

Activate your environment:


##### Game Usage
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

##### Schedule Usage
To fetch a season's schedule, either initially or to update (as you will need to do with each playoff round) it, you must indicate the particular season:<br>
<code>python run_schedule.py 20182019</code>

### Acknowledgements
