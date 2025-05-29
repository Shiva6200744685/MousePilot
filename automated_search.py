import os
import time
import threading
import queue
import pyautogui
import cv2
import numpy as np
import subprocess
from file_search import search_file

class AutomatedFileSearch:
    def __init__(self):
        self.search_queue = queue.Queue()
        self.is_running = False
        self.current_task = None
        self.screen_width, self.screen_height = pyautogui.size()
        
    def start(self):
        """Start the automated search system"""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
        self.display_thread = threading.Thread(target=self._display_overlay, daemon=True)
        self.display_thread.start()
        print("Automated file search system started")
        
    def stop(self):
        """Stop the automated search system"""
        self.is_running = False
        if hasattr(self, 'worker_thread'):
            self.worker_thread.join(timeout=1)
        if hasattr(self, 'display_thread'):
            self.display_thread.join(timeout=1)
        print("Automated file search system stopped")
        
    def search(self, keyword):
        """Add a search task to the queue"""
        self.search_queue.put(keyword)
        print(f"Search for '{keyword}' added to queue")
        
    def _process_queue(self):
        """Process search tasks from the queue"""
        while self.is_running:
            try:
                if not self.search_queue.empty():
                    keyword = self.search_queue.get()
                    self.current_task = f"Searching for: {keyword}"
                    print(f"\nProcessing search: {keyword}")
                    
                    # Search for files
                    start_time = time.time()
                    matches = search_file(keyword)
                    search_time = time.time() - start_time
                    print(f"Search completed in {search_time:.2f} seconds")
                    
                    if matches:
                        # Take the first match
                        best_match = matches[0]
                        path = best_match['path']
                        
                        self.current_task = f"Navigating to: {path}"
                        print(f"Automatically navigating to: {path}")
                        
                        # Navigate to and open the file
                        self._navigate_to_file(path)
                    else:
                        print("No files found")
                        
                    self.current_task = None
                    self.search_queue.task_done()
                else:
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error processing search: {e}")
                self.current_task = None
                time.sleep(1)
    
    def _navigate_to_file(self, path):
        """Navigate to and open a file"""
        try:
            # Open Windows Explorer to the file's directory
            subprocess.Popen(f'explorer /select,"{path}"', shell=True)
            time.sleep(1)
            
            # Move mouse to simulate navigation
            pyautogui.moveTo(self.screen_width // 4, self.screen_height // 4, duration=0.5)
            time.sleep(0.5)
            pyautogui.moveTo(self.screen_width // 2, self.screen_height // 2, duration=0.5)
            
            # Open the file
            subprocess.Popen([path], shell=True)
            print(f"File opened: {path}")
            
        except Exception as e:
            print(f"Error navigating to file: {e}")
    
    def _display_overlay(self):
        """Display real-time overlay showing system status and mouse position"""
        cv2.namedWindow("Automated File Search", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Automated File Search", self.screen_width // 3, self.screen_height // 3)
        
        prev_x, prev_y = pyautogui.position()
        
        while self.is_running:
            try:
                # Take screenshot
                screen = pyautogui.screenshot()
                frame = np.array(screen)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Get current mouse position
                x, y = pyautogui.position()
                
                # Draw circle at mouse position
                cv2.circle(frame, (x, y), 15, (0, 0, 255), -1)
                
                # Draw trail
                cv2.line(frame, (prev_x, prev_y), (x, y), (0, 255, 0), 2)
                prev_x, prev_y = x, y
                
                # Add system status
                cv2.putText(frame, "Automated File Search System", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                if self.current_task:
                    cv2.putText(frame, self.current_task, (10, 60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Waiting for search tasks...", (10, 60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Show the frame
                cv2.imshow("Automated File Search", frame)
                
                # Break loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_running = False
                    break
                
                # Short delay
                time.sleep(0.05)
                
            except Exception as e:
                print(f"Error in display overlay: {e}")
                time.sleep(1)
        
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    auto_search = AutomatedFileSearch()
    auto_search.start()
    
    try:
        while True:
            keyword = input("\nEnter file to search (or 'exit' to quit): ")
            if keyword.lower() == 'exit':
                break
            auto_search.search(keyword)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        auto_search.stop()