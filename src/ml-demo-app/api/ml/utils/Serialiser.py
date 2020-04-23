import json
import collections
import numpy as np
import scipy.sparse

"""
Extension of serialisation/deserialisation tools found in this source:
http://robotfantastic.org/serializing-python-data-to-json-some-edge-cases.html

"""

def isnamedtuple(obj):
    """Heuristic check if an object is a namedtuple."""
    return isinstance(obj, tuple) \
        and hasattr(obj, "_fields") \
        and hasattr(obj, "_asdict") \
        and callable(obj._asdict)

"""
Function for JSON serialisation of machine learning models and transformers for persistence
"""
        
def serialize(data):

    """
    Args:
        data (dict): The parameters and properties of a machine learning model or transformer
                     in the form of a dictionary
                     - Obtained through using .__dict__ function

    Returns:
        (dict): A dictionary/JSON encoded version of the value that is passed into the function
                E.g: a Numpy ndarray type value passed in will be serialised into a dictionary
                     containing the values of the ndarray in the form of a list, with the
                     original ndarray datatype appended as another property in the dictionary
    """


    if data is None or isinstance(data, (bool, int, float, str)):
        return data
    if isinstance(data, list):
        return [serialize(val) for val in data]
    if isinstance(data, collections.OrderedDict):
        return {"py/collections.OrderedDict":
                [[serialize(k), serialize(v)] for k, v in data.iteritems()]}
    if isnamedtuple(data):
        return {"py/collections.namedtuple": {
            "type":   type(data).__name__,
            "fields": list(data._fields),
            "values": [serialize(getattr(data, f)) for f in data._fields]}}
    if isinstance(data, dict):
        if all(isinstance(k, str) for k in data):
            return {k: serialize(v) for k, v in data.items()}
        return {"py/dict": [[serialize(k), serialize(v)] for k, v in data.items()]}
    if isinstance(data, tuple):
        return {"py/tuple": [serialize(val) for val in data]}
    if isinstance(data, set):
        return {"py/set": [serialize(val) for val in data]}
    
    """
    Extension of serialize() function to cater for numpy.ndarray & scipy.csr.matrix data types
    Allows for the serialising of SVM and KNearestNeighbours scikit-learn classifier models
    """
    if isinstance(data, np.ndarray):
        return {"py/numpy.ndarray": {
            "values": data.tolist(),
            "dtype":  str(data.dtype)}}
    if isinstance(data, scipy.sparse.csr.csr_matrix):
        data = data.toarray()
        return {"py/scipy.csr_matrix": {
            "values": data.tolist(),
            "dtype":  str(data.dtype)}}
    if isinstance(data, OneHotEncoder):
        return
    raise TypeError("Type %s not data-serializable" % type(data))
    

"""
Function for returning the values of a JSON serialised model/transformer as their real
data types
"""
def restore(dct):

    """
    Args:
        data (dict/JSON): The JSON representation of the serialised model or transformer

    Returns:
        (dtype): The values of a model/transformer property/attribute in their real data types
    """


    if "py/dict" in dct:
        return dict(dct["py/dict"])
    if "py/tuple" in dct:
        return tuple(dct["py/tuple"])
    if "py/set" in dct:
        return set(dct["py/set"])
    if "py/collections.namedtuple" in dct:
        data = dct["py/collections.namedtuple"]
        return namedtuple(data["type"], data["fields"])(*data["values"])
    if "py/numpy.ndarray" in dct:
        data = dct["py/numpy.ndarray"]
        return np.array(data["values"], dtype=data["dtype"])
    if "py/collections.OrderedDict" in dct:
        return OrderedDict(dct["py/collections.OrderedDict"])
    if "py/scipy.csr_matrix" in dct:
        data = dct["py/scipy.csr_matrix"]
        arr =  np.array(data["values"], dtype=data["dtype"])
        return scipy.sparse.csr_matrix(arr)
    if "py/sklearn.preprocessing._encoders.OneHotEncoder" in dct:
        attr = dct["py/sklearn.preprocessing._encoders.OneHotEncoder"]
        return deserialize(SVC(), attr)
    return dct
    
"""
Function for saving the data of a model/transformer as a serialised JSON file
"""
def data_to_json(data, location):
    """
    Args:
        data (dict): The __dict__ value of a model/transformer's attributes
        location (str): The location of the resulting JSON file

    Returns:
        (dict/JSON): The fully serialised JSON of the model/transformer
    """
    attr_json = serialize(data)
    with open(location, "w") as write_file:
        json.dump(attr_json, write_file)
    return json.dumps(attr_json, indent=4)

def json_to_data(s, file):
    with open(file, "r") as read_file:
        attr_data = json.load(read_file, object_hook=restore)
        return attr_data

"""
Function for setting the attributes of a passed in model/transformer with values
from the json_to_data() function
"""
def deserialize(estim, attr):
    """
    Args:
        estim (dtype): The default initialised model/transformer object
                       E.g: SVC()
        attr (dict): Key-value dictionary returned from the json_to_data() function 

    Returns:
        estim(dtype): The fully reinitialised model/transformer object
    """
    for k, v in attr.items():
        setattr(estim, k, v)
    return estim