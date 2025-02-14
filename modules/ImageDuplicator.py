import os
from PIL import Image

def duplicate_images_in_folder(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        # Recreate the directory structure in the output folder
        relative_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, file)
                try:
                    duplicate_image(input_path, output_path)
                except Exception as e:
                    print(f"Error processing {input_path}: {e}")

def duplicate_image(input_path, output_path):
    img = Image.open(input_path)
    width, height = img.size
    new_img = Image.new('RGB', (width * 2, height), (255, 255, 255))
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    new_img.paste(flipped_img, (0, 0))
    new_img.paste(flipped_img, (width, 0))
    new_img.save(output_path)
    print(f"Image saved as {output_path}")

# Example usage
input_folder = 'textures/raws'
output_folder = 'textures/cylinder'
duplicate_images_in_folder(input_folder, output_folder)
