import datetime
import math
import os

import fire
import logging
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.keras.callbacks import ModelCheckpoint
from fastprogress.fastprogress import master_bar, progress_bar

from mozhi.bin.urn.datasets_urn import DATASET_OBJ_MAP
from mozhi.bin.urn.models_urn import TF_MODEL_OBJECT_MAP
from mozhi.bin.urn.preprocessor_urn import PREPROCESSOR_OBJ_MAP

from mozhi.config.config import settings
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report
from  sklearn_crfsuite.metrics import flat_classification_report

# https://medium.com/analytics-vidhya/ner-tensorflow-2-2-0-9f10dcf5a0a
# https://github.com/bhuvanakundumani/NER_tensorflow2.2.0
from mozhi.utils.pretty_print import print_info, print_error


def plot_history(history):
    plt.style.use('ggplot')

    accuracy = history.history['accuracy']
    val_accuracy = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(accuracy) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, accuracy, 'b', label='Training acc')
    plt.plot(x, val_accuracy, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    # plt.waitforbuttonpress()


def pred2label(pred, preprocessor):
    out = []
    for pred_i in pred:
        out_i = []
        for p in pred_i:
            p_i = np.argmax(p)
            out_i.append(preprocessor.id2label(p_i))
        out.append(out_i)
    return out


def main(dataset_name,
         preprocessor_name,
         model_name):
    epochs = 10
    batch_size = 128
    logging.basicConfig(format='%(asctime)s - %(levelname)s -   %(message)s',
                        datefmt='%m/%d/%Y ',
                        level=logging.INFO)

    dataset = DATASET_OBJ_MAP[dataset_name](**settings.datasets[dataset_name])
    preprocessor = PREPROCESSOR_OBJ_MAP[preprocessor_name].init_vf(dataset_info=dataset.get_dataset_info(),
                                                                   **settings.preprocessor[preprocessor_name])
    model = TF_MODEL_OBJECT_MAP[model_name].init_vf(preprocessor_data_info=preprocessor.get_preprocessor_info(),
                                                    **settings.models[model_name])
    optimizer = model.optimizer
    loss_fn = model.loss

    train_dataset = preprocessor.get_tf_data_iterator(sentences=dataset.train_tuple_pairs)
    valid_dataset = preprocessor.get_tf_data_iterator(sentences=dataset.val_tuple_pairs)
    test_dataset = preprocessor.get_tf_data_iterator(sentences=dataset.test_tuple_pairs)

    shuffled_train_dataset = train_dataset.shuffle(buffer_size=len(dataset.train_tuple_pairs),
                                                   reshuffle_each_iteration=True)

    batched_train_dataset = shuffled_train_dataset.batch(batch_size,
                                                         drop_remainder=True)
    batched_valid_dataset = valid_dataset.batch(batch_size,
                                                drop_remainder=True)
    batched_test_dataset = test_dataset.batch(batch_size,
                                              drop_remainder=True)

    train_log_dir = os.path.expanduser(f"~/.mozhi/logs/{str(model.NAME).lower()}/train")
    valid_log_dir = os.path.expanduser(f"~/.mozhi/logs/{str(model.NAME).lower()}/valid")
    train_summary_writer = tf.summary.create_file_writer(train_log_dir)
    valid_summary_writer = tf.summary.create_file_writer(valid_log_dir)

    tf.summary.trace_on(graph=True)
    tf.profiler.experimental.start(train_log_dir)

    train_loss_metric = tf.keras.metrics.Mean('training_loss', dtype=tf.float32)
    valid_loss_metric = tf.keras.metrics.Mean('valid_loss', dtype=tf.float32)

    epoch_bar = master_bar(range(epochs))
    train_pb_max_len = math.ceil(float(len(dataset.train_tuple_pairs)) / float(batch_size))
    valid_pb_max_len = math.ceil(float(len(dataset.val_tuple_pairs)) / float(batch_size))
    test_pb_max_len = math.ceil(float(len(dataset.test_tuple_pairs)) / float(batch_size))


    def train_step_fn(sentences_batch, labels_batch):
        with tf.GradientTape() as tape:
            logits = model(sentences_batch)  # batchsize, max_seq_len, num_labels
            loss = loss_fn(labels_batch, logits)  # batchsize, max_seq_len

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(
            (grad, var)
            for (grad, var) in zip(gradients, model.trainable_variables)
            if grad is not None
        )
        return loss, logits

    def valid_step_fn(sentences_batch, labels_batch):
        logits = model(sentences_batch)
        loss = loss_fn(labels_batch, logits)
        return loss, logits

    for epoch in epoch_bar:
        with train_summary_writer.as_default():
            for sentences_batch, labels_batch in progress_bar(batched_train_dataset,
                                                              total=train_pb_max_len,
                                                              parent=epoch_bar):
                loss, logits = train_step_fn(sentences_batch, labels_batch)
                train_loss_metric(loss)
                epoch_bar.child.comment = f'training loss : {train_loss_metric.result()}'
            tf.summary.scalar('training loss', train_loss_metric.result(), step=epoch)
            train_loss_metric.reset_states()

        with valid_summary_writer.as_default():
            for sentences_batch, labels_batch in progress_bar(batched_valid_dataset, total=valid_pb_max_len,
                                                              parent=epoch_bar):
                loss, logits = valid_step_fn(sentences_batch, labels_batch)
                valid_loss_metric.update_state(loss)

                epoch_bar.child.comment = f'validation loss : {valid_loss_metric.result()}'

            # Logging after each Epoch !
            tf.summary.scalar('valid loss', valid_loss_metric.result(), step=epoch)
            valid_loss_metric.reset_states()

        print_info(f"Saving model weights to {model.model_file_path}")
        # model.save_weights(f"{model.model_file_path}/model_weights", save_format='tf')
        # tf.saved_model.save(model, f"{model.model_file_path}")
        tf.keras.models.save_model(model, f"{model.model_file_path}")
        # model.save(f"{model.model_file_path}/model_weights")
        print_info(f"Model weights saved")

    # model.load_weights(f"{model.model_file_path}/model_weights")
    # model = tf.saved_model.load(f"{model.model_file_path}")
    # model = tf.keras.models.load_model(f"{model.model_file_path}/model_weights")
    model = tf.keras.models.load_model(f"{model.model_file_path}")
    print_error("loaded")

    y_test = []
    y_pred = []

    for sentences_batch, labels_batch in progress_bar(batched_test_dataset,
                                                      total=test_pb_max_len):
        logits = model(sentences_batch)
        preds = tf.nn.softmax(logits)
        y_test.append(np.asarray(labels_batch))
        y_pred.append(np.asarray(preds))

    y_pred = pred2label(pred=y_pred, preprocessor=preprocessor)
    y_test = pred2label(pred=y_test, preprocessor=preprocessor)
    print_info("*"*100)
    print_info("F1-score: {:.1%}".format(f1_score(y_test, y_pred)))
    print_info("*"*100)
    report = flat_classification_report(y_pred=y_pred, y_true=y_test)
    print_info(report)


if __name__ == '__main__':

    # Ref: https://www.tensorflow.org/guide/gpu
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)


    fire.Fire(main)
