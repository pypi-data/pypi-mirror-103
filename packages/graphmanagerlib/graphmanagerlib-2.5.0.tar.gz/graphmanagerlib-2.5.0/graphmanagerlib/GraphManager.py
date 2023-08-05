from graphmanagerlib.Data_for_gcn import get_data
from graphmanagerlib.Model_formation import CreateTrainAndSaveGCN
from graphmanagerlib.Inference import predictionsUnique


class GraphManager:
    def CreateTrainAndSaveGCN(self,documents,saved_folder, nb_classes):
        traindata, testdata= get_data(documents=documents)
        CreateTrainAndSaveGCN(traindata, testdata,saved_folder, nb_classes)
        print("===== Modèle entrainé et sauvegardé =====")

    def single_prediction(self, saved_model_folder, document_to_predict_json, labels_tab):
        return predictionsUnique(saved_model_folder, document_to_predict_json, labels_tab)
