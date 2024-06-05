from PIL import Image, ImageDraw

# Create a new image with white background
icon_size = (32, 32)  # Set the size of the icon
pin_icon = Image.new("RGBA", icon_size, (255, 255, 255, 0))

# Draw the pin shape on the image
draw = ImageDraw.Draw(pin_icon)
draw.polygon([(12, 0), (20, 10), (12, 32), (4, 10)], fill="red")  # Adjust coordinates to create a pin shape

# Save the icon to a file
pin_icon.save("pin_icon.png", "PNG")
