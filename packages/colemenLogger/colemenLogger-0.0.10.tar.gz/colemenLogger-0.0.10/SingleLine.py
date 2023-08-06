import re
import sys
import time
from LoadingBar import LoadingBar


class SingleLine:
    def __init__(self, RaLog, data):
        self.RaLog = RaLog
        self.data = data
        self.__setDefaults()

    def __setDefaults(self):
        self.Colors = self.RaLog.Colors
        if 'colorByIndent' not in self.data:
            self.data['colorByIndent'] = False
        if 'textDivider' not in self.data:
            self.data['textDivider'] = False
        if 'value' not in self.data:
            self.data['value'] = ''
        self.data['default_style'] = self.RaLog.data['default_preset']
        self.data['liveValue'] = self.data['value'].strip()
        self.data['presets_array'] = []
        self.data['style_tags_array'] = []

        # if this line is a loading bar, initiate the loading Bar setup
        # if hasattr(self, '_LoadingBar__setDefaults') is True:
        # pylint: disable=no-member
        # self._LoadingBar__setDefaults()

    def master(self):
        if self.__isValueEmpty() is True:
            return " "
        self.__parseTags()
        # print(self.data['style_tags_array'])
        # print(self.data['presets_array'])
        self.__applyTextDivider()

        self.__applyPresets()
        self.__applyStyleTags()
        self.__colorTxtByIndent()
        self.__applyIndent()

        self.__applyLineReset()

        return self.data['liveValue']

    def updateLine(self, newValue):
        """
        Updates this lines value in the console.

        @name updateLine
        @author Colemen Atwood
        @created 04/25/2021 08:31:35
        @version 1.0
        @param str $newValue The new value to set.
        @return datatype Description
        TODO: documentation for updateLine
        """
        # set the liveValue to the new value so we can parse it
        self.data['liveValue'] = newValue

        # move the cursor to this line in the terminal
        self.RaLog.goToLineNumber(self.data['lineNumber'])
        # time.sleep(5)
        # clear everything from the line
        self.RaLog.clearLine()

        # if self.data['loadingBar'] is not None:
        #     newValue = self.LoadingBar.update(newValue)

        # if isinstance(self.data['liveValue'], str) is True:

        # apply all of the shit
        lv = self.master()
        optnl = self.RaLog.data['PRINT_TO_NEW_LINE']
        ow = self.RaLog.data['OVER_WRITE']

        self.RaLog.data['PRINT_TO_NEW_LINE'] = False
        self.RaLog.data['OVER_WRITE'] = False
        # write the new value to the terminal
        # sys.stdout.flush()
        self.RaLog._sendToTerminal(lv)
        # sys.stdout.flush()
        self.RaLog.goToLineNumber("LAST")
        self.RaLog.data['PRINT_TO_NEW_LINE'] = optnl
        self.RaLog.data['OVER_WRITE'] = ow

    def genLoadingBar(self, data):
        """
        description

        @name loadingBar
        @author Colemen Atwood
        @created 04/25/2021 09:21:26
        @version 1.0
        @param datatype $Argument Description
        @return datatype Description
        TODO: documentation for loadingBar
        """
        self.LoadingBar = LoadingBar(self, data)
        self.update = self.LoadingBar.update

    def __applyTextDivider(self):
        if self.data['textDivider'] is True:
            self.data['liveValue'] = f"==============================\033[0m {self.data['liveValue']}\033[0m =============================="

    def __applyLineReset(self):
        if self.RaLog.data['RESET_AT_END_OF_LINE'] is True:
            self.data['liveValue'] += "\033[0m"

    def __applyIndent(self):
        indentCount = self.RaLog.data['indentCount']
        indentString = ""
        if indentCount > 0:
            # pylint: disable=unused-variable
            for x in range(indentCount):
                indentString += "   "
        self.data['liveValue'] = f"{indentString}{self.data['liveValue']}"

    def __colorTxtByIndent(self):
        # print(f"__colorTxtByIndent: {self.data['colorByIndent']}")
        if self.data['colorByIndent'] is True:
            lv = self.data['liveValue']
            lv = re.sub(r'(\\x1b[\[0-9;m]*)', '', lv)
            self.data['liveValue'] = f"{self.__getIndentColor()}{lv}"

    def __getIndentColor(self):
        ic = self.RaLog.data['indentCount']
        igc = self.Colors.data['indentGradientColors']
        if len(igc) > 0:
            nic = ic
            if nic > len(igc) - 1:
                while nic > len(igc) - 1:
                    nic -= len(igc) - 1
                return igc[nic]
            return igc[ic]

    def __applyPresets(self):
        lv = self.data['liveValue']
        pa = self.data['presets_array']
        if len(pa) > 0:
            for x in pa:
                if self.RaLog.data['APPLY_PRESET_AFTER_RESET'] is True:
                    lv = lv.replace("<RESET>", fr"<RESET>{x['seq']}")
                lv = lv.replace(x['replace'], x['seq'])
                # print(f"REPLACING PRESET: {x['replace']} WITH: {repr(x['seq'])}")
                # self.__applyStyleObjToValue(x)

        # print(fr"LIVEVALUE : after Style Tags:  {repr(lv)}")
        self.data['liveValue'] = lv

    def __applyStyleTags(self):
        lv = self.data['liveValue']
        lv = lv.replace("<RESET>", "\033[0m")
        lv = lv.replace("<reset>", "\033[0m")
        styleArray = self.data['style_tags_array']
        for x in styleArray:
            if self.__isStyleTagObject(x) is True:
                seq = self.__generateStyleTagSeq(x)
                seq = seq.strip()
                lv = lv.replace(x['replace'], fr"{seq}")
                # print(f"REPLACING: {x['replace']} WITH: {repr(seq)}")
                # self.__applyStyleObjToValue(x)

        # print(fr"LIVEVALUE : after Style Tags:  {repr(lv)}")
        self.data['liveValue'] = lv

    def __generateStyleTagSeq(self, obj):
        finalString = ""
        if obj['bgColor'] is not False:
            b = obj['bgColor']
            if b['seq'] is False:
                b['seq'] = ''
            finalString += b['seq']

        if obj['txtColor'] is not False:
            b = obj['txtColor']
            if b['seq'] is False:
                b['seq'] = ''
            finalString += b['seq']
        return finalString

    def __isStyleTagObject(self, obj):
        if obj['bgColor'] is False and obj['txtColor'] is False:
            return False
        else:
            return True

    def __isValueEmpty(self):
        if len(self.data['liveValue']) == 0:
            return True
        return False

    def __parseTags(self):
        self.__parsePresets()
        self.__parseStyleTags()

    def __parseStyleTags(self):
        self.data['style_tags_array'] = []
        r = re.compile(r'(?P<STYLE_TAG>\<(?P<CONTENT>[^\>]*)\>)')
        match = [m.groupdict() for m in r.finditer(self.data['liveValue'])]
        if match is not None:
            for x in match:
                styleTagData = self.__parseStyleTagContents(x['CONTENT'])
                styleTagData['replace'] = x['STYLE_TAG']
                self.data['style_tags_array'].append(styleTagData)
        return False

    def __parseStyleTagContents(self, string):
        contents = {}
        contents['bgColor'] = self.__parseBgColor(string)
        contents['txtColor'] = self.__parseTxtColor(string)

        return contents

    def __parseBgColor(self, string):
        match = re.search(r'(?P<BGCOLOR>bg:(?P<COLOR>[^\>,]*))', string)
        if match is not None:
            res = {}
            res['replace'] = match['BGCOLOR']
            res['rgb'] = self.Colors.getRGB(match['COLOR'])
            res[r'seq'] = self.Colors.genRGBBgColorSeq(res['rgb'])
            return res
        else:
            return False

    def __parseTxtColor(self, string):
        match = re.search(r'(?P<BGCOLOR>txt:(?P<COLOR>[^\>,]*))', string)
        if match is not None:
            res = {}
            res['replace'] = match['BGCOLOR']
            res['rgb'] = self.Colors.getRGB(match['COLOR'])
            res[r'seq'] = self.Colors.genRGBTextColorSeq(res['rgb'])
            return res
        else:
            return False

    def __parsePresets(self):
        self.data['presets_array'] = []
        # print(self.data['liveValue'])
        r = re.compile(r'(?P<PRESET>\<p:(?P<NAME>[^\>,]*)\>)')
        match = [m.groupdict() for m in r.finditer(self.data['liveValue'])]
        if match is not None:
            for x in match:
                seq = self.RaLog.getPresetByName(x['NAME'])
                if seq is not False:
                    d = {}
                    d['replace'] = x['PRESET']
                    d['seq'] = seq
                    self.data['presets_array'].append(d)
        return False


# def singleLineFactory(base):
#     # base = [base].append(SingleLine)

#     class MyCode(SingleLine, *base):
#         def printMyData(self):
#             print(self.data)

#         def listMyMethods(self):
#             object_methods = [method_name for method_name in dir(self)
#                               if callable(getattr(self, method_name))]
#             for x in object_methods:
#                 print(f"{x}")
#             # print(f"singleLineFactory Test Method")

#     return MyCode
