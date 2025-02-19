import time
import os
import platform
from tkinter import Tk, Label
from PIL import Image, ImageTk
import requests

# Configuration
image_url = "https://miro.medium.com/v2/resize:fit:1400/0*uQo-YVFfoMp9Eai9"

# Determine the temp directory based on the OS
temp_dir = os.getenv("TEMP") if platform.system() == "Windows" else "/tmp"
local_image_path = os.path.join(temp_dir, "downloaded_image.png")


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
    """ Display an image properly in a scheduled task. """
    try:
        # Ensure the image file exists before proceeding
        if not os.path.exists(image_path):
            print(f"Error: Image file does not exist at {image_path}")
            return

        # Load image properly
        img = Image.open(image_path)
        img = img.copy()  # Fixes potential PIL file locking issue

        # Create a Tkinter window
        root = Tk()
        root.attributes("-topmost", True)  # Keep on top
        root.overrideredirect(True)  # Remove window decorations

        # Ensure image is properly loaded into memory before displaying
        tk_image = ImageTk.PhotoImage(img)

        # Create a label to display image
        label = Label(root, image=tk_image)
        label.image = tk_image  # Store reference to prevent garbage collection
        label.pack()

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Resize image
        max_width, max_height = screen_width // 2, screen_height // 2
        img.thumbnail((max_width, max_height))

        # Position window in the center
        window_width, window_height = img.width, img.height
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Fix transparency issue
        root.attributes("-alpha", 1.0)  # Ensure the window is not transparent

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


if __name__ == "__main__":
    time.sleep(5)  # Give the system a moment to load properly

    if download_image(image_url, local_image_path):
        display_image(local_image_path, display_time=100)
        clean_up_image(local_image_path)
