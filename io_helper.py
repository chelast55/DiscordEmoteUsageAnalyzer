import os
import csv


# create file at file path if not already exists
def create_filepath(filepath: str):
    if not os.path.exists(filepath):
        os.mkdir(filepath)


# read in file as list of its lines
def read_emotes(emotes_filepath: str):
    emotes = []
    with open(emotes_filepath, encoding="utf8") as emote_file:
        emote_reader = csv.reader(emote_file)
        for row in emote_reader:
            emotes += row
    return emotes


# read in all .txt files in given directory and return list of them
def read_input_files(input_directory: str):
    text_channels = []
    for file in os.listdir(input_directory):
        if file.endswith(".txt"):
            with open(input_directory + file, 'r', encoding="utf8") as text_file:
                text_channels += [text_file.read()]
    return text_channels
