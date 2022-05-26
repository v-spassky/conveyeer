import os
import csv
import json
import yaml

"""
This is a set of functions for converting listings 
of electrical items from multi-platform formats to a list.
Supposed to be used in context, shown in .example/demo.py.
"""


def txt2list(path_to_file):
    """
    Converts .txt file to a list.
    """

    res = []

    with open(path_to_file, 'r') as txtfile:
        for line in txtfile:
            items_in_line = line.rstrip().split(', ')
            for item in items_in_line:
                res.append(item)

    return res


def csv2list(path_to_file):
    """
    Converts .csv file to a list.
    """

    res = []

    with open(path_to_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            for item in row:
                res.append(item)

    return res


def json2list(path_to_file):
    """
    Converts .json file of the following structure to a list:

    [
        "item_1",
        "item_2",
        "item_3",
        ...
        "item_N"
    ]
    """

    with open(path_to_file, 'r') as json_file:
        try:
            list = json.load(json_file)
        except json.JSONDecodeError as exc:
            print(exc)
            return f'Error! {exc}'

    return list


def yaml2list(path_to_file):
    """
    Converts .yaml file of the following structure to a list:

    - item_1
    - item_2
    - item_3
    ...
    - item_N
    """

    with open(path_to_file, 'r') as yaml_file:
        try:
            list = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
            return f'Error! {exc}'

    return list


convertion_functions = {
    '.txt': txt2list,
    '.csv': csv2list,
    '.json': json2list,
    '.yaml': yaml2list,
}


def to_list(path_to_file):
    """
    Converts .txt, .csv, .json, .yaml file to a list.
    """

    file_extension = os.path.splitext(path_to_file)[1].lower()

    corresponding_function = convertion_functions.get(file_extension)

    return corresponding_function(path_to_file)
