import os
import platform
from tkinter import Tk, Label
from PIL import Image, ImageTk
import requests

# Configuration
image_url = "https://miro.medium.com/v2/resize:fit:1400/0*uQo-YVFfoMp9Eai9"  # Replace with the URL of your image.

# Determine a temporary directory based on the OS
if platform.system() == "Windows":
    temp_dir = "C:\\Windows\\Temp"
else:  # For Linux/Mac
    temp_dir = "/tmp"

local_image_path = os.path.join(temp_dir, "downloaded_image.png")  # Path to save the downloaded image.
script_path = os.path.abspath(__file__)  # Get the current script's file path


def download_image(image_url, save_path):
    """Download an image from the internet and save it locally."""
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an error if the request failed.
        with open(save_path, "wb") as image_file:
            for chunk in response.iter_content(1024):  # Download in chunks.
                image_file.write(chunk)
    except:
        pass  # Fail silently


def display_image(image_path, display_time=0.1):
    """Display an image in the center of the screen on top of all windows for a short time."""
    try:
        img = Image.open(image_path)

        root = Tk()
        root.attributes("-topmost", True)  # Keep the window on top
        root.overrideredirect(True)  # Remove window decorations

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Resize image to fit in the center of the screen
        max_width = int(screen_width * 0.5)
        max_height = int(screen_height * 0.5)
        img.thumbnail((max_width, max_height))

        tk_image = ImageTk.PhotoImage(img)

        label = Label(root, image=tk_image)
        label.pack()

        window_width, window_height = img.width, img.height
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        root.after(int(display_time * 1000), root.destroy)  # Close the window after display time
        root.mainloop()
    except:
        pass  # Fail silently


def clean_up_image(file_path):
    """Delete the image file after it is no longer needed."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass  # Fail silently


def self_delete(script_path):
    """Deletes the script itself after execution."""
    try:
        os.remove(script_path)
    except:
        pass  # Fail silently


if __name__ == "__main__":
    # Download the image
    download_image(image_url, local_image_path)

    # Display the image if it was successfully downloaded
    if os.path.exists(local_image_path):
        display_image(local_image_path, display_time=0.1)

    # Clean up: Delete the image file
    clean_up_image(local_image_path)

    # Self-delete the script
    self_delete(script_path)
