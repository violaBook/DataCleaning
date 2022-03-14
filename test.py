import pandas as pd

csv_data = pd.read_pickle('new_data.pkl')
print(csv_data)
# csv_data['start_time'] = csv_data['start_time'].astype('object')
# csv_data['end_time'] = csv_data['end_time'].astype('object')
# print(csv_data.dtypes)
# print(csv_data)
# csv_data.to_pickle('new_data.pkl')