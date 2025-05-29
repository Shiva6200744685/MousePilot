import pyautogui
import cv2
import numpy as np
import time

def show_mouse_position(duration=5):
    """
    Show mouse position on screen for a limited duration
    
    Args:
        duration: Number of seconds to show the overlay
    """
    start_time = time.time()
    
    # Create a named window that can be resized
    cv2.namedWindow("Mouse Position", cv2.WINDOW_NORMAL)
    
    while time.time() - start_time < duration:
        try:
            # Take screenshot
            screen = pyautogui.screenshot()
            frame = np.array(screen)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Correct color conversion
            
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Draw circle at mouse position
            cv2.circle(frame, (x, y), 15, (0, 0, 255), -1)
            
            # Add text showing coordinates
            cv2.putText(frame, f"({x}, {y})", (x + 20, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Show the frame
            cv2.imshow("Mouse Position", frame)
            
            # Break loop if 'q' is pressed or window is closed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # q or ESC
                break
                
            # Short delay to reduce CPU usage
            time.sleep(0.05)
            
        except Exception as e:
            print(f"Error in mouse overlay: {e}")
            break
    
    # Clean up
    cv2.destroyAllWindows()