import os
import fire
import numpy as np
import transformers
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer, AutoTokenizer
from transformers import DataCollatorForTokenClassification
from datasets import load_dataset, load_metric

from mozhi.bin.urn.urn import URNLoader
from mozhi.config.config import settings
from mozhi.utils.pretty_print import print_info

metric = load_metric("seqeval")


def compute_metrics(p, label_list):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    # Remove ignored index (special tokens)
    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


class MozhiHFtrainer(object):
    def __init__(self,
                 dataset,
                 hf_pretrained_model_checkpoint,
                 hf_pretrained_tokenizer_checkpoint,
                 preprocessor,
                 model_n_version):

        urn = URNLoader()
        if type(dataset) == str:
            # Load the class
            hf_dataset = urn.load_dataset_class(dataset)
            # Initialize the class
            hf_dataset = hf_dataset(**settings.datasets[dataset])
        else:
            hf_dataset = dataset
            
        if type(preprocessor) == str:
            preprocessor = urn.load_preprocess_class(preprocessor)
            preprocessor.init_vf(
                hf_pretrained_tokenizer_checkpoint=hf_pretrained_tokenizer_checkpoint)

        hf_model = AutoModelForTokenClassification.from_pretrained(hf_pretrained_model_checkpoint,
                                                                   num_labels=len(hf_dataset.labels))
        hf_model.config.id2label = hf_dataset.id2label
        hf_model.config.label2id = hf_dataset.label2id

        tokenized_datasets = hf_dataset.datasets.map(preprocessor.tokenize_and_align_labels, batched=True)

        # ---------------------------------------------------------------------------------------------------

        args = TrainingArguments(
            f"test-ner",
            evaluation_strategy="epoch",
            learning_rate=settings.hf_trainer.learning_rate,
            per_device_train_batch_size=settings.hf_trainer.batch_size,
            per_device_eval_batch_size=settings.hf_trainer.batch_size,
            num_train_epochs=settings.hf_trainer.max_epochs,
            weight_decay=0.01,
        )

        print_info(tokenized_datasets["train"])
        data_collator = DataCollatorForTokenClassification(preprocessor.tokenizer)
        trainer = Trainer(
            hf_model,
            args,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["validation"],
            data_collator=data_collator,
            tokenizer=preprocessor.tokenizer,
            compute_metrics=lambda p: compute_metrics(p=p, label_list=hf_dataset.labels)
        )

        trainer.train()
        trainer.evaluate()

        # ---------------------------------------------------------------------------------------------------

        predictions, labels, _ = trainer.predict(tokenized_datasets["test"])
        predictions = np.argmax(predictions, axis=2)

        # Remove ignored index (special tokens)
        true_predictions = [
            [hf_dataset.labels[p] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [hf_dataset.labels[l] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]

        results = metric.compute(predictions=true_predictions, references=true_labels)
        print(results)

        out_dir = os.path.expanduser(settings.hf_trainer.model_root_dir) + "/" + model_n_version
        trainer.save_model(out_dir)


def main(dataset,
         hf_pretrained_model_checkpoint,
         hf_pretrained_tokenizer_checkpoint,
         preprocessor,
         model_n_version):

    MozhiHFtrainer(dataset=dataset,
                   hf_pretrained_model_checkpoint=hf_pretrained_model_checkpoint,
                   hf_pretrained_tokenizer_checkpoint=hf_pretrained_tokenizer_checkpoint,
                   preprocessor=preprocessor,
                   model_n_version=model_n_version)


if __name__ == '__main__':
    fire.Fire(main)