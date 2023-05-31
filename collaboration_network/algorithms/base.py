class Algorithm:
    def __init__(self, name=None):
        if name is None:
            self.name = self.default_name 
        else:
            self.name = name

    @property
    def default_name(self):
        raise NotImplementedError