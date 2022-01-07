#! /bin/python3

import json
import os

def fix_paths_for_rpp_project(project_string, configuration):
    # Take in file as a string, return file as a string where paths are fixed
    paths = configuration["paths"]
    for path_replacement in paths:
        project_string = project_string.replace(path_replacement["old"], path_replacement["new"])

    return project_string

def print_old_paths(configuration):
    for path in configuration["paths"]:
        print("old: " + path["old"])
        print("new: " + path["new"])

def read_configuration(config_path):
    # Read the json config file. TODO: Make a class that holds info about config
    configuration = {}

    with open("config.json", "r") as config_file:
        configuration = json.load(config_file)

    return configuration

def read_project_to_string(project_path):
    with open(project_path, "r") as project_file:
        project_string = project_file.read()
    return project_string

def write_project_to_file(project_path, project_string):
    with open(project_path, "w") as project_file:
        project_file.write(project_string)

def get_fixed_project_path(project_path, configuration):
    return project_path[:-4] + configuration["fixed_project_suffix"] + ".RPP"

def traverse_paths(configuration):
    # Traverse paths and fix projects
    root_directory = configuration["default_projects_root_dir"]

    print(root_directory)

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".RPP"):
                #print(file)
                full_project_path = os.path.join(root, file)
                project_string = read_project_to_string(full_project_path)
                fixed_project_string = fix_paths_for_rpp_project(project_string, configuration)
                fixed_project_path = get_fixed_project_path(full_project_path, configuration)
                print("write new file to path: " + fixed_project_path)
                write_project_to_file(fixed_project_path, fixed_project_string)

def main():
    # For now just read config from config.json and run. Take in parameters later
    configuration = read_configuration("config.json")
    print_old_paths(configuration)
    traverse_paths(configuration)

if __name__ == "__main__":
    main()
