from deepface import DeepFace
import os
import random
# from fawkes.protection import Fawkes

def main():
    # Remove invalid faces not recognized by the model.
    # remove_invalid_faces()
    similarity_check()


def generate_synthetic_images():
    pass

# Verify all images return 100% similarities against themselves
def similarity_check():
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
        iteration += 1
    print('===== Finished =====')

# return similarity between cloaked images and the original images
def cloaked_similarity_check():
    #files = list(os.listdir('../images'))
    files = list(os.listdir('../images_cloaked'))
    print(len(list(os.listdir('../images_cloaked'))))
    iteration = 0

    for f in files:
        try:
            print(f'===== Iteration {iteration} - File {f} =====')
            path1 = f'../images/{f}'
            print(path1)

            path2 = f'../images_cloaked/{f}'
            print(path2)


            # result = DeepFace.verify(img1_path=path1, img2_path=path2)
            # print(result["distance"])

        except Exception as e:
            print(f'Problem with DeepFace: {e.__str__()}')
            iteration += 1
    print('===== Finished =====')


# Each entry is verified as having a compatible face.
def remove_invalid_faces():
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


if __name__ == "__main__":
    main()
