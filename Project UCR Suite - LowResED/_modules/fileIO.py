"""
This module is for input and outout files from hard disk sequence.
Functions:  readQuery () --> [query0, query1, query2, query3, query4]
            readData () --> data
"""
import os
import json
import time


def readQuery(script_dir: str):
    """
    This function is for reading query from hard disk.
    ================================================================
    Input:
      rawQuery: [], a list of unnormalized raw queries
      script_dir: string, the path of python script
    Output:
      rawQuery: [query0, query1, query2, query3, query4], in which query is list of float
    """
    rawQuery = []

    read_path = os.path.join(script_dir, 'rawData/query0.json')
    textfile = open(read_path, "r")
    rawQuery.append(json.loads(textfile.read()))
    textfile.close()

    read_path = os.path.join(script_dir, 'rawData/query1.json')
    textfile = open(read_path, "r")
    rawQuery.append(json.loads(textfile.read()))
    textfile.close()

    read_path = os.path.join(script_dir, 'rawData/query2.json')
    textfile = open(read_path, "r")
    rawQuery.append(json.loads(textfile.read()))
    textfile.close()

    read_path = os.path.join(script_dir, 'rawData/query3.json')
    textfile = open(read_path, "r")
    rawQuery.append(json.loads(textfile.read()))
    textfile.close()

    read_path = os.path.join(script_dir, 'rawData/query4.json')
    textfile = open(read_path, "r")
    rawQuery.append(json.loads(textfile.read()))
    textfile.close()

    return rawQuery


def readData(script_dir: str):
    """
    This function is for reading data from hard disk.
    ================================================================
    Input:
      script_dir: string, the path of python script
    Output:
      rawData: [float, float, float, ...]
    """

    print('......', time.ctime(), ' start loading data ......')

    read_path = os.path.join(script_dir, 'rawData/data.json')
    textfile = open(read_path, "r")
    rawData = json.loads(textfile.read())
    textfile.close()
    print('......', time.ctime(), ' finsih loading data ......')

    return rawData
