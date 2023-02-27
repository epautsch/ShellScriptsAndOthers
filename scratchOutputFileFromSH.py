import os
import subprocess
import time

# Get the folder name passed as an argument
search_folder = sys.argv[1]
dump_folder = sys.argv[2]

# Find all the files in the current directory that end in '.git'
files = subprocess.check_output(["find", search_folder, "-name", "*.git", "-type", "d"])
files = files.decode().strip().split("\n")

# Log the start of the script
print("Starting PTM_json_pipeline.sh")
start_time = time.time()
with open(os.path.join(dump_folder, "PTM_json_pipeline.log"), "a") as log_file:
    log_file.write("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

# Iterate through all of the found files
for file in files:
    # Remove the '.git' portion of the directory path
    file = os.path.dirname(file)

    # Extract the name of the model from the file path
    model = os.path.basename(file)

    # Extract the name of the author from the file path
    author = os.path.basename(os.path.dirname(file))

    # Extract the name of the modelHub from the file path
    modelHub = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(file))))


    # Call clime command and name output according to the modelHub, author, and model
    output_file = os.path.join(dump_folder, f"{modelHub}_{author}_{model}.json")
    subprocess.run(["clime-git-commits-extract", "-d", file, "-o", output_file])

# Log the end of the script
end_time = time.time()
with open(os.path.join(dump_folder, "PTM_json_pipeline.log"), "a") as log_file:
    log_file.write("End Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

# Calculate the total time the script took to run
duration = end_time - start_time
with open(os.path.join(dump_folder, "PTM_json_pipeline.log"), "a") as log_file:
    log_file.write("Total Time: " + str(duration) + "\n")
print("Total Time:", duration)
