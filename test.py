from PIL import Image

img = Image.open("assets/original_return.png")
resized_img = img.resize((100, 100))
resized_img.save("assets/return.png")