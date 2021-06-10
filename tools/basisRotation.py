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
    #P = FIT.PMATRIX.T
    #PT = FIT.PMATRIX


    # Extract Hessian
    # Approach 1: expected covariance matrix
    Vinv = FIT.INPUTS[0].Vinv
    # Approach 2: numerical calculation of Hessian (at bestfit point?) # TODO

    # Calculate fisher matrix for linearised model
    FIT.FISHERMATRIX = PT.dot(Vinv.dot(P))

    # Eigenvector decomposition of fisher matrix
    l,v = linalg.eig(FIT.FISHERMATRIX)
    # Order by decreasing eigenvalues
    il = np.argsort(l*-1)
    FIT.EIGVECS = v.T[il]
    FIT.EIGVALS = l[il]

    # Check: does this always work
    FIT.ROTATIONMATRIX = linalg.inv(FIT.EIGVECS)

  # Rotate according to use input rotation matrix
  else:
    FIT.ROTATIONMATRIX = linalg.inv(rmatrix)

  # Prepare rotated pois and informations
  FIT.RPOIS = od()
  FIT.RPList = []
  FIT.RP0 = []
  FIT.RPBounds = []
  FIT.RPDefinitions = {}
  FIT.RPEigenvalues = {}
  for i in range(len(FIT.EIGVECS)):
    FIT.RPOIS["c%g"%(i+1)] = {}
    FIT.RPOIS["c%g"%(i+1)]['factor'] = 1.
    FIT.RPOIS["c%g"%(i+1)]['multiplier'] = 1.
    FIT.RPList.append("c%g"%(i+1))
    FIT.RPEigenvalues["c%g"%(i+1)] = abs(FIT.EIGVALS[i])
    # Loop over nominal pois
    rdef = {}
    nominal = 0
    for ipoi, poi in enumerate(FIT.PList):
      rdef[poi] = FIT.EIGVECS[i][ipoi]
      nominal += FIT.POIS[poi]['nominal']*rdef[poi]
    if abs(FIT.EIGVALS[i])<=1e-10:
      hrange = 50
      lrange = -50
    else:
      hrange = nominal+4*(1./(abs(FIT.EIGVALS[i])**0.5))
      lrange = nominal-4*(1./(abs(FIT.EIGVALS[i])**0.5))
    FIT.RPOIS["c%g"%(i+1)]['range'] = [lrange,hrange]
    FIT.RPOIS["c%g"%(i+1)]['title'] = "C_{%g}"%(i+1)
    FIT.RPOIS["c%g"%(i+1)]['freeze'] = 1 if abs(FIT.EIGVALS[i]) < 0.01 else 0
    FIT.RPOIS["c%g"%(i+1)]['nominal'] = nominal
    FIT.RPDefinitions["c%g"%(i+1)] = rdef
    FIT.RP0.append(nominal)
    FIT.RPBounds.append([lrange,hrange])
  FIT.RP0 = np.array(FIT.RP0)
  FIT.RPToFitList = []
   
  # If successfully found rotated basis
  return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to set fit rotated basis as nominal and save old nominal for switching back
def set_rotated_basis(FIT):
  # Reset nominal and save nominal POI basis
  FIT.resetPOIS()
  FIT.nominalPOIS = FIT.POIS
  FIT.nominalPList = FIT.PList
  FIT.nominalP0 = FIT.P0
  FIT.nominalPBounds = FIT.PBounds

  # Set new rotated POI basis
  FIT.POIS = FIT.RPOIS
  FIT.PList = FIT.RPList
  FIT.P0 = FIT.RP0
  FIT.PBounds = FIT.RPBounds
  FIT.RMATRIX = FIT.ROTATIONMATRIX
  # TEST
  #FIT.RMATRIX = FIT.ROTATIONMATRIX.T
  FIT.rotated = True

def reset_rotated_basis(FIT):
  # Reset nominal POI basis
  FIT.resetPOIS()
  FIT.POIS = FIT.nominalPOIS
  FIT.PList = FIT.nominalPList
  FIT.P0 = FIT.nominalP0
  FIT.PBounds = FIT.nominalPBounds
  FIT.RMATRIX = None
  FIT.rotated = False



  
