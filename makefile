
CrystalTarget= Materials/CrystalTargetToDescriptor_*.yml
TargetValuePrediction= Materials/TheoreticalTargetValuePrediction_*.yml
AtomicProperty= Materials/AtomicProperty_Caus*.yml
MaterialsList= Materials/MaterialsList_*.yml
AtomicCoordinate2Descriptor= Materials/AtomicCoordinate2Descriptor_*.yml

PROG= prog/cauFirst.py # --no_wf --no_taxo --no_connect_invis --concentrate

CONVERT= prog/unitfiletest.py 

default: decisionTree

#------------------------
Prediction= $(TargetValuePrediction)  $(MaterialsList) Materials/Richer_DB.yml
Prediction:  $(TargetValuePrediction)  $(MaterialsList) 
	$(CONVERT) $(Prediction)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG) --samerank="updateMaterialsList,get_NewMaterialSatisfyingSelectionCriterion"  $(Prediction)
	cp caus.gv.png /media/sf_local_pc
#---------------------------
DescriptorGeneration= $(CrystalTarget)  $(AtomicProperty)  $(AtomicCoordinate2Descriptor)
DescriptorGeneration: $(DescriptorGeneration)
	$(PROG) $(DescriptorGeneration)
	cp caus.gv.png /media/sf_local_pc
#------------------------
UnderstandingFiles= Materials/Understand_Taxo.yml sample/SparseModeling.yml sample/LinearModel_Taxo.yml sample/EXSparseModel*.yml  $(Importance) $(Group)
Importance= Materials/Importance_*.yml
Group= Materials/Group_*.yml


Understanding: $(UnderstandingFiles)
	$(CONVERT) $(UnderstandingFiles)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG)  $(UnderstandingFiles)
	cp caus.gv.png /media/sf_local_pc

#---------------------------
distributionfiles=  distribution/*.yml
sdistribution: 
	$(PROG)   $(distributionfiles)
	cp caus.gv.png /media/sf_local_pc
#---------------------------
decisionTreefiles= DecisionTree/EnsembleTree.yml

decisionTree: 
	$(PROG) --samerank="updateDecisionTreeNode,generateDecisionTreeModel,getInitialStatusForDecisionTreeConstruction"   $(decisionTreefiles)
	cp caus.gv.png /media/sf_local_pc


clean:
	rm -f jupyter/*.gv jupyter/*.gv.png *.gv *.png
	rm -f Materials/*.gv sample/*.gv.png 

