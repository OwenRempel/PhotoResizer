import os
from PIL import Image
import time

def resize_image(input_path, output_path, sizes):
    if type(sizes) != list:
        sizes = [sizes]

    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            base_name, ext = os.path.splitext(output_path)

            # This saves the original file in the new folder structure
            output_path = f"{base_name}{ext}"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path)
            print(f"Moved Original: {input_path} -> {output_path}")

            for size in sizes:
                # Calculate new dimensions while maintaining aspect ratio
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
                output_path = f"{base_name}_{size}px{ext}"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img_resized.save(output_path)
                print(f"Resized: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")



def batch_resize_nested(input_folder, output_folder, size):
    start_time = time.time()  # Record the start time
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                resize_image(input_path, output_path, size)

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(f"Batch resizing completed in {total_time:.2f} seconds.")

# Example usage
input_folder = "Imgs"  # Folder containing the original images
output_folder = "resized_imagesTest"  # Folder to save resized images
desired_width = [100, 300, 500, 2000, 5000] # Desired size

batch_resize_nested(input_folder, output_folder, desired_width)
