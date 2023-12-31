#!/bin/bash

# Initialize variable
source_dir=""

# Define a list of files and dirs to copy
file_list=("logins.json"
           "key4.db"
           "places.sqlite"
           "favicons.sqlite")
dir_list=("bookmarkbackups")


# Function to create a directory to hold ff profile backup and return its full path
create_dir() {
  local date_str=$(date +"%Y-%m-%d")
  local dir_name="${date_str}-ff-profile"
  local full_path="$(pwd)/$dir_name"
  
  if [ ! -d "$dir_name" ]; then
    mkdir "$dir_name"
  fi

  echo "$full_path"
}

# Parse the positional argument for source directory
if [ $# -eq 1 ]; then
  source_dir="$1"
else
  echo "Usage: $0 source_dir"
  exit 1
fi

# Check that the source directory exists
if [ ! -d "$source_dir" ]; then
  echo "Error: Source directory '$source_dir' not found."
  exit 1
fi

# Copy files from source directory to new directory
new_dir=$(create_dir)
for file in "${file_list[@]}"; do
  cp "$source_dir/$file" "$new_dir"
done
echo "Copied files from $source_dir to $new_dir."

# Copy directories listed in dir_list
for dir in "${dir_list[@]}"; do
  if [ -d "$source_dir/$dir" ]; then
    cp -r "$source_dir/$dir" "$new_dir"
    echo "Copied directory '$dir' from $source_dir to $new_dir."
  fi
done

echo "Can now do something like: cp -r new_dir /run/media/username/..."

exit 0

