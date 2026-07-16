#Bag Of Words
import pandas as pd
import numpy as np

df = pd.read_csv("spam.csv")
df['spam'] = df['Category'].apply(lambda x: 1 if x == 'spam' else 0)
print(df.head())
print(df. Category.value_counts())
#it is supposed to print the total number of email and at those emails, it is supposed to print the spam ones
