import pickle
import pandas
import glob
from collections import OrderedDict as od
import re

files = glob.glob("coeffs/production/*.pkl")

coeffMap = od()

for f in files:
  with open(f,"r") as fpkl: data = pickle.load(fpkl)
  cols = data.columns
  # Iterate over rows and fill dataframe
  for ir,r in data.iterrows():
    coeffMap[r['proc']] = od()
    for col in cols:
      if col == "proc": continue
      # Uncertainties
      if col[0] == "u":
        p = "_".join(col.split("_")[1:])
        # If val is zero then continue
        if abs(r[p]) < 1e-6: continue
        # Linear terms
        if len(p.split("_")) == 1: coeffMap[r['proc']]['u_A_%s'%p] = r[col]
        # Quadratic terms
        else: coeffMap[r['proc']]['u_B_%s'%p] = r[col]          
      # Values
      else:
        if abs(r[col]) < 1e-6: continue
        # Linear terms
        if len(col.split("_")) == 1: coeffMap[r['proc']]['A_%s'%col] = r[col]
        # Quadratic terms
        else: coeffMap[r['proc']]['B_%s'%col] = r[col]

procs = coeffMap.keys()
for proc in procs:
  if "qqH" in proc: 
    coeffMap[re.sub("qqH","WH_had",proc)] = coeffMap[proc]
    coeffMap[re.sub("qqH","ZH_had",proc)] = coeffMap[proc]
  elif "ZH_lep" in proc:
    coeffMap[re.sub("ZH_lep","ggZH_lep",proc)] = coeffMap[proc]

# Write to json file
with open("xs_coeffs.json","w") as fout:
  fout.write("{\n")
  for k,v in coeffMap.iteritems():
    if k == "unknown": continue
    fout.write("  \"%s\":{\n"%k)
    for ip,p in enumerate(v.keys()):
      if ip == (len(v.keys())-1): fout.write("    \"%s\":%.10f\n"%(p,v[p]))
      else: fout.write("    \"%s\":%.10f,\n"%(p,v[p]))
    fout.write("  },\n")
  fout.write("}")
  

