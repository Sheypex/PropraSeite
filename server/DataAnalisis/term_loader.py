#!/usr/bin/env python

import pandas as pd
from datetime import datetime


def distance_between_dates(min_time, max_time):
    date_format = "%Y-%m-%d %H:%M:%S"
    a = datetime.strptime(min_time, date_format)
    b = datetime.strptime(max_time, date_format)
    delta = b - a
    days, seconds = delta.days, delta.seconds
    hours = days * 24 + seconds // 3600
    return hours


def get_first_last_date(column, last_date):  # determines the first/last item based on a column
    if last_date:
        counter = column.size - 1
        while pd.isnull(column[counter]):
            counter -= 1
        return column[counter]
    else:
        counter = 0
        while pd.isnull(column[counter]):
            counter += 1
        return column[counter]


def define_intervals(tweets):  # defines the distance between the first and last tweet
    max_time = get_first_last_date(tweets.Time, last_date=True)
    min_time = get_first_last_date(tweets.Time, last_date=False)
    return distance_between_dates(min_time, max_time)


def drop_rows(tweets):
    return tweets[['Tweet', 'Time']].copy()


def sort_by(value, tweets):  # sorts the tweets on a descending order
    return tweets.sort_values(value, ascending=False)


def build_json(tweets):  # based on the tweets collected it builds the data in json to be graphed later
    tweets['Time'] = pd.to_datetime(tweets.Time, format='%Y-%m-%d %H:%M:%S', errors='coerce')
    tweets = tweets.dropna(subset=['Time'])
    tweets = tweets.set_index('Time').resample('H')['Tweet'].count()
    return tweets


def load_term_file(path):  # loads the file, sorts it and builds a json
    tweets = pd.read_csv(path, sep=";", error_bad_lines=False)
    tweets = sort_by("Time", tweets)
    tweets = drop_rows(tweets)
    return build_json(tweets)


__author__ = 'Cesar Mauricio Acuna Herrera'
