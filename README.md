# Fix old Reaper project paths

If you've moved your old Reaper project to a new computer and have your samples and `REAPER Media` directory in a new path
you have to manually find all the old samples or other files.

This script helps update the old Reaper project paths.

## Configuration

Configuration is a json file which describes the old file path root (for example "C:\Users\Lauri\REAPER Media") and
the new file path root you want to replace it with (for example "D:\REAPER Media").

The resulting fixed project file is written to a suffix of your choosing. By default it is set to "-fixed"
meaning a project file `project.RPP` will be written to a new file `project-fixed.RPP`. If you want to
overwrite your old projects you can set `"fixed_project_suffix": ""`.

## Usage

To fix the reaper paths run the script

```
$ ./fix-reaper-paths.py
```

or

```
$ python3 fix-reaper-paths.py
```

For the first "release" this is almost a naive search and replace which could easily be implemented with some shell magic.

## Dependencies

Running the script requires for python3 to be installed on your system PATH.

## Disclaimer

This script was only created for my personal use when I decided to move all my old Reaper projects from an old laptop to
my new computer. Most likely you should not use the software as is, but feel free to use it as a starting point if
you happen to have the same problem I'm having. Always make a backup of your project root before running.

## TODO

I have a bunch of projects where I use a VST sampler called "shortcircuit". The
settings for each of the VST are encoded in base64. Luckily most of shortcircuits
settings are in xml and not in some incomprehensible binary format. This
allows me to read each setting, search and replace the paths I want and
encode the resulting bytes back to base64 format.

This could be done for other VSTs as well as long as they use a comprehensible
format for their settings.
