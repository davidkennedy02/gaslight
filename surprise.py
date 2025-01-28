import time
import random
import os
import platform
from tkinter import Tk, Label
from PIL import Image, ImageTk
import requests

# Configuration
image_url = "https://miro.medium.com/v2/resize:fit:1400/0*uQo-YVFfoMp9Eai9"  # Replace with the URL of your image.


# Determine a rarely monitored directory based on the OS
if platform.system() == "Windows":
    temp_dir = "C:\\Windows\\Temp"
else:  # For Linux/Mac
    temp_dir = "/tmp"
local_image_path = os.path.join(temp_dir, "downloaded_image.png")  # Path to save the downloaded image.


def download_image(image_url, save_path):
    """
    Download an image from the internet and save it locally.
    Fails silently if the download fails.
    """
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an error if the request failed.

        # Write the image data to a file.
        with open(save_path, "wb") as image_file:
            for chunk in response.iter_content(1024):  # Download in chunks.
                image_file.write(chunk)
    except:
        # Fail silently by skipping any error handling
        pass


def display_image(image_path, display_time=0.1):
    """
    Display an image in the center of the screen on top of all windows for a short time.
    """
    try:
        # Load the image using Pillow.
        img = Image.open(image_path)

        # Create a Tkinter window.
        root = Tk()
        root.attributes("-topmost", True)  # Keep the window on top of all others.
        root.overrideredirect(True)  # Remove window decorations (border, close button).

        # Get screen dimensions.
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Resize image to fit nicely in the center of the screen.
        max_width = int(screen_width * 0.5)  # Use 50% of the screen width.
        max_height = int(screen_height * 0.5)  # Use 50% of the screen height.
        img.thumbnail((max_width, max_height))

        # Convert the image to a Tkinter-compatible format.
        tk_image = ImageTk.PhotoImage(img)

        # Create a label to display the image.
        label = Label(root, image=tk_image)
        label.pack()

        # Calculate the window position to center the image on the screen.
        window_width = img.width
        window_height = img.height
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Set the position of the window.
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Show the image for a short period.
        root.after(int(display_time * 1000), root.destroy)  # Close the window after the display time.
        root.mainloop()
    except:
        # Fail silently if the image cannot be displayed
        pass


def clean_up_image(file_path):
    """
    Delete the image file after it is no longer needed.
    Fails silently if the file cannot be deleted.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        # Fail silently if the file cannot be deleted
        pass


if __name__ == "__main__":
    while True:  # Infinite loop
        # Wait for a random interval between 1 and 2 minutes
        interval = random.randint(60, 120)
        time.sleep(interval)

        # Download the image
        download_image(image_url, local_image_path)

        # Display the image for 0.1 seconds (if successfully downloaded)
        if os.path.exists(local_image_path):  # Only display if the image was successfully downloaded
            display_image(local_image_path, display_time=0.1)

        # Delete the image after displaying it
        clean_up_image(local_image_path)
