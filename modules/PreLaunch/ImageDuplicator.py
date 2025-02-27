import os
from PIL import Image
from tqdm import tqdm

def duplicate_images_in_folder(input_folder, output_folder, what):
    for root, dirs, files in os.walk(input_folder):
        # Recreate the directory structure in the output folder
        relative_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        
        for file in tqdm(files):
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, file)
                try:
                    if what:
                        duplicate_image(input_path, output_path)
                    else:
                        rotate_image_90_clockwise(input_path,output_path)
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

def rotate_image_90_clockwise(input_path, output_path):
    img = Image.open(input_path)
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_img = flipped_img.rotate(90, expand=True)  # Rotates 90 degrees clockwise
    rotated_img.save(output_path)

# Example usage
input_folder = 'textures/images'
output_folder = 'textures/plane'
duplicate_images_in_folder(input_folder, output_folder, False)

#True and cylinder for cylinder
#False and plane for plane