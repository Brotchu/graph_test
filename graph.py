#!/usr/bin/python3

import re
import json

class InputFile:
    def __init__( self, file_url, json_dml):
        self.file_url = file_url
        dml_file = open(json_dml, "r")
        dml_string = dml_file.read()
        parsed_dml = json.loads( dml_string)
        temp = list( parsed_dml.items() )

        self.dml = [(i[0], list(i[1].keys())[0], list(i[1].values())[0]) for i in temp ]
        self.castDict = { "int": lambda x : int(x), "float": lambda x : float(x), "string": lambda x: x}

    def readData(self):
        def mapType(a,b):
            return b(a)

        re_list = []
        for item in self.dml:
            re_list.append(item[2])
        delims_re = "|".join( map(re.escape, re_list) )

        fileVar = open(self.file_url, "r")
        dataList = []

        for line in fileVar:
            line = line.rstrip('\n')
            line = re.split(delims_re, line)
            temp_line = []
            for field in line:
                temp_line.append( mapType(field, self.castDict[self.dml[line.index(field)][1]]) )
            dataList.append(temp_line)

        typeList = []
        for vals in dataList[0]:
            typeList.append( (self.dml[dataList[0].index(vals)][0], type(vals)) )

        return (dataList,typeList)

class Reformat:
    def __init__(self, dataInfo):
        self.in_dml = dataInfo[1]
        self.field = []
        for i in self.in_dml:
            self.field.append(i[0])

    def getType(self, recs):
        typeList = []
        for i in recs:
            typeList.append( type(i))
        return typeList

    def transformData(self, inData, transformFunc = None ):
        def map_transform(in_list, in_func):
            res = []
            print(self.field)
            print(type(self.field))
            for i in in_list:
                res.append( in_func(i, self.field))
            return res

        if transformFunc == None:
            return (inData, self.in_dml)
        else:
            return map_transform( inData, transformFunc)


class OutputFile:
    def __init__(self, file_path, mode):
        self.file_path = file_path
        self.mode = mode

    def writeFile(self, inData):
        fileDesc = open(self.file_path , self.mode )
        def mapCast(in_list):
            res = []
            for i in in_list:
                res.append(str(i))
            return (",".join(res)+'\n')
        convertedData = [mapCast(j) for j in inData]
        print(convertedData)
        fileDesc.writelines(convertedData)
        fileDesc.close()
        
