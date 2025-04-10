# Diphoton ID BDT training

## Intro

This directory contains script that are used to train the Diphoton ID BDT starting from NanoAOD.
This tools is used to discriminate against the QCD background in the Higgs to GG analysis. It was used already in Run 2 in the context of the STXS Xsection measurement.
Here are some links to the presentations about the training in the Hgg PAG meeting:
* [22/08/22](https://indico.cern.ch/event/1184696/contributions/4994927/)
* [23/07/10](https://indico.cern.ch/event/1298068/contributions/5490250/)
* [23/11/07](https://indico.cern.ch/event/1344768/contributions/5660435/attachments/2747410/4780954/HToGG_Follow_up_DiphotonBDT_nAOD_training_1123.pdf)

## Training

The training is done using a jupyter notebook: [Training_v4.ipynb](https://github.com/TizianoBevilacqua/PhD/blob/master/HToGG/BDT_training/DiphotonID/Training_v4.ipynb), this files uses some NTuples as input that are created using HiggsDNA applying the Diphoton selection only.
Some NTuples to run on 2017 can be found here: `/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017`, 
for 2018 instead they're a bit more tidy here: `/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018`.

There are some auxiliary files in this directory that contain:
* the DiphotnID BDT conficuration parameters: [diphoton_bdt_config.json](https://github.com/TizianoBevilacqua/PhD/blob/master/HToGG/BDT_training/DiphotonID/diphoton_bdt_config.json)
* the cross section metadata: [cross_sections.json](https://github.com/TizianoBevilacqua/PhD/blob/master/HToGG/BDT_training/cross_sections.json)
* the SF calculation script to correct for the absolute value of the weight: [weight_study.py](https://github.com/TizianoBevilacqua/PhD/blob/master/HToGG/BDT_training/DiphotonID/weight_study.py)
* the SF themselves: [abs_to_nominal.json.gz](https://github.com/TizianoBevilacqua/PhD/blob/master/HToGG/BDT_training/DiphotonID/abs_to_nominal.json.gz)

## To do:

* add to the code the cH and bH samples.