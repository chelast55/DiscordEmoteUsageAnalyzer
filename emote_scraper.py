import csv
import re

import io_helper as io


custom_emote_filepath = "res/custom.csv"


def run(input_directory: str):
    # import discord channel text files
    text_channels = io.read_input_files(input_directory)

    # scan all text channels for emotes or rather text surrounded by colons
    custom_emotes = set([])
    for text_channel in text_channels:

        for found_emote in re.findall(re.compile(rf":([A-Za-z0-9_\-]+|{{Reactions}}[A-Za-z0-9_\-]+ ):"), text_channel):
            custom_emotes.add(found_emote)

    # print csv (usage count)
    with open(custom_emote_filepath, 'w', newline='', encoding="utf8") as custom_emotes_file:
        emote_usage_writer = csv.writer(custom_emotes_file, delimiter=';')
        for custom_emote in custom_emotes:
            emote_usage_writer.writerow([custom_emote])