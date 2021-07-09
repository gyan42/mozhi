import os

import numpy as np
import fire
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning import loggers as pl_loggers

from mozhi.bin.urn.datasets_urn import DATASET_OBJ_MAP
from mozhi.bin.urn.models_urn import PYTORCH_MODEL_OBJECT_MAP
from mozhi.bin.urn.preprocessor_urn import PREPROCESSOR_OBJ_MAP

from mozhi.config.config import settings
from mozhi.utils.pretty_print import print_info


def main(experiment_name: str,
         dataset_name: str,
         preprocessor_name: str,
         model_name: str):
    """

    Args:
        experiment_name:
        dataset_name:
        preprocessor_name:
        model_name:

    Returns:

    """

    dataset = DATASET_OBJ_MAP[dataset_name](**settings.datasets[dataset_name])
    preprocessor = PREPROCESSOR_OBJ_MAP[preprocessor_name].init_vf(dataset_info=dataset.get_dataset_info(),
                                                                   **settings.preprocessor[preprocessor_name])

    preprocessor_store_path = os.path.expanduser(
        settings.pl_trainer.preprocessor_root_dir + experiment_name + "/" + preprocessor.NAME)
    # Save preprocessor object as pickle for prediction
    preprocessor.dump(preprocessor_store_path, preprocessor)

    tagger = PYTORCH_MODEL_OBJECT_MAP[model_name].init_vf(preprocessor_data_info=preprocessor.get_preprocessor_info(),
                                                          **settings.models[model_name])

    train_dataset = preprocessor.get_torch_dataloader(sentences=dataset.train_tuple_pairs)
    val_dataset = preprocessor.get_torch_dataloader(sentences=dataset.val_tuple_pairs)
    test_dataset = preprocessor.get_torch_dataloader(sentences=dataset.test_tuple_pairs)

    model_store_dir = os.path.expanduser(settings.pl_trainer.model_root_dir + experiment_name + "/" + tagger.NAME.lower())
    # saves a file like: my/path/sample-mnist-epoch=02-val_loss=0.32.ckpt
    checkpoint_callback = ModelCheckpoint(
        monitor='val_loss',
        dirpath=model_store_dir,
        filename=tagger.NAME.lower() + '-{epoch:02d}-{val_loss:.2f}',
        save_top_k=3,
        mode='min',
    )
    early_stop_callback = EarlyStopping(monitor='val_loss', min_delta=0.00, patience=5, verbose=True, mode='min')
    tb_logger = pl_loggers.TensorBoardLogger(os.path.expanduser(settings.pl_trainer.log_root_dir + experiment_name + "/" + tagger.NAME.lower()))

    trainer = pl.Trainer(callbacks=[checkpoint_callback, early_stop_callback],
                         logger=tb_logger,
                         gpus=settings.pl_trainer.gpus,
                         max_epochs=settings.pl_trainer.max_epochs,
                         auto_lr_find=False,
                         auto_scale_batch_size=False)  # https://arxiv.org/abs/1506.01186
    trainer.fit(model=tagger,
                train_dataloader=train_dataset,
                val_dataloaders=val_dataset)

    # trainer.save_checkpoint()

    test_res = trainer.test(model=tagger,
                            test_dataloaders=test_dataset,
                            verbose=True)

    # Prepare the best model for serving
    tagger.load_from_checkpoint(checkpoint_callback.best_model_path)
    script = tagger.to_torchscript()
    # save for use in production environment
    torch.jit.save(script, model_store_dir + f"/{tagger.NAME.lower()}.pt", map)

    # torch.jit.save(tagger.to_torchscript(), "/tmp/model.pt")

    print_info("*" * 100)
    print_info(f"Preprocessor data stored in {preprocessor_store_path}")
    print_info(f"Model checkpoint directory {model_store_dir}")
    print_info(f"Best model checkpoint : {checkpoint_callback.best_model_path}")
    print_info("*" * 100)

if __name__ == '__main__':
    fire.Fire(main)