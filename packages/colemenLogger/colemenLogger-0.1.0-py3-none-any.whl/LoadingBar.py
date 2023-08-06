from Colors import Colors
# from SingleLine import SingleLine
from datetime import datetime
import os
import re
import sys
import time
import math
# pylint: disable=no-member


class LoadingBar:
    def __init__(self, singleLine, data):
        self.singleLine = singleLine
        self.RaLog = singleLine.RaLog
        self.Colors = self.RaLog.Colors
        self.data = data
        self.__setDefaults()

    def __setDefaults(self):
        self.defaults = {
            "total_tasks": {"default": 0, "type": int},
            "tasks_complete": {"default": 0, "type": int},
            "append_message": {"default": '', "type": str},

            # this sets the color of all the loading chars (if use_text_gradient is False)
            "txt_load_color": {"default": None, "type": str},
            # this sets the background color of all the loading chars (if use_text_gradient is False)
            "bg_load_color": {"default": None, "type": str},
            "bg_start_color": {"default": None, "type": str},
            "bg_end_color": {"default": None, "type": str},
            # if True, the gradient colors are applied to the loading bar characters
            "use_text_gradient": {"default": False, "type": bool},
            "use_bg_gradient": {"default": False, "type": bool},
            # The color [hex|colorname] to start the gradient from
            "txt_start_color": {"default": None, "type": str},
            # The color [hex|colorname] to end the gradient on
            "txt_end_color": {"default": None, "type": str},
            "bar_ends_color": {"default": None, "type": str},
            "bar_end_chars": {"default": ["[", "]"], "type": list},

            # contains the array of colors to use for each char of the loading bar
            "txt_gradient_array": {"default": [], "type": list},
            # contains the array of background colors to use for each char of the loading bar
            "bg_gradient_array": {"default": [], "type": list},
            # How many characters wide the loading bar will be, this does not include the percentage or brackets
            "total_width": {"default": 50, "type": int},
            # The character to use within the loading bar.
            "loading_char": {"default": "#", "type": str},
            "incomplete_char": {"default": " ", "type": str},
            # If True, show the percentage value on the left of the loading bar.
            "show_percent": {"default": True, "type": bool},
            "reverse_direction": {"default": False, "type": bool},
            "show_task_summary": {"default": False, "type": bool},
            "show_est_duration": {"default": False, "type": bool}
        }

        # pylint: disable=unused-variable
        for i, x in enumerate(self.defaults):
            key = x
            default = self.defaults[x]['default']
            dType = self.defaults[x]['type']

            # print(f"key: {key} - default: {default} - dType: {dType}")
            # print(f"i: {i} - x: {x} = {self.defaults[x]}")
            if key not in self.data:
                self.data[key] = default
            else:
                existsVal = self.data[key]
                # print(self.defaults[x])
                if isinstance(existsVal, dType) is False:
                    self.data[x] = default

        # self.printMyData()

        if len(str(self.data['loading_char'])) > 1:
            self.data['loading_char'] = "#"
        if len(str(self.data['incomplete_char'])) > 1:
            self.data['incomplete_char'] = " "

        self.data['__live_timestamp'] = False
        self.data['__updates_array'] = []
        # how many characters wide the "complete" portion of the loading bar is
        self.data['__complete_width'] = 0
        self.data['__complete_string'] = ''
        self.data['__percentage_string'] = ''
        # how many characters wide the "incomplete" portion of the loading bar is
        self.data['__incomplete_width'] = 1
        self.data['__incomplete_string'] = ''
        self.__generateGradientArrays()

    def __generateGradientArrays(self):
        """
        generates the color array for the loading bar text and background.
        This should execute regardless of if the use_text_gradient setting is True or False, because
        each character is colored individually, regardless.

        @name generateGradientArray
        @author Colemen Atwood
        @created 04/25/2021 10:01:21
        @version 1.0
        """
        self.__genTextColorArray()

        self.data['bg_gradient_array'] = False
        # bg_startColor = self.data['bg_load_color']
        # bg_endColor = self.data['bg_load_color']
        # if self.data['use_text_gradient'] is True:
        #     bg_startColor = self.data['bg_start_color']
        #     bg_endColor = self.data['bg_end_color']
        # if bg_startColor is not None and bg_endColor is not None:
        #     self.data['bg_gradient_array'] = self.Colors.calculateGradient(bg_startColor, bg_endColor, self.data['total_width'])

    def update(self, data):
        # pylint: disable=unused-variable
        for i, x in enumerate(data):
            # print(f"i: {i} - x: {x} = {defaults[x]}")
            self.data[x] = data[x]

        self.__calculateCurrentStats()
        self.__generateStrings()
        # print(self.data['__full_line'])

        # self.singleLine.data['liveValue'] = self.data['__full_line']
        self.singleLine.updateLine(self.data['__full_line'])

    def __logUpdate(self):
        self.data['__estimated_sec_remaining'] = len(self.data['__updates_array'])
        if len(self.data['__updates_array']) > 10:
            self.data['__estimated_sec_remaining'] = "purge updates array"
            self.data['__updates_array'] = self.data['__updates_array'][:10]
        # if len(self.data['__updates_array']) > 0:
        data = {}
        data['avgTimePerTask'] = self.__calcAvgTimePerTask()
        data['totalTasks'] = self.data['total_tasks']
        data['tasksComplete'] = self.data['tasks_complete']
        data['timestamp'] = self.data['__update_timestamp']
        data['timeRemaining'] = data['avgTimePerTask'] * (data['totalTasks'] - data['tasksComplete'])
        self.data['__estimated_sec_remaining'] = data['timeRemaining']
        self.data['__updates_array'].append(data)

    def __calcAvgTimePerTask(self):
        tasksPerMS = 1
        if len(self.data['__updates_array']) > 0:
            startTasksComplete = self.data['__updates_array'][-1]['tasksComplete']
            startTimeStamp = self.data['__updates_array'][-1]['timestamp']

            endTasksComplete = self.data['tasks_complete']
            endTimeStamp = self.data['__update_timestamp']

            timeDelta = endTimeStamp - startTimeStamp
            taskDelta = startTasksComplete - endTasksComplete
            if taskDelta > 0:
                tasksPerMS = math.floor((timeDelta/taskDelta))
        return tasksPerMS

    def __calculateCurrentStats(self):
        self.data['__update_timestamp'] = time.time()
        totalTasks = self.data['total_tasks']
        tasksComplete = self.data['tasks_complete']
        if totalTasks is not False and tasksComplete is not False and totalTasks != 0:
            if totalTasks < tasksComplete:
                tasksComplete = totalTasks
            self.data['__complete_percent'] = tasksComplete / totalTasks
            # self.data['__complete_width'] = round(self.data['total_width'] * self.data['__complete_percent'])
            self.data['__complete_width'] = math.ceil(self.data['total_width'] * self.data['__complete_percent'])
            self.data['__incomplete_width'] = self.data['total_width'] - self.data['__complete_width']

        self.data['__live_timestamp'] = datetime.utcfromtimestamp(self.data['__update_timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        if self.data['show_est_duration'] is True:
            self.__logUpdate()

    def __generateStrings(self):
        """
        Generates the __complete_string, __incomplete_string,__percentage_string,__bar_string

        @name __generateStrings
        @author Colemen Atwood
        @created 04/25/2021 10:12:57
        @version 1.0
        """
        self.data['__complete_string'] = ""
        self.data['__incomplete_string'] = ""
        self.data['__percentage_string'] = "0%"
        self.__generateCompleteString()
        self.data['__complete_string'] = self.__arrayToString(self.data['__complete_txt_array'])
        self.data['__incomplete_string'] = f"{self.data['incomplete_char']}"*self.data['__incomplete_width']

        self.data['__percentage_string'] = f"{math.ceil(self.data['__complete_percent'] * 100)}%"
        self.data['__full_line'] = self.__generateBarString()
        if self.data['show_percent'] is True:
            pstr = f"{math.ceil(self.data['__complete_percent'] * 100)}%"
            if self.data['total_tasks'] == self.data['tasks_complete']:
                pstr = f"100%"
            plen = len(pstr)
            pgap = " "*(4 - plen)
            compWhole = f"{pstr}{pgap}"
            self.data['__full_line'] = f"{compWhole} - {self.data['__full_line']}"

        if self.data['show_task_summary'] is True:
            tasksComplete = self.data['tasks_complete']
            totalTasks = self.data['total_tasks']

            if self.data['__complete_width'] == self.data['total_width']:
                tasksComplete = totalTasks

            totalTasksCharLen = len(str(totalTasks))
            tasksCompleteCharLen = len(str(tasksComplete))

            gapString = " "*(totalTasksCharLen - tasksCompleteCharLen)
            taskString = f"[ {tasksComplete}{gapString} | {totalTasks} ]"
            self.data['__full_line'] = f"{self.data['__full_line']}  {taskString}"

        if self.data['show_est_duration'] is True and self.data['__estimated_sec_remaining'] >= 0:
            if self.data['__complete_width'] != self.data['total_width']:
                self.data['__full_line'] = f"{self.data['__full_line']} - {self.data['__estimated_sec_remaining']}"

        appendMessage = str(self.data['append_message'])
        if len(appendMessage) > 0:
            self.data['__full_line'] = f"{self.data['__full_line']} - {appendMessage}"

        self.data['__full_line'] = f"{self.data['__full_line']}                                     "

    def __generateBarString(self):
        bar_ends_color = self.data['bar_ends_color']
        openingBracket = f"["
        closingBracket = f"]"
        if len(self.data['bar_end_chars']) == 2:
            openingBracket = f"{self.data['bar_end_chars'][0]}"
            closingBracket = f"{self.data['bar_end_chars'][1]}"

        barInterior = f"{self.data['__complete_string']}{self.data['__incomplete_string']}"
        if bar_ends_color is not None:
            openingBracket = f"<txt:{bar_ends_color}>{openingBracket}<RESET>"
            closingBracket = f"<txt:{bar_ends_color}>{closingBracket}<RESET>"

        if self.data['reverse_direction'] is True:
            barInterior = f"{self.data['__incomplete_string']}{self.data['__complete_string']}"

        return f"{openingBracket}{barInterior}{closingBracket}"

    def __arrayToString(self, array):
        string = ''
        for x in array:
            string += x
        return string

    def __generateCompleteString(self):
        self.data['__complete_string'] = ""
        # first, populate the txtOnlyArray with the characters and resets, but no colors
        self.data['__complete_txt_array'] = []
        for x in range(self.data['__complete_width']):
            self.data['__complete_txt_array'].append(f"{self.data['loading_char']}<RESET>")

        self.__applyTextLoadColor()
        # txtColorArray = []

        # if self.data['bg_load_color'] is None or self.data['use_bg_gradient'] is False:
        #     return txtColorArray

        # finalArray = []
        # for i, x in enumerate(txtColorArray):
        #     line = f"<bg:{self.data['bg_gradient_array'][i]}>{x}"
        #     finalArray.append(line)

        # self.data['__complete_string'] += f"<bg:{self.data['bg_gradient_array'][x]},txt:{self.data['txt_gradient_array'][x]}>{self.data['loading_char']}<RESET>"
        # self.data['__incomplete_string'] = ' '*self.data['__incomplete_width']

    def __genTextColorArray(self):
        txt_startColor = False
        txt_endColor = False

        if self.data['txt_load_color'] is not None:
            txt_startColor = self.data['txt_load_color']
            txt_endColor = self.data['txt_load_color']

        if self.data['txt_start_color'] is not None and self.data['txt_end_color'] is not None:
            txt_startColor = self.data['txt_start_color']
            txt_endColor = self.data['txt_end_color']

        if txt_startColor is False or txt_endColor is False:
            self.data['txt_gradient_array'] = False
        else:
            self.data['txt_gradient_array'] = self.Colors.calculateGradient(txt_startColor, txt_endColor, self.data['total_width'] + 10)

    def __applyTextLoadColor(self):
        txtGradArray = self.data['txt_gradient_array']
        # print(txtGradArray)

        if txtGradArray is not False:
            outputArray = []
            for i, x in enumerate(self.data['__complete_txt_array']):
                line = f"<txt:{txtGradArray[i]}>{x}"
                outputArray.append(line)
            self.data['__complete_txt_array'] = outputArray

        # def loadingBar_OLD(self, complete=False, **kwargs):
        #     showPercent = True
        #     totalTasks = False
        #     loadColor = self.data['txt_load_color']
        #     loadColor = self.data['txt_load_color']
        #     startColor = self.data['txt_start_color']
        #     endColor = self.data['txt_end_color']

        #     if complete is False:
        #         complete = self.data['lastLoadingBarValue']

        #     self.data['loadingBarActive'] = True
        #     if 'TOTAL_TASKS' in kwargs:
        #         totalTasks = kwargs['TOTAL_TASKS']
        #     if 'TASKS_COMPLETE' in kwargs:
        #         tasksComplete = kwargs['TASKS_COMPLETE']
        #         if totalTasks is not False:
        #             complete = math.ceil(tasksComplete / totalTasks)

        #     if '__MESSAGE' in kwargs:
        #         self.data['loadingBar_appendMessage'] = kwargs['__MESSAGE']

        #     if 'HIDE_PERCENT' in kwargs:
        #         if kwargs['HIDE_PERCENT'] is False:
        #             showPercent = False

        #     if complete > 1:
        #         complete = complete / 100

        #     totalWidth = 50
        #     completeWidth = math.ceil(totalWidth * complete)

        #     bar = f"[{completeString}{incompleteString}]"
        #     if showPercent is True:
        #         pstr = f"{math.ceil(complete * 100)}%"
        #         if completeWidth == totalWidth:
        #             pstr = f"100%"
        #         plen = len(pstr)
        #         pgap = " "*(4 - plen)
        #         compWhole = f"{pstr}{pgap}"
        #         bar = f"{compWhole} - {bar}"

        #     if self.data['loadingBar_appendMessage'] is not False:
        #         bar = f"{bar}  {self.data['loadingBar_appendMessage']}"

        #     if completeWidth == totalWidth:
        #         self.data['loadingBarActive'] = False
        #         self.data['lastLoadingBarValue'] = 0
        #         self.data['loadingBar_appendMessage'] = False

        #     self.data['lastLoadingBarValue'] = complete
        #     self.RaLog.log("<p:LOADING_BAR>" + bar, SAME_LINE=True, __RETURN_MESSAGE=True, PRESET="LOADING_BAR")
        #     # self.log("<p:LOADING_BAR>" + bar, SAME_LINE=True, __RETURN_MESSAGE=True, PRESET="LOADING_BAR")
        #     # sys.stdout.write(u"\u001b[1000D" + bar + "                                                          ")
        #     # sys.stdout.flush()
