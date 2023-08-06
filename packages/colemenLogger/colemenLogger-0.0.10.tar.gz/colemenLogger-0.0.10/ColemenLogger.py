from Colors import Colors
from SingleLine import SingleLine
# from SingleLine import singleLineFactory
from LoadingBar import LoadingBar

import os
import re
import sys
import time
import math

# RaLog_Colors.getRGBByColorName("red")
# css = fileUtils.readFile(r'K:\OneDrive\Structure\Ra9\2021\21-0056 - RaLog\REV-0001\.venv\RaLog\css\defaultStyles.css')

# dct = {}
# sheet = cssutils.parseString(css)

# for rule in sheet:
#     selector = rule.selectorText
#     styles = rule.style.cssText
#     dct[selector] = styles


class ColemenLogger:
    def __init__(self):
        self.data = {}
        self.terminal = sys.stdout
        self.__setDefaults()

    def __setDefaults(self):
        # self.data['loadingBar_appendMessage'] = False
        # self.data['loadingBar_loadColor'] = '#ff000d'
        # self.data['loadingBar_startColor'] = '#ff000d'
        # self.data['loadingBar_endColor'] = '#53f600'
        # contains the line number that the cursor is currently on
        self.data['cursor_line_num'] = 0
        self.data['BASE_INDENT'] = 0
        self.data['indentCount'] = self.data['BASE_INDENT']
        self.data['COLOR_BY_INDENT'] = False
        # apply the current preset settings immediately after each <RESET>
        self.data['APPLY_PRESET_AFTER_RESET'] = True
        # resets the all styles to the default settings
        self.data['RESET_AT_END_OF_LINE'] = True
        # Add a new line after each log
        self.data['PRINT_TO_NEW_LINE'] = True
        self.data['OVER_WRITE'] = True
        # stores the array of SingleLine objects that have been submitted to the console
        self.data['console_log'] = []
        self.data['default_preset'] = "INFO"
        self.Colors = Colors()
        self.data['PRESET_SEQUENCES'] = {}
        self.data['PRESETS_RAW'] = {
            "SUCCESS": ["LIGHT_GRAY", "LIGHT_GREEN", "NONE"],
            "SUCCESS_INVERT": ["BLACK", "LIGHT_GREEN", "INVERSE"],
            "FATAL_ERROR": ["RED", "BLACK", "BOLD"],
            "FATAL_ERROR_INVERT": ["RED", "BLACK", "INVERSE,BOLD"],
            "WARNING": ["LIGHT_GRAY", "YELLOW", "BOLD"],
            "WARNING_INVERT": ["LIGHT_GRAY", "YELLOW", "INVERSE"],
            "INFO": ["LIGHT_GRAY", "BLACK", "NONE"],
            "INFO_INVERT": ["LIGHT_GRAY", "BLACK", "INVERSE"],
            "INFO_HEADER": ["WHITE", "BLACK", "BOLD"],
            "LOADING_BAR": ["lawngreen", "NONE", "NONE"],
        }
        self.__generatePresetSequences()

    def log(self, value, **kwargs):

        textDivider = False
        colorByIndent = self.data['COLOR_BY_INDENT']
        if 'INCDEC' in kwargs:
            incdecVal = kwargs['INCDEC']
            self.__parseIncDec(incdecVal)

        if 'COLOR_BY_INDENT' in kwargs:
            if self.data['COLOR_BY_INDENT'] is True:
                self.data['COLOR_BY_INDENT'] = False
            else:
                self.data['COLOR_BY_INDENT'] = True
                colorByIndent = True
        if 'TEXT_DIVIDER' in kwargs:
            if kwargs['TEXT_DIVIDER'] is True:
                textDivider = True
        if 'SAME_LINE' in kwargs:
            if kwargs['SAME_LINE'] is True:
                self.data['PRINT_TO_NEW_LINE'] = False

        ld = {
            "value": value,
            "lineNumber": len(self.data['console_log']),
            "textDivider": textDivider,
            "colorByIndent": colorByIndent
        }
        singleLine = SingleLine(self, ld)
        self.data['console_log'].append(singleLine)
        value = singleLine.master()

        self._sendToTerminal(value)
        self.data['PRINT_TO_NEW_LINE'] = True
        self.data['cursor_line_num'] += 1
        return singleLine
        # print(len(self.data['console_log'])-1)

    def __parseIncDec(self, value):
        if value is False or value is None:
            self.data['indentCount'] = self.data['BASE_INDENT']

        # if the INCDEC is an integer, set the indentCount absolutely
        if isinstance(value, int) is True:
            if value >= 0:
                self.data['indentCount'] = value
            else:
                self.data['indentCount'] -= value

        if isinstance(value, str) is True:
            # reset is the same as incdec being False or none, it sets the indentCount to the base level
            if value == "RESET":
                self.data['indentCount'] = self.data['BASE_INDENT']
            else:
                matches = re.search(r'(?P<OPERATOR>[+-])?(?P<VALUE>[0-9]+)', value)
                operator = matches.group('OPERATOR')
                value = int(matches.group('VALUE'))
                if operator == "-":
                    self.data['indentCount'] -= value
                if operator == "+":
                    self.data['indentCount'] += value

    def _sendToTerminal(self, fullMessage):
        if self.data['OVER_WRITE'] is True:
            fullMessage += "\r"

        if self.data['PRINT_TO_NEW_LINE'] is True:
            fullMessage += "\n"

        sys.stdout.flush()
        # fullMessage = f"{self.data['cursor_line_num']}  {fullMessage}"
        self.terminal.write(fullMessage)
        sys.stdout.flush()

    def __generatePresetSequences(self):
        pr = self.data['PRESETS_RAW']
        if len(pr) > 0:
            # pylint: disable = unused-variable
            for i, x in enumerate(pr):
                name = x
                d = self.data['PRESETS_RAW'][name]
                seq = ""
                txtColor = self.Colors.getRGBByColorName(d[0])
                # print(f"PRESET ======= txtColor: {txtColor}")
                bgColor = self.Colors.getRGBByColorName(d[1])
                # print(f"PRESET ======= bgColor: {bgColor}")
                if bgColor is not False:
                    seq += self.Colors.genRGBBgColorSeq(bgColor)
                if txtColor is not False:
                    seq += self.Colors.genRGBTextColorSeq(txtColor)
                self.data['PRESET_SEQUENCES'][name] = seq

        # print(f"self.data['PRESET_SEQUENCES']: {self.data['PRESET_SEQUENCES']}")

    def getPresetByName(self, name):
        name = name.strip()
        name = name.upper()
        # print(f"getPresetByName: {name}")
        if name in self.data['PRESET_SEQUENCES']:
            return self.data['PRESET_SEQUENCES'][name]
        else:
            return False

    def __genCursorNavSeq(self, dire, count):
        """
        Generates the ANSI escape sequences to move the cursor in the console
        """
        if dire == "UP":
            return f"\u001b[{count}A"
        if dire == "DOWN":
            return f"\u001b[{count}B"

    def goToLineNumber(self, lineNum=0):
        # print(f"goToLineNumber: {lineNum}")
        # print(f"cursor_line_num: {self.data['cursor_line_num']}")
        # time.sleep(2)
        if isinstance(lineNum, str) is True:
            lineNum = lineNum.strip().upper()
            if lineNum == "LAST":
                lineNum = len(self.data['console_log'])-1

        if lineNum > self.data['cursor_line_num']:
            delta = lineNum - self.data['cursor_line_num']
            sys.stdout.write(self.__genCursorNavSeq("DOWN", delta))
            self.data['cursor_line_num'] = lineNum

        if lineNum < self.data['cursor_line_num']:
            delta = self.data['cursor_line_num'] - lineNum
            sys.stdout.write(self.__genCursorNavSeq("UP", delta))
            self.data['cursor_line_num'] = lineNum

    def upLine(self, count=1):
        """
        Move the cursor up x number of lines
        """
        sys.stdout.write(self.__genCursorNavSeq("UP", count))

    def goToBottom(self):
        sys.stdout.write(self.__genCursorNavSeq("DOWN", 1000))

    def clearTerminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clearLine(self, lineNum=False):
        if lineNum is not False:
            self.goToLineNumber(lineNum)
        fullMessage = f"\033[K\r"
        self.terminal.write(fullMessage)
        sys.stdout.flush()
        # print("\033[K", end='\r')

    def loadingBar(self, data):
        data['lineNumber'] = len(self.data['console_log']) - 1

        ld = {
            "value": '',
            "lineNumber": len(self.data['console_log']),
            "textDivider": False,
            "colorByIndent": False
        }

        sl = SingleLine(self, ld)
        sl.master()
        sl.genLoadingBar(data)
        # slCode = singleLineFactory([LoadingBar])
        # sl = slCode(self, data)
        self.data['console_log'].append(sl)
        # print(self.data['console_log'])
        # sl.printMyData()
        # sl.listMyMethods()

        # singleLine = SingleLine(self, ld)
        # self.data['console_log'].append(sl)
        # value = sl.genLoadingBar()
        # self.data['cursor_line_num'] += 1
        return sl


