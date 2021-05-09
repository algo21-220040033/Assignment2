import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

list=['BTC.csv', 'ETH.csv', 'LTC.csv', 'LINK.csv', 'BCH.csv', 'XLM.csv', 'AAVE.csv', 'EOS.csv', 'ATOM.csv',
        'XTZ.csv', 'DASH.csv', 'MKR.csv', 'SNX.csv', 'COMP.csv', 'ZEC.csv', 'ETC.csv', 'YFI.csv',
         'OMG.csv', 'UNI.csv']

df1 =pd.DataFrame()
fi = True

for file in list:
     if fi:
             df1=pd.read_csv(file)
             df1=df1[['open_time','close']]
             df1.rename(columns={'open_time':'date','close': file}, inplace=True)
             # df1=df1.set_index('date')
             fi=False
     else:
             df3=pd.read_csv(file)

             df1[file]=df3['close']
     # plt.plot((df1[file]-df1[file].mean())/df1[file].std(),color='grey')


df1['date']=pd.to_datetime(df1['date'])
df1=df1.set_index('date')
df1=df1.loc['2021-03-14 00:30:00':'2021-03-15 00:00:00']

### 画出btc价格走势
# plt.plot((df1['BTC.csv']-df1['BTC.csv'].mean())/df1['BTC.csv'].std(),color='r')
# plt.xlabel('Date')
# plt.ylabel('BTC price')
# plt.show()

#
# print(df1)

###计算fraction 即其他数字货币与比特币走势相同的比例
df1_ret=df1.pct_change(periods=1)
mask = df1_ret.isna()
df1_ret[mask] = np.nan

df1_ret.dropna(how='all', axis=0, inplace=True)
df1_ret_dir=df1_ret.copy()

for i in range(0,df1_ret.shape[0]):
    row=df1_ret.iloc[i]
    csi_sign=-1 if df1_ret.iloc[i][0]<0.0 else 1
    df1_ret_dir.iloc[i] =np.sign(row) == csi_sign

# print(df1_ret_dir)
fraction = df1_ret_dir.astype(int).sum(axis=1)/df1_ret_dir.shape[1]
df2=pd.DataFrame(fraction,columns=['fraction'])
# print(df1)
# plt.plot(fraction,color='orange')
# plt.show()
#


### 观察分析fraction与btc走势的相关性
fig,ax1=plt.subplots(1,1,figsize=(12,9))


ax1.plot((df1['BTC.csv']-df1['BTC.csv'][0])/df1['BTC.csv'][0],color='red',label='BTC_return')
ax1.grid()
ax1.set_ylabel('Return')
ax1.set_xlabel('Date and Time')
ax2 =ax1.twinx()
ax2.plot(fraction.rolling(10).mean(),color='orange',label='10-min rolling average ratio')
ax2.set_ylabel('fraction')
ax2.legend(loc=4)
ax2.legend(loc=3)
ax1.set_xlim(pd.to_datetime('2021-03-14 00:30'),pd.to_datetime('2021-03-15 00:00'))

fig.tight_layout()
plt.show()

