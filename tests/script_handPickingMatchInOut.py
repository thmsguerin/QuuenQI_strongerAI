import os

folder_path1 = './fitness_poses_images_out/pushups_up/'  # Replace with the path to the first subfolder
folder_path2 = './fitness_poses_images_in/pushups_up/'  # Replace with the path to the second subfolder

# Get a list of all file names in the first subfolder
file_names1 = os.listdir(folder_path1)

# Loop through all files in the second subfolder
for file_name2 in os.listdir(folder_path2):
    if file_name2 not in file_names1:
        # Delete the file if it doesn't match the list
        os.remove(os.path.join(folder_path2, file_name2))