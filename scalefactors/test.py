import uproot


Events = uproot.open("egammaEffi.txt_Ele_Medium_EGM2D.root")
print(Events["EGamma_SF2D"].errors())
