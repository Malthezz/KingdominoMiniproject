from pythonProject.New import tileGrid, load_and_process_image
from pythonProject.burn import countpoints
from pythonProject.target import point_calculator, load_templates, crown


def main():
    # Set the image path to the specific image you want to calculate
    image_path = 'Croppedandperspectivecorrectedboards/6.jpg'

    # Load and process the image
    img, img_hsv = load_and_process_image(image_path)

    # Call the original `countpoints` function
    countpoints(image_path)

    # Call the original `crown` function
    crown(image_path)

    # Load crown templates
    template_files = [
        # (Your template file names here)
    ]

    # Generate a grid using `tileGrid`
    grid = tileGrid(img, img_hsv)

    # Call the point calculator to get the total multiplier
    total_multiplier = point_calculator(image_path, grid, load_templates(template_files))

    # Optionally, print the total multiplier again if needed
    print(f"Total Multiplier from Main: {total_multiplier}")

if __name__ == "__main__":
    main()