import csv
import os
import re
import numpy
from threading import Thread

vanilla_emote_filepath = 'res/vanilla.csv'
custom_emote_filepath = 'res/custom.csv'
max_threads = 4


# TODO: overload constructor properly
def run(input_directory, output_directory, filename):
    run_vanilla_check(input_directory, output_directory, filename, False)


def run(input_directory, output_directory, filename, include_vanilla_emotes):
    run_vanilla_check(input_directory, output_directory, filename, include_vanilla_emotes)


def run_vanilla_check(input_directory, output_directory, filename, include_vanilla_emotes):

    # predifine counting functions for multi-threading
    def count_text_uses(emotes_partition, index):
        indent = index * (len(emotes) // max_threads)
        for e in range(0, len(emotes_partition)):
            # unicode emotes are never surrounded by colons in discord-chat-exporter's .txt format
            if include_vanilla_emotes and len(emotes_partition[e]) == 1:
                in_text = re.compile(rf"{re.escape(emotes_partition[e])}")
            else:
                in_text = re.compile(rf":{re.escape(emotes_partition[e])}:")
            for t in range(0, len(text_channels)):
                text_uses[e+indent] += len(re.findall(in_text, text_channels[t]))

    def count_react_uses(emotes_partition, index):
        indent = index * (len(emotes) // max_threads)
        for e in range(0, len(emotes_partition)):
            in_react = re.compile(rf"{{Reactions}}\n.*{re.escape(emotes_partition[e])} ")
            for t in range(0, len(text_channels)):
                per_channel_react_uses = len(re.findall(in_react, text_channels[t]))
                react_uses[e+indent] += per_channel_react_uses
                # text and react uses for unicode emotes are indistinguishable, remove duplicate counts
                if include_vanilla_emotes and len(emotes_partition[e]) == 1:
                    text_uses[e+indent] -= per_channel_react_uses

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

    # ensure emote list is integer dividable by thread_count
    for i in range(0, max_threads - (len(emotes) % max_threads)):
        emotes += ['DUMMY_EMOTE_'] # nobody should use this as an emote ever

    # import discord channel text files
    text_channels = []
    for file in os.listdir(input_directory):
        if file.endswith(".txt"):
            with open(input_directory + file, "r", encoding="utf8") as text_file:
                text_channels += [text_file.read()]

    # count emote uses
    text_uses = [0] * len(emotes)
    react_uses = [0] * len(emotes)
    if len(emotes) < max_threads:
        count_react_uses(0, len(emotes))
        count_text_uses(0, len(emotes))
    else:
        threads = []
        emotes_partitioned = numpy.array_split(emotes, max_threads)
        for i in range(0, max_threads):
            threads += [Thread(count_text_uses(emotes_partitioned[i], i))]
            threads += [Thread(count_react_uses(emotes_partitioned[i], i))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    # print csv (usage count)
    with open(output_directory + filename, 'w+', newline='', encoding="utf8") as emote_usage_file:
        emote_usage_writer = csv.writer(emote_usage_file, delimiter=';')
        emote_usage_writer.writerow(['emote'] + ['text_uses'] + ['react_uses'] + ['total_uses'])
        for e in range(0, len(emotes) - (max_threads - (len(emotes) % max_threads))):
            emote_usage_writer.writerow([emotes[e]] + [text_uses[e]] + [react_uses[e]] + [text_uses[e] + react_uses[e]])
