import csv
import os
import re


def run():

    # collect desired emotes
    emotes = []
    with open('res/emotes.csv') as emote_file:
        emote_reader = csv.reader(emote_file)
        for row in emote_reader:
            emotes += row

    # import discord channel text files
    text_channels = []
    for file in os.listdir('in'):
        if file.endswith(".txt"):
            with open("in/" + file, "r", encoding="utf8") as text_file:
                text_channels += [text_file.read()]

    # count emote uses
    text_uses = [0] * len(emotes)
    react_uses = [0] * len(emotes)
    for e in range(0, len(emotes)):
        in_text = re.compile(rf":{emotes[e]}:")
        in_react = re.compile(rf"{{Reactions}}\n.*{emotes[e]} ")
        for t in range(0, len(text_channels)):
            text_uses[e] += len(re.findall(in_text, text_channels[t]))
            react_uses[e] += len(re.findall(in_react, text_channels[t]))

    # print csv (usage count)
    with open('out/emote_usage.csv', 'w+', newline='') as emote_usage_file:
        emote_usage_writer = csv.writer(emote_usage_file, delimiter=';')
        emote_usage_writer.writerow(['emote'] + ['text_uses'] + ['react_uses'] + ['total_uses'])
        for e in range(0, len(emotes)):
            emote_usage_writer.writerow([emotes[e]] + [text_uses[e]] + [react_uses[e]] + [text_uses[e] + react_uses[e]])