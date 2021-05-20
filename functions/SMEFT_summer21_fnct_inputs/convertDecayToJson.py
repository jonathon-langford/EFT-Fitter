import pickle
import pandas
import glob
from collections import OrderedDict as od
import re

f = "coeffs/decay/all.pkl"

coeffMap = od()

with open(f,"r") as fpkl: data = pickle.load(fpkl)
cols = data.columns
# Iterate over rows and fill dataframe
for ir,r in data.iterrows():
  coeffMap[r['channel']] = od()
  for col in cols:
    if(col == "channel")|(col=="gamma"): continue
    # Uncertainties
    if col[0] == "u":
      p = "_".join(col.split("_")[1:])
      # If val is zero then continue
      if abs(r[p]) < 1e-6: continue
      # Linear terms
      if len(p.split("_")) == 1: coeffMap[r['channel']]['u_A_%s'%p] = r[col]
      # Quadratic terms
      else: coeffMap[r['channel']]['u_B_%s'%p] = r[col]          
    # Values
    else:
      if abs(r[col]) < 1e-6: continue
      # Linear terms
      if len(col.split("_")) == 1: coeffMap[r['channel']]['A_%s'%col] = r[col]
      # Quadratic terms
      else: coeffMap[r['channel']]['B_%s'%col] = r[col]

# Extract total width
gamma_tot = data['gamma'].sum()
coeffMap['tot'] = od()
for col in cols:
  if(col == "channel")|(col=="gamma"): continue
  # Uncertainties
  if col[0] == "u":
    p = "_".join(col.split("_")[1:])
    # Linear terms
    if len(p.split("_")) == 1: 
      if abs((data[p]*(data['gamma']/gamma_tot)).sum()) < 1e-6: continue
      coeffMap['tot']['u_A_%s'%p] = ((data[col]*data[col]*(data['gamma']/gamma_tot)).sum())**0.5
    # Quadratic terms
    else: 
      if abs((data[p]*(data['gamma']/gamma_tot)).sum()) < 1e-6: continue
      coeffMap['tot']['u_B_%s'%p] = ((data[col]*data[col]*(data['gamma']/gamma_tot)).sum())**0.5
  # Values
  else:
    if abs((data[col]*(data['gamma']/gamma_tot)).sum()) < 1e-6: continue
    # Linear terms
    if len(col.split("_")) == 1: coeffMap['tot']['A_%s'%col] = (data[col]*(data['gamma']/gamma_tot)).sum()
    # Quadratic terms
    else: coeffMap['tot']['B_%s'%col] = (data[col]*(data['gamma']/gamma_tot)).sum()
      
# Channel name mapping
channelNameMap = od()
channelNameMap['H_4l'] = 'ZZ'
channelNameMap['H_aa'] = 'gamgam'
channelNameMap['H_lvlv'] = 'WW'
channelNameMap['H_bb'] = 'bb'
channelNameMap['H_tautau'] = 'tautau'
channelNameMap['tot'] = 'tot'

# Write to json file
with open("dec_coeffs.json","w") as fout:
  fout.write("{\n")
  for k,v in coeffMap.iteritems():
    if k not in channelNameMap: continue
    knew = channelNameMap[k]
    fout.write("  \"%s\":{\n"%knew)
    for ip,p in enumerate(v.keys()):
      if ip == (len(v.keys())-1): fout.write("    \"%s\":%.10f\n"%(p,v[p]))
      else: fout.write("    \"%s\":%.10f,\n"%(p,v[p]))
    fout.write("  },\n")
  fout.write("}")
  

