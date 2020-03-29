import json
import collections
import numpy as np
import scipy

class Serialiser():
    def __init__(self):
        super().__init__()

    def isnamedtuple(obj):
        """Heuristic check if an object is a namedtuple."""
        return isinstance(obj, tuple) \
            and hasattr(obj, "_fields") \
            and hasattr(obj, "_asdict") \
            and callable(obj._asdict)
            
    """
    Extension of serialisation/deserialisation tools found in this source:
    http://robotfantastic.org/serializing-python-data-to-json-some-edge-cases.html
    Added in functionalitiy for catering for numpy ndarray dtypes and iterating through dicts differently
    """
    def serialize(data):
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
        
        
    def restore(dct):
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
            return sparse.csr_matrix(arr)
        if "py/sklearn.preprocessing._encoders.OneHotEncoder" in dct:
            attr = dct["py/sklearn.preprocessing._encoders.OneHotEncoder"]
            return deserialize(SVC(), attr)
        return dct
        
    def data_to_json(data, location):
        attr_json = serialize(data)
        with open(location, "w") as write_file:
            json.dump(attr_json, write_file)
        return json.dumps(attr_json, indent=4)

    def json_to_data(s, file):
        with open(file, "r") as read_file:
            attr_data = json.load(read_file, object_hook=restore)
            return attr_data

    def deserialize(estim, attr):
        for k, v in attr.items():
            setattr(estim, k, v)
        return estim