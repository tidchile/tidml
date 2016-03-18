from abc import ABCMeta, abstractmethod


class ModelPersistor(object):
    """Abstract base class of algorithm classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self._params = params

    @property
    def params(self):
        return self._params

    @abstractmethod
    def save(self, model):
        """
        :param model: Model
        """

    @staticmethod
    def prepare_path(path):
        """
        :rtype: str
        """
        import os
        path = os.path.expanduser(path)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return path


class PickleModelPersistor(ModelPersistor):
    """Persist model using pickling."""

    def save(self, model):
        path = self._params['model.pickle']
        path = self.prepare_path(path)
        if hasattr(model, 'to_pickle'):
            # Support Pandas
            model.to_pickle(path)
        else:
            import pickle
            with open(path, 'w') as f:
                pickle.dump(model, f)
