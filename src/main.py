from deepface import DeepFace
import os
import random
import datetime
# from fawkes.protection import Fawkes

def swap_words(s, x, y):
    return y.join(part.replace(y, x) for part in s.split(x))

# DateTime for unique file naming. Add the Fawkes mode to the filename as well.
DATE=swap_words(datetime.datetime.now().strftime("%x-%H:%M:%S"), "/", "_")




def main():
    # Remove invalid faces not recognized by the model.
    # remove_invalid_faces()
    print(f'-----Program invoked at: {DATE}-----\n')

    # Similarity Check
    result = cloaked_similarity_check()
    print('\n\nResult list:')
    for r in result:
        print(r)

    # TODO: Write Results to CSV File

    # TODO: Generate Synthetic Dataset

    print(f'\n-----Program terminated at: {swap_words(datetime.datetime.now().strftime("%x-%H:%M:%S"), "/", "_")}-----')

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
    files = list(os.listdir('../images_cloaked'))
    iteration = 0
    ret_list = []
    ret_list.append(["filename", "verified", "distance"])
    print(f'Processing cloaked images in {cloaked_dir}\n')
    for f in files:
        try:
            print(f'===== Iteration {iteration} - File {f} =====')
            path1 = f'../images/{f}'
            path2 = f'../images_cloaked/{f}'
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


# Each entry is verified as having a compatible face.
def remove_invalid_faces() -> None:
    # Create a list of all files first to avoid issues when deleting during iteration
    files = list(os.listdir('../images'))
    random.shuffle(files)
    print(f'Total files: {len(files)}')
    ref_img = "../images/100_0_0_20170112213500903.jpg"
    iteration = 0
    deleted_count = 0
    for f in files:
        print(f'Processing: {f} - iteration: {iteration}')
        try:
            result: dict = DeepFace.verify(
                img1_path=ref_img,
                img2_path=(f"../images/{f}")
            )
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
    print(f'========== Moving cloaked images from {src_path} --> {dest_path} ==========')
    with os.scandir(src_path) as source:
        filenames = [f for f in source if f.name.endswith("cloaked.jpg")]
    print(f'*  {len(filenames)} cloaked image(s) detected')
    print(filenames)
    for f in filenames:
        new_filename = f.split('.')[0]
        os.rename(f'{src_path}/{f}', f'{dest_path}/{new_filename}.jpg')


if __name__ == "__main__":
    main()
