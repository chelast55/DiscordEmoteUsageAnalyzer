import csv
import os
import re

vanilla_emote_filepath = 'res/vanilla.csv'
custom_emote_filepath = 'res/custom.csv'


# TODO: overload constructor properly
def run(input_directory, output_directory, filename):
    run_vanilla_check(input_directory, output_directory, filename, False)


def run(input_directory, output_directory, filename, include_vanilla_emotes):
    run_vanilla_check(input_directory, output_directory, filename, include_vanilla_emotes)


def run_vanilla_check(input_directory, output_directory, filename, include_vanilla_emotes):
    # collect desired emotes
    emotes = []
    if include_vanilla_emotes:
        with open(vanilla_emote_filepath, encoding="utf8") as emote_file:
            emote_reader = csv.reader(emote_file)
            for row in emote_reader:
                emotes += row
    with open(custom_emote_filepath, encoding="utf8") as emote_file:
        emote_reader = csv.reader(emote_file)
        for row in emote_reader:
            emotes += row

    # import discord channel text files
    text_channels = []
    for file in os.listdir(input_directory):
        if file.endswith(".txt"):
            with open(input_directory + file, "r", encoding="utf8") as text_file:
                text_channels += [text_file.read()]

    # count emote uses
    text_uses = [0] * len(emotes)
    react_uses = [0] * len(emotes)
    for e in range(0, len(emotes)):
        # unicode emotes are never surrounded by colons in discord-chat-exporter's .txt format
        if include_vanilla_emotes and len(emotes[e]) == 1:
            in_text = re.compile(rf"{re.escape(emotes[e])}")
        else:
            in_text = re.compile(rf":{re.escape(emotes[e])}:")
        in_react = re.compile(rf"{{Reactions}}\n.*{re.escape(emotes[e])} ")
        for t in range(0, len(text_channels)):
            react_uses[e] += len(re.findall(in_react, text_channels[t]))
            if include_vanilla_emotes and len(emotes[e]) == 1:
                text_uses[e] += len(re.findall(in_text, text_channels[t]))-react_uses[e]
            else:
                text_uses[e] += len(re.findall(in_text, text_channels[t]))

    # print csv (usage count)
    with open(output_directory + filename, 'w+', newline='', encoding="utf8") as emote_usage_file:
        emote_usage_writer = csv.writer(emote_usage_file, delimiter=';')
        emote_usage_writer.writerow(['emote'] + ['text_uses'] + ['react_uses'] + ['total_uses'])
        for e in range(0, len(emotes)):
            emote_usage_writer.writerow([emotes[e]] + [text_uses[e]] + [react_uses[e]] + [text_uses[e] + react_uses[e]])
