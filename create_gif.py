from PIL import Image
import os


def create_gif(root, image_paths, output_gif_path, duration=200):
    images = [Image.open(rf"{root}\{image_path}") for image_path in image_paths]
    # Save as GIF
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,  # 0 means infinite loop
    )


if __name__ == "__main__":
    # List of image file paths
    root = r"C:\Users\trand\longg\code\python\deep learning\mnist\pytorch\GAN\one2manyGAN_adam_image"
    image_paths = os.listdir(root)
    # Output GIF path
    output_gif_path = "output.gif"
    # Create GIF
    create_gif(root, image_paths, output_gif_path)

print(f"GIF created and saved at {output_gif_path}")
