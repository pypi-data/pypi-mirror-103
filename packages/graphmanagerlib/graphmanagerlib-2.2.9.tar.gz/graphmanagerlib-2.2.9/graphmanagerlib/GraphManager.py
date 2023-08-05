from graphmanagerlib.Data_for_gcn import get_data, load_train_test_split
from graphmanagerlib.Model_formation import CreateTrainAndSaveGCN
from graphmanagerlib.Inference import predictionsUnique


class GraphManager:
    def CreateTrainAndSaveGCN(self,documents, save_dataset_fd,nb_classes):
        get_data(documents=documents, save_dataset_fd=save_dataset_fd)
        traindata, testdata = load_train_test_split(save_dataset_fd)
        CreateTrainAndSaveGCN(traindata, testdata,save_dataset_fd, nb_classes)
        print("===== Modèle entrainé et sauvegardé =====")

    def single_prediction(self, saved_model_folder, saved_prediction_dataset_folder, document_to_predict_json, labels_tab):
        return predictionsUnique(saved_model_folder, saved_prediction_dataset_folder, document_to_predict_json, labels_tab)
