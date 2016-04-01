import glob
from multiprocessing import Pool

class Trainer:
    """ Fetch data for a language and train it"""
    def __init__(self, directory):
        for file_name in glob.glob('*.txt'):
            with open(file_name) as f:


