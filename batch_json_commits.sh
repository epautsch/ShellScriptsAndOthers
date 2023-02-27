#!/bin/bash

# Get the folder name passed as an argument
search_folder=$1
dump_folder=$2

# Find all the files in the current directory that end in '.git'
files=$(find "$search_folder" -name "*.git" -type d)

# Log the start of the script
echo "Starting PTM_json_pipeline.sh"
start_time=$(date +%s)
echo "Start Time: $(date +"%Y-%m-%d %H:%M:%S")" >> "$dump_folder"/PTM_json_pipeline.log

# Iterate through all of the found files
for file in $files
do
  # Remove the '.git' portion of the directory path
  file=${file%/*}

  # Extract the name of the model from the file path
  model=$(basename "$file")

  # Extract the name of the author from the file path
  author=$(basename "$(dirname "$file")")

  # Extract the name of the modelHub from the file path
  modelHub=$(basename "$(dirname "$(dirname "$(dirname "$file")")")")

  # Call clime command and name output according to the modelHub, author, and model
  clime-git-commits-extract -d "$file" -o "$dump_folder"/"$modelHub""_""$author""_""$model".json
done

# Log the end of the script
end_time=$(date +%s)
echo "End Time: $(date +"%Y-%m-%d %H:%M:%S")" >> "$dump_folder"/PTM_json_pipeline.log

# Calculate the total time the script took to run
duration=$((end_time-start_time))
echo "Total Time: $duration" >> "$dump_folder"/PTM_json_pipeline.log
echo "Total Time: $duration"