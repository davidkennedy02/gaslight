import time
import os
import platform
from tkinter import Tk, Label
from PIL import Image, ImageTk
import requests

# Configuration
image_url = "https://i.ytimg.com/vi/y_qkfiVEFqQ/maxresdefault.jpg"

# Determine the temp directory based on the OS
temp_dir = os.getenv("TEMP") if platform.system() == "Windows" else "/tmp"
local_image_path = os.path.join(temp_dir, "downloaded_image.png")
script_path = os.path.abspath(__file__)  # Get the current script's file path

def download_image(image_url, save_path):
    """ Download an image from the internet and save it locally. """
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as image_file:
            for chunk in response.iter_content(1024):
                image_file.write(chunk)
        return True
    except Exception as e:
        print(f"Image download failed: {e}")
        return False


def display_image(image_path, display_time=1000):
    """ Display an image at full screen size while maintaining aspect ratio. """
    try:
        # Ensure the image file exists before proceeding
        if not os.path.exists(image_path):
            print(f"Error: Image file does not exist at {image_path}")
            return

        # Load image
        img = Image.open(image_path)
        img = img.copy()  # Fixes potential PIL file locking issue

        # Create a Tkinter window
        root = Tk()
        root.attributes("-topmost", True)  # Keep window on top
        root.overrideredirect(True)  # Remove window decorations

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Resize image while maintaining aspect ratio
        img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

        # Convert to Tkinter-compatible format
        tk_image = ImageTk.PhotoImage(img)

        # Create a label to display image
        label = Label(root, image=tk_image)
        label.image = tk_image  # Store reference to prevent garbage collection
        label.pack()

        # Set the window size to full screen
        root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Fix transparency issue
        root.attributes("-alpha", 1.0)

        # Close window after display_time milliseconds
        root.after(display_time, root.destroy)
        root.mainloop()
    except Exception as e:
        print(f"Display failed: {e}")



def clean_up_image(file_path):
    """ Delete the image file after it is displayed. """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Cleanup failed: {e}")
        

def self_delete(script_path):
    """Deletes the script itself after execution."""
    try:
        os.remove(script_path)
    except:
        pass  # Fail silently


if __name__ == "__main__":
    time.sleep(5)  # Give the system a moment to load properly

    if download_image(image_url, local_image_path):
        display_image(local_image_path, display_time=100)
        clean_up_image(local_image_path)
        time.sleep(1)
        self_delete(script_path=script_path)
