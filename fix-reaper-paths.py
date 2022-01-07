#! /bin/python3

import json
import os
import base64
import textwrap

def fix_shortcircuit_header(vst_settings_bytes):
    # In shortcircuit header there is a value that denotes the length of the xml.
    # After making changes to xml fix the length in header
    header_length = 156
    end_length = len(vst_settings_bytes.rsplit(b'>', 1)[1]) # Length of binary after xml
    xml_length = len(vst_settings_bytes) - header_length - end_length
    xml_length_position = 144
    vst_settings_before_xml_len = vst_settings_bytes[:xml_length_position]
    vst_settings_after_xml_len = vst_settings_bytes[xml_length_position + 4:]
    return vst_settings_before_xml_len + int.to_bytes(xml_length, length=4, byteorder="little") + vst_settings_after_xml_len

def decode_fix_and_encode_base64(accumulated_base64_string, configuration, line_ending="\n"):
    # Decode the accumulated base64 string, fix the paths, fix the header and
    # encode back into a base64 string ready to be embedded in the .RPP file
    b64_bytes = accumulated_base64_string.encode("utf-8")
    vst_settings_bytes = base64.b64decode(b64_bytes)
    for path_replacement in configuration["paths"]:
        vst_settings_bytes = vst_settings_bytes.replace(path_replacement["old"].encode(), path_replacement["new"].encode())

    # TODO: Some kind of check if we actually want to do this
    vst_settings_bytes = fix_shortcircuit_header(vst_settings_bytes)

    b64string = base64.b64encode(vst_settings_bytes).decode("utf-8")
    b64lines = "".join(["        " + line + line_ending for line in textwrap.wrap(b64string, 128)])
    return b64lines

def fix_paths_for_rpp_project_vsts(project_string, configuration):
    project_lines = project_string.splitlines(True) # Preserve ends
    new_project_string = ""
    accumulated_base64_string = ""
    accumulating = False # Accumulating the base64 encoded vst setting
    for line in project_lines:
        if accumulating:
            if line.strip() == ">":
                new_project_string += decode_fix_and_encode_base64(accumulated_base64_string, configuration)
                new_project_string += line
                accumulating = False
            else:
                accumulated_base64_string += line.strip()
            continue
        elif line.strip().startswith("<VST"):
            for vst_to_fix in configuration["vsts_to_fix"]:
                if vst_to_fix in line:
                    accumulating = True
                    break
        new_project_string += line
    return new_project_string

def fix_paths_for_rpp_project(project_string, configuration):
    # Take in file as a string, return file as a string where paths are fixed
    paths = configuration["paths"]
    for path_replacement in paths:
        project_string = project_string.replace(path_replacement["old"], path_replacement["new"])

    if len(configuration["vsts_to_fix"]) != 0:
        project_string = fix_paths_for_rpp_project_vsts(project_string, configuration)

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

def traverse_paths_and_fix_projects(configuration):
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
    traverse_paths_and_fix_projects(configuration)

if __name__ == "__main__":
    main()
