

class IDataset(object):
    def __init__(self):
        pass

    def train(self):
        raise RuntimeError("No implementation found!")

    def val(self):
        raise RuntimeError("No implementation found!")

    def test(self):
        raise RuntimeError("No implementation found!")
