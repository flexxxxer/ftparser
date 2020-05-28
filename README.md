# Fthndlr
Tool for extracting and creating frame time statistics from logs of frametime recording programs

## Getting Started
### Prerequisites
To work correctly, you need the installed **relevant** Python language environment version. Relevant versions Python environments and installation files (official site): [link](https://www.python.org/downloads/).
### Installing
For installation you just need to download the [fthndlr.py](https://github.com/FlexxxerAlex/fthndlr/blob/master/fthndlr.py) file (which is located in the root directory of the repository) and do not forget the location of the downloaded file :grinning:

## Usage
##### Learn how to execute python
Depending on the operating systems (windows, macos, linux) and the environment, starting Python may be *slightly* different. Our goal is to find out which command launches (and whether it launches) the current version of python on your device. *All the following commands must be executed in the console / terminal*

**First case:** `python --version`. If the result (which was printed in the console / terminal) is equal to *Python N* (where N - relevant Python language version), then all usage instructions below are valid for your device. You should not follow subsequent cases.

**Second case:** `pythonM --version`, where M - **first digit** of relevant Python language version (e.g. you installed the Python version number 3.8.2 - you must substitute 3 for M). If the result (which was printed in the console / terminal) is equal to *Python N* (where N - relevant Python language version), then you should use the **pythonM** entry instead of **python** in the usage instructions.

##### Script execution
In order to run the [fthndlr.py](https://github.com/FlexxxerAlex/fthndlr/blob/master/fthndlr.py) script, you need to write the following to console/terminal:

`$> python fthndlr.py [args]`, where `[args]` - script arguments

**What arguments can be passed?**
Show help info and supported arguments list:

`$> python fthndlr.py --help` or `python fthndlr.py -h`

#### FAQ
**How can I process the FrameView logs?**

`$> python fthndlr.py -f frameviewlog.csv -p frameview`, where `frameviewlog.csv` - FrameView log file.

**How can I process the Fraps logs?**

`$> python fthndlr.py -f frapslog.csv -p fraps`, where `frapslog.csv` - Fraps log file.

**How can I write the processing results to a file?**
You should append `-o filename` after the main part with `-f [file] -p [program]`, e.g. for FrameView:

`$> python fthndlr.py -f fvlog.csv -p frameview -o results.txt`

## Roadmap
| Feature | Summary | Linked issues | Status |
| --- | --- | --- | --- |
| frameview support | parer support for frameview log files | | :heavy_check_mark: |
| fraps support | parer support for frameview log files | | :heavy_check_mark: |
| any linux tool support | parer support for any linux frametime tool | | :clock9: |
| any macos tool support | parer support for any macos frametime tool | | :clock9: |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
