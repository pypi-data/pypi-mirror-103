import csv
from graphmanagerlib.Data_for_gcn import get_data
from graphmanagerlib.Model_formation import CreateTrainAndSaveGCN
from graphmanagerlib.Inference import predictionsUnique


class GraphManager:
    def CreateTrainAndSaveGCN(self,documents,saved_folder, tagsPath):
        tags = self._getTagsList(tagsPath)
        traindata, testdata = get_data(documents=documents, tags=tags)
        return CreateTrainAndSaveGCN(traindata, testdata,saved_folder, len(tags))

    def _getTagsList(self, tagsPath):
        tags = []
        with open(tagsPath, newline='') as inputfile:
            for row in csv.reader(inputfile):
                tags.append(row[0])
        return tags

    def single_prediction(self, saved_model_folder, document_to_predict_json, tagsPath):
        tags = self._getTagsList(tagsPath)
        return predictionsUnique(saved_model_folder, document_to_predict_json, tags)
