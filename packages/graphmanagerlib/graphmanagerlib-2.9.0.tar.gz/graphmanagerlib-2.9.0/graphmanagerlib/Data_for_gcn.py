import os

import random
import torch
import torch_geometric
import numpy as np
from torch_geometric.utils.convert import from_networkx
from bpemb import BPEmb
from sentence_transformers import SentenceTransformer
from graphmanagerlib.Graph import Grapher
from graphmanagerlib.JsonManager import ConvertJsonToDocumentsObjects

bpemb_en = BPEmb(lang="en", dim=100)
sent_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')


def make_sent_bert_features(text):
    emb = sent_model.encode([text])[0]
    return emb


def get_data(documents,tags):
    """
    returns one big graph with unconnected graphs with the following:
    - x (Tensor, optional) – Node feature matrix with shape [num_nodes, num_node_features]. (default: None)
    - edge_index (LongTensor, optional) – Graph connectivity in COO format with shape [2, num_edges]. (default: None)
    - edge_attr (Tensor, optional) – Edge feature matrix with shape [num_edges, num_edge_features]. (default: None)
    - y (Tensor, optional) – Graph or node targets with arbitrary shape. (default: None)
    - validation mask, training mask and testing mask
    """
    all_files = documents.copy()
    random.shuffle(all_files)


    train_list_of_graphs, test_list_of_graphs = [],[]

    trainingProportion = round(((len(all_files) / 100) * 80))

    training, testing = all_files[:trainingProportion], all_files[trainingProportion:]

    for file in all_files:
        individual_data = makeIndividualData(file,tags)

        if file in training:
            train_list_of_graphs.append(individual_data)
        elif file in testing:
            test_list_of_graphs.append(individual_data)

    train_data = torch_geometric.data.Batch.from_data_list(train_list_of_graphs)
    train_data.edge_attr = None
    test_data = torch_geometric.data.Batch.from_data_list(test_list_of_graphs)
    test_data.edge_attr = None
    return train_data,test_data


def makeIndividualData(file,tags):
    connect = Grapher(file)
    G, _, _ = connect.graph_formation()
    df = connect.relative_distance(file.width,file.height)
    individual_data = from_networkx(G)

    feature_cols = ['rd_b', 'rd_r', 'rd_t', 'rd_l', 'line_number', \
                    'n_upper', 'n_alpha', 'n_spaces', 'n_numeric', 'n_special']

    text_features = np.array(df["Object"].map(make_sent_bert_features).tolist()).astype(np.float32)
    numeric_features = df[feature_cols].values.astype(np.float32)

    features = np.concatenate((numeric_features, text_features), axis=1)
    features = torch.tensor(features)

    for col in df.columns:
        try:
            df[col] = df[col].str.strip()
        except AttributeError as e:
            pass

    df['Tag'] = df['Tag'].fillna('undefined')
    for i, tagValue in enumerate(tags):
        df.loc[df['Tag'] == tagValue, 'num_labels'] = i+1

    assert df[
               'num_labels'].isnull().values.any() == False, f'labeling error! Invalid label(s) present in {file}.csv, df:{df}'
    labels = torch.tensor(df['num_labels'].values.astype(int))
    text = df['Object'].values

    individual_data.x = features
    individual_data.y = labels
    individual_data.text = text
    individual_data.img_id = file.index
    print(f'File {file.index} --> Success')
    return individual_data

def getDataForUniquePrediction(json,tags):
    test_list_of_graphs = []
    documents = ConvertJsonToDocumentsObjects(json)[0]
    individual_data = makeIndividualData(documents, tags)
    test_list_of_graphs.append(individual_data)
    test_data = torch_geometric.data.Batch.from_data_list(test_list_of_graphs)
    test_data.edge_attr = None
    return test_data




