import ROOT
import re
from optparse import OptionParser

usage = "say 'dio boia' and go on with your life"
parser = OptionParser(usage=usage)
parser.add_option("--input", dest="input", type="string", default="tua mamma", help="input filename ")
parser.add_option("--cats", dest="cats", type="string", default="pdfindex_bTag_low_2017_13TeV,pdfindex_bTag_high_2017_13TeV,pdfindex_cTag_high_2017_13TeV,pdfindex_cTag_low_2017_13TeV,pdfindex_lTag_2017_13TeV,pdfindex_tthTag_2017_13TeV,pdfindex_vbfTag_2017_13TeV,pdfindex_vhTag_2017_13TeV", help="comma separated list of categories ")
parser.add_option("--snap", dest="snap", type="string", default="clean", help="input dir")
parser.add_option("--verbose", dest="verbose", action="store_true", default=False, help="additional printout level")
(opt,args) = parser.parse_args()

# Path to your RooFit workspace file (e.g. output of MultiDimFit)
filename = opt.input  
workspace_name = "w"  

# Open the ROOT file and get the workspace
file = ROOT.TFile.Open(filename)
workspace = file.Get(workspace_name)

if not workspace:
    print("Workspace not found!")
    exit()

# Snapshot to read from
snapshot_name = "MultiDimFit"

# Load snapshot
if workspace.loadSnapshot(snapshot_name):
    print(f"Loaded snapshot: {snapshot_name}")
else:
    print(f"Snapshot '{snapshot_name}' not found.")
    exit()

categories = opt.cats.split(",")

print("\n📌 Extracted pdfindex parameters:")
#for param in workspace.allVars():
pdf_indeces = []
for param in workspace.allCats():
    name = param.GetName()
    if name in categories:
        try:
            # Some pdfindex vars might be RooCategory
            if hasattr(param, "getLabel"):
                value = param.getLabel()
            else:
                value = param.getVal()
            if opt.verbose == "DEBUG":
                print(f"{name:<40}: {value}")
            pdf_indeces.append(f"{name}={value[-1]}")
        except Exception as e:
            print(f"{name:<40}: [Error] {e}")

command = "combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_float_bH_5POIs --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 -P r_c --floatOtherPOIs 1 --saveFitResult --setParameters r_c=1.,r_b=1,"
for x in pdf_indeces:
    command += f"{x}," 
print(command)