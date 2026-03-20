# Faices
# CSCI-497
# Charlie Laursen, Kyle Downing

from deepface import DeepFace
import os
import random
import datetime
import csv
import requests
import json
import urllib.request

def swap_words(s, x, y):
    """
    Swap all occurnaces of two substrings within a given string

    Args:
        s: Input string
        x: Substring
        y: Substring

    Returns:
        New String
    """
    return y.join(part.replace(y, x) for part in s.split(x))


# DateTime for unique file naming. Add the Fawkes mode to the filename as well.
DATE=swap_words(datetime.datetime.now().strftime("%x-%H:%M:%S"), "/", "_")

def main():
    print(f'-----Program invoked at: {DATE}-----\n')
    # Depending on your usage, invoke the corresponding function.
    print(f'\n-----Program terminated at: {swap_words(datetime.datetime.now().strftime("%x-%H:%M:%S"), "/", "_")}-----')


def similarity_check() -> bool:
    """
    Run similarity checks between all images against themselves,
    ensuring those images can be processed by DeepFace and do not
    cause unintended side effects later

    Args:
        None
                
    Returns:
        Bool
    """
    files = list(os.listdir('../images'))
    iteration = 0
    for f in files:
        try:
            print(f'===== Iteration {iteration} - File {f} =====')
            path = f'../images/{f}'
            result = DeepFace.verify(img1_path=path, img2_path=path)
            if not result["distance"] == 0.0:
                print(f'File {f} - Did not pass..')
        except Exception as e:
            print(f'Problem with DeepFace: {e.__str__()}')
            return False
        iteration += 1
    print('===== Finished =====')
    return True


def cloaked_similarity_check(cloaked_dir="../images_cloaked") -> []:
    """
    Run similarity check between cloaked images and normal images
    Cloaked image filepaths are assumed to be the same as default

    Args:
        cloaked_dir: Directory containing cloaked images
        
    Returns:
        List of results
    """
    files = list(os.listdir('../images_cloaked'))
    iteration = 0
    ret_list = []
    ret_list.append(["filename", "verified", "distance"])
    print(f'Processing cloaked images in {cloaked_dir}\n')
    for f in files:
        try:
            print(f'===== Iteration {iteration} - File {f} =====')
            path1 = f'../images/{f}'
            path2 = f'../images-cloaked-low/{f}'
            result = DeepFace.verify(img1_path=path1, img2_path=path2)
            baseline = DeepFace.verify(img1_path=path1, img2_path=path1)
            print(f'===== Baseline: {baseline["distance"]}, Result: {result["distance"]} =====\n')
            iteration_result = [f, result["verified"], result["distance"]]
            ret_list.append(iteration_result)
        except Exception as e:
            print(f'Problem with DeepFace: {e.__str__()}')
        iteration += 1
    print('===== Finished =====')
    return ret_list


def face_check(source_dir="../images", cloaked_dir="../images-cloaked-med", ai_dir="../images-ai"):
    """
    Process face similarity checks between original and cloaked, and original and AI

    Args:
        source_dir: Directory containing original images
        cloaked_dir: Directory containing cloaked images
        ai_dir: Directory containing AI images

    Returns:
        List of results [filename, cloaked_distance, ai_distance]
    """
    base_filenames = [f.split('.')[0] for f in list(os.listdir(source_dir))]
    cloaked_filenames = [f.split('.')[0] for f in list(os.listdir(cloaked_dir))]
    ai_filenames = [f.split('.')[0] for f in list(os.listdir(ai_dir))]
    for i in range(len(base_filenames)):
        assert base_filenames[i] in cloaked_filenames and base_filenames[i] in ai_filenames
    total_files = len(base_filenames)
    print(f'Total files to process: {total_files}')
    ret_list = []
    ret_list.append(["filename", "cloaked_distance", "ai_distance"])
    # Process files
    for f in base_filenames:
        try:
            print(f'===== Iteration [{global_idx}/{total_files}] - File {f} =====')
            og_path = f'../images/{f}.jpg'
            cloaked_path = f'{cloaked_dir}/{f}.jpg'
            ai_path = f'../images-ai/{f}.jpg'
            cloaked_result = DeepFace.verify(img1_path=og_path, img2_path=cloaked_path)
            ai_result = DeepFace.verify(img1_path=og_path, img2_path=ai_path)
            print(f'===== CLOAKED: {cloaked_result["distance"]}, AI: {ai_result["distance"]} =====\n')
            iteration_result = [f, cloaked_result["distance"], ai_result["distance"]]
            ret_list.append(iteration_result)
        except Exception as e:
            print(f'Problem with DeepFace: {e.__str__()}')
            # Add ERROR entry
            ret_list.append([f, "ERROR", "ERROR"])
    print('===== All batches finished =====')
    return ret_list


