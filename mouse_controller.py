import subprocess
import os
import pyautogui
import time
import cv2
import numpy as np

def navigate_to_file(path, duration=5):
    """
    Show navigation through folders to reach the file with mouse movement
    """
    # Get file location components
    drive, remaining_path = os.path.splitdrive(path)
    folders = remaining_path.strip(os.sep).split(os.sep)
    filename = folders.pop() if folders else os.path.basename(path)
    folder_path = os.path.dirname(path)
    
    # Get screen dimensions
    screen_width, screen_height = pyautogui.size()
    
    # Create a named window that can be resized
    cv2.namedWindow("File Navigation", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("File Navigation", screen_width // 2, screen_height // 2)
    
    # Start recording
    print(f"\nNavigating to: {path}")
    print(f"Recording mouse movement for {duration} seconds...")
    
    try:
        # Open Windows Explorer to the file's directory directly
        subprocess.Popen(f'explorer /select,"{path}"', shell=True)
        time.sleep(1)  # Wait for Explorer to open
        
        # Move mouse to different positions to simulate navigation
        # Start from top left corner
        pyautogui.moveTo(50, 50, duration=0.5)
        
        # Move to address bar area
        pyautogui.moveTo(screen_width // 4, 80, duration=0.5)
        
        # Move to file area
        pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
        
        # Start recording and showing mouse movement
        start_time = time.time()
        end_time = start_time + duration
        
        # For recording
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'navigation.avi')
        out = cv2.VideoWriter(video_path, fourcc, 20.0, (screen_width, screen_height))
        
        print("Recording screen and mouse movements...")
        
        while time.time() < end_time:
            # Take screenshot
            screen = pyautogui.screenshot()
            frame = np.array(screen)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Draw circle at mouse position (more visible)
            cv2.circle(frame, (x, y), 20, (0, 0, 255), -1)
            
            # Draw trail (line from previous position)
            if 'prev_x' in locals():
                cv2.line(frame, (prev_x, prev_y), (x, y), (0, 255, 0), 2)
            
            prev_x, prev_y = x, y
            
            # Add navigation info
            cv2.putText(frame, f"File: {filename}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.putText(frame, f"Location: {folder_path}", (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add time remaining
            time_left = max(0, int(end_time - time.time()))
            cv2.putText(frame, f"Time: {time_left}s", (10, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Write frame to video
            out.write(frame)
            
            # Show the frame
            cv2.imshow("File Navigation", frame)
            
            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            # Move mouse randomly to show movement
            if time.time() - start_time > 2 and time.time() % 1 < 0.1:
                # Random movement around the center area
                rand_x = screen_width // 2 + np.random.randint(-200, 200)
                rand_y = screen_height // 2 + np.random.randint(-200, 200)
                pyautogui.moveTo(rand_x, rand_y, duration=0.3)
            
            # Short delay
            time.sleep(0.02)
        
        # Release video writer
        out.release()
        cv2.destroyAllWindows()
        print(f"Navigation recording saved to: {video_path}")
        
    except Exception as e:
        print(f"Error during navigation: {e}")
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()

def open_file_after_navigation(path, duration=5):
    """
    Open the file after navigation
    """
    filename = os.path.basename(path)
    
    # Get screen dimensions
    screen_width, screen_height = pyautogui.size()
    
    # Create a named window that can be resized
    cv2.namedWindow("File Opening", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("File Opening", screen_width // 2, screen_height // 2)
    
    try:
        # Start recording and showing mouse movement
        start_time = time.time()
        end_time = start_time + duration
        
        # For recording
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_opening.avi')
        out = cv2.VideoWriter(video_path, fourcc, 20.0, (screen_width, screen_height))
        
        # Move mouse to file and click
        pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
        pyautogui.doubleClick()
        
        # Open the file using command line
        subprocess.Popen([path], shell=True)
        print(f"Opening file: {filename}")
        
        while time.time() < end_time:
            # Take screenshot
            screen = pyautogui.screenshot()
            frame = np.array(screen)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Draw circle at mouse position
            cv2.circle(frame, (x, y), 20, (0, 0, 255), -1)
            
            # Add file info
            cv2.putText(frame, f"Opening: {filename}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Write frame to video
            out.write(frame)
            
            # Show the frame
            cv2.imshow("File Opening", frame)
            
            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Short delay
            time.sleep(0.02)
        
        # Release video writer
        out.release()
        cv2.destroyAllWindows()
        print(f"File opening recording saved to: {video_path}")
        
    except Exception as e:
        print(f"Error during file opening: {e}")
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()

def open_file_with_mouse(path):
    """
    Open a file and display its location information with mouse movement
    """
    # Show file location information
    print("\nFile Location Information:")
    print(f"Full path: {path}")
    print(f"Directory: {os.path.dirname(path)}")
    print(f"Filename: {os.path.basename(path)}")
    
    # Navigate to file location with visual tracking
    navigate_to_file(path)
    
    # Open the file
    open_file_after_navigation(path)
    
    print("File opened successfully with visual navigation.")