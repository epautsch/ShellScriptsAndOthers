if [ $# -eq 0 ]
  then
    echo "Please provide a directory name as an argument"
    exit 1
fi

# Loop through json files in specified directory
for file in "$1"*.json
do

  # Remove the '.json' extension ft