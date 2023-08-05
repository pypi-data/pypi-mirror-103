class Document:
    def __init__(self, index, width, height, nodes):
        self.index = str(index).zfill(3)
        self.width = width
        self.height = height
        self.nodes = nodes
