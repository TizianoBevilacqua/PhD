import argparse
import os
import ROOT
import re
from math import sqrt

ROOT.gStyle.SetOptStat(0)

metadata = {
   # "TimingScan": {
   #     "file": "MiniTimingScan_Apr2023.root",
   #     "int_lumi": 42,
   #     "fill": [8550],
   #     "bias": 400,
   #     "marker_color": ROOT.kRed+1,
   #     "marker_style": 20,
   #     "marker_syze": .5,
   #     "outname": "MiniTimingScan_Apr2023",
   #     "sqrts": 900,
   #     "year": 2023,
   #     "legend": "Mini Timing Scan Apr2023",
   #     "write": True,
   # },
    # "FullTimingScan": {
    #     "file": "fullTimingScan_Apr2023_160523.root",
    #     "int_lumi": 42,
    #     "fill": [8550],
    #     "bias": 400,
    #     "marker_color": ROOT.kRed+1,
    #     "marker_style": 20,
    #     "marker_syze": .5,
    #     "outname": "FullTimingScan_Apr2023",
    #     "sqrts": 13.6,
    #     "year": 2023,
    #     "legend": "Full Timing Scan Apr2023",
    #     "write": True,
    # }
    "FullTimingScan": {
        "file": "/work/bevila_t/EPR/my_fork/CMSSW_10_2_16_UL/src/SiPixelTools/PixelHistoMaker/PHM_PHASE1_out/FullTimingScan_Apr2024/FullTimingScan_Apr2024.root",
        "int_lumi": 60,
        "fill": [9475],
        "bias": 450,
        "marker_color": ROOT.kRed+1,
        "marker_style": 20,
        "marker_syze": .5,
        "outname": "FullTimingScan_Apr2024",
        "outdir": "plots/FullTimingScan_Apr2024",
        "sqrts": 13.6,
        "year": 2024,
        "legend": "Full Timing Scan Apr2024",
        "write": True,
    }
}

plotdict ={
    "dirs": {
        "AvgNormOnTrkCluCharge_vs_Delay":{
            "xtitle": "Time Delay [ns]",
            "ytitle": "Avg. Norm. On-Trk Clu. Charge [ke]",
            "type": "charge_norm"
        },
        "AvgOnTrkCluCharge_vs_Delay":{
            "xtitle": "Time Delay [ns]",
            "ytitle": "Avg. On-Trk Clu. Charge [ke]",
            "type": "charge"
        },
        "AvgOnTrkCluSize_vs_Delay":{
            "xtitle": "Time Delay [ns]",
            "ytitle": "Avg. On-Trk Clu. Size [pixel]",
            "type": "size"
        },
        "AvgOnTrkCluSizeX_vs_Delay":{
            "xtitle": "Time Delay [ns]",
            "ytitle": "Avg. On-Trk Clu. Size [pixel]",
            "type": "size"
        },
        "AvgOnTrkCluSizeY_vs_Delay":{
            "xtitle": "Time Delay [ns]",
            "ytitle": "Avg. On-Trk Clu. Size [pixel]",
            "type": "size"
        },
        "HitEfficiency_vs_Delay":{
            "xtitle": "Time Delay [ns]",
            "ytitle": "Hit Efficiency",
            "type": "eff"
        },
    },

    "plots":{
        "Layers_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "BPIX",
            "outtitle": "Layers",
        },
        "Layers_BpI_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "BPIX",
            "outtitle": "Layers_BpI",
        },
        "Layers_BpO_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "BPIX",
            "outtitle": "Layers_BpO",
        },
        "Layers_BmI_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "BPIX",
            "outtitle": "Layers_BmI",
        },
        "Layers_BmO_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "BPIX",
            "outtitle": "Layers_BmO",
        },
        "Shell_Lay1_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "Layer 1",
            "outtitle": "Shell_Lay1",
        },
        "Shell_Lay2_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "Layer 2",
            "outtitle": "Shell_Lay2",
        },
        "Shell_Lay3_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "Layer 3",
            "outtitle": "Shell_Lay3",
        },
        "Shell_Lay4_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 9],
            "ranges_charge": [-20,20, 10, 60],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "Layer 4",
            "outtitle": "Shell_Lay4",
        },
        "Disks_2024AprFullScan": {
            "ranges_size": [-20,20, 0, 4],
            "ranges_charge": [-20,20, 10, 30],
            "ranges_charge_norm": [-20,20, 10, 30],
            "ranges_eff": [-20,20, 0.9, 1.05],
            "legtitle": "FPIX",
            "outtitle": "Disks",
        },
    },
}

file = []
for j,filename in enumerate(metadata):
    file.append(ROOT.TFile.Open(metadata[filename]["file"]))
    for dir in plotdict["dirs"]:
        for plot in plotdict["plots"]:
            print(dir+"/"+plot)
            c = file[j].Get(dir+"/"+plot)
            c.SetCanvasSize(600,700)
            c.SetTitle("")
            leg = None
        
            for item in c.GetListOfPrimitives():
                if item.GetName()!="TPave":
                    item.SetTitle("")
                    item.GetXaxis().SetRangeUser(plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][0], plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][1])
                    item.GetXaxis().SetTitle(plotdict["dirs"][dir]["xtitle"])
                    item.GetYaxis().SetRangeUser(plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2], plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3])
                    item.GetYaxis().SetTitle(plotdict["dirs"][dir]["ytitle"])
                if item.GetName()=="TPave":
                    leg=item
                if leg != None:
                    leg.SetHeader(plotdict["plots"][plot]["legtitle"])
                    leg.SetX1(0.2)
                    leg.SetX2(0.4)
                    leg.SetY1(0.7)
                    leg.SetY2(0.9)

            # shades
            left  = ROOT.TGraph(4)
            right = ROOT.TGraph(4)
            left.SetPoint(0,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][0],plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2])
            left.SetPoint(1,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][0],plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3])
            left.SetPoint(2,-15,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3])
            left.SetPoint(3,-15,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2])
            left.SetFillColorAlpha(ROOT.kBlue, 0.1)
            left.Draw("f")

            right.SetPoint(0,8,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2])
            right.SetPoint(1,8,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3])
            right.SetPoint(2,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][1]+1,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3])
            right.SetPoint(3,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][1]+1,plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2])
            right.SetFillColorAlpha(ROOT.kBlue, 0.1)
            right.Draw("f")


            CMS = ROOT.TLatex(plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][0], plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3]+(plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3]-plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2])*0.03, "CMS#scale[0.75]{#font[52]{Work in progress}}")
            CMS.SetLineWidth(2)
            CMS.Draw()
            era = ROOT.TLatex(plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][1]*0.45, plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3]+(plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][3]-plotdict["plots"][plot]["ranges_"+plotdict["dirs"][dir]["type"]][2])*0.03, "#scale[0.7]{#font[40]{(%s) %s TeV}}" % (metadata[filename]["year"], metadata[filename]["sqrts"]) )
            era.SetLineWidth(1)
            era.Draw()
            c.SetGridx()
            c.SetGridy()
            c.Draw()
            if metadata[filename]["write"]:
                c.SaveAs('%s/%s_%s_%s.root' % (metadata[filename]["outdir"], metadata[filename]["outname"], dir, plotdict["plots"][plot]["outtitle"]))
                c.SaveAs('%s/%s_%s_%s.pdf' % (metadata[filename]["outdir"], metadata[filename]["outname"], dir, plotdict["plots"][plot]["outtitle"]))
                c.SaveAs('%s/%s_%s_%s.png' % (metadata[filename]["outdir"], metadata[filename]["outname"], dir, plotdict["plots"][plot]["outtitle"]))
        
