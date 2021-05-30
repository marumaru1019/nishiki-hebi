from random import choice
import pandas


def get_tips():
    pd = pandas.read_csv('./tips.csv')
    return choice(pd.text)

