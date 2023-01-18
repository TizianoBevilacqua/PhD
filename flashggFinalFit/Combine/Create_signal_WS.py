import ROOT
import argparse
import os
import ROOT
import re
import numpy

#create the workspace to save the pdfs and variables
workspace = ROOT.RooWorkspace("wsig_13TeV","wsig_13TeV") 

#open input file and define variables
f  = ROOT.TFile.Open("../higgs_dna_signals_2017/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H_WStest.root")
win = f.Get("tagsDumper/cms_hgg_13TeV")
sQr  = ROOT.RooRealVar("SqrtS", "SqrtS in TeV", 13, "TeV")
intL = win.var("intLumi")
mass = win.var("CMS_hgg_mass")
win.Print()
sQr.Print()
intL.Print()
mass.Print()
norm = ROOT.RooRealVar("CMS_hgg_WStest_2017_13TeV_bkgshape_norm", "normalization", 1, 0, ROOT.RooNumber.infinity())
norm.Print()
_MH = ROOT.RooRealVar("MH", "higgs mass value", 125, 120, 130, "GeV")
_MH.setConstant(True)
_MH.Print()
signal = win.data("ggh_125_13TeV_WStest")
dh = ROOT.RooDataHist("Signal_13TeV_WStest", "Signal_13TeV_WStest", ROOT.RooArgSet(mass), signal)
dh.Print()
sumW = 452172498.84887695# 447352556.17126465 #SUm of weight for ggH sample (before selections)

from collections import OrderedDict as od

# Parameter lookup table for initialisation
# So far defined up to MHPolyOrder=2
pLUT = od()
pLUT['DCB'] = od()
pLUT['DCB']['dm_p0'] = [0.1,-2.5,2.5]
pLUT['DCB']['dm_p1'] = [0.0,-0.1,0.1]
pLUT['DCB']['dm_p2'] = [0.0,-0.001,0.001]
pLUT['DCB']['sigma_p0'] = [2.,1.,20.]
pLUT['DCB']['sigma_p1'] = [0.0,-0.1,0.1]
pLUT['DCB']['sigma_p2'] = [0.0,-0.001,0.001]
pLUT['DCB']['n1_p0'] = [20.,1.00001,500]
pLUT['DCB']['n1_p1'] = [0.0,-0.1,0.1]
pLUT['DCB']['n1_p2'] = [0.0,-0.001,0.001]
pLUT['DCB']['n2_p0'] = [20.,1.00001,500]
pLUT['DCB']['n2_p1'] = [0.0,-0.1,0.1]
pLUT['DCB']['n2_p2'] = [0.0,-0.001,0.001]
pLUT['DCB']['a1_p0'] = [1.,1.,10.]
pLUT['DCB']['a1_p1'] = [0.0,-0.1,0.1]
pLUT['DCB']['a1_p2'] = [0.0,-0.001,0.001]
pLUT['DCB']['a2_p0'] = [1.,1.,20.]
pLUT['DCB']['a2_p1'] = [0.0,-0.1,0.1]
pLUT['DCB']['a2_p2'] = [0.0,-0.001,0.001]
pLUT['Gaussian_wdcb'] = od()
pLUT['Gaussian_wdcb']['dm_p0'] = [0.1,-1.5,1.5]
pLUT['Gaussian_wdcb']['dm_p1'] = [0.01,-0.01,0.01]
pLUT['Gaussian_wdcb']['dm_p2'] = [0.01,-0.01,0.01]
pLUT['Gaussian_wdcb']['sigma_p0'] = [1.5,1.0,4.]
pLUT['Gaussian_wdcb']['sigma_p1'] = [0.0,-0.1,0.1]
pLUT['Gaussian_wdcb']['sigma_p2'] = [0.0,-0.001,0.001]
pLUT['Frac'] = od()
pLUT['Frac']['p0'] = [0.25,0.01,0.99]
pLUT['Frac']['p1'] = [0.,-0.05,0.05]
pLUT['Frac']['p2'] = [0.,-0.0001,0.0001]
pLUT['Gaussian'] = od()
pLUT['Gaussian']['dm_p0'] = [0.1,-5.,5.]
pLUT['Gaussian']['dm_p1'] = [0.0,-0.01,0.01]
pLUT['Gaussian']['dm_p2'] = [0.0,-0.01,0.01]
pLUT['Gaussian']['sigma_p0'] = ['func',1,10.0]
pLUT['Gaussian']['sigma_p1'] = [0.0,-0.01,0.01]
pLUT['Gaussian']['sigma_p2'] = [0.0,-0.01,0.01]
pLUT['FracGaussian'] = od()
pLUT['FracGaussian']['p0'] = ['func',0.01,0.99]
pLUT['FracGaussian']['p1'] = [0.01,-0.005,0.005]
pLUT['FracGaussian']['p2'] = [0.00001,-0.00001,0.00001]

