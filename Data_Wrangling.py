#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:28:21 2024

@author: robertocardillo
"""

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

data_wdi = pd.read_excel('(2.2) WDI World Bank.xlsx', na_values='..')

data_group = pd.read_excel('(2.3) WDI Income Group.xlsx')

data_country = pd.read_excel('(2.4) WDI Country.xlsx')

data_wdi.info()
data_wdi['Country Name'].unique()
data_wdi['Series Name'].unique()
data_wdi['Topic'].unique()
       

data_wdi.rename(columns={'Country Name': 'country',
                        'Country Code': 'country_cod',
                        'Series Name': 'series',
                        'Series Code': 'series_cod',
                        '2021 [YR2021]': '2021',
                        'Topic': 'topic'},inplace= True)

data_wdi['country'].tail(n=20)

data_wdi = data_wdi.iloc[0:383572,]

data_wdi['country'].tail(n=20)

data_financial = data_wdi[data_wdi['topic'].str.startswith('Financial')]


data_financial = pd.pivot(data_financial,
                          index=['country', 'country_cod'],
                          columns=['series'],
                          values= '2021')

data_financial.reset_index(inplace=True)

data_country.rename(columns={'Country': 'country'}, inplace=True)

data_country.rename(columns={'Country': 'country_cod'}, inplace=True)

data_country.rename(columns={'country': 'country_cod'}, inplace=True)

data_financial = pd.merge(data_financial, data_country,
                          how= 'left',
                          on= 'country_cod')                          

data_financial = data_financial[~ data_financial['Name'].isna()].reset_index(drop=True)

data_financial.drop(columns=['Name'], inplace=True)

data_financial.dropna(axis=1, how='all', inplace= True)

data_group_select = data_group[['Code', 'Income Group']].copy()

data_group_select.rename(columns={'Code': 'country_cod'},inplace=True)

data_financial = pd.merge(data_financial, data_group_select,
                          how= 'left',
                          on= 'country_cod')

organize = data_financial.pop('Income Group')

data_financial.insert(2, 'Group', organize)

col_pos = data_financial.columns
data_financial.iloc[:,26].describe()

stat_group = data_financial.iloc[:,[2,26]].groupby('Group').mean().reset_index()

plt.figure(figsize=(15,9), dpi = 600)
ax = sns.barplot(data=stat_group, x=stat_group.iloc[:,0], y=stat_group.iloc[:,1])
for container in ax.containers: ax.bar_label(container, fmt='%.2f', padding=3, fontsize=12)
plt.xlabel('Group',fontsize=15)
plt.ylabel('Inflation Consumer Price (annual %)', fontsize=15)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()
