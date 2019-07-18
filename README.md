## NHL_Single
A tool for scraping and parsing the available source files for any NHL game, beginning with the 20062007 season, in order to generate tabular and visualized data.

### Prerequisites
At minimum, a vanilla installation of Python3 (code written with 3.6.5; tested with 3.6.8). If you don't already have Python on your machine, the simplest remedy is to install the <a href="https://www.anaconda.com/distribution/">Anaconda Distribution</a> or, alternatively, <a href="https://docs.conda.io/en/latest/miniconda.html">Miniconda</a>.

### Setup
1. Clone/Download the NHL_Single files
2. Move the folder containing the NHL_Single files wherever you want them stored on your machine
3. Using your machine's interactive Python shell (i.e. command-line interface; for Anaconda or Miniconda, this is Anaconda Prompt):<br>
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
   c. Input your own <code>APP_KEY</code>, <code>APP_SECRET</code>, <code>OAUTH_TOKEN</code> and <code>OAUTH_TOKEN_SECRET</code><br>

5. Rename <code>parameters_sample.py</code> to <code>parameters.py</code> and update the <code>files_root</code> and <code>charts_root</code> objects with the path to your NHL_Single folder

### Usage
You must be within your machine's the command-line interface and need to activate the environment you created.

##### Game
At minimum, you must indicate two positional arguments, which are the particular season and the 5-digit game number:<br>
<code>python run_game.py 20182019 20001</code>

There are optional arguments available for you to tack onto the basic structure as well:<br>
<code>--fetch</code> set to 'skip'<br>
<code>--images</code> set to 'show'<br>
<code>--load_pbp</code> set to 'true' (pertains to, as explained in the 'Notes' section below, 20062007 only)<br>
<code>--parse</code> set to 'skip'<br>
<code>--players</code> set to 'skip'<br>
<code>--scope</code> set to 'full'<br>
<code>--teams</code> set to 'skip'<br>
<code>--tweet</code> set to 'no'<br>
<code>--units</code> set to 'skip'<br>

To re-run a game without bothering to fetch and parse the game files again plus not tweet any generated charts:<br>
<code>python run_game.py 20182019 20001 --fetch skip --parse skip --tweet no</code>

To generate all of the team, player and unit tables and charts possible, as well as have the charts display on your screen as they're made:<br>
<code>python run_game.py 20182019 20001 --scope full --images show</code>

Reference the required and optional arguments in the shell by typing the following:<br>
<code>python run_game.py -h</code>

##### Schedule
To fetch a season's schedule manually, indicate the particular season as demonstrated below:<br>
<code>python run_schedule.py 20182019</code>

### Notes

##### What's Next?
NHL_Single, as its name implies, only processes one game at a time. With the release of v2.0--which extended compatibility back to the 20062007 season--the next major change will be to enable fetching and parsing a range of games within a season.<br>

##### Compatability
This tool was developed and tested within Windows. It may (or may not!) play nice with other operating systems, for which testing in and feedback is most welcome!

##### The Optional 'load_pbp' Command-Line Argument
An inelegant solution to a persistent problem exclusive to the 20062007 season arising from the complexity of parsing this season's unique play-by-play formatting: NUL bytes somehow wind up in the play-by-play data, stopping any further processing of the rows that follow their insertion. If you care for further elaboration, hit me up <a href="https://twitter.com/mikegallimore/">on Twitter</a> but the result, simply put, is the loss of some events in the play-by-play output.

After much trial and all error, NHL_Single lacks a means for automating the removal of the NUL bytes. Thus the necessity, at present, for manually doing so--which is easy enough in Excel with a macro but obviously tedious--in order to get a complete play-by-play file as output.

To spare any potential user the drudgery, <a href="https://www.dropbox.com/home/20062007_pbp">this Dropbox folder</a> contains purged 20062007 play-by-play files users should download before using the optional 'load_pbp' command-line argument as shown below:<br>
<code>python run_game.py 20062007 20001 --load_pbp true </code>

### Acknowledgements
A lot of people have, in varying ways (be it by patiently answering questions, making their own code available for consultation, offering suggestions or simply encouragement), helped me learn enough to put this thing together. I am grateful for all of the feedback received and resources made available.