Varlists = od()
Vars = od()
Polynomials = od()
Pdfs = od()
Coeffs = od()
Splines = od()

Functions = od()

MH = _MH
MH.setConstant(True)
MH.setVal(125)
MH.setBins(10)
dMH = ROOT.RooFormulaVar("dMH","dMH","@0-125.0",ROOT.RooArgList(MH)) 
xvar = mass
nBins = 160
xvar.setVal(125)
xvar.setBins(nBins)
proc = "GG2H"
cat = "WStest"

# function to initialize a pdf adding n gaussians
def buildNGaussians(nGaussians,_recursive=True):
    MHPolyOrder = 0
    # Loop over NGaussians
    for g in range(0,nGaussians):
        # Define polynominal functions for mean and sigma (in MH)
        for f in ['dm','sigma']:
            k = "%s_g%g"%(f,g)
            Varlists[k] = ROOT.RooArgList("%s_coeffs"%k)
	        # Create coeff for polynominal of order MHPolyOrder: y = a+bx+cx^2+...
            for po in range(0,MHPolyOrder+1):
                # p0 value of sigma is function of g (creates gaussians of increasing width)
                if(f == "sigma")&(po==0): 
                    Vars['%s_p%g'%(k,po)] = ROOT.RooRealVar("%s_p%g"%(k,po),"%s_p%g"%(k,po),(g+1)*1.0,pLUT['Gaussian']["%s_p%s"%(f,po)][1],pLUT['Gaussian']["%s_p%s"%(f,po)][2])
                else:
                    Vars['%s_p%g'%(k,po)] = ROOT.RooRealVar("%s_p%g"%(k,po),"%s_p%g"%(k,po),pLUT['Gaussian']["%s_p%s"%(f,po)][0],pLUT['Gaussian']["%s_p%s"%(f,po)][1],pLUT['Gaussian']["%s_p%s"%(f,po)][2])
                Varlists[k].add( Vars['%s_p%g'%(k,po)] ) 
	        # Define polynominal
            Polynomials[k] = ROOT.RooPolyVar(k,k,dMH,Varlists[k])
        # Mean function
        Polynomials['mean_g%g'%g] = ROOT.RooFormulaVar("mean_g%g"%g,"mean_g%g"%g,"(@0+@1)",ROOT.RooArgList(MH,Polynomials['dm_g%g'%g]))
        # Build Gaussian
        Pdfs['gaus_g%g'%g] = ROOT.RooGaussian("gaus_g%g"%g,"gaus_g%g"%g,xvar,Polynomials['mean_g%g'%g],Polynomials['sigma_g%g'%g])

        # Relative fractions: also polynomials of order MHPolyOrder (define up to n=nGaussians-1)
        if g < nGaussians-1:
            Varlists['frac_g%g'%g] = ROOT.RooArgList("frac_g%g_coeffs"%g)
            for po in range(0,MHPolyOrder+1):
                if po == 0 and g == 0:
                    Vars['frac_g%g_p%g'%(g,po)] = ROOT.RooRealVar("frac_g%g_p%g"%(g,po),"frac_g%g_p%g"%(g,po),0.3,pLUT['FracGaussian']['p%g'%po][1],pLUT['FracGaussian']['p%g'%po][2])
                elif po == 0:
                    Vars['frac_g%g_p%g'%(g,po)] = ROOT.RooRealVar("frac_g%g_p%g"%(g,po),"frac_g%g_p%g"%(g,po),0.5-0.05*g,pLUT['FracGaussian']['p%g'%po][1],pLUT['FracGaussian']['p%g'%po][2])
                else:
                    Vars['frac_g%g_p%g'%(g,po)] = ROOT.RooRealVar("frac_g%g_p%g"%(g,po),"frac_g%g_p%g"%(g,po),pLUT['FracGaussian']['p%g'%po][0],pLUT['FracGaussian']['p%g'%po][1],pLUT['FracGaussian']['p%g'%po][2])
                Varlists['frac_g%g'%g].add( Vars['frac_g%g_p%g'%(g,po)] )
	        # Define Polynomial
            Polynomials['frac_g%g'%g] = ROOT.RooPolyVar("frac_g%g"%g,"frac_g%g"%g,dMH,Varlists['frac_g%g'%g])
            # Constrain fraction to not be above 1 or below 0
            Polynomials['frac_g%g_constrained'%g] = ROOT.RooFormulaVar('frac_g%g_constrained'%g,'frac_g%g_constrained'%g,"(@0>0)*(@0<1)*@0+ (@0>1.0)*0.9999",ROOT.RooArgList(Polynomials['frac_g%g'%g]))
            Coeffs['frac_g%g_constrained'%g] = Polynomials['frac_g%g_constrained'%g]
    # End of loop over n Gaussians
    
    # Define total PDF
    _pdfs, _coeffs = ROOT.RooArgList(), ROOT.RooArgList()
    for g in range(0,nGaussians): 
        _pdfs.add(Pdfs['gaus_g%g'%g])
        if g < nGaussians-1: _coeffs.add(Coeffs['frac_g%g_constrained'%g])
    Pdfs['final'] = ROOT.RooAddPdf("%s_%s"%(proc,cat),"%s_%s"%(proc,cat),_pdfs,_coeffs,_recursive)

