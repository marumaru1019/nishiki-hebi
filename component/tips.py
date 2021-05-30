from random import choice
import pandas


def get_tips():
    pd = pandas.read_csv('./tips.csv')
    return choice(pd.text)


if __name__ == '__main__':

    print(get_tips())
