# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 09:33:38 2021

@author: ASUS
"""

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

base = importr('base')

packageNames = ('afex', 'emmeans')
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)

packnames_to_install = [x for x in packageNames if not rpackages.isinstalled(x)]

if len(packnames_to_install) > 0:
    utils.install_packages(StrVector(packnames_to_install))
    
data = robjects.r('read.table(file =' \
       '"http://personality-project.org/r/datasets/R.appendix3.data", header = T)')

data.head()


afex = rpackages.importr('afex') 
model = afex.aov_ez('Subject', 'Recall', data, within='Valence')
print(model)