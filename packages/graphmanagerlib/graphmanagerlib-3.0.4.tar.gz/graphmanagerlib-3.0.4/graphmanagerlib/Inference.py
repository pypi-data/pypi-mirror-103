import os
import numpy as np
import torch

from graphmanagerlib.Graph import Grapher
from graphmanagerlib.Data_for_gcn import getDataForUniquePrediction
from torch_geometric.utils.convert import from_networkx
from graphmanagerlib.JsonManager import ConvertJsonToDocumentsObjects,ConvertPredictionToJson


def make_info(document):
    connect = Grapher(document)
    G, _, _ = connect.graph_formation()
    df = connect.relative_distance(document.width, document.height)
    individual_data = from_networkx(G)
    return G, df, individual_data

def predictionsUnique(saved_model_folder,json,labels_tab):
    predictions_data = getDataForUniquePrediction(json,labels_tab)

    model = torch.load(os.path.join(saved_model_folder, "saved_model.pt"))

    y_preds = model(predictions_data).max(dim=1)[1].cpu().numpy()

    test_batch = predictions_data.batch.cpu().numpy()
    sample_indexes = np.where(test_batch == 0)[0]
    y_pred = y_preds[sample_indexes]

    print("Beginning of the prediction")

    """
    OBTENIR LE DOC EN DOC
    """
    document = ConvertJsonToDocumentsObjects(json)[0]
    _, df, _ = make_info(document)

    assert len(y_pred) == df.shape[0]

    predictions = []
    for row_index, row in df.iterrows():
        _y_pred = y_pred[row_index]
        _label = labels_tab[_y_pred]
        if _label != 'undefined':
            _text = row['Object']
            xmin, ymin, xmax, ymax = row[['xmin', 'ymin', 'xmax', 'ymax']]
            predictions.append({'Text': _text,
                                'Label': _label,
                                'XMin': xmin,
                                'YMin': ymin,
                                'XMax': xmax,
                                'YMax': ymax
                                })

    return ConvertPredictionToJson(predictions)

if __name__ == "__main__":
    predictionsUnique()