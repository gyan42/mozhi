"""

"""
import os

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import fire

from mozhi.dataset.ner.conll.vf_conll_2003 import CoNLLLoader
from mozhi.utils.pretty_print import print_info


def delete_table(table_name, engine):
    """

    :param table_name:
    :param engine:
    :return:
    """
    sql_command = f"drop table if exists {table_name} cascade "
    engine.execute(sql_command)


def parse_conll(txt_file_path):
    """
    Parses and converts the vanilla CoNLL 2003 dataset into Dataframe
    Args:
        txt_file_path:

    Returns: pandas.DataFrame with columns [text, features, labels]

    """
    sentences = CoNLLLoader.split_text_label(txt_file_path)
    text_list = []
    features_list = []
    labels_list = []
    labels_set = set()
    for sentence in sentences:
        features = []
        labels = []
        for word, tag in sentence:
            features.append(word)
            labels.append(tag)
            labels_set.add(tag)
        text_list.append(" ".join(features))
        features_list.append(" ".join(features))
        labels_list.append(" ".join(labels))
    df = pd.DataFrame({"text": text_list, "features": features_list, "labels": labels_list})
    df['id'] = df.index
    return df, list(labels_set)


def upload_text_data(dir_root_path,
                     is_delete,
                     engine,
                     experiment_name):
    print_info("Uploading text data...")

    for f_name in os.listdir(dir_root_path):
        dfs = []
        labels = []
        file_path = dir_root_path + '/' + f_name
        print_info(f"Processing {file_path}...")
        if file_path.endswith(".txt"):
            df, labels = parse_conll(file_path)
            dfs = [df]
        else:
            RuntimeError("Only CoNLL vanilla text format is supported, enable the flag `is_conll` to process")

        table_name = experiment_name + '_' + f_name.split(".")[0]

        # Delete text and tag data
        if is_delete:
            delete_table(table_name=table_name, engine=engine)
            delete_table(table_name=table_name + '_tags', engine=engine)

        # Create DF frm tags collected and upload
        df = pd.DataFrame({'name': labels})
        if 'id' not in df.columns:
            df['id'] = df.index
            # Upload the tags
            df.to_sql(
                table_name + "_tags",
                engine,
                index=False,
                if_exists='replace'
            )

        # Upload text data in chunks
        for df in dfs:
            if 'features' not in df.columns:
                df['features'] = ""
            if 'labels' not in df.columns:
                df['labels'] = ""
            if 'id' not in df.columns:
                df['id'] = df.index

            df.to_sql(
                table_name,
                engine,
                index=False,
                if_exists='append'  # if the table already exists, append this data
            )


def upload_table_data(dir_root_path,
                      is_delete,
                      engine,
                      experiment_name):
    print_info("Uploading table data...")
    for f_name in os.listdir(dir_root_path):
        file_path = dir_root_path + '/' + f_name
        print_info(f"Processing {file_path}...")
        if file_path.endswith(".parquet"):
            dfs = pd.read_parquet(file_path, chunksize=1000)
        elif file_path.endswith(".csv"):
            dfs = pd.read_csv(file_path, chunksize=1000)
        else:
            raise RuntimeError(f"File format not supported : {file_path}")

        table_name = experiment_name + '_' + f_name.split(".")[0]

        if is_delete:
            delete_table(table_name=table_name, engine=engine)

        if '_tags' in file_path:
           for df in dfs:
                if 'id' not in df.columns:
                    df['id'] = df.index
                # Upload the tags
                df.to_sql(
                    table_name,
                    engine,
                    index=False,
                    if_exists='replace'
                )
        else:
            for df in dfs:
                if 'features' not in df.columns:
                    df['features'] = ""
                if 'labels' not in df.columns:
                    df['labels'] = ""
                if 'id' not in df.columns:
                    df['id'] = df.index

                df.to_sql(
                    table_name,
                    engine,
                    index=False,
                    if_exists='append'  # if the table already exists, append this data
                )


def to_bool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes']


def main(host: str,
         port: str,
         db_name: str,
         user: str,
         password: str,
         dir_root: str,
         is_delete: str,
         is_conll: str,
         experiment_name: str):
    """
    Uploads csv/parquet files to DB for annotation.

    Table data is expected to have following schema:
        text: string
        features: string (optional) Space separated tokenized text
        labels: string (optional) Space separated corresponding tags

    Tag data is expected to have following schema:
        name: string Name of the tag

    File name is used as table names. Recommended file name format:
        {file_name}.csv and {file_name}_tags.csv

    Args:
        host:
        port:
        db_name:
        user:
        password:
        dir_root:
        is_delete: bool Delete existing table data
        is_conll:
        experiment_name:

    Returns:

    """
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    if to_bool(is_conll):
        upload_text_data(dir_root_path=dir_root,
                         is_delete=to_bool(is_delete),
                         engine=engine,
                         experiment_name=experiment_name)
    else:
        upload_table_data(dir_root_path=dir_root,
                          is_delete=to_bool(is_delete),
                          engine=engine,
                          experiment_name=experiment_name)


if __name__ == "__main__":
    fire.Fire(main)