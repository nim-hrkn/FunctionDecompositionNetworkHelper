
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


atomicproperty:
	for i in Materials/AtomicProperty_*.yml; do \
	  $(PROG) --doit=each --gen_wf --gen_taxo $$i; \
    done
	$(PROG) Materials/AtomicProperty_*.yml 
	

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
	$(PROG) --samerank="updateDecisionTreeNodeForNewSearch,generateDecisionTreeModel,getInitialStatusForDecisionTreeConstruction"   $(decisionTreefiles)
	cp caus.gv.png /media/sf_local_pc

PredictionAbilityFiles = PredictionAbility/*.yml

predictionAbility:
	$(PROG) $(PredictionAbilityFiles)
	cp caus.gv.png /media/sf_local_pc
	
steepestDescentFiles = SteepestDescent/*.yml

steepestDescent:
	$(PROG) --samerank="updatePositionForNewSearch,initializePositionForceDatabase" $(steepestDescentFiles)
	cp caus.gv.png /media/sf_local_pc

logmeshFiles = LogMesh/*.yml
logMesh: 
	$(PROG) --samerank="updateLoopCounterForNewLoop,getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $(logmeshFiles)
	cp caus.gv.png /media/sf_local_pc

metropolisFiles = Metropolis/*.yml
metropolis: 
	$(PROG) --samerank="appendXAndGetNewX,initializeDatabase" $(metropolisFiles)
	cp caus.gv.png /media/sf_local_pc

optFiles = Optimization/*.yml
optimization: 
	$(PROG) --samerank="getTheBestVariable,updateVariableForNewSearch" $(optFiles)
	cp caus.gv.png /media/sf_local_pc

umlfig11_1 = UMLbook/fig11_1.yml
umlfig11_1: 
	$(PROG) $(umlfig11_1)
	cp caus.gv.png /media/sf_local_pc

umlfig11_5 = UMLbook/fig11_11.yml
umlfig11_5: 
	$(PROG) $(umlfig11_5)
	cp caus.gv.png /media/sf_local_pc

umlfig11_6 = UMLbook/fig11_11.yml
umlfig11_6: 
	$(PROG) $(umlfig11_6)
	cp caus.gv.png /media/sf_local_pc

umlfig11_11 = UMLbook/fig11_11.yml
umlfig11_11: 
	$(PROG) $(umlfig11_11)
	cp caus.gv.png /media/sf_local_pc

umlfig11_12 = UMLbook/fig11_11.yml
umlfig11_12: 
	$(PROG) $(umlfig11_12)
	cp caus.gv.png /media/sf_local_pc

umlfig16_1 = UMLbook/fig16_1.yml
umlfig16_1: 
	$(PROG) $(umlfig16_1)
	cp caus.gv.png /media/sf_local_pc


clean:
	rm -f jupyter/*.gv jupyter/*.gv.png *.gv *.png
	rm -f Materials/*.gv sample/*.gv.png 

