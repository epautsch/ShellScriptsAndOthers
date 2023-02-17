import sys
import glob
import os


def search_for_json_files(search_directory):
    # search for all json files in the directory
    json_files = glob.glob(os.path.join(search_directory, '*.json'))

    # print the names of each file to the console
    for file in json_files:
        print(file)


if __name__ == '__main__':
    # get the directory to search from the command line
    search_directory = sys.argv[1]

    # search for json files
    search_for_json_files(search_directory)
