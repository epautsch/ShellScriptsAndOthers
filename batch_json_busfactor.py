import sys
import glob
import os
import subprocess


# function to search for json files in a directory
def search_for_json_files(search_directory):
    # search for all json files in the directory
    json_files_full_path = glob.glob(os.path.join(search_directory, '*.json'))
    return json_files_full_path


# function to call the clime-git-commits-graph script
def make_bus_factor_json(list_of_json_files, output_directory):
    # get base name of each file
    list_of_json_no_path = [os.path.basename(x) for x in list_of_json_files]

    list_of_output_names = []
    # get filename parts
    for filename in list_of_json_no_path:
        # Split the filename into parts using the underscore character
        parts = filename.split("_")

        modelhub = parts[0]
        parts.remove(modelhub)

        author = parts[0]
        parts.remove(author)

        model = ""
        for i in range(len(parts) - 1):
            model += parts[i] + "_"
        model = model[:-1]

        # check if output directory has '/' at the end
        if output_directory[-1] != "/":
            output_directory += "/"

        output_graph_name = output_directory + modelhub + "_" + author + "_" + model + "_busFactor.json"
        list_of_output_names.append(output_graph_name)

    # map each full path to each output name
    input_output_map = dict(zip(list_of_json_files, list_of_output_names))

    # call the clime-git-commits-graph script
    for input_file, output_file in input_output_map.items():
        subprocess.call(["clime-git-bus-factor-compute",
                         "-i", input_file,
                         "-o", output_file])
        print("Bus factor .json created for: " + output_file)


if __name__ == '__main__':
    # get the directory to search from the command line
    search_directory = sys.argv[1]

    # get the output directory from the command line
    output_directory = sys.argv[2]

    # search for json files
    json_files = search_for_json_files(search_directory)

    # make graphs
    make_bus_factor_json(json_files, output_directory)
