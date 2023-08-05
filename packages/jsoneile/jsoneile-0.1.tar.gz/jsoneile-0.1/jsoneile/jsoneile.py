from json import *

def load_jsonl(fp, **kwargs):
    '''
    Load a JSONL file

    Inputs:
        - fp (io): a .read()-supporting text file or binary file containing a JSON document
        - **kwargs: to be passed to json.loads
    Output:
        (list) a list of objects
    '''
    data = [loads(x, **kwargs) for x in fp.readlines()]
    return data

def loads_jsonl(s, **kwargs):
    '''
    Load a JSONL string

    Inputs:
        - s (str): A string that contains newline-delimited (\n) JSON formatted strings
        - **kwargs: to be passed to json.loads
    Output:
        (list) a list of objects
    '''
    return [loads(x, **kwargs) for x in s.split('\n')]

def dump_jsonl(data, fp, **kwargs):
    '''
    Serialize list of objects in data to a single string to fp

    Inputs:
        - data (list): A list of JSON-serializable objects
        - fp (io) a .write()-supporting file-like object
        - **kwargs: to be passed to json.dump
    Output:
        None
    '''
    try:
        iter(data)
    except:
        raise TypeError("data should be an iterable of JSON serializable objects")
    fp.writelines(dumps(x, **kwargs)+'\n' for x in data)

def dumps_jsonl(data, **kwargs):
    '''
    Serialize list of objects in data to a single string of newline-delimited JSON formatted strings

    Inputs:
        - data (list): A list of JSON-serializable objects
        - **kwargs: to be passed to json.dumps
    Output:
        (str) a list of objects
    '''
    try:
        iter(data)
    except:
        raise TypeError("data should be an iterable of JSON serializable objects")
    return "\n".join(dumps(x, **kwargs) for x in data)