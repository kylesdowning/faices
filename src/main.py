from deepface import DeepFace
import os
import random
import datetime
import csv
import requests
import json
import urllib.request
# from fawkes.protection import Fawkes

def swap_words(s, x, y):
    return y.join(part.replace(y, x) for part in s.split(x))

# DateTime for unique file naming. Add the Fawkes mode to the filename as well.
DATE=swap_words(datetime.datetime.now().strftime("%x-%H:%M:%S"), "/", "_")




def main():
    # # Remove invalid faces not recognized by the model.
    # # remove_invalid_faces()
    # print(f'-----Program invoked at: {DATE}-----\n')

    # # Similarity Check
    # #result = cloaked_similarity_check()
    # #print('\n\nResult list:')
    # #for r in result:
    #     #print(r)

    # content = [["1", "2"], ["a", "b"], ["c", "d"]]
    # csv_writer(content)

    # # TODO: Write Results to CSV File

    # # TODO: Generate Synthetic Dataset

    # print(f'\n-----Program terminated at: {swap_words(datetime.datetime.now().strftime("%x-%H:%M:%S"), "/", "_")}-----')
    
    # #used to move the images
    # #move_cloaked_images("../images-0", "../images-cloaked-low")
    # #move_cloaked_images("../images-1", "../images-cloaked-low")

    #generate_ai_images()
    missing_ai_images()

def generate_synthetic_images():
    pass

# Verify all images return 100% similarities against themselves
def similarity_check() -> bool:
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

# return similarity between cloaked images and the original images
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


# For all images in the src directory, move them to the destination directory.
def move_cloaked_images(src_path="../images", dest_path="../images-cloaked"):
    """
    Move cloaked images from one directory to another

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
    files = list(os.listdir('../images-cloaked-med'))
    iteration = 0
    
    for f in files:
            
        path = f'../images-ai/{f}'
        
        if(os.path.exists(path) != True):
            print(path)
        
        iteration += 1
    print(iteration)
            
            


def generate_ai_images(input_dir="../images-cloaked-med"): 

    images = list(os.listdir(input_dir))

    for f in images:
        try:

            path = f'../images-cloaked-med/{f}'

            split_data = path.split("../images-cloaked-med/")[1].split("_")
            
            if(split_data[1] == "0"):
                split_data[1] = "male"
            
            else:
                split_data[1] = "female"

            files = [("input_image", open(path, "rb"))]
            payload = {
                "text_prompt": "Marketer, " + split_data[1] + ", " + split_data[0] + " years old, professional headshot, solid background, portrait for linkedin",
                "face_scale": 0.4,
                "face_pos_x": 0.5,
                "face_pos_y": 0.5,
            }

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

            urllib.request.urlretrieve(output_images[0], "../images-ai/" + path.split("../images-cloaked-med/")[1])
            
        except Exception as e:
            print("ERROR!")
    

if __name__ == "__main__":
    main()
