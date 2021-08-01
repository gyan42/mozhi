import os
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import numpy as np

# Create the predictor, and the raw predictor somewhere in your code
from calamari_ocr.ocr.predict.predictor import Predictor, PredictorParams
predictor = Predictor.from_checkpoint(params=PredictorParams(), checkpoint='/home/model-server/model-store/best.ckpt')

# raw_predictor = predictor.raw().__enter()__  # you can also wrap the following lines in a `with`-block

# files = os.listdir("data/test/")
# for f in files:
#     raw_image = plt.imread("data/test/" + f)
#     sample = predictor.predict_raw(raw_image)  # raw_image is e.g. np.zeros(200, 50)
#     inputs, prediction, meta = sample.inputs, sample.outputs, sample.meta
#     print(prediction)

# prediction is usually what you are looking for


def handle_craft_intermediate_files(source_dir):
    def raw_image_generator():
        files = os.listdir(source_dir)
        # /data/test//X51008142068_crops/crop_0.png
        files = sorted(files, key=lambda x: int(x.split(".")[0].split("_")[-1]))
        for f in files:
            print(source_dir + f)
            yield np.asarray(ImageOps.grayscale(Image.open(source_dir + f).convert('LA')))

    # i = Image.open("data/test/X51006619561_46.jpg").convert('LA')
    sentences = []
    for sample in predictor.predict_raw(raw_image_generator()):
        inputs, prediction, meta = sample.inputs, sample.outputs, sample.meta
        sentences.append(prediction.sentence)

    return sentences


""":param

files = [
"/data/test//X51008142068_crops/crop_51.png",
"/data/test//X51008142068_crops/crop_52.png",
"/data/test//X51008142068_crops/crop_53.png",
"/data/test//X51008142068_crops/crop_54.png",
"/data/test//X51008142068_crops/crop_55.png",
"/data/test//X51008142068_crops/crop_56.png",
"/data/test//X51008142068_crops/crop_57.png",
"/data/test//X51008142068_crops/crop_58.png",
"/data/test//X51008142068_crops/crop_59.png",
"/data/test//X51008142068_crops/crop_6.png",
"/data/test//X51008142068_crops/crop_60.png",
"/data/test//X51008142068_crops/crop_61.png",
"/data/test//X51008142068_crops/crop_7.png",
"/data/test//X51008142068_crops/crop_8.png",
"/data/test//X51008142068_crops/crop_9.png"
]

files = sorted(files, key=lambda x: int(x.split("/")[-1].split(".")[0].split("_")[-1]))
"""