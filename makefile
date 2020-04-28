
CrystalTarget= sample/CrystalTargetToDescriptor_*.yml
TargetValuePrediction= sample/TheoreticalTargetValuePrediction_*.yml
AtomicProperty= sample/AtomicProperty_Caus*.yml
MaterialsList= sample/MaterialsList_*.yml
AtomicCoordinate2Descriptor= sample/AtomicCoordinate2Descriptor_*.yml

PROG= prog/cauFirst.py --no_wf --no_taxo

Prediction= $(TargetValuePrediction)  $(MaterialsList)
Prediction:  $(TargetValuePrediction)  $(MaterialsList) 
	$(PROG) $(Prediction)
	mv caus.gv.png Prediction.png

CrystalTarget:
	$(PROG) $(CrystalTarget)
TheoreticalTargetValuePrediction:
	$(PROG) $(TargetValuePrediction)

DescriptorGeneration= $(CrystalTarget)  $(AtomicProperty)  $(AtomicCoordinate2Descriptor)
DescriptorGeneration: $(DescriptorGeneration)
	$(PROG) $(DescriptorGeneration)
	mv caus.gv.png DescriptorGeneration.png

MaterialsList:
	$(PROG) $(MaterialsList)
AtomicCoordinate2Descriptor:
	$(PROG) $(AtomicCoordinate2Descriptor)
AtomicProperty:
	$(PROG) $(AtomicProperty)


UnderstandingFiles= sample/Understand_taxo.yml sample/SparseModeling.yml sample/LinearModel_taxo.yml $(Importance) $(Group)

Understanding: $(UnderstandingFiles)
	$(PROG) $(UnderstandingFiles)



Importance= sample/Importance_*.yml
Group= sample/Group_*.yml

Importance:
	$(PROG) $(Importance)
Group:
	$(PROG) $(Group)
clean:
	rm -f sample/*.gv sample/*.png *.gv *.png

