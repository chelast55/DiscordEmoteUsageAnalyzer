import csv
import os
import re

custom_emote_filepath = 'res/custom.csv'

def run(input_directory):
    # TODO: refactor, code duplicate
    # import discord channel text files
    text_channels = []
    for file in os.listdir(input_directory):
        if file.endswith(".txt"):
            with open(input_directory + file, "r", encoding="utf8") as text_file:
                text_channels += [text_file.read()]

    # scan all text channels for emotes or rather text surrounded by colons
    custom_emotes = set([])
    for text_channel in text_channels:

        for found_emote in re.findall(re.compile(rf":([A-Za-z0-9_\-]+|{{Reactions}}[A-Za-z0-9_\-]+ ):"), text_channel):
            custom_emotes.add(found_emote)

    # print csv (usage count)
    with open(custom_emote_filepath, 'w+', newline='', encoding="utf8") as custom_emotes_file:
        emote_usage_writer = csv.writer(custom_emotes_file, delimiter=';')
        for custom_emote in custom_emotes:
            emote_usage_writer.writerow([custom_emote])