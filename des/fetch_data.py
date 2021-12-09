import json
import investpy
import pandas as pd
from datetime import date

def fetch_bitcoin(from_date='01/01/2009', to_date='17/9/2022'):
	bit = investpy.get_crypto_historical_data(crypto='bitcoin', from_date=from_date, to_date=to_date).reset_index()
	return bit


def fetch_ada(from_date='01/01/2014', to_date='17/9/2021'):
	cardano = investpy.get_crypto_historical_data(crypto='cardano',	from_date=from_date,to_date=to_date).reset_index()
	return cardano


def fetch_ether(from_date='01/01/2014', to_date='17/9/2021'):
	eth = investpy.get_crypto_historical_data(crypto='ethereum', from_date=from_date, to_date=to_date).reset_index() 
	return eth


if __name__=='__main__':
	bit = fetch_bitcoin(to_date=date.today().strftime('%d/%m/%Y'))
	eth = fetch_ether()
	ada = fetch_ada()
	bit.to_json('../data/historical_bit_{}_{}.json'.format( min(bit['Date']).date(), max(bit['Date']).date()))
	eth.to_json('../data/historical_eth_{}_{}.json'.format(min(eth['Date']).date(), max(eth['Date']).date()))
	ada.to_json('../data/historical_ada_{}_{}.json'.format(min(ada['Date']).date(), max(ada['Date']).date()))
