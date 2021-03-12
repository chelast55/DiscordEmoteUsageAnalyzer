import emote_scraper
import emote_counter
import date_splitter

input_directory = 'in/'
output_directory = 'out/'

if __name__ == '__main__':

    # extract custom emotes form discord channel text file
    #emote_scraper.run(input_directory)

    # generate .csv file logging custom emote use of all discord channel text documents in input_directory combined
    #emote_counter.run(input_directory, output_directory, 'emote_usage.csv')

    # generate .csv file logging emote use of all discord channel text documents in input_directory combined
    emote_counter.run(input_directory, output_directory, 'emote_usage.csv', True)

    # split all discord channel text documents in input_directory by month in chronological order
    #date_splitter.run(input_directory)