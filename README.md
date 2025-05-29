# AI-Powered File Search with Visual Navigation

This project provides an AI-powered file search system that visually shows navigation to files across your PC.

## Features

- Search for files across all drives (C:, D:, E:)
- Visual representation of file navigation with mouse movement
- Real-time screen recording of the navigation process
- Automated file search and navigation system

## Components

### Standard Search (main.py)
- Interactive file search with user selection
- Visual navigation to selected files
- Records navigation to video files

### Automated Search (automated_search.py)
- Real-time automated file search system
- Continuous visual overlay showing system status
- Automatic navigation to found files
- Queue-based processing for multiple searches

## Usage

### Standard Search
```
python main.py
```
- Enter a file name or keyword to search
- Select from the list of found files
- Watch the visual navigation to the file

### Automated Search
```
python automated_search.py
```
- Enter file names to search
- System automatically finds and opens the best match
- Real-time overlay shows system status and mouse movement

## Requirements

- Python 3.6+
- OpenCV
- PyAutoGUI
- NumPy

## Installation

1. Create a virtual environment:
   ```
   python -m venv myenv
   ```

2. Activate the environment:
   ```
   myenv\Scripts\activate  # Windows
   source myenv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.py` to customize:
- Search drives
- File extensions to ignore
- Directories to skip