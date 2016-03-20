from abc import ABCMeta, abstractmethod
from tidml.utils import Parameterized, prepare_path


class ModelPersistor(Parameterized):
    """Abstract base class of algorithm classes."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, model):
        """
        :param model: Model
        """

    @abstractmethod
    def load(self):
        """

        :return: Model
        """


class PickleModelPersistor(ModelPersistor):
    """Persist model using pickling."""

    def save(self, model):
        path = self.params['model.pickle']
        path = prepare_path(path)
        if hasattr(model, 'to_pickle'):
            # Support Pandas
            model.to_pickle(path)
        else:
            with open(path, 'w') as f:
                import pickle
                pickle.dump(model, f)

    def load(self):
        path = self.params['model.pickle']
        path = prepare_path(path)
        with open(path, 'r') as f:
            import pickle
            return pickle.load(f)
