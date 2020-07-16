import sys
import os
import re
import argparse
import configparser

# statistics object. can create by constructor
class frametime_statistics:
    def __init__(self, frametimes: []):
        self._frametimes = frametimes.copy()

        self._testTime = sum(self._frametimes)

        oneTenthPercentTime = self._testTime / 1000.0  # 0.1%
        onePercentTime = self._testTime / 100.0  # 1%
        fivePercentTime = self._testTime / 20.0  # 5%
        fiftyPercentTime = self._testTime / 2.0  # 50%

        self._frametimes.sort(reverse=True)

        frametimeSum = 0.0
        index = 0

        while frametimeSum < oneTenthPercentTime:
            frametimeSum += self._frametimes[index]
            index += 1

        frametimeSum += self._frametimes[index]
        self._oneTenthPercentFPS = 1000.0 / self._frametimes[index]

        while frametimeSum < onePercentTime:
            frametimeSum += self._frametimes[index]
            index += 1

        self._onePercentFPS = 1000.0 / self._frametimes[index - 1]

        while frametimeSum < fivePercentTime:
            frametimeSum += self._frametimes[index]
            index += 1

        self._fivePercentFPS = 1000.0 / self._frametimes[index - 1]

        while frametimeSum < fiftyPercentTime:
            frametimeSum += self._frametimes[index]
            index += 1

        self._fiftyPercentFPS = 1000.0 / self._frametimes[index - 1]
        self._avgFPS = len(frametimes) / self._testTime * 1000.0

        self._frametimes = frametimes

    @property
    def frametimes(self):
        return self._frametimes

    @property
    def oneTenthPercentFPS(self):
        return self._oneTenthPercentFPS

    @property
    def onePercentFPS(self):
        return self._onePercentFPS

    @property
    def fivePercentFPS(self):
        return self._fivePercentFPS

    @property
    def fiftyPercentFPS(self):
        return self._fiftyPercentFPS

    @property
    def avgFPS(self):
        return self._avgFPS

    @property
    def testTime(self):
        return self._testTime

# error output function
def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# fraps parser
def fraps_parser(filepath: str):
    file = open(filepath, 'r')
    file.readline()  # skip first line

    extract_line_data_regex = r'^\s*(?P<number>.*?),\s*(?P<time>.*?)\s*$'
    last_item_frame_time = 0.0
    frame_times = []

    for line in file:
        matches = re.findall(extract_line_data_regex, line)
        current_time = float(matches[0][1])
        frame_times.append(current_time - last_item_frame_time)
        last_item_frame_time = current_time

    file.close()

    return frame_times

# nvidia frameview parser
def frameview_parser(filepath: str):
    file = open(filepath, 'r')

    column_index = file.readline().split(',').index("MsBetweenDisplayChangeActual")
    frame_times = []

    for line in file:
        frame_time = float(line.split(',')[column_index])
        frame_times.append(frame_time)

    file.close()

    return frame_times

# rtsstimerender parser
def rtsstimerender_parser(filepath: str):
    fraps_parser(filepath)

# supported programs names and them parser functions
parsers_dict = {
    "fraps": fraps_parser,
    "frameview": frameview_parser,
    "rtsstimerender": rtsstimerender_parser
}

argParser = argparse.ArgumentParser(description='tool for frame time parsing and statistics creation')

# script arguments
argParser.add_argument('-f', '--logfile', dest='logfile', help='frame time recording program output file', default=None)
argParser.add_argument('-p', '--programname', dest='pname', help='frame time recording program name', choices=parsers_dict.keys(), default=None)
argParser.add_argument('-o', '--output', dest='outputfilename', help='output filename. if not specified then the output is in stdout', nargs='?', default=None)
argParser.add_argument('--allframes', dest='writeallframes', help='write all frames times to output (by default disabled)', action='store_true', default=False)
argParser.add_argument('--version', dest='showversion', help='show version', action='store_true', default=False)
argParser.add_argument('--spn', dest='supportedprograms', help='supported recording programs names', action='store_true', default=False)

argslist = argParser.parse_args()

# if user want to get version
if argslist.showversion is True:
    print("{name} 0.1".format(name=sys.argv[0]))
    sys.exit()

# if user want to get supported recording programs names
if argslist.supportedprograms is True:
    print(';'.join(list(parsers_dict.keys())))
    sys.exit()

# if the arguments are not specified together
if argslist.logfile is None or argslist.pname is None:
    errprint("Params 'logfile' and 'programname' must be specified together")
    sys.exit()

# if file does not exist
if not os.path.isfile(argslist.logfile):
    errprint("Argument error: {filepath} does not exist. ".format(filepath=os.path.abspath(argslist.logfile)), end='')

    # if output file was specified, then print, else nothing
    if argslist.outputfilename is not None:
        errprint("File '{outputfile}' does not created".format(outputfile=argslist.outputfilename))
    else:
        errprint()

    sys.exit()

# get parser function using supported program name and perform parsing
parser_func = parsers_dict[argslist.pname]
frame_times_list = parser_func(argslist.logfile)

# get statistics
statistics = frametime_statistics(frame_times_list)

# create config file
config = configparser.ConfigParser()

config['frame times'] = {
    '0.1%': statistics.oneTenthPercentFPS,
    '1%': statistics.onePercentFPS,
    '5%': statistics.fivePercentFPS,
    '50%': statistics.fiftyPercentFPS
}
config['statistics'] = {
    'avg': statistics.oneTenthPercentFPS,
    'test time': statistics.testTime
}

# if user want to write all frametimes
if argslist.writeallframes is True:
    config.set('statistics', 'all frames times', str(statistics.frametimes))

# write to file or stdout
if argslist.outputfilename is not None:
    with open(argslist.outputfilename, 'w') as output_file:
        config.write(output_file)
else:
    config.write(sys.stdout)
