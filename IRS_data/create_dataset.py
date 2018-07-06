import pandas as pd 
import numpy as np 



def run(df_path, zip_file):

	zip_list = get_philly_zips(zip_file)
	df = pivot_data(clean_data(pd.read_csv(df_path)))
	philly_df = filter_philly_zips(df,zip_list)
	print philly_df.info()

def get_philly_zips(zip_file):
	#zip_file = 'zip_codes.txt'
	#read_zips = open(zip_file, 'r')
	#zip_list = [line.rstrip('\n') for line in read_zips.readlines()] 
	with open(zip_file,'r') as read_zips:
		zip_list = [line.rstrip('\n') for line in read_zips.readlines()] 
	return zip_list

def clean_data(df):
	df = df.drop([0,1])
	df = df.rename(columns={'ZIP\ncode [1]': "zip_code"})
	df = df.dropna(how='all')
	values = {'Size of adjusted gross income': 'Total', 'Number of returns':0}
	df = df.fillna(value = values)
	df['Number of returns'] = df['Number of returns'].str.replace(',', '')
	df['Number of returns'] = df['Number of returns'].str.replace('*', '')
	df['Number of returns'] = df['Number of returns'].str.replace(' ', '')
	df['Number of returns'] = df['Number of returns'].astype(float)
	df = df.reset_index(drop=True)
	return df

def pivot_data(df):
	pivot = pd.pivot_table(df, values='Number of returns', index='zip_code', columns = 'Size of adjusted gross income').reset_index()
	return pivot 

def filter_philly_zips(df,zips):
	philly_df = df[df['zip_code'].isin(zips)]
	return philly_df

if __name__ == "__main__":
	run('~/torbanr/Documents/RE/data/irs_data/pa_2015_total_number_returns.csv', 'zip_codes.txt')
	

