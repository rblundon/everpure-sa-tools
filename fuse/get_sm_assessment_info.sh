#!/bin/bash

# Initialize variables
customer_name=""
date=$(date +%Y%m%d)

# Parse flags
# The ":" after c means the -c flag requires an argument
while getopts "c:" opt; do
  case $opt in
    c) customer_name="$OPTARG" ;;
    *) echo "Usage: $0 -c <customer_name>" >&2
       exit 1 ;;
  esac
done

tar_file="$HOME/${customer_name}_${date}.tar.gz"
list_file="${customer_name}_fa_list.txt"

# Validation: Check if the variable is still empty
if [ -z "$customer_name" ]; then
    echo "Error: The -c (customer name) flag is required."
    echo "Usage: $0 -c \"Customer Name\""
    exit 1
fi

echo "Successfully identified customer: $customer_name"

# Open Flash Array List ${customer_name}_fa_list.txt and process each line (array name)
while IFS= read -r line; do
    echo "Processing $line"
    # Create (if it doesn't exist) or clear the output directory
    target_dir="$HOME/${customer_name}/${line}"

    if [ -d "$target_dir" ]; then
        # Directory exists: delete contents only (including hidden files)
        # Using 'dotglob' ensures hidden files are caught
        shopt -s dotglob
        rm -rf "${target_dir}"/*
        shopt -u dotglob
    else
        # Directory doesn't exist: create it
        mkdir -p "$target_dir"
    fi
    # Go to the array directory
    goto "$line"
    # purearray list > "$target_dir/purearray_list.txt"
    purearray list > "$target_dir/purearray_list.txt"
    # purearray list --space --physical > "$target_dir/purearray_list_space_physical.txt"
    purearray list --space --physical > "$target_dir/purearray_list_space_physical.txt"
    # purearray list --space --effective > "$target_dir/purearray_list_space_effective.txt"
    purearray list --space --effective > "$target_dir/purearray_list_space_effective.txt"
    # purearray eradication-config list > "$target_dir/purearray_list_eradication_config.txt"
    purearray eradication-config list > "$target_dir/purearray_list_eradication_config.txt"
    # purepgroup list > "$target_dir/purepgroup_list.txt"
    purepgroup list > "$target_dir/purepgroup_list.txt"
    # purepgroup list --retention-lock --pending > "$target_dir/purepgroup_list_retention_lock_pending.txt"
    purepgroup list --retention-lock --pending > "$target_dir/purepgroup_list_retention_lock_pending.txt"
    # purepgroup list --schedule > "$target_dir/purepgroup_list_schedule.txt"
    purepgroup list --schedule > "$target_dir/purepgroup_list_schedule.txt"
    # purepgroup list --retention > "$target_dir/purepgroup_list_retention.txt"
    purepgroup list --retention > "$target_dir/purepgroup_list_retention.txt"
    # purepgroup list --space --physical --total > "$target_dir/purepgroup_list_space_physical_total.txt"
    purepgroup list --space --physical --total > "$target_dir/purepgroup_list_space_physical_total.txt"
    # purehgroup list --connect > "$target_dir/purehgroup_list_connect.txt"
    purehgroup list --connect > "$target_dir/purehgroup_list_connect.txt"
    # purevol list --space --effective --total --pending > "$target_dir/purevol_list_space_effective_total_pending.txt"
    purevol list --space --effective --total --pending > "$target_dir/purevol_list_space_effective_total_pending.txt"
done < "$list_file"

# Create a tar file of the output directory
cd "$HOME"
tar -czvf "$tar_file" "${customer_name}"

echo -e "\n--------------------------------"
echo "Please run 'scp $USER@fuse:${tar_file} ${tar_file}' to transfer the file to the server."
echo "--------------------------------"
