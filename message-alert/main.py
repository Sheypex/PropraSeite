import sys
from DataAnalisis.term_loader import load_term_file
from DataAnalisis.terms_counted_loader import load_terms_counted_file
from DataAnalisis.term_top_users_loader import load_terms_topuser_file


def load_variables():
    """
    Loads the passed arguments.
    argument 1: the search term, for example Trump or FakeNews
    argument 2: action type. Example -> 1: GET, 2: POST (not yet implemented. Use should be for new search)
    """
    arg1 = str(sys.argv[1])  # defines the term to be passed to a function
    arg2 = str(sys.argv[2])  # defines what function should be used
    return arg1, arg2


def is_in_database():  # TODO: check with the database if the search term is valid
    if search in tweets_available:
        return True
    else:
        return False


def get_tweets():  # loads the tweets
    if is_in_database():
        term_result = load_term_file("/Users/mauri/Desktop/ProPra/" + search + ".csv")  # result = JSON_Object containing pair of JSON_Objects
        term_counted_result = load_terms_counted_file("/Users/mauri/Desktop/ProPra/" + search + "TermsCounted.csv")  # result = JSON_Array containing JSON_Arrays
        term_topuser_result = load_terms_topuser_file("/Users/mauri/Desktop/ProPra/" + search + "TopUserTwoColumns.csv")  # result = JSON_Array containing JSON_Arrays
        result = "{\"result\":{\"term\":"+term_result+",\"counted\":"+term_counted_result+",\"topuser\":"+term_topuser_result+"}}"
        return result
    return {"error": "unable to retrieve data from the search term: "+search}


def start_loading_tweets():  # creates a new job to collect data about the searched word
    return {"load_tweets": "still undefined action..."+search_type}  # TODO: logic for dinamic search of tweets. Should be triggered by a POST function coming from the user


def unkown_action():
    return {"error": "unkown action... "+search_type}


def define_action():  # defines the action: 1. get_tweets 2. load_tweets
    if search_type == "1":
        return get_tweets()
    elif search_type == "2":
        return start_loading_tweets()  # TODO: define more functions and load posibilities
    else:
        return unkown_action()


search, search_type = load_variables()  # type: (str, str)
tweets_available = ["Trump", "Klimawandel","FakeNews"]
result = define_action()

print(str(result))  # this print is the one who is responsible for sending the json results back to the node server
sys.stdout.flush()

__author__ = 'Cesar Mauricio Acuna Herrera'
