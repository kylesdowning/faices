from deepface import DeepFace
import os
import random

def main():
    # Remove invalid faces not recognized by the model.
    remove_invalid_faces()

    
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