ngauss=3
buildNGaussians(ngauss)
print(Pdfs)

fv = Pdfs['final'].getVariables().Clone()
fv.remove(xvar)
FitParameters = ROOT.RooArgList(fv)
Ndof = None
Chi2 = None
FitResult = None
name = "fTest_%g"
verbose = True

from scipy.optimize import minimize

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
# Function to extract param bounds
def extractXBounds():
    XBounds = []
    for i in range(len(FitParameters)): XBounds.append((FitParameters[i].getMin(),FitParameters[i].getMax()))
    return numpy.asarray(XBounds)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
# Function to extract initial param value vector
def extractX0():
    X0 = []
    for i in range(len(FitParameters)): X0.append(FitParameters[i].getVal())
    return numpy.asarray(X0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
def runFit(data):
    # Extract fit variables: remove xvar from fit parameters
    #fv = Pdfs['final'].getVariables().Clone()
    #fv.remove(xvar)
    #FitParameters = ROOT.RooArgList(fv)
    
    # Create initial vector of parameters and calculate initial Chi2
    if verbose: print ("\n --> (%s) Initialising fit parameters"%name)
    x0 = extractX0()
    xbounds = extractXBounds()

    # Run fit
    if verbose: print (" --> (%s) Running fit"%name)
    nll = Pdfs['final'].createNLL(data)
    nll.Print()
    minim = ROOT.RooMinimizer(nll)
    FitResult = minim.minimize("Minuit2","migrad")
    #Chi2 = nChi2Addition(FitResult['x'],self)
    # Print parameter post-fit values
    return FitResult

Pdfs["final"].Print()
nll = Pdfs['final'].createNLL(dh)
nll.Print()
#ROOT.Math.MinimizerOptions.SetDefaultTolerance(0.5)
minim = ROOT.RooMinimizer(nll)
minim.setPrintLevel(1)
minim.setVerbose(False)
minim.minimize("Minuit2","migrad")

frame = mass.frame()
c = ROOT.TCanvas()

dh.plotOn(frame)
datahist= dh.createHistogram("h_data",mass,ROOT.RooFit.Binning(160))
datahist.SetMarkerStyle(20)
datahist.Draw("SAME,P")
Pdfs['final'].plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
frac_g0_constrained = Pdfs['final'].getComponents().getRealValue("frac_g0_constrained")
hists = []
LineColorMap = [ROOT.kBlue, ROOT.kViolet, ROOT.kYellow, ROOT.kGreen, ROOT.kCyan ]
frame.SetMinimum(0.0001)
frame.Draw("SAME")
for i in range(0,ngauss):
    frac = Pdfs['final'].getComponents().getRealValue("%s_%s_recursive_fraction_gaus_g%d"%("GG2H","WStest",i))
    if i == 0: frac = frac_g0_constrained
    print(frac_g0_constrained,frac, dh.sumEntries())
    hists.append(Pdfs['gaus_g%d' % (i)].createHistogram("h_%d"%(i),mass,ROOT.RooFit.Binning(160000)))
    hists[i].Scale(frac)
    hists[i].Scale(dh.sumEntries()*1000)
    hists[i].SetLineColor(LineColorMap[i])
    hists[i].SetLineWidth(2)
    hists[i].SetLineStyle(2)
    hists[i].Draw("HIST SAME")

c.Draw()
Pdfs['final'].Print()

print(Pdfs["final"].getNorm())
print(dh.sumEntries())
sel_sumW = dh.sumEntries()
print(sel_sumW)

Splines = od()
Splines['xs'] = ROOT.RooRealVar("xs", "xs in pb", 48.58, "pb")
Splines['br'] = ROOT.RooRealVar("br", "br", 0.00227)
sel_wgt = ROOT.RooRealVar("selW", "sum of weight of selected events",145455287.533, -ROOT.RooNumber.infinity(), ROOT.RooNumber.infinity())
sel_wgt.setConstant(True)
sum_wgt = ROOT.RooRealVar("sumW", "sumW", 452172498.849, -ROOT.RooNumber.infinity(), ROOT.RooNumber.infinity())
sum_wgt.setConstant(True)
Splines['ea'] = ROOT.RooFormulaVar("ea", "efficiency times acceptance", "@0/@1", ROOT.RooArgList(sel_wgt, sum_wgt))#ROOT.RooRealVar("selW", "sum of weight of selected events",sel_sumW), ROOT.RooRealVar("sumW", "sumW", sumW)))
Splines['ea'].Print()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to build extended Pdfs and normalisation with luminosity
def buildExtended(Pdfs, Functions):
  finalPdfName = Pdfs['final'].GetName()
  Functions['final_norm'] = ROOT.RooFormulaVar("%s_norm"%finalPdfName,"%s_norm"%finalPdfName,"@0*@1*@2",ROOT.RooArgList(Splines['xs'],Splines['br'],Splines['ea']))
  Functions['final_normThisLumi'] = ROOT.RooFormulaVar("%s_normThisLumi"%finalPdfName,"%s_normThisLumi"%finalPdfName,"@0*@1*@2*@3",ROOT.RooArgList(Splines['xs'],Splines['br'],Splines['ea'],intL))
  Pdfs['final_extend'] = ROOT.RooExtendPdf("extend%s"%finalPdfName,"extend%s"%finalPdfName,Pdfs['final'],Functions['final_norm'])
  Pdfs['final_extendThisLumi'] = ROOT.RooExtendPdf("extend%sThisLumi"%finalPdfName,"extend%sThisLumi"%finalPdfName,Pdfs['final'],Functions['final_normThisLumi'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function for saving to output workspace
def save(wsout):
  getattr(wsout,"import")(Pdfs['final'],ROOT.RooFit.RecycleConflictNodes())
  getattr(wsout,"import")(Functions['final_norm'],ROOT.RooFit.RecycleConflictNodes())
  getattr(wsout,"import")(Functions['final_normThisLumi'],ROOT.RooFit.RecycleConflictNodes())
  getattr(wsout,"import")(Pdfs['final_extend'],ROOT.RooFit.RecycleConflictNodes())
  getattr(wsout,"import")(Pdfs['final_extendThisLumi'],ROOT.RooFit.RecycleConflictNodes())
  getattr(wsout,"import")(dh) 

buildExtended(Pdfs, Functions)
Pdfs["final_extendThisLumi"].Print()

getattr(workspace,"import")(Pdfs['final'],ROOT.RooFit.RecycleConflictNodes())
print("final done")
getattr(workspace,"import")(Functions['final_norm'],ROOT.RooFit.RecycleConflictNodes())
print("final norm done")
getattr(workspace,"import")(Functions['final_normThisLumi'],ROOT.RooFit.RecycleConflictNodes())
print("final norm this lumi done")
getattr(workspace,"import")(Pdfs['final_extend'],ROOT.RooFit.RecycleConflictNodes())
print("finalextended done")
getattr(workspace,"import")(Pdfs['final_extendThisLumi'],ROOT.RooFit.RecycleConflictNodes())
print("final extended this lumi done")
getattr(workspace,'import')(signal)

workspace.Print()
workspace.writeToFile("mysignalpdf_workspace_bdt.root")

print("workspace written")