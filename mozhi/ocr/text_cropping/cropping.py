import time

import matplotlib.pyplot as plt
import os
import concurrent.futures
import pathlib
import fire
from tqdm import tqdm


def _process(image_file_path,
             text_file_path,
             out_base_file_name,
             out_extension,
             out_dir):
    image = plt.imread(image_file_path)
    text_lines = open(text_file_path).readlines()
    for i, text_line in enumerate(text_lines):
        x1_1, y1_1, x2_1, y2_1, x3_1, y3_1, x4_1, y4_1, transcript = text_line.split(",")[:9]
        x1_1, y1_1, x2_1, y2_1, x3_1, y3_1, x4_1, y4_1 = int(x1_1), int(y1_1), int(x2_1), int(y2_1), int(x3_1), int(
            y3_1), int(x4_1), int(y4_1)
        cropped_image = image[y1_1:y3_1, x1_1:x3_1]
        img_out_file = out_dir + out_base_file_name + "_" + str(i) + out_extension
        plt.imsave(img_out_file, cropped_image)
        txt_out_file = out_dir + out_base_file_name + "_" + str(i) + ".gt.txt"
        with open(txt_out_file, "w+") as f:
            f.write(transcript)

    return f"Finished processing {image_file_path}"


class SROIE2019TextImageCropper(object):
    """
    Splits the text image into individual line images, based on teh vertices starting from top.

    Receipt(.png/.jpg)

    x1_1, y1_1,x2_1,y2_1,x3_1,y3_1,x4_1,y4_1, transcript_1
    x1_2,y1_2,x2_2,y2_2,x3_2,y3_2,x4_2,y4_2, transcript_2
    x1_3,y1_3,x2_3,y2_3,x3_3,y3_3,x4_3,y4_3, transcript_3
    ...

    """

    def __init__(self, input_dir, file_ext, out_dir, num_threads):
        self._input_dir = input_dir
        self._file_ext = file_ext
        self._out_dir = out_dir
        self._image_files = self._collect_image_files()
        self._text_files = self._collect_text_files()
        self._data_files = self._collect_data()
        self._num_threads = int(num_threads)

        os.makedirs(self._out_dir, exist_ok=True)

    def _collect_image_files(self):
        files = os.listdir(self._input_dir)
        files = [_file for _file in files if _file.endswith(self._file_ext)]
        # print(files)
        return files

    def _collect_text_files(self):
        files = os.listdir(self._input_dir)
        files = [_file for _file in files if _file.endswith("txt")]
        # print(files)
        return files

    def _collect_data(self):
        res = {}

        for _file in self._image_files:
            _text_files = [_f for _f in self._text_files if _file.split(".")[0] in _f]
            if len(_text_files) > 0:
                res[_file] = _text_files[0]  # TODO only considering the first ground truth text

        return res

    def process(self):
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._num_threads) as executor:
            result_futures = list(map(lambda image_text_file:
                               executor.submit(_process,
                                                self._input_dir + image_text_file[0],
                                                self._input_dir + image_text_file[1],
                                                image_text_file[0].split(".")[0],
                                                self._file_ext,
                                                self._out_dir),
                           self._data_files.items()))

            for future in tqdm(concurrent.futures.as_completed(result_futures), total=len(self._data_files.items())):
                try:
                    future.result()
                except Exception as e:
                    print(e)
        print(f"Time takes on ThreadPoolExecutor: {time.time() - start}")


def main(input_dir, file_ext, out_dir, num_threads):
    """

    Args:
        input_dir: SROIE2019 data directory
        file_ext: .jpeg
        out_dir:
        num_threads:

    Returns:

    """
    cropper = SROIE2019TextImageCropper(input_dir,
                                        file_ext,
                                        out_dir,
                                        num_threads)
    cropper.process()


"""
cd /path/to/mozhi/
export PYTHONPATH=$PYTHONPATH:$(pwd)/mozhi/
python mozhi/ocr/text_cropping/cropping.py --input_dir=data/SROIE2019/0325updated.task1train\(626p\)/ \
--file_ext=.jpg \
--out_dir=/tmp/vf/cropper/ \
--num_threads=8

"""
if __name__ == "__main__":
    fire.Fire(main)