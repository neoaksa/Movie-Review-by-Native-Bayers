import pandas as pd
import matplotlib.pyplot as plt


df =  pd.read_csv("/home/jie/Documents/aclImdb/pos_output.csv")
plt.figure()
print(df["perc"].mean())
print(df["perc"].median())
print(df["perc"])
plt.interactive(False)

df = df[df["perc"] >0]
df["perc"].plot.hist(alpha=0.5,bins=100)
plt.show()

df =  pd.read_csv("/home/jie/Documents/aclImdb/neg_output.csv")
plt.figure()
print(df["perc"].mean())
print(df["perc"].median())
plt.interactive(False)
df = df[df["perc"] >0]
df["perc"].plot.hist(alpha=0.5,bins=100)
plt.show()