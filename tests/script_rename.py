import os

folder_path = './fitness_poses_images_in/pushups_up/'  # Replace with the path to your folder
new_file_name_prefix = 'img_'  # Replace with the desired prefix for the new file names

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Sort the list of files by name
files.sort()

# Loop through all files in the folder
for i, file_name in enumerate(files):
    if file_name.endswith('.txt'):
        # Delete the file
        os.remove(os.path.join(folder_path, file_name))
    else:
        # Generate the new file name
        new_file_name = new_file_name_prefix + str(i+1).zfill(4) + os.path.splitext(file_name)[1]
        # Rename the file
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))