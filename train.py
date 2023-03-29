import csv
import os
import numpy as np

from classApp.class_bootstrapHelper import BootstrapHelper
from classApp.class_bootstrapHelper import show_image
from classApp.class_poseclassifier import PoseClassifier
from classApp.class_fullBodyPoseEmbedder import FullBodyPoseEmbedder


bootstrap_images_in_folder = 'fitness_poses_images_in'
bootstrap_images_out_folder = 'fitness_poses_images_out'
bootstrap_csvs_out_folder = 'fitness_poses_csvs_out'

pose_samples_folder = 'fitness_poses_csvs_out'
pose_samples_csv_path = 'fitness_poses_csvs_out.csv'
file_extension = 'csv'
file_separator = ','


def trainmodel(bootstrap_images_in_folder, bootstrap_images_out_folder, bootstrap_csvs_out_folder, exercise):
    # Initialize helper.
    bootstrap_helper = BootstrapHelper(
        images_in_folder=bootstrap_images_in_folder+'/'+exercise,
        images_out_folder=bootstrap_images_out_folder+'/'+exercise,
        csvs_out_folder=bootstrap_csvs_out_folder+'/'+exercise,
    )

    # Check how many pose classes and images for them are available.
    bootstrap_helper.print_images_in_statistics()

    # Bootstrap all images.
    # Set limit to some small number for debug.
    bootstrap_helper.bootstrap(per_pose_class_limit=None)

    # Check how many images were bootstrapped.
    bootstrap_helper.print_images_out_statistics()

    # After initial bootstrapping images without detected poses were still saved in
    # the folderd (but not in the CSVs) for debug purpose. Let's remove them.
    bootstrap_helper.align_images_and_csvs(print_removed_items=False)
    bootstrap_helper.print_images_out_statistics()

    # Find outliers.
    # Transforms pose landmarks into embedding.
    pose_embedder = FullBodyPoseEmbedder()

    # Classifies give pose against database of poses.
    pose_classifier = PoseClassifier(
        pose_samples_folder=bootstrap_csvs_out_folder,
        pose_embedder=pose_embedder,
        top_n_by_max_distance=30,
        top_n_by_mean_distance=10)

    outliers = pose_classifier.find_pose_sample_outliers()
    print('Number of outliers: ', len(outliers))

    # # Analyze outliers.
    # bootstrap_helper.analyze_outliers(outliers)
    # # Remove all outliers (if you don't want to manually pick).
    # bootstrap_helper.remove_outliers(outliers)
    # # Align CSVs with images after removing outliers.
    # bootstrap_helper.align_images_and_csvs(print_removed_items=False)
    # bootstrap_helper.print_images_out_statistics()


def dump_for_the_app(pose_samples_folder, pose_samples_csv_path, file_extension, file_separator):
  # Each file in the folder represents one pose class.
  file_names = [name for name in os.listdir(pose_samples_folder) if name.endswith(file_extension)]

  with open(pose_samples_csv_path, 'w') as csv_out:
    csv_out_writer = csv.writer(csv_out, delimiter=file_separator, quoting=csv.QUOTE_MINIMAL)
    for file_name in file_names:
      # Use file name as pose class name.
      class_name = file_name[:-(len(file_extension) + 1)]

      # One file line: `sample_00001,x1,y1,x2,y2,....`.
      with open(os.path.join(pose_samples_folder, file_name)) as csv_in:
        csv_in_reader = csv.reader(csv_in, delimiter=file_separator)
        for row in csv_in_reader:
          row.insert(1, class_name)
          csv_out_writer.writerow(row)

  # files.download(pose_samples_csv_path)


def main():
    trainmodel(bootstrap_images_in_folder, bootstrap_images_out_folder, bootstrap_csvs_out_folder, exercise='squats')
    dump_for_the_app(pose_samples_folder, pose_samples_csv_path, file_extension, file_separator)


if __name__ == "__main__":
    main()