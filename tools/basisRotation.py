import numpy as np
import array
from scipy import linalg
import sys
from collections import OrderedDict as od

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to extract production term
def extractProdTerm(prod,poi,coeffs,merges,xsmap):
  # If merged bin
  if prod in merges:
    mbins = merges[prod]
    A = 0
    xs_tot = 0
    for mb in mbins:
      xs_tot += xsmap[mb]
      # Add linear term
      if "A_%s"%poi in coeffs[mb]: A += xsmap[mb]*coeffs[mb]["A_%s"%poi]
    # Divide through by total xs
    A = A/xs_tot
  # If not merged bin
  else: 
    A = coeffs[prod]["A_%s"%poi] if "A_%s"%poi in coeffs[prod] else 0.
  return A

# Function to extract decay term: partial-total
def extractDecayTerm(dec,poi,coeffs):
  A_partial = coeffs[dec]["A_%s"%poi] if "A_%s"%poi in coeffs[dec] else 0.
  A_tot = coeffs['tot']["A_%s"%poi] if "A_%s"%poi in coeffs['tot'] else 0.
  A = A_partial-A_tot
  return A
 
# Function to extract P matrix from linearised model
def extractPMatrix(FIT):
  # Assuming single input for now. FIXME: Add functionality for multiple inputs (sum Vinv as diag blocks)
  assert( len(FIT.INPUTS) == 1 )
  P = []
  # Loop over input measurements
  for i in range(FIT.INPUTS[0].nbins):
    p = []
    _x = FIT.INPUTS[0].XList[i]
    # Extract production and decay name from x
    _prod, _dec = _x.split("_BR_")[0].split("_XS_")[-1], _x.split("_BR_")[-1]
    # Loop over pois
    for j in range(len(FIT.P0)):
      _poi = FIT.PList[j]
      A_prod = extractProdTerm(_prod,_poi,FIT.xs_coeffs,FIT.merges,FIT.XSMap)
      A_dec = extractDecayTerm(_dec,_poi,FIT.dec_coeffs)
      p.append(A_prod+A_dec)
    P.append(p)
  return np.array(P)
      

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to perform basis rotation
def basis_rotation(FIT,rmatrix=None):
  # If no rotation matrix is specified then calculate:
  if rmatrix is None:
    # Assuming single input for now. FIXME: Add functionality for multiple inputs (sum Vinv as diag blocks)
    assert( len(FIT.INPUTS) == 1 )

    # Extract P matrix based on linearised model
    P = FIT.PMATRIX
    PT = P.T

    # Extract Hessian
    # Approach 1: expected covariance matrix
    Vinv = FIT.INPUTS[0].Vinv
    # Approach 2: numerical calculation of Hessian (at bestfit point?) # TODO

    # Calculate fisher matrix for linearised model
    FIT.FISHERMATRIX = PT.dot(Vinv.dot(P))

    # Eigenvector decomposition of fisher matrix
    FIT.EIGVALS, FIT.EIGVECS = linalg.eig(FIT.FISHERMATRIX)

    # Check: does this always work
    FIT.RMATRIX = linalg.inv(FIT.EIGVECS)


  # Rotate according to use input rotation matrix
  else:
    FIT.RMATRIX = linalg.inv(rmatrix)

  # Prepare rotated pois
  FIT.rPOIS = od()
  FIT.rPList = []
  FIT.rP0 = []
  FIT.rPBounds = []
  FIT.rPDefinitions = {}
  FIT.rPEigenvalues = []
  for i in range(len(FIT.EIGVECS)):
    FIT.rPOIS["c%g"%(i+1)] = {}
    FIT.rPOIS["c%g"%(i+1)]['factor'] = 1.
    FIT.rPOIS["c%g"%(i+1)]['multiplier'] = 1.
    FIT.rPList.append("c%g"%(i+1))
    FIT.rPEigenvalues.append(abs(FIT.EIGVALS[i]))
    # Loop over nominal pois
    rdef = {}
    nominal,lb,hb = 0,0,0
    for ipoi, poi in enumerate(FIT.PList):
      rdef[poi] = FIT.EIGVECS[i][ipoi]
      nominal += FIT.POIS[poi]['nominal']*rdef[poi]
      lb += FIT.POIS[poi]['range'][0]*rdef[poi]
      hb += FIT.POIS[poi]['range'][1]*rdef[poi]
    if lb>hb: hrange,lrange = lb,hb
    else: hrange,lrange = hb,lb
    FIT.rPOIS["c%g"%(i+1)]['range'] = [lrange,hrange]
    FIT.rPOIS["c%g"%(i+1)]['title'] = "C_{%g}"%(i+1)
    FIT.rPOIS["c%g"%(i+1)]['freeze'] = 0
    FIT.rPDefinitions["c%g"%(i+1)] = rdef
    FIT.rP0.append(nominal)
    FIT.rPBounds.append([lrange,hrange])
    # Initially freeze all POIS: change state in minimizer functions
    FIT.rPToFitList = []
   
  # If successfully rotated then return True
  return True

