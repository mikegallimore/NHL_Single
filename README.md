## NHL_Single

### Purpose
Enabling the scraping and parsing the play-by-play, roster and shift files available for an NHL game in order to generate tabular and visualized data.

### Prerequisites
At minimum, a vanilla installation of Python3 (code written with 3.6.5; tested with 3.6.8). If you don't already have Python on your machine, the simplest remedy is to install the <a href="https://www.anaconda.com/distribution/">Anaconda Distribution</a> or, alternatively, <a href="https://docs.conda.io/en/latest/miniconda.html">Miniconda</a>. 

### Setup
1. Clone/Download the NHL_Single files
2. Move the folder containing the NHL_Single files wherever you want them stored on your machine
3. Using your machine's interactive Python shell (i.e. command line interface; for Anaconda or Miniconda, this is Anaconda Prompt):<br>
   a. Change the working directory to the NHL_Single folder<br>
   b. Create a new environment<br>
   c. Install dependencies<br>
  
   ##### Anaconda or Miniconda as package and environment manager
   <code>conda create -n environment_name -f environment.yml</code><br>
   
   ##### PIP as package manager; Pipenv as environment manager
   <code>pipenv install</code><br>
   
   ##### PIP as package manager; venv as environment manager
   <code>py -m venv env</code><br>
   <code>pip install -r requirements.txt</code><br>      

4. If you intend on using the script's Twitter functionality:<br>
   a. Create a <a href="https://apps.twitter.com/app/new">Twitter application</a> and request its Access Token<br>
   b. Rename <code>twitter_credentials_sample.py</code> to <code>twitter_credentials.py</code><br>
   c. Input your own APP_KEY, APP_SECRET, OAUTH_TOKEN and OAUTH_TOKEN_SECRET<br>

5. Rename <code>parameters_sample.py</code> to <code>parameters.py</code> and update the files_root and charts_root objects with the path to your NHL_Single folder

### Usage
You must be within your machine's the command-line interface and need to activate the environment you created.

##### Game
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

##### Schedule
To fetch a season's schedule, either initially or to update (as you will need to do with each playoff round) it, you must indicate the particular season:<br>
<code>python run_schedule.py 20182019</code>

### Limitations

NHL_Single, obviously, only works for a single game, though it is the pilot effort for a larger project that expands the scope across a range of games and seasons.<br>

Additionally, NHL_Single depends on the availability of files that feed the league's Real-Time Scoring Statistics (RTSS) system. 2007-2008 is the earliest season it might work as designed but it has only been tested, to this point, for 2018-2019 regular season and playoff games. The league is reportedly introducing new <a href="https://www.nhl.com/news/nhl-plans-to-deploy-puck-and-player-tracking-technology-in-2019-2020/c-304218820">tracking technology</a> for the 2019-2020 season but it is not yet clear how the RTSS system will be impacted.

### Acknowledgements
A lot of people have, in varying ways (be it by patiently answering questions, making their own code available for consultation, offering suggestions or simply encouragement), helped me learn enough to put this thing together. I am grateful for all of the feedback I received and the resources that were available. Thank you.
