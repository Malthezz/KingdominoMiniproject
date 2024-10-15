'''
    WHAT NEEDS TO BE DONE:
    -   CROWNS - check
    -   NMS - check

    -   COLOURS MATCHED PERFECTLY!

    -   RAPPORT - meh

    - HIGH FIVE
'''
import cv2
from pythonProject.New import load_and_process_image, tileGrid
from pythonProject.burn import countpoints, ignite
from pythonProject.target import crown, divide_into_grid, match_templates, load_templates
from pythonProject.target import point_calculator

def main():
    # Image path to process
    image_path = 'Croppedandperspectivecorrectedboards/1.jpg' # Update as necessary

    # Load and process the image
    img_rgb, img_hsv = load_and_process_image(image_path)

    # Step 1: Call the original `countpoints` function
    countpoints(image_path)

    # Step 4: Load crown templates (update paths to crown template images as needed)
    template_files = [
            "1 Krone1 Desert.jpg",
            "1 Krone1 Desert 90.jpg", "1 Krone1 Desert 180.jpg", "1 Krone1 Desert 270.jpg",
            "1 Krone1 Grass.jpg",
            "1 Krone1 Grass 90.jpg", "1 Krone1 Grass 180.jpg", "1 Krone1 Grass 270.jpg",
            "1 Krone2 Desert.jpg",
            "1 Krone2 Desert 90.jpg", "1 Krone2 Desert 180.jpg", "1 Krone2 Desert 270.jpg",
            "1 Krone2 Grass.jpg",
            "1 Krone2 Grass 90.jpg", "1 Krone2 Grass 180.jpg", "1 Krone2 Grass 270.jpg",
            "1 Krone3 Desert.jpg",
            "1 Krone3 Desert 90.jpg", "1 Krone3 Desert 180.jpg", "1 Krone3 Desert 270.jpg",
            "1 Krone3 Grass.jpg",
            "1 Krone3 Grass 90.jpg", "1 Krone3 Grass 180.jpg", "1 Krone3 Grass 270.jpg",
            "1 Krone Skov.jpg",
            "1 Krone Skov 90.jpg", "1 Krone Skov 180.jpg", "1 Krone Skov 270.jpg",
            "1 Krone Water.jpg",
            "1 Krone Water 90.jpg", "1 Krone Water 180.jpg", "1 Krone Water 270.jpg",
            "4Krone1Sand.jpg",
            "4Krone1Sand90.jpg", "4Krone1Sand180.jpg", "4Krone1Sand270.jpg",
            "8Krone1Sand.jpg",
            "8Krone1Sand90.jpg", "8Krone1Sand180.jpg", "8Krone1Sand270.jpg",
            "9Krone1Sand.jpg",
            "9Krone1Sand90.jpg", "9Krone1Sand180.jpg", "9Krone1Sand270.jpg"
    ]
    templates = load_templates(template_files)

    # Step 3: Generate a grid using `tileGrid`
    grid = tileGrid(img_rgb, img_hsv)

    # Step 2: Detect crowns and get total sum, crown count, and crown IDs
    total_sum, crown_count, crown_ids = point_calculator(image_path, grid, templates)

    print(f"Total Crowns Detected: {crown_count}")
    print(f"Crown IDs with their positions: {crown_ids}")
    print(f"Total Value Calculated: {total_sum}")

    # Step 5: Call the new function to multiply connected blocks with crowns
    result = point_calculator(image_path, grid, templates)

    # Print the new result
    print(f'Total multiplier (connected blocks * crowns): {result}')

    # Step 6: Process the grid with the detected crown positions (if required)
    # Initialize total score and current ID
    total_score = 0
    current_id = 0

    # Loop through the grid and calculate scores for each "blob" of crowns
    for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                    # Ensure cell has at least 4 elements before accessing cell[3]
                    if len(cell) > 3 and cell[3] is None:  # Check if the tile has not been processed
                            size, crowns = ignite(cell[1], y, x, grid, current_id)  # Use ignite to process the tile
                            current_id += 1  # Increment the ID for the next blob
                            score = size * crowns  # Calculate the score for this blob
                            total_score += score  # Add to the total score

                            # Print detailed blob information
                            print(f"ID: {current_id}, Blob Size: {size}, Crowns: {crowns}, Score: {score}")

    # Step 7: Output the total score
    print(f"Total Score: {total_score}")

if __name__ == "__main__":
    main()

