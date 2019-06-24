import pandas as pd


def load_terms_topuser_file(path):  # loads the file, sorts it and builds a json
    """
    Loads the topuser file from the given path and returns the json version ordered from smallest to biggest
    """
    result = pd.read_csv(path, sep=";", error_bad_lines=False)
    result = result[['User', 'Count']].copy()
    result = result[::-1]
    #  print result.to_json(orient='values')
    return result


__author__ = 'Cesar Mauricio Acuna Herrera'
