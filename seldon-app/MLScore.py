"""
This module contains a class that conforms to the Seldon core interface
for ML model.
"""


class MLScore:
    """
    Model template. You can load your model parameters in __init__ from
    a location accessible at runtime
    """

    def __init__(self):
        """
        Load models and add any initialization parameters (these will
        be passed at runtime from the graph definition parameters
        defined in your seldondeployment kubernetes resource manifest).
        """
        print("Initializing")
        # This folder must have read/write permission
        # Check Dockerfile
        self.root_path = "/mnt/model"

    def predict(self, X, names=[], meta=[]):
        """
        Return a prediction.

        Parameters
        ----------
        X : array-like
        feature_names : array of feature names (optional)
        """
        print("Predict called - will run identity function")
        return X

    # def predict_raw(self, X, names=[], meta=[]):
    #     """
    #     If you don't want Seldon convert the input automatically to np.array
    #     then you can use this predict_raw function instead of predict function.
    #     """
    #     return X
