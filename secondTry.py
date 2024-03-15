import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def remove_background_and_make_transparent(image_path, selected_color):
    # Step 1: Load the image with OpenCV
    image = cv2.imread(image_path)

    _, thresholded_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow("thresholded", thresholded_image)

    # Step 2: Convert the image to RGBA format
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Step 3: Define lower and upper bounds for background color
    lower_background = np.array([210, 210, 210, 255])
    upper_background = np.array([255, 255, 255, 255])

    # Step 4: Create a mask to identify background pixels
    mask = cv2.inRange(image_rgba, lower_background, upper_background)

    # Step 5: Apply the mask to make the background transparent
    image_rgba[mask == 255] = [0, 0, 0, 0]  # Set alpha channel to 0 for background pixels
    cv2.imwrite("transparent.png", image_rgba)

    # Step 6: Replace non-background pixels with the selected color
    color_map = {"Red": [0, 0, 255, 255],
                 "Green": [0, 255, 0, 255],
                 "Blue": [255, 0, 0, 255]}

    if selected_color in color_map:
        image_rgba[mask != 255] = color_map[selected_color]

    # Step 7: Save the modified image with transparency
    cv2.imwrite(f"transparent_image_{selected_color.lower()}_foreground.png", image_rgba)
    return image_rgba
def on_combobox_selected(event):
    selected_color = color_combobox.get()
    if selected_file:
        cv2.imshow("New Color image", remove_background_and_make_transparent(selected_file, selected_color))



def select_image_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select an image file
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("PNG",".png"),("JPG",".jpg"),("JPEG",".jpeg"),("ICON",".ico")])

    if file_path:
        print("Selected image file:", file_path)
        return file_path
    else:
        print("No file selected.")
        return None

# Example usage
selected_file = select_image_file()

# Create a Tkinter window
root = tk.Tk()
root.title("Remove Background and Change Color")

# Create a frame
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Create a label
label = ttk.Label(frame, text="Choose an image and select foreground color:")
label.grid(column=0, row=0, columnspan=2, pady=10)

# Create a combo box for selecting foreground color
color_combobox = ttk.Combobox(frame, values=["Red", "Green", "Blue"])
color_combobox.current(0)  # Default selection: Red
color_combobox.grid(column=1, row=1, pady=5)

# Bind the event handler to the combobox selection event
color_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

root.mainloop()
