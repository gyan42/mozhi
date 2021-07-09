import os
from tqdm import tqdm
from glob import glob


def find_files_with_ext(search_folder, exts):
    all_files = glob(search_folder + '**/**', recursive=True)
    bag = []
    if exts:
        for _ext in exts:
            bag += [file for file in all_files if file.endswith(_ext)]
    else:
        bag = all_files
    return bag


def get_all_input_files(source_dir, input_files_types):
    """Get the list of images files from the source directory"""
    return find_files_with_ext(source_dir, input_files_types)


def handle_file(input_txt_files_dir, out_file_path):
    input_txt_files = get_all_input_files(source_dir=input_txt_files_dir,
                                          input_files_types=['.txt'])
    # sort based on file number Eg: /tmp/vf/output/fee93e28-55ac-4cfd-aaca-919e0d3ab34d_text_image.png/fee93e28-55ac-4cfd-aaca-919e0d3ab34d_text_image_crops/crop_0.pred.txt
    input_txt_files = sorted(input_txt_files,
                      key=lambda f: int(os.path.splitext(f)[0].split("/")[-1].split(".")[0].split("_")[-1]))
    lines = []

    for each_in_text_prediction in tqdm(input_txt_files):
        if os.path.isfile(out_file_path) and os.path.isfile(each_in_text_prediction):
            #  read the file and append values
            with open(out_file_path, "a") as fd:
                line = open(each_in_text_prediction, "r").read()
                lines.append(line)
                fd.write(line)
                fd.write("\n")
        else:
            # create a new file with headers
            with open(out_file_path, "w") as fd:
                line = open(each_in_text_prediction, "r").read()
                lines.append(line)
                fd.write(line)
                fd.write("\n")

    return lines