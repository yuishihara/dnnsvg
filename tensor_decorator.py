class TensorDecorator(object):
    def __init__(self):
        pass

    def __call__(self, tensor):
        return self.decorate(tensor)

    def decorate(self, tensor):
        pass
