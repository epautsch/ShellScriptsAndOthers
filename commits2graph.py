import sys
import glob
import os


def search_for_json_files(search_directory):
    # search for all json files in the directory
    json_files = glob.glob(os.path.join(search_directory, '*.json'))

    # store the name of each json file in a list without the full path
    json_files = [os.path.basename(json_file) for json_file in json_files]

    for file in json_files:
        print(file)


if __name__ == '__main__':
    # get the directory to search from the command line
    search_directory = sys.argv[1]

    # search for json files
    search_for_json_files(search_directory)
