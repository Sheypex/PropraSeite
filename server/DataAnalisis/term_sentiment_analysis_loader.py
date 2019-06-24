import pandas as pd


def load_terms_sentiment_file(path):
    # read csv into python
    result = pd.read_csv(path, sep=";", error_bad_lines=False)
    result = result[['Term', 'Sentiment', 'Time', 'Tweet_ID']].copy()

    # group by tweet id
    group = result.groupby('Tweet_ID')

    # create list to store dict elements
    result_list = []

    # loop through sentiments
    for sen in group["Sentiment"]:
        my_dict = {"Tweet_ID": '', "Sentiment": '', 'Time': ""}
        Tweet_ID = sen[0]
        sentiment_status = sen[1]

        positive = 0
        count = 0
        # Calculate Score
        for elem in sentiment_status:
            if elem == 'POSITIVE':
                count += 1
                positive += 1
            else:
                positive += 1

        # Score = [0 - 1] -> 1:totally Positive | 0:totally Negative
        score = count / positive

        line = result[result.Tweet_ID == Tweet_ID]
        time = line["Time"].iloc[0]

        # adding elements to dict
        my_dict.update({"Time": time})
        my_dict.update({'Tweet_ID': Tweet_ID})
        my_dict.update({'Sentiment': score})
        # appending dict to list
        result_list.append(my_dict)
    return result_list


__author__ = 'Sammy'