# RaLog = RaLog()
# log = RaLog.log
# # print = RaLog.log


# log(f"<p:FATAL_ERROR> test <txt:aqua>message <RESET>with<txt:green,bg:blue> preset")
# time.sleep(1)
# log(f"here is some message")
# lbd = {
#     "total_tasks": 100,
#     "tasks_complete": 0,
#     "reverse_direction": False,
#     "txt_load_color": "#EE82EE",
#     "txt_start_color": "#9932CC",
#     "txt_end_color": "#FF00FF",
#     "bar_end_chars": ["", ""],
#     "bar_ends_color": "#ffffff",
#     "loading_char": "\\",
#     "incomplete_char": "/",
#     "show_percent": True,
#     "show_est_duration": True,
#     "total_width": 100,
#     # "show_task_summary": True,
# }
# lineObj = log(f"<p:INFO_HEADER> Another Message!!!", COLOR_BY_INDENT=True)
# # time.sleep(1)
# log(f"Another Message!!!", INCDEC=2)
# lineObj.updateLine("UPDATED LINE VALUE")

# Loader = RaLog.loadingBar(lbd)
# LoaderOne = RaLog.loadingBar(lbd)
# for i in range(0, 100):
#     time.sleep(0.025)
#     # ts = time.time()
#     Loader.update({"total_tasks": 100, "tasks_complete": i})
#     # LoaderOne.update({"total_tasks": 80, "tasks_complete": i})
# # print("")

# Loader.update({"loading_char": "/", "reverse_direction": True})
# for i in range(0, 100):
#     # time.sleep(0.1)
#     time.sleep(0.05)
#     ts = time.time()
#     # log(f"<p:INFO_HEADER> Another Message!!!", COLOR_BY_INDENT=True)
#     Loader.update({"tasks_complete": i})
# print("")


# twine upload dist/*
