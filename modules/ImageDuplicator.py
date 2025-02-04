from PIL import Image

def duplicate_image(input_path, output_path):

    img = Image.open(input_path)
    width, height = img.size
    print(img.size)
    new_img = Image.new('RGB', (width * 2, height), (255, 255, 255))
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    new_img.paste(flipped_img, (0, 0))
    new_img.paste(flipped_img, (width, 0))
    new_img.save(output_path)
    print(f"Image saved as {output_path}")

duplicate_image('textures/render2.png', 'textures/office.png')
