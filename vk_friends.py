import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


# just a bunch of pandas output tuning
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 200)

df = pd.read_csv('vk_friends.csv', sep=';', header=None)

### data cleaning / preprocessing
df.columns = ['uid', 'name', 'frndsnum', 'friends']
df['friends'] = df['friends'].str.split('|')
df = df[['name', 'friends']].explode('friends')
df['count'] = 1
df = df.groupby(['name', 'friends'], as_index=False).sum()
df = df[df['friends'] != 'DELETED']
df = df.sort_values(by='count', ascending=False)

print(df.reset_index(drop=True).head(20).rename(columns={'name': 'Имя человека', 'friends': 'Имя друга', 'count': 'Количество'}))

### variables
topfriendlover = 20
records = df.shape[0]

### list of top friend-lovers
bestfr = df[['name', 'count']].groupby('name', as_index=False).sum().sort_values(by='count', ascending=False)[:topfriendlover]['name'].to_list()
df = df[df['name'].isin(bestfr)]

# df = df[:pow(topfriendlover, 2)]
df = df.pivot('name', 'friends', 'count')
df = df.reindex(df.sum().sort_values(ascending=False).index, axis=1).iloc[:, :50]
df.fillna(0, inplace=True)
print(df.head(20))

plt.figure(figsize=(14, 6))
sns.heatmap(df, linewidths=0.5, linecolor='black', cbar_kws={'label': 'Кол-во случаев дружбы'})
plt.xlabel('Имя друга')
plt.ylabel('Имя человека')
plt.title('Heatmap дружбы в России (топ 20 дружелюбных человек, выборка %d пар друзей)' % records)
plt.tight_layout()
plt.savefig('friendship.jpg')
plt.show()