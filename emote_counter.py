import csv
import re
import numpy
from os import cpu_count
from math import ceil
from pathos.multiprocessing import ProcessPool
from operator import add

import io_helper as io


vanilla_emote_filepath = "res/vanilla.csv"
custom_emote_filepath = "res/custom.csv"


def run(input_directory: str, output_directory: str, filename: str, include_vanilla_emotes: bool):

    # set thread count to allow one parallel thread per logical cpu core in later emote counting step
    max_threads = ceil(cpu_count()/2)

    # predefine counting functions for multi-threading
    def count_text_uses(emotes_partition: list, index: int):
        indent = index * (len(emotes) // max_threads)
        for emote_position in range(0, len(emotes_partition)):
            # unicode emotes are never surrounded by colons in discord-chat-exporter's .txt format
            if include_vanilla_emotes and len(emotes_partition[emote_position]) == 1:
                in_text = re.compile(rf"{re.escape(emotes_partition[emote_position])}")
            else:
                in_text = re.compile(rf":{re.escape(emotes_partition[emote_position])}:")
            for t in range(0, len(text_channels)):
                text_uses[emote_position+indent] += len(re.findall(in_text, text_channels[t]))
        return text_uses

    def count_react_uses(emotes_partition: list, index: int):
        indent = index * (len(emotes) // max_threads)
        for emote_position in range(0, len(emotes_partition)):
            in_react = re.compile(rf"{{Reactions}}\n.*{re.escape(emotes_partition[emote_position])} ")
            for t in range(0, len(text_channels)):
                per_channel_react_uses = len(re.findall(in_react, text_channels[t]))
                react_uses[emote_position+indent] += per_channel_react_uses
                # text and react uses for unicode emotes are indistinguishable, remove duplicate counts
                if include_vanilla_emotes and len(emotes_partition[emote_position]) == 1:
                    text_uses[emote_position+indent] -= per_channel_react_uses
        return react_uses

    # collect desired emotes
    emotes = []
    if include_vanilla_emotes:
        emotes += io.read_emotes(vanilla_emote_filepath)
    emotes += io.read_emotes(custom_emote_filepath)

    # ensure emote list is integer dividable by thread_count
    original_emote_count = len(emotes)
    for j in range(0, max_threads - (len(emotes) % max_threads)):
        emotes += ["DUMMY_NOT_AN_EMOTE"]  # nobody should use this as an emote ever

    # import discord channel text files
    text_channels = io.read_input_files(input_directory)
    temp_text_channels = [""]
    for text_channel in text_channels:
        temp_text_channels[0] += text_channel
    text_channels = temp_text_channels

    # count emote uses
    text_uses = [0] * len(emotes)
    react_uses = [0] * len(emotes)
    pool = ProcessPool(nodes=max_threads*2)
    emotes_partitioned = numpy.array_split(emotes, max_threads)
    text_results = []
    react_results = []
    for i in range(0, max_threads):
        text_results += [pool.apipe(count_text_uses, emotes_partitioned[i], i)]
        react_results += [pool.apipe(count_react_uses, emotes_partitioned[i], i)]
    for i in range(0, max_threads):
        text_uses = list(map(add, text_uses, text_results[i].get()))
        react_uses = list(map(add, react_uses, react_results[i].get()))

    # print csv (usage count)
    with open(output_directory + filename, 'w', newline='', encoding="utf8") as emote_usage_file:
        emote_usage_writer = csv.writer(emote_usage_file, delimiter=';')
        emote_usage_writer.writerow(["emote"] + ["text_uses"] + ["react_uses"] + ["total_uses"])
        for e in range(0, original_emote_count):
            emote_usage_writer.writerow([emotes[e]] + [text_uses[e]] + [react_uses[e]] + [text_uses[e] + react_uses[e]])
