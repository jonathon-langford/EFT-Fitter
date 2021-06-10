from collections import OrderedDict as od
import json
import numpy as np

params = ['mu_XS_simVBF_lowmjj_highpthjj_BR_ZZ', 'mu_XS_VBF_highMJJ_PTHGT200_BR_gamgam', 'mu_XS_ggH_PTH_GT200_BR_ZZ', 'mu_XS_ttH_PTH_120_200_BR_gamgam', 'mu_XS_ggH_0J_PTH_0_10_BR_gamgam', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_tautau', 'mu_XS_ttH_PTH_0_60_BR_ZZ', 'mu_XS_VBF_MJJ_120_350_BR_tautau', 'mu_XS_WH_lep_PTV_GT150_BR_gamgam', 'mu_XS_ttH_PTH_200_300_BR_bb', 'mu_XS_WH_lep_PTV_GT150_BR_WW', 'mu_XS_totZH_lep_PTV_75_150_BR_bb', 'mu_XS_WH_lep_PTV_75_150_BR_gamgam', 'mu_XS_ttH_PTH_0_60_BR_tautau', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_ZZ', 'mu_XS_ttH_PTH_120_200_BR_bb', 'mu_XS_ggH_1J_PTH_0_60_BR_tautau', 'mu_XS_ttH_PTH_GT300_BR_WW', 'mu_XS_ggH_1J_PTH_60_120_BR_tautau', 'mu_XS_WH_lep_PTV_75_150_BR_WW', 'mu_XS_WH_lep_PTV_150_250_0J_BR_tautau', 'mu_XS_totZH_lep_PTV_0_75_BR_tautau', 'mu_XS_simVBF_lowmjj_BR_WW', 'mu_XS_simVBF_lowmjj_highpthjj_BR_tautau', 'mu_XS_VBF_MJJ_60_120_BR_WW', 'mu_XS_totZH_lep_PTV_0_75_BR_gamgam', 'mu_XS_ttH_PTH_0_60_BR_gamgam', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_gamgam', 'mu_XS_ggH_PTH_GT450_BR_gamgam', 'mu_XS_ttH_PTH_60_120_BR_bb', 'mu_XS_VBF_rest_BR_ZZ', 'mu_XS_ggH_0J_PTH_0_10_BR_ZZ', 'mu_XS_WH_lep_PTV_75_150_BR_tautau', 'mu_XS_totZH_lep_PTV_GT150_BR_WW', 'mu_XS_ttH_PTH_200_300_BR_ZZ', 'mu_XS_VBF_MJJ_60_120_BR_ZZ', 'mu_XS_ggH_1J_PTH_60_120_BR_WW', 'mu_XS_totZH_lep_PTV_75_150_BR_WW', 'mu_XS_ggH_PTH_200_300_BR_tautau', 'mu_XS_ttH_PTH_120_200_BR_ZZ', 'mu_XS_totZH_lep_PTV_75_150_BR_gamgam', 'mu_XS_VBF_MJJ_60_120_BR_tautau', 'mu_XS_simVBF_lowmjj_lowpthjj_BR_ZZ', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_tautau', 'mu_XS_WH_lep_PTV_75_150_BR_bb', 'mu_XS_totZH_lep_PTV_GT75_BR_tautau', 'mu_XS_simVBF_highmjj_BR_WW', 'mu_XS_simVBF_lowmjj_lowpthjj_BR_gamgam', 'mu_XS_ttH_PTH_60_120_BR_WW', 'mu_XS_WH_lep_PTV_GT75_BR_ZZ', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_WW', 'mu_XS_ggH_1J_PTH_0_60_BR_WW', 'mu_XS_simVBF_highmjj_highpthjj_BR_tautau', 'mu_XS_VBF_MJJ_0_60_BR_tautau', 'mu_XS_ggH_1J_PTH_120_200_BR_ZZ', 'mu_XS_totZH_lep_PTV_150_250_GE1J_BR_bb', 'mu_XS_VBF_MJJ_60_120_BR_gamgam', 'mu_XS_ggH_0J_PTH_GT10_BR_ZZ', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_ZZ', 'mu_XS_totZH_lep_PTV_0_75_BR_WW', 'mu_XS_ggH_0J_PTH_0_10_BR_tautau', 'mu_XS_simVBF_lowmjj_highpthjj_BR_gamgam', 'mu_XS_WH_lep_PTV_0_75_BR_tautau', 'mu_XS_VBF_MJJ_120_350_BR_WW', 'mu_XS_ggH_1J_PTH_120_200_BR_WW', 'mu_XS_VBF_highMJJ_PTHGT200_BR_WW', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_60_120_BR_ZZ', 'mu_XS_ttH_PTH_GT300_BR_ZZ', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_gamgam', 'mu_XS_simVBF_highmjj_highpthjj_BR_gamgam', 'mu_XS_ggH_PTH_200_300_BR_gamgam', 'mu_XS_simVBF_highmjj_highpthjj_BR_ZZ', 'mu_XS_simVBF_highmjj_lowpthjj_BR_tautau', 'mu_XS_ggH_0J_PTH_0_10_BR_WW', 'mu_XS_ttH_PTH_60_120_BR_gamgam', 'mu_XS_simVBF_lowmjj_lowpthjj_BR_tautau', 'mu_XS_WH_lep_PTV_0_75_BR_ZZ', 'mu_XS_ggH_1J_PTH_0_60_BR_ZZ', 'mu_XS_ggH_1J_PTH_60_120_BR_gamgam', 'mu_XS_ttH_PTH_60_120_BR_tautau', 'mu_XS_ttH_PTH_200_300_BR_gamgam', 'mu_XS_VBF_highMJJ_PTHGT200_BR_tautau', 'mu_XS_ggH_1J_PTH_120_200_BR_tautau', 'mu_XS_ggH_PTH_200_300_BR_WW', 'mu_XS_WH_lep_PTV_150_250_0J_BR_bb', 'mu_XS_ttH_PTH_200_300_BR_tautau', 'mu_XS_ggH_PTH_300_450_BR_gamgam', 'mu_XS_WH_lep_PTV_GT250_BR_bb', 'mu_XS_ttH_PTH_GT300_BR_gamgam', 'mu_XS_totZH_lep_PTV_150_250_0J_BR_bb', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_tautau', 'mu_XS_ggH_PTH_GT300_BR_WW', 'mu_XS_ggH_1J_PTH_0_60_BR_gamgam', 'mu_XS_WH_lep_PTV_0_75_BR_gamgam', 'mu_XS_ttH_PTH_60_120_BR_ZZ', 'mu_XS_ttH_PTH_120_200_BR_tautau', 'mu_XS_VBF_MJJ_0_60_BR_WW', 'mu_XS_WH_lep_PTV_150_250_GE1J_BR_bb', 'mu_XS_ttH_PTH_0_60_BR_bb', 'mu_XS_ggH_0J_PTH_GT10_BR_WW', 'mu_XS_ttH_PTH_GT300_BR_bb', 'mu_XS_WH_lep_PTV_0_75_BR_WW', 'mu_XS_WH_lep_PTV_GT250_BR_tautau', 'mu_XS_totZH_lep_PTV_GT150_BR_gamgam', 'mu_XS_ggH_1J_PTH_60_120_BR_ZZ', 'mu_XS_VBF_LT2J_BR_WW', 'mu_XS_totZH_lep_PTV_GT250_BR_bb', 'mu_XS_ttH_PTH_GT300_BR_tautau', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_120_200_BR_WW', 'mu_XS_WH_lep_PTV_150_250_GE1J_BR_tautau', 'mu_XS_ttH_PTH_120_200_BR_WW', 'mu_XS_ggH_0J_PTH_GT10_BR_tautau', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_gamgam', 'mu_XS_ggH_1J_PTH_120_200_BR_gamgam', 'mu_XS_simVBF_highmjj_lowpthjj_BR_ZZ', 'mu_XS_ggH_PTH_300_450_BR_tautau', 'mu_XS_ggH_GE2J_MJJ_0_350_PTH_0_60_BR_WW', 'mu_XS_simVBF_highmjj_lowpthjj_BR_gamgam', 'mu_XS_ttH_PTH_0_60_BR_WW', 'mu_XS_ggH_PTH_GT450_BR_tautau', 'mu_XS_ggH_0J_PTH_GT10_BR_gamgam', 'mu_XS_ttH_PTH_200_300_BR_WW']

# Json file storing Aj, Bjk coefficients
with open("functions/SMEFT/xs_coeffs.json","r") as fj: xs_coeffs = json.load(fj)

with open("functions/SMEFT/dec_coeffs.json","r") as fj: dec_coeffs = json.load(fj)

#pois = {}

# Json file storing merged bin definitions
with open("functions/SMEFT/stxs_stage1p2_merge.json","r") as fj: merges = json.load(fj)
# Load STXS cross sections: reweight functions by SM cross section in merging
with open("functions/SMEFT/XS.json","r") as fj: XSMap = json.load(fj)

# Save A matrix
def makeA(_poinames,_coeffs,_x):
  npois = len(_poinames)
  A = np.zeros(npois)
  for i,ip in enumerate(_poinames):
    if "A_%s"%ip in _coeffs[_x]: A[i] = _coeffs[_x]["A_%s"%ip]
  return A

# Save B matrix
def makeB(_poinames,_coeffs,_x):
  npois = len(_poinames)
  B = np.zeros((npois,npois))
  for i,ip in enumerate(_poinames):
    for j,jp in enumerate(_poinames):
      # Squared terms
      if j == i:
        if "B_%s_2"%ip in _coeffs[_x]: B[i][j] = _coeffs[_x]["B_%s_2"%ip]
      # Cross terms
      elif j>i:
        if "B_%s_%s"%(ip,jp) in _coeffs[_x]: B[i][j] = _coeffs[_x]["B_%s_%s"%(ip,jp)]
        elif "B_%s_%s"%(jp,ip) in _coeffs[_x]: B[i][j] = _coeffs[_x]["B_%s_%s"%(jp,ip)]
  return B

# Matrix calculation
def MU(_pois,_A,_B,_linearOnly=False):
  pvec = np.array(list(_pois.values()))
  pvecT = pvec.T
  if _linearOnly: return 1+_A.dot(pvec)  
  else: return 1+_A.dot(pvec)+pvecT.dot(_B.dot(pvec))

def MU_rot(_rpois,_R,_A,_B,_linearOnly=False):
  rpvec = np.array(list(_rpois.values()))
  rpvecT = rpvec.T
  _RT = _R.T
  if _linearOnly: return 1+_A.dot(_R.dot(rpvec))
  else: return 1+_A.dot(_R.dot(rpvec))+rpvecT.dot(_RT.dot(_B.dot(_R.dot(rpvec))))


def GRAD(_pois,_param,_A,_B,_linearOnly=False):
  pvec = np.array(list(_pois.values()))
  pvecT = pvec.T
  # Identity vector: pick out gradient for _param
  Ivec = np.array(list(_pois.keys()))==_param
  IvecT = Ivec.T
  if _linearOnly: return _A.dot(Ivec)
  else: return _A.dot(Ivec)+IvecT.dot(_B.dot(pvec))+pvecT.dot(_B.dot(Ivec))

def GRAD_rot(_rpois,_param,_R,_A,_B,_linearOnly=False):
  rpvec = np.array(list(_rpois.values()))
  rpvecT = rpvec.T
  Ivec = np.array(list(_rpois.keys()))==_param
  IvecT = Ivec.T
  _RT = _R.T
  if _linearOnly: return _A.dot(_R.dot(Ivec))
  else: return _A.dot(_R.dot(Ivec))+IvecT.dot(_RT.dot(_B.dot(_R.dot(rpvec))))+rpvecT.dot(_RT.dot(_B.dot(_R.dot(Ivec))))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Directory to store EFT functions
class functionDirectory:
  def __init__(self,name): 
    self.name = name
    self.ADir = od()
    self.BDir = od()

  def clearMatrices(self):
    self.ADir = od()
    self.BDir = od()

  # For decay channel scaling
  def createDecayFunction(self,d):
    # First check if already created function
    if hasattr(self,"dec_%s"%d): return getattr(self,"dec_%s"%d)

    # Otherwise create function
    def dec_function(pois,rpois=None,rmatrix=None,linearonly=False):
      # Nominal poi names
      cnames = pois.keys()
      Nc = len(cnames)
      A,B = None,None
      # If already created load row vector of A terms
      if d in self.ADir: A = self.ADir[d]
      # Else create...
      else: 
        A = makeA(cnames,dec_coeffs,d)
        self.ADir[d] = A

      # Load matrix of B terms (squared on diagonal, cross terms on 1/2 off-diagonal)
      if not linearonly: 
        if d in self.BDir: B = self.BDir[d]
        # Else create
        else:
          B = makeB(cnames,dec_coeffs,d)
          self.BDir[d] = B

      # Matrix calculation
      if( rpois is None ): mu = MU(pois,A,B,linearonly)
      else: mu = MU_rot(rpois,rmatrix,A,B,linearonly)
      return mu

    # Add decay scaling as attribute in case other inputs share same name
    setattr(self,"dec_%s"%d,dec_function)
    return dec_function

  # For decay channel scaling gradient
  def createDecayGradient(self,d):
    # First check if already created gradient
    if hasattr(self,"dec_grad_%s"%d): return getattr(self,"dec_grad_%s"%d)

    # Otherwise create function
    def dec_grad(pois,param,rpois=None,rmatrix=None,linearonly=False):
      # Nominal poi names
      cnames = pois.keys()
      Nc = len(cnames)
      A,B = None,None
      # If already created load row vector of A terms
      if d in self.ADir: A = self.ADir[d]
      # Else create...
      else: 
        A = makeA(cnames,dec_coeffs,d)
        self.ADir[d] = A

      # Load matrix of B terms (squared on diagonal, cross terms on 1/2 off-diagonal)
      if not linearonly: 
        if d in self.BDir: B = self.BDir[d]
        # Else create
        else:
          B = makeB(cnames,dec_coeffs,d)
          self.BDir[d] = B

      # Matrix calculation
      if( rpois is None ): grad = GRAD(pois,param,A,B,linearonly)
      else: grad = GRAD_rot(rpois,param,rmatrix,A,B,linearonly)
      return grad

    # Add decay scaling as attribute in case other inputs share same name
    setattr(self,"dec_grad_%s"%d,dec_grad)
    return dec_grad


  # For production cross section bin scaling
  def createXSFunction(self,p):
    # First check if already created function
    if hasattr(self,"xs_%s"%p): return getattr(self,"xs_%s"%p)

    # Otherwise create function
    def xs_function(pois,rpois=None,rmatrix=None,linearonly=False):
      cnames = pois.keys()
      Nc = len(cnames)
      A,B = None,None
      # Load matrix of A coefficients
      if p in self.ADir: 
        A = self.ADir[p]
      else:
        # Save matrix of A coefficients
        # If merged bin: loop over bins (nominal STXS bins) and add equations with relative fraction
        if p in merges:
          A = np.zeros(Nc)  
          # Loop over merged bins
          mbins = merges[p]
          xs_tot = 0
          for mb in mbins:
            xs_tot += XSMap[mb]
            a = makeA(cnames,xs_coeffs,mb)
            A += XSMap[mb]*a
          # Divide through by total xs
          if xs_tot != 0: A = A/xs_tot
          else: 
            print(" --> [ERROR] Total cross section for merged bin is zero")
            sys.exit(1)
          self.ADir[p] = A
        # Otherwise        
        else:
          A = makeA(cnames,xs_coeffs,p)
          self.ADir[p] = A
          
      # Load matrix of B terms (squared on diagonal, cross terms on 1/2 off-diagonal)
      if not linearonly:
        if p in self.BDir: 
          B = self.BDir[p]
        else:
          # For merged bin
          if p in merges:
            B = np.zeros((Nc,Nc))
            # Loop over merged bins
            mbins = merges[p]
            xs_tot = 0
            for mb in mbins:
              xs_tot += XSMap[mb]
              b = makeB(cnames,xs_coeffs,mb)
              B += XSMap[mb]*b
            # Divide through by total xs
            if xs_tot != 0: B = B/xs_tot
            else:
              print(" --> [ERROR] Total cross section for merged bin is zero")
              sys.exit(1)
            self.BDir[p] = B
          # Otherwise
          else:
            B = makeB(cnames,xs_coeffs,p)
            self.BDir[p] = B

      # Matrix calculation
      if( rpois is None ): mu = MU(pois,A,B,linearonly)
      else: mu = MU_rot(rpois,rmatrix,A,B,linearonly)
      return mu

    # Add xs scaling as attribute in case other inputs share same name
    setattr(self,"xs_%s"%p,xs_function)
    return xs_function

  # For production cross section bin scaling gradient
  def createXSGradient(self,p):
    # First check if already created function
    if hasattr(self,"xs_grad_%s"%p): return getattr(self,"xs_grad_%s"%p)

    # Otherwise create function
    def xs_grad(pois,param,rpois=None,rmatrix=None,linearonly=False):
      cnames = pois.keys()
      Nc = len(cnames)
      A,B = None,None
      # Load matrix of A coefficients
      if p in self.ADir: 
        A = self.ADir[p]
      else:
        # Save matrix of A coefficients
        # If merged bin: loop over bins (nominal STXS bins) and add equations with relative fraction
        if p in merges:
          A = np.zeros(Nc)  
          # Loop over merged bins
          mbins = merges[p]
          xs_tot = 0
          for mb in mbins:
            xs_tot += XSMap[mb]
            a = makeA(cnames,xs_coeffs,mb)
            A += XSMap[mb]*a
          # Divide through by total xs
          if xs_tot != 0: A = A/xs_tot
          else: 
            print(" --> [ERROR] Total cross section for merged bin is zero")
            sys.exit(1)
          self.ADir[p] = A
        # Otherwise        
        else:
          A = makeA(cnames,xs_coeffs,p)
          self.ADir[p] = A
          
      # Load matrix of B terms (squared on diagonal, cross terms on 1/2 off-diagonal)
      if not linearonly:
        if p in self.BDir: 
          B = self.BDir[p]
        else:
          # For merged bin
          if p in merges:
            B = np.zeros((Nc,Nc))
            # Loop over merged bins
            mbins = merges[p]
            xs_tot = 0
            for mb in mbins:
              xs_tot += XSMap[mb]
              b = makeB(cnames,xs_coeffs,mb)
              B += XSMap[mb]*b
            # Divide through by total xs
            if xs_tot != 0: B = B/xs_tot
            else:
              print(" --> [ERROR] Total cross section for merged bin is zero")
              sys.exit(1)
            self.BDir[p] = B
          # Otherwise
          else:
            B = makeB(cnames,xs_coeffs,p)
            self.BDir[p] = B

      # Matrix calculation
      if( rpois is None ): grad = GRAD(pois,param,A,B,linearonly)
      else: grad = GRAD_rot(rpois,param,rmatrix,A,B,linearonly)
      return grad

    # Add xs gradient as attribute in case other inputs share same name
    setattr(self,"xs_grad_%s"%p,xs_grad)
    return xs_grad

  def EFTFunction(self,XS,GAMMA,TOT):
    def eft_function(pois,RPOIS=None,RMATRIX=None,LINEARONLY=False):
      return XS(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)*(GAMMA(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)/TOT(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY))
    return eft_function

  def EFTGradient(self,XS,XSP,GAMMA,GAMMAP,TOT,TOTP):
    def eft_grad(pois,param,RPOIS=None,RMATRIX=None,LINEARONLY=False):
      # Complicated quotient rule equation
      return ((XS(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)*GAMMAP(pois,param,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)+XSP(pois,param,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)*GAMMA(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY))/TOT(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY))+((XS(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)*(GAMMA(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)/TOT(pois,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY)))*TOTP(pois,param,rpois=RPOIS,rmatrix=RMATRIX,linearonly=LINEARONLY))
    return eft_grad

  def addFunction(self,name):
    # Extract production and decay channel
    prod = name.split("_BR_")[0].split("_XS_")[-1]
    dec = name.split("_BR_")[-1]
    # Create production scaling
    xs = self.createXSFunction(prod)
    # Create decay scaling
    gamma = self.createDecayFunction(dec)
    tot = self.createDecayFunction('tot')
    # Create total scaling
    x = self.EFTFunction(xs,gamma,tot)
    setattr(self,name,x)

  def addGradient(self,name):
    # Extract production and decay channel
    prod = name.split("_BR_")[0].split("_XS_")[-1]
    dec = name.split("_BR_")[-1]
    # Create production scaling and gradient
    xs = self.createXSFunction(prod)
    xsgrad = self.createXSGradient(prod)
    # Create decay scaling and gradients
    gamma = self.createDecayFunction(dec)
    gammagrad = self.createDecayGradient(dec)
    tot = self.createDecayFunction('tot')
    totgrad = self.createDecayGradient('tot')
    # Create total gradient
    v = self.EFTGradient(xs,xsgrad,gamma,gammagrad,tot,totgrad)
    setattr(self,"%s_grad"%name,v)

  def getfunction(self,name):
    return getattr(self,name)

  def getgrad(self,name):
    return getattr(self,"%s_grad"%name)


# Create function directory, with scaling functions for each input parameter
myfuncs = functionDirectory("SMEFT_summer21")
for p in params: 
  myfuncs.addFunction(p)

# Add gradients
for p in params:
  myfuncs.addGradient(p)

functions = od()
grad_functions = od()
for p in params: 
  functions[p] = myfuncs.getfunction(p)
  grad_functions[p] = myfuncs.getgrad(p)
