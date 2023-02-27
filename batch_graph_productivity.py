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
def make_graphs(list_of_json_files, output_directory, stylesheet):
    # get base name of each file
    list_of_json_no_path = [os.path.basename(x) for x in list_of_json_files]

    list_of_output_names = []
    # get filename parts
    for filename in list_of_json_no_path:
        # Split the filename into parts using the underscore character
        parts = filename.split("_")
        # print(parts)

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

        output_graph_name = output_directory + modelhub + "_" + author + "_" + model + "_productivity.png"
        graph_title = "Productivity/Days Since 0 for" + modelhub.title() + ": " + author + "/" + model
        list_of_output_names.append((output_graph_name, graph_title))

    # map each full path to each output name
    input_output_map = dict(zip(list_of_json_files, list_of_output_names))

    # call the clime-git-commits-graph script
    for input_file, output_tuple in input_output_map.items():
        subprocess.call(["clime-productivity-graph",
                         "-i", input_file,
                         "-o", output_tuple[0],
                         "--type", "line",
                         "--title", output_tuple[1],
                         "--x-label", "Author Days Since 0",
                         "--y-label", "Productivity",
                         "--stylesheet" if stylesheet != "" else "",
                         stylesheet if stylesheet != "" else ""])
        print("Graph created for: " + output_tuple[0])


if __name__ == '__main__':
    # get the directory to search from the command line
    search_directory = sys.argv[1]

    # get the output directory from the command line
    output_directory = sys.argv[2]

    # get the stylesheet from the command line
    stylesheet = sys.argv[3] if len(sys.argv) > 3 else ""

    # search for json files
    json_files = search_for_json_files(search_directory)

    # make graphs
    make_graphs(json_files, output_directory, stylesheet)
