#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 11:47:57 2021

@author: saikat
"""

import urllib.request
import pandas as pd
urllib.request.urlretrieve('https://data.dgl.ai/tutorial/dataset/members.csv', './members.csv')
urllib.request.urlretrieve('https://data.dgl.ai/tutorial/dataset/interactions.csv', './interactions.csv')

members = pd.read_csv('./members.csv')
members.head()

interactions = pd.read_csv('./interactions.csv')
interactions.head()