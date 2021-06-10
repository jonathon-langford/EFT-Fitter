from collections import OrderedDict as od

allParams = ['cg', 'cw', 'ch', 'chbox', 'chdd', 'chg', 'chw', 'chb', 'chwb', 'cehre', 'cuhre', 'cdhre', 'cewre', 'cebre', 'cugre', 'cuwre', 'cubre', 'cdgre', 'cdwre', 'cdbre', 'chl1', 'chl3', 'che', 'chq1', 'chq3', 'chu', 'chd', 'chudre', 'cll', 'cll1', 'cqq1', 'cqq11', 'cqq3', 'cqq31', 'clq1', 'clq3', 'cee', 'cuu', 'cuu1', 'cdd', 'cdd1', 'ceu', 'ced', 'cud1', 'cud8', 'cle', 'clu', 'cld', 'cqe', 'cqu1', 'cqu8', 'cqd1', 'cqd8', 'cledqre', 'cquqd1re', 'cquqd11re', 'cquqd8re', 'cquqd81re', 'clequ1re', 'clequ3re', 'cgtil', 'cwtil', 'chgtil', 'chwtil', 'chbtil', 'chwbtil', 'cewim', 'cebim', 'cugim', 'cuwim', 'cubim', 'cdgim', 'cdwim', 'cdbim', 'chudim', 'cehim', 'cuhim', 'cdhim', 'cledqim', 'cquqd1im', 'cquqd8im', 'cquqd11im', 'cquqd81im', 'clequ1im', 'clequ3im']

SMEFTParamers = ['cg', 'cw', 'ch', 'chbox', 'chdd', 'chg', 'chw', 'chb', 'chwb', 'cehre', 'cuhre', 'cdhre', 'cewre', 'cebre', 'cugre', 'cuwre', 'cubre', 'cdgre', 'cdwre', 'cdbre', 'chl1', 'chl3', 'che', 'chq1', 'chq3', 'chu', 'chd', 'chudre', 'cll', 'cll1', 'cqq1', 'cqq11', 'cqq3', 'cqq31', 'clq1', 'clq3', 'cee', 'cuu', 'cuu1', 'cdd', 'cdd1', 'ceu', 'ced', 'cud1', 'cud8', 'cle', 'clu', 'cld', 'cqe', 'cqu1', 'cqu8', 'cqd1', 'cqd8', 'cledqre', 'cquqd1re', 'cquqd11re', 'cquqd8re', 'cquqd81re', 'clequ1re', 'clequ3re']

SMEFTCPVParams = ['cgtil', 'cwtil', 'chgtil', 'chwtil', 'chbtil', 'chwbtil', 'cewim', 'cebim', 'cugim', 'cuwim', 'cubim', 'cdgim', 'cdwim', 'cdbim', 'chudim', 'cehim', 'cuhim', 'cdhim', 'cledqim', 'cquqd1im', 'cquqd8im', 'cquqd11im', 'cquqd81im', 'clequ1im', 'clequ3im']

CParams = ['cg', 'ch', 'chbox', 'chdd', 'chg', 'chw', 'chb', 'chwb', 'cehre', 'cuhre', 'cdhre', 'cewre', 'cebre', 'cugre', 'cuwre', 'cubre', 'cdgre', 'cdwre', 'cdbre', 'chl1', 'chl3', 'che', 'chq1', 'chq3', 'chu', 'chd', 'chudre', 'cll1', 'cqq1', 'cqq11', 'cqq3', 'cqq31', 'clq1', 'clq3', 'cee', 'cuu', 'cuu1', 'cdd1', 'ced', 'cud1', 'cud8', 'cle', 'cqu1', 'cqu8', 'cqd1', 'cqd8']

FParams = ['chg','chb','chwb','chw','chq3','cugre','chu','cdhre','cqq31','cg','cuu1','chq1','cqq11','chd','chl3','cqu8','cll1','chl1','chbox','cud8','che','cqd8','cehre','cuhre','cqq3']

ProfileTest = ['chw','chb','chwb']

adjustRanges = od()
adjustRanges['chg'] = [-0.01,0.01]
adjustRanges['chq3'] = [-0.05,0.05]
#adjustRanges['chw'] = [-0.05,0.05]
adjustRanges['chw'] = [-1,1]
#adjustRanges['chb'] = [-0.05,0.05]
adjustRanges['chb'] = [-1,1]
#adjustRanges['chwb'] = [-0.05,0.05]
adjustRanges['chwb'] = [-1,1]


pois = od()

#for cp in CParams:
#for cp in FParams:
for cp in ProfileTest:
  pois[cp] = {
    "factor":1,
    "multiplier":1,
    "range":[-1,1],
    "title":cp,
    "nominal":0
  }
  if cp in adjustRanges:
    pois[cp]['range'] = adjustRanges[cp]
