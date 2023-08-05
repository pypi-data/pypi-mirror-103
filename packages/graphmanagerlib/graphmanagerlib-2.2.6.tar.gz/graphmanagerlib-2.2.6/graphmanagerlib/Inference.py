import os
import shutil
import numpy as np
import torch

from graphmanagerlib.Graph import Grapher
from graphmanagerlib.Data_for_gcn import load_predictionData, getDataForUniquePrediction
from torch_geometric.utils.convert import from_networkx
from graphmanagerlib.JsonManager import ConvertJsonToDocumentsObjects

def clearOutputFolder(test_output_fd):
    shutil.rmtree(test_output_fd)
    if not os.path.exists(test_output_fd):
        os.mkdir(test_output_fd)


def make_info(document):
    connect = Grapher(document)
    G, _, _ = connect.graph_formation()
    df = connect.relative_distance(700,850)
    individual_data = from_networkx(G)
    return G, df, individual_data

def predictionsUnique(saved_model_folder,saved_prediction_dataset_folder,document_to_predict_json,labels_tab):
    getDataForUniquePrediction(document_to_predict_json,saved_prediction_dataset_folder)

    predictions_data = load_predictionData(save_fd=saved_prediction_dataset_folder)

    model = torch.load(os.path.join(saved_model_folder, "saved_model.pt"))

    y_preds = model.max(dim=1)[1].cpu().numpy()

    test_batch = predictions_data.batch.cpu().numpy()
    sample_indexes = np.where(test_batch == 0)[0]
    y_pred = y_preds[sample_indexes]

    print("Beginning of the prediction")

    """
    OBTENIR LE DOC EN DOC
    """
    document = ConvertJsonToDocumentsObjects(document_to_predict_json)[0]
    _, df, _ , _ = make_info(document)

    assert len(y_pred) == df.shape[0]

    predictions = []
    for row_index, row in df.iterrows():
        _y_pred = y_pred[row_index]
        _label = labels_tab[_y_pred]
        if _label != 'undefined':
            _text = row['Object']
            predictions.append({'Text': _text, 'Label': _label})

    return predictions

def load_predictionData(save_fd):
    predictions_data = torch.load(os.path.join(save_fd, 'predictions_data.dataset'))
    return predictions_data

if __name__ == "__main__":
    predictionsUnique()