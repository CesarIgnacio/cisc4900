import pandas as pd

df=pd.read_csv('ML_2022-03-13T00-44_monpar_photo.csv')

newdf=df.fillna(value='NA')

print(newdf.head)

newdf.to_csv('Monkparakees_NA.csv')