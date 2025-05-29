import os
import concurrent.futures
from config import SEARCH_DRIVES, IGNORE_EXTENSIONS, SKIP_DIRECTORIES

def should_skip_directory(dir_path):
    """Check if directory should be skipped"""
    dir_name = os.path.basename(dir_path)
    return any(skip_dir.lower() in dir_name.lower() for skip_dir in SKIP_DIRECTORIES)

def should_skip_file(file_name):
    """Check if file should be skipped based on extension"""
    _, ext = os.path.splitext(file_name)
    return ext.lower() in IGNORE_EXTENSIONS

def search_drive(drive, keyword):
    """Search a single drive for files matching keyword"""
    matches = []
    print(f"Searching drive {drive}...")
    try:
        for root, dirs, files in os.walk(drive):
            # Skip directories that match the skip list
            dirs[:] = [d for d in dirs if not should_skip_directory(os.path.join(root, d))]
            
            for file in files:
                if should_skip_file(file):
                    continue
                    
                if keyword.lower() in file.lower():
                    matches.append({
                        'path': os.path.join(root, file),
                        'location': root,
                        'filename': file
                    })
                    # No limit on matches per drive
    except PermissionError:
        pass  # Skip directories we don't have access to
    except Exception as e:
        print(f"Error searching {drive}: {e}")
    
    return matches

def search_file(keyword):
    """
    Search all drives for files matching the keyword using parallel processing
    """
    all_matches = []
    
    # Make sure all drives are properly formatted with trailing backslash
    formatted_drives = [f"{drive}\\" if not drive.endswith('\\') else drive for drive in SEARCH_DRIVES]
    
    print(f"Searching drives: {', '.join(formatted_drives)}")
    
    # Use ThreadPoolExecutor for parallel searching
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit search tasks for each drive
        future_to_drive = {
            executor.submit(search_drive, drive, keyword): drive 
            for drive in formatted_drives
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_drive):
            drive = future_to_drive[future]
            try:
                matches = future.result()
                if matches:
                    print(f"Found {len(matches)} matches on drive {drive}")
                    all_matches.extend(matches)
            except Exception as e:
                print(f"Error processing drive {drive}: {e}")
    
    return all_matches