import json
from collections import OrderedDict as od

# Best fit values and uncertainties
with open("prefit_asimov.json","r") as jf: data = json.load(jf)

f = open("prefit_asimov.py","w")
f.write("from collections import OrderedDict as od\n\n")
f.write("name = \"hcomb_stxsbr_prefit_asimov\"\n\n")
f.write("# Bestfit + uncertainties\n")
f.write("X = od()\n")


for p, pInfo in data['STXSStage1p2XSBR'].iteritems():
  pname = p
  bf = 1.
  up01sigma = pInfo['ErrorHi']
  down01sigma = pInfo['ErrorLo']
  validup01sigma = pInfo['ValidErrorHi']
  validdown01sigma = pInfo['ValidErrorHi']
  f.write("X[\"%s\"] = {\"bestfit\":%.2f, \"Up01Sigma\":%.2f, \"Down01Sigma\":%.2f, \"Up01SigmaExp\":%.2f, \"Down01SigmaExp\":%.2f, \"validUp01Sigma\":%g, \"validDown01Sigma\":%g, \"merged\":False}\n"%(pname,bf,up01sigma,abs(down01sigma),up01sigma,abs(down01sigma),validup01sigma,validdown01sigma))

# Correlatuions
corrDict = od()
with open("correlations_stage12_xsbr.json","r") as jf: corrdata = json.load(jf)
f.write("\n# Correlations\n")
f.write("rho = od()\n")
for p, qcorr in corrdata.iteritems():
  for q, corr in qcorr.iteritems():
    if p==q: continue
    if (p,q) in corrDict: continue
    elif (q,p) in corrDict: continue
    else:
      corrDict[(p,q)] = corr

for k,v in corrDict.iteritems():
  if abs(v) < 0.005: continue #f.write("rho[(\"%s\"),(\"%s\")] = 0.\n"%(k[0],k[1]))
  f.write("rho[(\"%s\"),(\"%s\")] = %.3f\n"%(k[0],k[1],v))

f.close()
