
CrystalTarget= sample/CrystalTargetToDescriptor_*.yml
TargetValuePrediction= sample/TheoreticalTargetValuePrediction_*.yml
AtomicProperty= sample/AtomicProperty_Caus*.yml
MaterialsList= sample/MaterialsList_*.yml
AtomicCoordinate2Descriptor= sample/AtomicCoordinate2Descriptor_*.yml

PROG= prog/cauFirst.py --no_wf --no_taxo

CONVERT= prog/unitfiletest.py 

default: Prediction

#------------------------
Prediction= $(TargetValuePrediction)  $(MaterialsList) sample/Richer_DB.yml
Prediction:  $(TargetValuePrediction)  $(MaterialsList) 
	$(CONVERT) $(Prediction)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG) --samerank="updateMaterialsList,get_NewMaterialSatisfyingSelectionCriterion"  $(Prediction)
	cp caus.gv.png /media/sf_local_pc

TargetValuePrediction: $(TargetValuePrediction)
	$(PROG) $(TargetValuePrediction)

CrystalTarget:
	$(PROG) $(CrystalTarget)

#---------------------------
DescriptorGeneration= $(CrystalTarget)  $(AtomicProperty)  $(AtomicCoordinate2Descriptor)
DescriptorGeneration: $(DescriptorGeneration)
	$(PROG) $(DescriptorGeneration)
	cp caus.gv.png /media/sf_local_pc

MaterialsList:
	$(PROG) $(MaterialsList)
AtomicCoordinate2Descriptor:
	$(PROG) $(AtomicCoordinate2Descriptor)
AtomicProperty:
	$(PROG) $(AtomicProperty)

#------------------------
UnderstandingFiles= sample/Understand_Taxo.yml sample/SparseModeling.yml sample/LinearModel_Taxo.yml sample/EXSparseModel*.yml  $(Importance) $(Group)

Understanding: $(UnderstandingFiles)
	$(CONVERT) $(UnderstandingFiles)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG) $(UnderstandingFiles)
	cp caus.gv.png /media/sf_local_pc


#--------------------------
Importance= sample/Importance_*.yml
Group= sample/Group_*.yml

Importance:
	$(PROG) $(Importance)
Group:
	$(PROG) $(Group)
clean:
	rm -f jupyter/*.gv jupyter/*.gv.png *.gv *.png
	rm -f sample/*.gv sample/*.gv.png 