def remove_invalid_faces() -> None:
    """
    Remove invalid faces from dataset

    Args:
        None

    Returns:
        None
    """
    # Generate list of all files, random ordering
    files = list(os.listdir('../images'))
    random.shuffle(files)
    print(f'Total files: {len(files)}')
    # Reference image for similarity check
    ref_img = "../images/100_0_0_20170112213500903.jpg"
    # Run similarity check through each image
    iteration = 0
    deleted_count = 0
    for f in files:
        print(f'Processing: {f} - iteration: {iteration}')
        try:
            result: dict = DeepFace.verify(
                img1_path=ref_img,
                img2_path=(f"../images/{f}")
            )
        # If image is not valid, then remove from dataset
        except Exception as e:
            print(f'path: {f} not valid (Error: {type(e).__name__})... Attempting to delete file.')
            try:
                os.remove(f'../images/{f}')
                print(f'Successfully deleted: {f}')
                deleted_count += 1
            except Exception as delete_error:
                print(f'Failed to delete {f}: {delete_error}')
        iteration += 1
    print(f'Remaining files: {len(os.listdir("../images"))}')
    print(f'Total deleted: {deleted_count}')


def move_cloaked_images(src_path="../images", dest_path="../images-cloaked"):
    """
    Move cloaked images from one directory to another. Defualt from images directory
    where images are stored to the images-cloaked directory where they should exist.

    Args:
        src_path: Source directory path
        dest_path: Destination directory path

    Returns:
        None
    """
    print(f'========== Moving cloaked images from {src_path} --> {dest_path} ==========')
    
    # Generate list of filenames to move
    with os.scandir(src_path) as source:
        filenames = [f for f in source if f.name.endswith("cloaked.jpeg")]
    print(f'*  {len(filenames)} cloaked image(s) detected')
    print(filenames)
    
    # Move files
    for f in filenames:
        new_filename = f.name.split('_l')[0]
        os.rename(f'{src_path}/{f.name}', f'{dest_path}/{new_filename}.jpg')


def csv_writer(content: [[]], filename_ext="default", relative_dirpath="../results/"):
    """
    Write experiment results to file at: relative_dirpath

    Args:
        content: Content to write to CSV file
        filename_ext: Filename string to identify experiment type
        relative_dirpath: Relative directory path to write file to.

    Returns:
        None
    """
    # Create directory if not exists
    os.makedirs(relative_dirpath, exist_ok=True)
    filepath = f'{relative_dirpath}results_{filename_ext}_{DATE}.csv'
    # Write results to file
    print(f'Writing results to: {filepath}')
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)
    print(f'Results successfully written to: {filepath}')


def missing_ai_images():
    """
    Move AI images not in the processed AI diretory to the failed directory

    Args:
        None

    Returns:
        None
    """
    files = list(os.listdir('../images-cloaked-med'))
    iteration = 0
    for f in files:
        path = f'../images-ai/{f}'
        if(os.path.exists(path) != True):
            print(path)
            iteration += 1
            os.rename(f'{"../images-cloaked-med"}/{f}', f'{"../images-ai-failed"}/{f}')
    print(iteration)
    

def generate_ai_images(input_dir): 
    """
    Generate a set of AI generated images

    Args:
        input_dir: filepath to input directory containing source images

    Returns:
        None
    """
    images = list(os.listdir(input_dir))
    for f in images:
        try:
            path = f'{input_dir}/{f}'
            split_data = path.split(input_dir + "/")[1].split("_")
            if (split_data[1] == "0"):
                split_data[1] = "male"
            else:
                split_data[1] = "female"
            files = [("input_image", open(path, "rb"))]
            # Payload for API request
            payload = {
                "text_prompt": "Marketer, " + split_data[1] + ", " + split_data[0] + " years old, professional headshot, solid background, portrait for linkedin",
                "face_scale": 0.4,
                "face_pos_x": 0.5,
                "face_pos_y": 0.5,
            }
            # API Request
            response = requests.post(
                "https://api.gooey.ai/v2/FaceInpainting/form/",
                headers={
                    "Authorization": "bearer " + os.environ["GOOEY_API_KEY"],
                },
                files=files,
                data={"json": json.dumps(payload)},
            )
            assert response.ok, response.content
            result = response.json()
            output_images = result.get('output', {}).get('output_images', [])
            urllib.request.urlretrieve(output_images[0], "../images-ai/" + path.split(input_dir)[1])
        except Exception as e:
            print("ERROR!", e.__str__())
    


def mass_rename(input_dir="../images-ai", cloaked_ext="_mid"):
    """
    Rewrite filepaths of images in a directory, given the cloaked filename extension.
    This script should be used when fawkes generated a set of images and filenames are
    modified from the original, but should be renamed back to the original.

    Args:
        input_dir: Input directory containing images with incorrect filepaths
        cloaked_ext: Filename extension given by fawkes after processing

    Returns:
        None
    """
    for f in list(os.listdir(input_dir)):
        new = f.split('.')[0].split(cloaked_ext)[0]
        os.rename(f'../images-ai/{f}', f'../images-ai/{new}.jpg')


if __name__ == "__main__":
    main()
