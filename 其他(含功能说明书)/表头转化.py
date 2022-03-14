import pandas as pd

pickle_data = pd.read_pickle('t_data.pkl')
print(pickle_data)
pickle_data.columns = ['xForce', 'yForce', 'zForce', 'xVibration', 'yVibration', 'zVibration', 'aeRMS']
print(pickle_data)
pickle_data.to_pickle('t_data.pkl')