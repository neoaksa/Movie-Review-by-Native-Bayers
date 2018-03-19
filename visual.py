import pandas as pd
import matplotlib.pyplot as plt
import decimal as D


df =  pd.read_csv("/home/jie/Documents/aclImdb/pos_output.csv")
df = df.sort_values(by=["perc"],ascending=False)
print(df["word"],df["perc"])
plt.figure()
print(df["perc"].mean())
print(df["perc"].median())
print(df["perc"])
# plt.interactive(False)

# df = df[df["perc"] >0]
# df["perc"].plot.hist(alpha=0.5,bins=100)
# plt.show()

df =  pd.read_csv("/home/jie/Documents/aclImdb/neg_output.csv", converters={"perc":D.Decimal})
df = df.sort_values(by=["perc"],ascending=False)
print(df["word"],df["perc"])
# # plt.figure()
print(df["perc"].mean())
print(df["perc"].median())
# # plt.interactive(False)
# # df = df[df["perc"] >0]
# # df["perc"].plot.hist(alpha=0.5,bins=100)
# # plt.show()