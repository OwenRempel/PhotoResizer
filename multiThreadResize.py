import os
import time
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Configuration Variables
input_folder = "Imgs"  # Folder containing the original images
output_folder = "resized_images"  # Folder to save resized images
desired_widths = [100, 300, 500, 2000, 5000]  # Desired sizes for resizing

# Constants
VALID_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')  # Supported image formats

def resize_image(input_path, output_path, sizes):
    """
    Resizes the image at input_path to the specified sizes and saves them to output_path.
    """
    counter = 0
    counter_lock = Lock()


    # Ensure sizes is a list, even if a single size is passed
    if not isinstance(sizes, list):
        sizes = [sizes]

    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            base_name, ext = os.path.splitext(output_path)

            # Save the original image in the new folder structure
            original_output_path = f"{base_name}{ext}"
            os.makedirs(os.path.dirname(original_output_path), exist_ok=True)
            img.save(original_output_path)

            # Resize and save images for each size
            for size in sizes:
                if original_width > original_height:
                    scaling_factor = size / original_width
                    new_width = size
                    new_height = int(original_height * scaling_factor)
                else:
                    scaling_factor = size / original_height
                    new_height = size
                    new_width = int(original_width * scaling_factor)

                # Resize the image
                img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Save the resized image
                resized_output_path = f"{base_name}_{size}px{ext}"
                os.makedirs(os.path.dirname(resized_output_path), exist_ok=True)
                img_resized.save(resized_output_path)

            # Increment the counter and display progress
            with counter_lock:
                counter += 1
                print(f"Resized {counter} images so far...")

    except Exception as e:
        print(f"Error processing {input_path}: {e}")


def process_file(args):
    """
    Helper function for processing individual image resize tasks.
    """
    input_path, output_path, size = args
    resize_image(input_path, output_path, size)


def batch_resize_nested(input_folder, output_folder, sizes, max_threads=None):
    """
    Resizes all images in the input_folder and saves them to output_folder for the given sizes.
    Utilizes multiple threads to process images concurrently.
    """
    global counter

    start_time = time.time()  # Record the start time

    # Dynamically determine the number of threads if not provided
    if max_threads is None:
        max_threads = os.cpu_count() or 4  # Use the number of CPUs or default to 4

    print(f"Using {max_threads} threads for processing.")

    tasks = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(VALID_IMAGE_EXTENSIONS):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                tasks.append((input_path, output_path, sizes))

    # Use ThreadPoolExecutor to process files concurrently
    with ThreadPoolExecutor(max_threads) as executor:
        executor.map(process_file, tasks)

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(f"Batch resizing completed in {total_time:.2f} seconds.")
    print(f"Total images resized: {counter}")


# Ensure the script is not being used as a library
if __name__ == "__main__":
    batch_resize_nested(input_folder, output_folder, desired_widths)
