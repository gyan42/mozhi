import fire

from mozhi.ocr.text_detection import craft
from mozhi.ocr.text_extraction import calamari
from mozhi.ocr.text_stiching import combine_text_files


def main(input_image_path="data/receipts/X51008142068.jpg",
         intermediate_path="/tmp/vf/craft/X51008142068/",
         text_out_path="/tmp/vf/output",
         out_text_file_path="/tmp/vf/output/X51008142068.txt"):
    craft.text_detection_craft(input_image_path=input_image_path,
                               output_dir=intermediate_path)
    calamari.handle_files(source_dir=intermediate_path,
                          destination_dir=text_out_path)
    combine_text_files.handle_file(input_txt_files_dir=text_out_path+'/X51008142068_crops/',
                                   out_file_path=out_text_file_path)

    print(open(out_text_file_path, "r").readlines())


if __name__ == '__main__':
    fire.Fire(main)