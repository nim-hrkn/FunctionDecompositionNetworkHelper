
CrystalTarget= sample/CrystalTargetToDescriptor_*.yml
TargetValuePrediction= sample/TheoreticalTargetValuePrediction_*.yml
AtomicProperty= sample/AtomicProperty_Caus*.yml
MaterialsList= sample/MaterialsList_*.yml
AtomicCoordinate2Descriptor= sample/AtomicCoordinate2Descriptor_*.yml

PROG= prog/cauFirst.py --no_wf --no_taxo

CONVERT= prog/unitfiletest.py 

default: Understanding

Prediction= $(TargetValuePrediction)  $(MaterialsList)
Prediction:  $(TargetValuePrediction)  $(MaterialsList) 
	$(CONVERT) $(Prediction)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG) $(Prediction)

CrystalTarget:
	$(PROG) $(CrystalTarget)
TheoreticalTargetValuePrediction:
	$(PROG) $(TargetValuePrediction)

DescriptorGeneration= $(CrystalTarget)  $(AtomicProperty)  $(AtomicCoordinate2Descriptor)
DescriptorGeneration: $(DescriptorGeneration)
	$(PROG) $(DescriptorGeneration)

MaterialsList:
	$(PROG) $(MaterialsList)
AtomicCoordinate2Descriptor:
	$(PROG) $(AtomicCoordinate2Descriptor)
AtomicProperty:
	$(PROG) $(AtomicProperty)


UnderstandingFiles= sample/Understand_Taxo.yml sample/SparseModeling.yml sample/LinearModel_Taxo.yml sample/EXSparseModel.yml  $(Importance) $(Group)

Understanding: $(UnderstandingFiles)
	$(CONVERT) $(UnderstandingFiles)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG) $(UnderstandingFiles)





Importance= sample/Importance_*.yml
Group= sample/Group_*.yml

Importance:
	$(PROG) $(Importance)
Group:
	$(PROG) $(Group)
clean:
	rm -f sample/*.gv sample/*.png *.gv *.png

