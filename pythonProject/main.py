'''
    WHAT NEEDS TO BE DONE:
    -   CROWNS - check
    -   NMS - check

    -   COLOURS MATCHED PERFECTLY!

    -   RAPPORT - meh

    - HIGH FIVE
'''
from pythonProject.New import load_and_process_image, tileGrid
from pythonProject.burn import countpoints, ignite, getConnectedTiles
from pythonProject.target import crown, divide_into_grid, match_templates, load_templates
from pythonProject.target import point_calculator  # Import the new function

# Set the image path to the specific image you want to calculate
image_path = 'Croppedandperspectivecorrectedboards/1.jpg'

# Original functionality preserved
# Load and process the image
img, img_hsv = load_and_process_image(image_path)

# Call the original `countpoints` function
countpoints(image_path)

# Call the original `crown` function

# --- New functionality starts here ---

# Step 1: Generate a grid using `tileGrid`
grid = tileGrid(img, img_hsv)

# Step 2: Load crown templates (update paths to crown template images as needed)
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
        "8Krone1Sand90.jpg","8Krone1Sand180.jpg","8Krone1Sand270.jpg",
        "9Krone1Sand.jpg",
        "9Krone1Sand90.jpg", "9Krone1Sand180.jpg", "9Krone1Sand270.jpg"
    ]  # Update with actual paths
templates = load_templates(template_files)

# Step 3: Call the new function to multiply connected blocks with crowns
result = point_calculator(image_path, grid, templates)

myscore = 0
crown_detect = crown(image_path)  # Detect crowns from the image
print("Crowns detected:", crown_detect)

Tiles = getConnectedTiles()  # Get connected tiles
print("this is tiles", Tiles)

# Convert crown_detect to a set of coordinates for easy lookup
if crown_detect is not None:
    crown_set = set(tuple(crown) for crown in crown_detect)  # Convert to set of tuples for quick lookup

    # Loop through each group of connected tiles
    for tile_group in Tiles:
        crownsInGroup = 0
        group_size = 0
        group_tile_id = None  # To track the tile ID of the group

        # Iterate through the tiles in the group
        for tile in tile_group:
            coord = tile[0]  # Extract the coordinate
            terrain = tile[1]  # Extract the terrain type (not needed here)
            tile_id = tile[2]  # Extract the tile ID to determine connectedness

            # Set the tile ID for the group, assuming all tiles in the group share the same ID
            if group_tile_id is None:
                group_tile_id = tile_id
            elif group_tile_id != tile_id:
                print("Warning: Mismatched tile ID within a group, something might be wrong.")

            group_size += 1  # Count the number of tiles in the group

            # If the tile's coordinate matches a crown, increase the crown count
            if coord in crown_set:
                crownsInGroup += 1  # Increase crown count for this group

        # If crowns are detected in this group, calculate the score
        if crownsInGroup > 0:
            group_score = group_size * crownsInGroup
            myscore += group_score
            print(f"Group with tile ID {group_tile_id} has {crownsInGroup} crowns. Group score: {group_score}")

# Print the final score
print("Final score:", myscore)




