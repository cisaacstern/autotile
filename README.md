# autotile

`autotile` is a simple CLI that streamlines requesting, interactively color-balancing, and visualizing Landsat8 GeoTIFFs. 

For more detail on the motivating problem, and design choices I've made to solve it, check out <a href='https://github.com/cisaacstern/autotile/blob/main/CONTEXT.md'>CONTEXT.md</a>.

> **Note**: The directions below assume the user has read and understood the shell commands this interface executes and is comfortable running them on their machine!

## Setup

Build and activate the environment with:
```
conda env create --file environment.yml \
&& conda activate autotile
```

Make all the scripts executable with:
```
chmod -R +x scripts
```

Set environment variables and alias `python autotile.py` to `autotile` with:
```
. ./scripts/env.sh
```
> In my macOS Terminal running a zsh shell, the dot operator `.` (equivalent to `source` in bash) is required to ensure that the env variables are exported into the current shell. This may or may not be necessary depending on your specific setup.

## Interface

The `autotile` interface provides six sequential steps, each of which is called by `autotile $COMMAND`, where `$COMMAND` is one of:

1. **`stage`**: Places HTTP GET requests to https://landsat-pds.s3.amazonaws.com/ to retrieve RGB bands for the specified geographic location. Subsequently calculates top-of-atmosphere (TOA) correction and saves TOA-corrected GeoTIFFs to disk. This is the only command which takes arguments, which are:

    - **latitude**: A value between -90.0 and 90.0 (South negative).
    - **longitude**: A value within -180.0 and 180.0 (West negative).
    - **tooltip**: A label for the marker which will appear at the specified latitude and longitude.

    > In this early stage of development, the only Landsat8 scene retrieved is for WRS path 041 row 036 (the scene containing Los Angeles, CA). Therefore, the specified latitude and longitude must fall within that scene. One valid input would therefore be: `autotile stage 34.0739 -118.2400 'Dodger Stadium'`.

2. **`tune`**: Launches a Panel app from which the user can interactively adjust the color balance of the TOA-corrected GeoTIFFs and save the color-corrected bands back to disk. The image displayed by this browser interface is a downsampled preview but the version saved to disk is full resolution.

3. **`optimize`**: Optimizes the TOA-corrected and color-balanced GeoTIFFs into COGs and then creates two databases, one for each of these two image sets.

4. **`serve`**: Launches a separate tileserver for each of the two COG databases created in the previous step, then runs a Streamlit app which can be used to toggle between these two tile sets.

5. **`down`**: Stops the tileserver processes. (When the user exits from the Streamlit app, these processes remain running in the background. If they are not stopped, they will block successive calls of `autotile serve` from running on the specified ports.)

6. **`reset`**: Clears all the files from the `geotiffs/` directory so that the workflow can be repeated for a new location.

