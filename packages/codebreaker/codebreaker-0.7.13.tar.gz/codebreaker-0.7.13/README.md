[![Build Status](https://travis-ci.org/SaltieRL/codebreaker.svg?branch=master)](https://travis-ci.org/SaltieRL/codebreaker)
[![PyPI version](https://badge.fury.io/py/codebreaker.svg)](https://badge.fury.io/py/codebreaker)
[![codecov](https://codecov.io/gh/SaltieRL/codebreaker/branch/master/graph/badge.svg)](https://codecov.io/gh/SaltieRL/codebreaker)
[![Build status](https://ci.appveyor.com/api/projects/status/jxsa56l11fxv4jn4/branch/master?svg=true)](https://ci.appveyor.com/project/SaltieRL/codebreaker/branch/master)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/SaltieRL/codebreaker.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/SaltieRL/codebreaker/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/SaltieRL/codebreaker.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/SaltieRL/codebreaker/alerts/)


# codebreaker
codebreaker is an open-source project that combines multiple tools for decompiling Rocket League replays and then analysing them.

## Requirements

- Python 3.6.7+ (3.7 and 3.8 included)
- Windows, Mac or Linux

## Install

#### Install from pip:

`pip install codebreaker`

#### Clone for development

##### Windows
```
git clone https://github.com/SaltieRL/codebreaker
cd codebreaker/
python init.py
```

##### Linux
```
git clone https://github.com/SaltieRL/codebreaker
cd codebreaker/
./_travis/install-protoc.sh
python init.py
```

##### Mac
In MacOS Catalina, zsh replaced bash as the default shell, which may cause permission issues when trying to run `install-protoc.sh` in the above fashion. Simply invoking bash should resolve this issue, like so:
```
git clone https://github.com/SaltieRL/codebreaker
cd codebreaker/
bash ./_travis/install-protoc.sh
python init.py
```
Apple's decision to replace bash as the default shell may foreshadow the removal of bash in a future version of MacOS. In such a case, Homebrew users can [install protoc](http://google.github.io/proto-lens/installing-protoc.html) by replacing `bash ./travis/install-protoc.sh` with `brew install protobuf`.


## Examples / Usage
One of the main data structures used in codebreaker is the pandas.DataFrame, to learn more, see [its wiki page](https://github.com/SaltieRL/codebreaker/wiki/data_frame).

Decompile and analyze a replay:
```Python
import codebreaker

analysis_manager = codebreaker.analyze_replay_file('9EB5E5814D73F55B51A1BD9664D4CBF3.replay', 
                                      output_path='9EB5E5814D73F55B51A1BD9664D4CBF3.json', 
                                      overwrite=True)
proto_game = analysis_manager.get_protobuf_data()

# you can see more example of using the analysis manager below

```

Just decompile a replay to a JSON object:

```Python
import codebreaker

_json = codebreaker.decompile_replay('9EB5E5814D73F55B51A1BD9664D4CBF3.replay', 
                                output_path='9EB5E5814D73F55B51A1BD9664D4CBF3.json', 
                                overwrite=True)
```

Analyze a JSON game object:
```Python
import codebreaker
import gzip
from codebreaker.json_parser.game import Game
from codebreaker.analysis.analysis_manager import AnalysisManager

# _json is a JSON game object (from decompile_replay)
game = Game()
game.initialize(loaded_json=_json)

analysis_manager = AnalysisManager(game)
analysis_manager.create_analysis()
    
# return the proto object in python
proto_object = analysis_manager.get_protobuf_data()

# return the proto object as a json object
json_oject = analysis_manager.get_json_data()

# return the pandas data frame in python
dataframe = analysis_manager.get_data_frame()
```

You may want to save codebreaker analysis results for later use:

```python
# write proto out to a file
# read api/*.proto for info on the object properties
with open('output.pts', 'wb') as fo:
    analysis_manager.write_proto_out_to_file(fo)
    
# write pandas dataframe out as a gzipped numpy array
with gzip.open('output.gzip', 'wb') as fo:
    analysis_manager.write_pandas_out_to_file(fo)
```

Read the saved analysis files:

```python
import gzip
from codebreaker.analysis.utils.pandas_manager import PandasManager
from codebreaker.analysis.utils.proto_manager import ProtobufManager

# read proto from file
with open('output.pts', 'rb') as f:
    proto_object = ProtobufManager.read_proto_out_from_file(f)

# read pandas dataframe from gzipped numpy array file
with gzip.open('output.gzip', 'rb') as f:
    dataframe = PandasManager.read_numpy_from_memory(f)
```

### Command Line

codebreaker comes with a command line tool to analyze replays. To use codebreaker from the command line:

```bash
codebreaker -i 9EB5E5814D73F55B51A1BD9664D4CBF3.replay --json analysis.json
```

To get the analysis in both json and protobuf and also the compressed replay frame data frame:

```bash
codebreaker -i 9EB5E5814D73F55B51A1BD9664D4CBF3.replay --json analysis.json --proto analysis.pts --gzip frames.gzip
```

#### Command Line Arguments

```
usage: codebreaker [-h] -i INPUT [--proto PROTO] [--json JSON] [--gzip GZIP] [-sd]
               [-v] [-s]

Rocket League replay parsing and analysis.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to replay file that will be analyzed. codebreaker
                        expects a raw replay file unless --skip-decompile is
                        provided.
  --proto PROTO         The result of the analysis will be saved to this file
                        in protocol buffers format.
  --json JSON           The result of the analysis will be saved to this file
                        in json file format.
  --gzip GZIP           The pandas dataframe will be saved to this file in a
                        compressed gzip format.
  -v, --verbose         Set the logging level to INFO. To set the logging
                        level to DEBUG use -vv.
  -s, --silent          Disable logging altogether.
```

## Pipeline
![pipeline is in Parserformat.png](Parser%20format.png)

If you want to add a new stat it is best to do it in the advanced stats section of the pipeline.
You should look at:

[Stat base classes](codebreaker/analysis/stats/stats.py)

[Where you add a new stat](codebreaker/analysis/stats/stats_list.py)

If you want to see the output format of the stats created you can look [here](api)

Compile the proto files by running in this directory
`setup.bat` (Windows) or `setup.sh` (Linux/mac)

[![Build Status](https://travis-ci.org/SaltieRL/codebreaker.svg?branch=master)](https://travis-ci.org/SaltieRL/codebreaker)
[![codecov](https://codecov.io/gh/SaltieRL/codebreaker/branch/master/graph/badge.svg)](https://codecov.io/gh/SaltieRL/codebreaker)


## Tips

Linux set `python3.6` as `python`:
```Python3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
```
This assumes you already have 3.6 installed.

## Developing
Everyone is welcome to join the codebreaker (and calculated.gg) project! Even if you are a beginner, this can be used as an opportunity to learn more - you just need to be willing to learn and contribute.

### Usage of GitHub
All contributions end up on the codebreaker repository.  If you are new to the project you are required to use your own fork for first changes. If you do not have any previous git / github experience that is completely fine - we can help with it.
If we believe that you are comitted to working on the project and have experience in git we may give you write access so that you no longer have to use a fork. Nonetheless, please wait until your contrubtion is ready for a review to make the pull request because that will save resources for our tests and reduce spam.
For testing you should use your own fork, but take note that some codebreaker tests may fail on a fork

### Learning about codebreaker
Currently, there is active creation of the codebreaker wiki on GitHub - it aims to provide all relevant information about codebreaker and development, so if you are a beginner, definitely have a look there. If you can't find information that you were looking for, your next option is the calculated.gg Discord server, where you may send a message to the #help channel.

The codebreaker code is also documented, although sparsely. However, you still may find information there, too.

### Testing
The main requirement is to run PyTest. If you are using an IDE that supports integrated testing (e.g. PyCharm), you should enable PyTest there. The secondary requirement (to compile the proto files) is to run the appropriate `setup` file (setup.bat for Windows, setup.sh for Linux/Mac).

If you've never tested your code before, it is a good idea to learn that skill with PyTest! Have a look at their official documentation, or any other tutorials. 

### codebreaker Performance
codebreaker powers calculated.gg, which analyses tens of thousands of replays per day. Therefore, performance is very important, and it is monitored and controlled using PyTest-Benchmarking, which is implemented via GitHub Actions. However, you may see your contribution's performance locally - look into PyTest-Benchmarking documentation. If your contribution is very inefficient - it will fail automatically.

If you wish to see the current codebreaker analysis performance, it is split into 5 replay categories, and can be accessed below:
* [Short Sample](https://saltierl.github.io/codebreaker/dev/bench/short_sample/)
  * A very short soccar replay - for fast benchmarking.
* [Short Dropshot](https://saltierl.github.io/codebreaker/dev/bench/short_dropshot/)
  * A very short dropshot replay - to test dropshot performance.
* [Rumble](https://saltierl.github.io/codebreaker/dev/bench/full_rumble/)
  * A full game of rumble - to test rumble performance.
* [RLCS](https://saltierl.github.io/codebreaker/dev/bench/oce_rlcs/)
  * A full soccar RLCS game.
* [RLCS (Intensive)](https://saltierl.github.io/codebreaker/dev/bench/oce_rlcs_intensive/)
  * A full soccar RLCS game, but run with the intense analysis flag.
