from PIL import Image

def duplicate_image(input_path, output_path):

    img = Image.open(input_path)
    width, height = img.size
    
    new_img = Image.new('RGB', (width * 2, height), (255, 255, 255))
    new_img.paste(img, (0, 0))
    new_img.paste(img, (width, 0))
    new_img.save(output_path)
    print(f"Image saved as {output_path}")

duplicate_image('office.jpeg', 'output.jpg')
