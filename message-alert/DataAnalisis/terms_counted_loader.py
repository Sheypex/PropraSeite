import pandas as pd


def load_terms_counted_file(path):  # loads the file, sorts it and builds a json
    """
    Loads the counted file from the given path and returns the json version ordered from smallest to biggest
    """
    result = pd.read_csv(path, sep=";", error_bad_lines=False)
    result = result[['Term', 'Anzahl']].copy()
    result = result[::-1]
    return result.to_json(orient='values')


json = load_terms_counted_file('/Users/mauri/Desktop/ProPra/TrumpTermsCounted.csv')
# print json

__author__ = 'Cesar Mauricio Acuna Herrera'

