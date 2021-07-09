# import Craft class
from craft_text_detector import Craft

def text_detection_craft(input_image_path, output_dir):
    """

    :param input_image_path:
    :param out_dir:
    :return:
    """

    # create a craft instance
    craft = Craft(output_dir=output_dir, crop_type="poly", cuda=False)

    # apply craft text detection and export detected regions to output directory
    prediction_result = craft.detect_text(input_image_path)

    # unload models from ram/gpu
    craft.unload_craftnet_model()
    craft.unload_refinenet_model()
