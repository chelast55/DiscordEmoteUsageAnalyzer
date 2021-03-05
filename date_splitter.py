import os
import re

split_directory = 'split/'

numerical_month = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                   "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}


def run(input):
    # import discord channel text files
    text_channels = []
    for file in os.listdir(input):
        if file.endswith(".txt"):
            with open(input + file, "r", encoding="utf8") as text_file:
                text_channels += [text_file.read()]

    # split text channel at each comment (before month)
    before_month = re.compile(r'\[\d\d-')
    text_channels_split = []
    for text_channel in text_channels:
        text_channels_split += [re.split(before_month, text_channel)[1:]]

    # recombine by month
    text_channels_recombined = []
    for s in range(0, len(text_channels_split)):
        text_channel_recombined = []
        previous_month = text_channels_split[s][0][:6]
        messages_this_month = ""
        for i in range(0, len(text_channels_split[s])):
            if previous_month != text_channels_split[s][i][:6]:
                text_channel_recombined += [messages_this_month]
                previous_month = text_channels_split[s][i][:6]
                messages_this_month = ""
            messages_this_month += text_channels_split[s][i]
        if messages_this_month != "":
            text_channel_recombined += [messages_this_month]
        text_channels_recombined += [text_channel_recombined]

    # write split text channels to individual .txt files (by month)
    create_filepath(split_directory)
    for d in range(0, len(text_channels_recombined)):
        original_file_name = os.listdir(input)[d]
        create_filepath(split_directory + original_file_name[:(len(original_file_name) - 4)])
        for month_of_channel in text_channels_recombined[d]:
            with open(split_directory + original_file_name[:(len(original_file_name) - 4)] + '/'
                      + reformat_date(month_of_channel[:6]) + "_" + original_file_name, "w",
                      encoding="utf8") as output_file:
                output_file.write(month_of_channel)


def create_filepath(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)


# reformat date from 'Mmm-YY' to 'YY-MM'
def reformat_date(date):
    return str(date[len(date) - 2:len(date)]) + "-" + str(numerical_month.get(date[:3]))
