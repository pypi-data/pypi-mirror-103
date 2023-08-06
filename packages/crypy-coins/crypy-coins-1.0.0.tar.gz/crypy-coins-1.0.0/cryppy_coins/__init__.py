# import request and json for use API
import requests
import json

# url start
basic_api_url = 'https://api.coincap.io/v2'


# function for get data of a request
def return_data(end_url='/assets'):
    data = requests.get(f'{basic_api_url}{end_url}')

    return json.loads(data.text)


# get the 100 more expensive crypto-moneys in order of rank
def get_top_list():
    data = return_data()
    rank = []

    for crypto in data['data']:
        rank.append(crypto['id'])

    return rank


# get the name of a money by the rank
def get_money_by_rank(rank=1):
    return get_top_list()[rank - 1]


# get the rank of a money
def get_rank_by_money(money='bitcoin'):
    try:
        return get_top_list().index(money) + 1
    except:
        return 'not existing'

# get the info of a money
def get_money_info(money_name='bitcoin'):

    return return_data(f'/assets/{money_name}')

# get the history of money, with interval (m1, m5, m15, m30 / h1, h2, h6, h12 / d1 ; m = month, h = hour, d = day)
def get_history(money='bitcoin', interval='d1'):
    dictionary = {money: return_data(f'/assets/{money}/history?interval={interval}')}

    return dictionary

# get markets of a money
def get_markets(money='bitcoin'):

    dictionary = {money: return_data(f'/assets/{money}/markets')}

    return dictionary

# get rates of a money or off all the moneys
def get_rates(money=None):

    if money is None:
        return return_data('/rates')
    else:
        return return_data(f'/rates/{money}')

# get get_exchanges of a money or off all the moneys
def get_exchanges(money=None):

    if money is None:
        return return_data('/exchanges')
    else:
        return return_data(f'/exchanges/{money}')


print(get_markets('bitcoin'))
