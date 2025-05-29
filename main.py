import os
import time
from file_search import search_file
from mouse_controller import open_file_with_mouse

def display_search_results(matches):
    """Display search results and let user select which file to open"""
    if not matches:
        print("No files found.")
        return None
    
    print(f"\nFound {len(matches)} matching files:")
    for i, match in enumerate(matches, 1):
        print(f"{i}. {match['filename']}")
        print(f"   Location: {match['location']}")
        
        # Show all results, no limit
    
    while True:
        try:
            choice = input("\nEnter the number of the file to open (or 'q' to quit): ")
            if choice.lower() == 'q':
                return None
            
            choice = int(choice)
            if 1 <= choice <= len(matches):
                return matches[choice-1]['path']
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("=== AI-Powered File Search with Visual Navigation ===")
    print("This tool will search for files and show mouse navigation to the file location")
    
    # Get input from the user
    keyword = input("\nEnter the file name or keyword to search: ")
    
    # Show searching message
    print(f"\nSearching all drives for '{keyword}'...")
    start_time = time.time()
    
    # Search for the file
    matches = search_file(keyword)
    
    # Calculate search time
    search_time = time.time() - start_time
    print(f"Search completed in {search_time:.2f} seconds")

    # Display results and let user select a file
    file_path = display_search_results(matches)

    if file_path:
        print(f"\nSelected file: {file_path}")
        print("Starting visual navigation and file opening...")
        open_file_with_mouse(file_path)
    else:
        print("No file selected to open.")

if __name__ == "__main__":
    main()