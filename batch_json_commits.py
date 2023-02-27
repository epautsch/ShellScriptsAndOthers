import glob
import os
import subprocess
import sys
import time


# Search Directory
# C:/SSL/PTM_forked/PTM-Torrent/data/modelhub/repos/modelhub-ai

# function to search for git files in a directory
def search_for_git_files(_search_directory: str) -> list[str]:
    # search for all git files in the directory
    git_dirs = []
    for root, dirs, files in os.walk(_search_directory):
        if '.git' in dirs:
            git_dirs.append(root)
        dirs[:] = [d for d in dirs if d != '.git']
    return git_dirs


# function to call the clime-git-commits-extract script
def make_commits_json(_list_of_git_dirs: list[str], _output_directory: str) -> None:
    # list to hold output json names
    list_of_output_names = []
    # get filename parts
    for dir_path in _list_of_git_dirs:
        # Split the filename into parts using the underscore character
        model = os.path.basename(dir_path)

        author = os.path.basename(os.path.dirname(dir_path))

        model_hub = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(dir_path))))

        # check if output directory has '/' at the end
        if _output_directory[-1] != "/":
            _output_directory += "/"

        output_json_name = _output_directory + model_hub + "_" + author + "_" + model + ".json"
        list_of_output_names.append(output_json_name)

    # map each full path to each output name
    input_output_map = dict(zip(_list_of_git_dirs, list_of_output_names))

    # call the clime-git-commits-graph script
    for input_file, output_file in input_output_map.items():
        subprocess.call(["clime-git-commits-extract",
                         "-d", input_file,
                         "-o", output_file])
        print("Commits .json created for: " + output_file)


if __name__ == '__main__':
    # search_directory = sys.argv[1]
    search_directory = 'C:/SSL/PTM_forked/PTM-Torrent/data/modelhub/repos/modelhub-ai'

    # output_directory = sys.argv[2]
    output_directory = 'C:/SSL/ShellScriptsAndOthers/test_output_dir'

    print("Starting batch json commits generation on directory: " + search_directory)
    start_time = time.time()

    # get list of git files
    list_of_git_dirs = search_for_git_files(search_directory)

    # make commits json
    make_commits_json(list_of_git_dirs, output_directory)

    # Log the end of the script
    end_time = time.time()
    with open(os.path.join(output_directory, "batch_json_commits.log"), "a") as log_file:
        log_file.write("End Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

    # Calculate the total time the script took to run
    duration = end_time - start_time
    with open(os.path.join(output_directory, "batch_json_commits.log"), "a") as log_file:
        log_file.write("Total Time: " + str(duration) + "\n")
    print("Total Time:", duration)
