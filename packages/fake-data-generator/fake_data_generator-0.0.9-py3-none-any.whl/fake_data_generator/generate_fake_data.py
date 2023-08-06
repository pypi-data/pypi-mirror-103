


import pandas as pd
import numpy as np
from faker.providers.person.en import Provider
import sys
from random import randint
import random

loops = 1
size = 1000
file_path = 'dummy_data.csv'


def random_names(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)
	
def random_genders(size, p=None):
    """Generate n-length ndarray of genders."""
    if not p:
        # default probabilities
        p = (0.48, 0.50, 0.02)
    gender = ("M", "F", "U")
    return np.random.choice(gender, size=size, p=p)
	
def random_dates(start, end, size):
    """
    Generate random dates within range between start and end.    
    Source: https://stackoverflow.com/a/50668285
    """
    # Unix timestamp is in nanoseconds by default, so divide it by
    # 24*60*60*10**9 to convert to days.
    divide_by = 24 * 60 * 60 * 10**9
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")
	
def random_yearly_salary(x, y, size):
	return random.sample(range(x, y), size)

#try:
#	size = sys.argv[1]
#	file_path = sys.argv[2]
#	loops = sys.argv[3]
#except IndexError:
#	print("""Arguments expected as : [ number_of_rows, output_file_path, number_Column_loops ]
#Using default values for arguments not provided""")
	
def generate_data(loops=loops, size=size, file_path=file_path):	
	column_list = []

	for i in range(int(loops)):
		columns = ['First_Name' + '_' + str(i), 'Last_Name' + '_' + str(i), 'Gender' + '_' + str(i), 'Birthdate' + '_' + str(i),'salary' + '_' + str(i)]
		column_list.extend(columns)

	df = pd.DataFrame(columns=column_list)

	for i in range(int(loops)):
		df['First_Name' + '_' + str(i)] = random_names('first_names', int(size))
		df['Last_Name' + '_' + str(i)] = random_names('last_names', int(size)) 
		df['Gender' + '_' + str(i)] = random_genders(int(size))
		df['Birthdate' + '_' + str(i)] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2008-01-01'), size=int(size))
		df['salary' + '_' + str(i)] = random_yearly_salary(10000, 150000,int(size))

	df.to_csv(file_path, index = False)

if __name__ == "__main__":
	generate_data(loops, size, file_path)
	



