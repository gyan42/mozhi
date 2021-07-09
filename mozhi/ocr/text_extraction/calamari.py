# import os
# from glob import glob
#
# from calamari_ocr.ocr.dataset import DataSetType
# from calamari_ocr.scripts.predict import run as calamari_ocr_run
#
# # Add your files here
# calamari_models = ['data/models/calamari/calamari_models-1.0/antiqua_historical/0.ckpt']
# calamari_input_images = []  # glob(os.path.join(config.ROOT_DIR, config.TEXT_IMAGES) + '/*/*')  # Add your files here
#
#
# class CalamariArgs:
#     batch_size = 1
#     checkpoint = calamari_models
#     dataset = DataSetType.FILE
#     extended_prediction_data = False
#     extended_prediction_data_format = 'json'
#     files = calamari_input_images
#     no_progress_bars = False
#     output_dir = None
#     pagexml_text_index = 1
#     processes = 1
#     text_files = None
#     verbose = False
#     voter = 'confidence_voter_default_ctc'
#     extension = None
#     beam_width = 20
#     dictionary = []
#     dataset_pad = None
#
#
# def find_files_with_ext(search_folder, exts=['.JPG', '.jpg', '.png']):
#     all_files = glob(search_folder + '**/**', recursive=True)
#     bag = []
#     if exts:
#         for _ext in exts:
#             bag += [file for file in all_files if file.endswith(_ext)]
#     else:
#         bag = all_files
#     return bag
#
#
# def get_all_input_files(source_dir, input_files_types=['.JPG', '.jpg', '.png']):
#     """Get the list of images files from the source directory"""
#     return find_files_with_ext(source_dir, input_files_types)
#
#
# def handle_file(in_file_path, out_file_path):
#     destination_dir = out_file_path.split("/")[-2]
#     CalamariArgs.files = [in_file_path]
#     CalamariArgs.output_dir = destination_dir
#     calamari_ocr_run(CalamariArgs)
#
#
# def handle_files(source_dir, destination_dir):
#     """Plugin module should implement this to handle all the files in the given directory"""
#
#     if not os.path.exists(destination_dir):
#         os.makedirs(destination_dir)
#
#     if calamari_models is not None:
#         CalamariArgs.checkpoint = calamari_models
#
#     for dir in os.listdir(source_dir):
#
#         in_files = get_all_input_files(source_dir=os.path.join(source_dir, dir))
#
#         print(">>>>>>>>>>>>>>>>>> {}".format(in_files))
#
#         if in_files:
#             output_dir = os.path.join(destination_dir, dir)
#
#             if not os.path.exists(output_dir):
#                 os.makedirs(output_dir)
#
#             CalamariArgs.files = in_files
#             CalamariArgs.output_dir = output_dir
#             CalamariArgs.batch_size = len(in_files)
#             CalamariArgs.processes = 4
#             calamari_ocr_run(CalamariArgs)


import os
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import numpy as np

# Create the predictor, and the raw predictor somewhere in your code
from calamari_ocr.ocr.predict.predictor import Predictor, PredictorParams
predictor = Predictor.from_checkpoint(params=PredictorParams(), checkpoint='/data/model_output/best.ckpt')
raw_predictor = predictor.raw().__enter()__  # you can also wrap the following lines in a `with`-block

files = os.listdir("data/test/")
for f in files:
    raw_image = plt.imread("data/test/" + f)
    sample = predictor.predict_raw(raw_image)  # raw_image is e.g. np.zeros(200, 50)
    inputs, prediction, meta = sample.inputs, sample.outputs, sample.meta
    print(prediction)

# prediction is usually what you are looking for


def raw_image_generator():
    files = os.listdir("data/test/")
    for f in files:
        print("data/test/" + f)
        yield  np.asarray(ImageOps.grayscale(Image.open("data/test/" + f).convert('LA')))

# i = Image.open("data/test/X51006619561_46.jpg").convert('LA')

for sample in predictor.predict_raw(raw_image_generator()):
    inputs, prediction, meta = sample.inputs, sample.outputs, sample.meta
    print(prediction.sentence)