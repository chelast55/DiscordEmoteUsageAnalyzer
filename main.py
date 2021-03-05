import emote_counter
import date_splitter

input_directory = 'in/'
output_directory = 'out/'

if __name__ == '__main__':

    emote_counter.run(input_directory, output_directory, 'emote_usage.csv')
    date_splitter.run(input_directory)