from models import *


def insert_spatial_row(line):
    (key, )
    pass


def insert_stats_row(line):
    pass


def load_stats_data(path):
    f = open(path, "r")
    lines = f.readline()

    for line in lines:
        insert_stats_row(line)

    return


def load_spatial_data(path):
    f = open(path, "r")
    lines = f.readline()

    for line in lines:
        insert_spatial_row(line)

    return
