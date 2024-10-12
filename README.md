# Waveform Signal Automation Tool

### Overview

When debugging waveform signals in Chisel projects, managing multiple paths for signal entries can be tedious and error-prone. This tool simplifies the process by allowing users to specify a signal using a regular expression and automatically generating additional signal paths. It supports editing signal lists stored in text-based EDA software files, such as Verdi's `.rc` files and GTKWave's `.gtkw` files.

![WaveformSignalAutomationTool](images/WaveformSignalAutomationTool.gif)

### Features

- Add a single signal path using a regular expression and automatically generate additional paths by specifying the number needed.
- Instantly preview generated signal paths before writing changes back to waveform configuration files like (Verdi's `.rc`  later ) GTKWave's `.gtkw`.
- Easily organize different signal paths with autogenerated comments for improved readability and management.


### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Bowen-0x00/WaveformSignalAutomationTool
   cd WaveformSignalAutomationTool
   ```
2. Ensure you have Python installed (version 3.x recommended).


### Usage

1. Run the Python script:
   ```bash
   python gtkw_regex_repeator.py
   ```

2. Input the file path of your `.gtkw` (or `.rc` later) file.

3. Enter your regular expression to match the initial signal path.

4. Specify the number of signal paths you want to generate.

5. Preview the results and, if satisfied, press button write them back to the file.

### Example

Suppose you have an initial signal 

- `io_commits_commitValid_0`
- `io_commits_robIdx_0_value[7:0]`
  
Using this tool, you can automatically generate - 
- `io_commits_commitValid_0`
- `io_commits_robIdx_0_value[7:0]`


- `io_commits_commitValid_1`
- `io_commits_robIdx_1_value[7:0]`

...

- `io_commits_commitValid_7`
- `io_commits_robIdx_7_value[7:0]0` 

using a suitable regular expression.

`io_commits.*?_(\d+).*?`


### Contact

For questions or feedback, please contact [your email].
