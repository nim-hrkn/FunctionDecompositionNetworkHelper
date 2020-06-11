
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
UnderstandingFiles= Materials/Understand_Taxo.yml Materials/SparseModeling.yml Materials/LinearModel_Taxo.yml Materials/EXSparseModel*.yml  $(Importance) $(Group)
Importance= Materials/Importance_*.yml
Group= Materials/Group_*.yml


Understanding: $(UnderstandingFiles)
	$(CONVERT) $(UnderstandingFiles)
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG)  $(UnderstandingFiles)
	cp caus.gv.png /media/sf_local_pc

#---------------------------
distributionfiles=  Distribution/*.yml
SeparatedDistribution: 
	$(PROG)   $(distributionfiles)
	cp caus.gv.png /media/sf_local_pc
#---------------------------
decisionTreefiles= DecisionTree/EnsembleTree.yml

decisionTree: 
	$(PROG) --samerank="updateDecisionTreeNode,generateDecisionTreeModel,getInitialStatusForDecisionTreeConstruction"   $(decisionTreefiles)
	cp caus.gv.png /media/sf_local_pc

PredictionAbilityFiles = PredictionAbility/*.xml

predictionAbility:
	$(PROG) $(PredictionAbilityFiles)
	cp caus.gv.png /media/sf_local_pc
	
steepestDescentFiles = SteepestDescent/*.xml

steepestDescent:
	$(PROG) $(steepestDescentFiles)
	cp caus.gv.png /media/sf_local_pc

logmeshFiles = LogMesh/*.xml
logMesh: 
	$(PROG) $(logmeshFiles)
	cp caus.gv.png /media/sf_local_pc

metropolisFiles = Metropolis/*.xml
metropolis: 
	$(PROG) $(metropolisFiles)
	cp caus.gv.png /media/sf_local_pc

optFiles = Optimization/*.xml
optimization: 
	$(PROG) $(optFiles)
	cp caus.gv.png /media/sf_local_pc

umlfig11_1 = UMLbook/fig11_1.xml
umlfig11_1: 
	$(PROG) $(umlfig11_1)
	cp caus.gv.png /media/sf_local_pc

umlfig11_5 = UMLbook/fig11_11.xml
umlfig11_5: 
	$(PROG) $(umlfig11_5)
	cp caus.gv.png /media/sf_local_pc

umlfig11_6 = UMLbook/fig11_11.xml
umlfig11_6: 
	$(PROG) $(umlfig11_6)
	cp caus.gv.png /media/sf_local_pc

umlfig11_11 = UMLbook/fig11_11.xml
umlfig11_11: 
	$(PROG) $(umlfig11_11)
	cp caus.gv.png /media/sf_local_pc

umlfig11_12 = UMLbook/fig11_11.xml
umlfig11_12: 
	$(PROG) $(umlfig11_12)
	cp caus.gv.png /media/sf_local_pc

umlfig16_1 = UMLbook/fig16_1.xml
umlfig16_1: 
	$(PROG) $(umlfig16_1)
	cp caus.gv.png /media/sf_local_pc


clean:
	rm -f jupyter/*.gv jupyter/*.gv.png *.gv *.png
	rm -f Materials/*.gv sample/*.gv.png 

