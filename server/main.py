#! python3
import sys
from DataAnalisis import term_loader
from DataAnalisis import terms_counted_loader
from DataAnalisis import term_top_users_loader
from DataAnalisis import term_sentiment_analysis_loader
from Utilities import message_sender
import logging


def load_variables():
    """
    Loads the passed arguments from the server.
    argument 1: the search term, for example Trump or FakeNews
    argument 2: action type. Example -> 1: GET, 2: GET (send message)
    argument 3: files path
    """
    arg1 = str(sys.argv[1])  # defines the TERM to be passed to a function
    arg2 = str(sys.argv[2])  # defines what FUNCTION should be used (1,2)
    arg3 = str(sys.argv[3])  # defines the path where the files are located
    arg4 = ''                # defines the EMAIL to be send the data
    try:
        arg4 = str(sys.argv[4])
    except Exception:
        logging.warning("no email passed on arguments... exception ignored")

    return arg1, arg2, arg3, arg4


def is_in_database():  # TODO: check with the database if the search term is valid
    if search in tweets_available:
        return True
    else:
        return False


def get_data():
    """
    loads the data from the respective files and return a pre processed result
    :return: adds the data to a single String line in json format
    """
    try:
        term_result = term_loader.load_term_file(path + search + ".csv").to_json()  # result = JSON_Object containing pair of JSON_Objects
    except Exception:
        logging.warning("unable to load the term.csv file...")
        term_result = "\"no_data\""

    try:
        term_counted_result = terms_counted_loader.load_terms_counted_file(path + search + "TermsCounted.csv").to_json(orient='values')  # result = JSON_Array containing JSON_Arrays
    except Exception:
        logging.warning("unable to load the termsCounted.csv file...")
        terms_counted_result = "\"no_data\""

    try:
        term_topuser_result = term_top_users_loader.load_terms_topuser_file(path + search + "TopUser.csv").to_json(orient='values')  # result = JSON_Array containing JSON_Arrays
    except Exception:
        logging.warning("unable to load the termTopUser.csv file...")
        term_topuser_result = "\"no_data\""

    try:
        term_sentiment_result = "["+",".join(map(str, term_sentiment_analysis_loader.load_terms_sentiment_file(path + search + "Sentiments.csv")))+"]"
    except Exception:
        logging.warning("unable to load the termSentiments.csv file...")
        term_sentiment_result = "\"no_data\""

    json_result = "{\"result\":{\"term\":"+term_result+",\"counted\":"+term_counted_result+",\"topuser\":"+term_topuser_result+",\"sentiment\":"+term_sentiment_result+"}}"
    json_result = json_result.replace("\'", "\"")
    logging.warning("result: "+json_result)
    return json_result


def get_tweets():  # loads the tweets
    if is_in_database():
        return get_data()
    return {"error": "unable to retrieve data from the search term: "+search}


def send_message():
    """
    sends an email with a resume of the information obtained
    :return: 1 if it was succesfull to send the email. Otherwise 0
    """
    if is_in_database():
        try:
            term_result = term_loader.load_term_file(
                path + search + ".csv")  # result = JSON_Object containing pair of JSON_Objects
        except Exception:
            term_result = ""

        try:
            term_counted_result = terms_counted_loader.load_terms_counted_file(path + search + "TermsCounted.csv")  # result = JSON_Array containing JSON_Arrays
        except Exception:
            term_counted_result = ""

        try:
            term_topuser_result = term_top_users_loader.load_terms_topuser_file(path + search + "TopUser.csv")  # result = JSON_Array containing JSON_Arrays
        except Exception:
            term_topuser_result = ""

        try:
            term_sentiment_result = term_sentiment_analysis_loader.load_terms_sentiment_file(path + search + "Sentiments.csv")
        except Exception:
            term_sentiment_result = ""

        logging.info('starting to send message')
        message_sender.send_mail("Automatic message: Twitter Alert System Summary for #"+search, email,
                  term_result, term_topuser_result, term_sentiment_result, term_counted_result, search)
        logging.info('Finished sending message')
        return 1
    return 2


def unkown_action():  # error message if the action type wasnt defined
    logging.warning("unkown action..."+search_type)
    return {"error": "unkown action... "+search_type}


def define_action():
    """
    defines the action: 1. get_tweets 2. send message
    :return: based on the action type returns all the tweets (1) or return 1/0 and sends an email (2)
    """
    logging.info("search type: "+search_type)
    if search_type == "1":
        try:
            return get_tweets()
        except Exception:
            logging.exception("couldnt get the tweets data... some error ocurred:")
            return ""
    elif search_type == "2":
        try:
            return send_message()
        except Exception:
            logging.exception("couldnt send_message... some error ocurred: ")
            return 0
    else:
        return unkown_action()


logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
search, search_type, path, email = load_variables()  # type: (str, str, str, str)
logging.warning("loading variables... ", search, search_type, path)
tweets_available = ["Trump", "Klimawandel", "FakeNews"]  # TODO: replace with a database check
result = define_action()

print(str(result))  # this print is the one who is responsible for sending the json results back to the node server
sys.stdout.flush()

#  example input: python main.py Trump 2 ./Data/ message.alert.system@gmail.com
#  example input: python main.py Trump 1 ./Data/

__author__ = 'Cesar Mauricio Acuna Herrera'
