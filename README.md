# Fix old Reaper project paths

If you've moved your old [Reaper](https://www.reaper.fm/) project to a new computer and have your samples and `REAPER Media` directory in a new path
you may have to manually find all the old samples or other files on your new computer.

This script helps update the old Reaper projects paths without the need to manually having to fix every old project.

## Usage

To fix the file paths in your Reaper projects run the script

```
$ ./fix-reaper-paths.py
```

or

```
$ python3 fix-reaper-paths.py
```

This will go through the directory set in configuration under `"default_projects_root_dir"` and find each .RPP file recursively
under the root directory. For each project the file paths defined inside the project will be changed from `old` to `new`
of each entry in the configurations `paths` attribute.

The configuration is in json format and can be found in `config.json`. It describes the old file path
roots (for example `C:\Users\Lauri\REAPER Media`) and the new file path roots you want to replace it with (for example `D:\REAPER Media`).

The resulting fixed project file is written to the original path with a suffix of your choosing. By default it is set to `-fixed`
meaning a project file `project.RPP` will be written to a new file `project-fixed.RPP`. If you want to
overwrite your old projects you can set `"fixed_project_suffix": ""`.

## Dependencies

Running the script requires for python3 to be installed on your system PATH. I've only tested the script with Python 3.8.10.

The Reaper version I've used in my old projects was v4.77/x64. I don't know how similar the format is in later versions
and if this script is compatible with those newer ones.

## Disclaimer

This script was only created for my personal use when I decided to move all my old Reaper projects from an old laptop to
my new computer. Most likely you should not use the software as is, but feel free to use it as a starting point if
you happen to have the same problem I'm having. Always make a backup of your project root before running.

I have a bunch of projects where I use a VST sampler called [Shortcircuit](https://vemberaudio.se/shortcircuit/). The
settings for each of the VSTs are encoded in base64. If you don't use such a sampler
you can in the configuration file set `"vsts_to_fix = []"`. The script handles also changing paths for
Shortcircuit.

I've also used a plugin called [Sforzando](https://www.plogue.com/products/sforzando.html). The VST
plays back soundfonts. However my soundfonts are in a different directory in my current computer so
the paths need to be changed also for this plugin settings. Luckily I managed to figure out the file
format for the plugin. After a header there is xml (specifically ARIA format data) compressed with
zlib. This was found after a lucky guess. Now after some changes the script manages to change paths
for Sforzando too!

The script was not coded with releasing it in mind but maybe it will be helpful for someone out there.
