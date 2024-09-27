# Release Notes

## vr1114 *(stable)*

- **Toggle Button Renamed to Parent and Terminal Modes:**

    **Terminal Mode:** In this mode, the application processes directories that do not contain any subdirectories (referred to as terminal directories).

    **Parent Mode:** Opposite to Terminal Mode, Parent Mode is designed to work with directories that contain other subdirectories.

    **Schematic Directory Tree Explanation:**


<div style="font-family: monospace; background-color:#5052 ; padding: 5px; border-radius: 2px;">
<br>
  <strong>dir_master/</strong>        #Example of hierarchical structure

  ├── <strong>Parent_1/</strong><br>
  │   ├── <strong>Terminal_1/</strong>  #No further subdirectories <br>
  │   └── <strong>Terminal_2/</strong><br>
  ├── <strong>Parent_2/</strong><br>
  │   ├── <strong>Terminal_1/</strong><br>
  │   └── <strong>Terminal_2/</strong>
</div>


- **Unified Output Directory - 'dir_master':** All generated plots are now saved in a single directory named 'dir_master', located in the same directory as your executable file.

- **Improved Message Box:** The message box has been enhanced for better readability. It now supports scrolling, allowing to read through the detail the operations performed and their outcomes.

- **Date-Based Versioning:** Switched to a date-based versioning system for a clearer timeline of progress.

- **General Enhancements:** The application has received various improvements for efficiency, stability, and usability.

## vr02

- **Batch Mode Improvement**: Batch mode now creates plots for the parent directory, titled with terminal directory names.
- **Single Mode**: Now only creates a GIF if it's executed in a terminal folder.
- **Faster Plot Generation**: Improved the speed of plot generation and optimized memory usage during the process.

## vr01

- **Directory Navigation**: Navigate through directories to select the desired folder for plot generation.
- **Single Mode**: Combine multiple plots into a single directory.
- **Batch Mode**: Process multiple directories at once.
- **Toggle Switch**: Switch between Single Mode and Batch Mode.
- **Generate GIF**: Generate GIFs alongside subplots.
- **Settings Tab**: More customization options available.
