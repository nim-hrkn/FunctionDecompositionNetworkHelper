
CrystalTarget= Materials2/CrystalTargetToDescriptor_*.yml
TargetValuePrediction= Materials2/TheoreticalTargetValuePrediction_*.yml
AtomicProperty= Materials2/AtomicProperty_Caus*.yml
MaterialsList= Materials2/MaterialsList_*.yml
AtomicCoordinate2Descriptor= Materials2/AtomicCoordinate2Descriptor_*.yml

PROG= ../prog/cauFirst.py # --no_wf --no_taxo --no_connect_invis --concentrate

CONVERT= ../prog/unitfiletest.py 

default: decisionTree

#------------------------
Prediction= $(TargetValuePrediction)  $(MaterialsList) Materials2/Richer_DB.yml
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
UnderstandingFiles= Materials2/Understand_Taxo.yml Materials2/SparseModeling.yml Materials2/LinearModel_Taxo.yml Materials2/EXSparseModel*.yml  $(Importance) $(Group)
Importance= Materials2/Importance_*.yml
Group= Materials2/Group_*.yml


atomicproperty:
	for i in Materials2/AtomicProperty_*.yml; do \
	  $(PROG) --doit=each --gen_wf --gen_taxo $$i; \
    done
	$(PROG) Materials2/AtomicProperty_*.yml 
	

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

decisionTree2files= DecisionTree2/EnsembleTree.yml
decisionTree2: 
	$(PROG) --doit=each --gen_wf  $(decisionTree2files)
	$(PROG) --samerank="generateDecisionTreeModel"  $(decisionTree2files)
	cp caus.gv.png /media/sf_local_pc


PredictionAbilityFiles = PredictionAbility/*.yml

predictionAbility:
	$(PROG) $(PredictionAbilityFiles)
	cp caus.gv.png /media/sf_local_pc
	
steepestDescentFiles = SteepestDescent/*.yml
steepestDescent:
	$(PROG) --doit=each --gen_wf $(steepestDescentFiles)
	$(PROG) --samerank="getStablePosition,getStablerPosition" $(steepestDescentFiles)
	cp caus.gv.png /media/sf_local_pc

steepestDescent0Files = SteepestDescent0/*.yml
steepestDescent0:
	$(PROG) --samerank="initializePositionForceDatabase,getStablePosition,updatePositionForNewSearch" $(steepestDescent0Files)
	cp caus.gv.png /media/sf_local_pc


logmeshFiles = LogMesh/*.yml
logMesh: 
	$(PROG) --samerank="getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $(logmeshFiles)
	cp caus.gv.png /media/sf_local_pc

logmesh0Files = LogMesh0/*.yml
logMesh0: 
	$(PROG) --samerank="InitializeCounter,updateLoopCounterForNewExecution,getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $(logmesh0Files)
	cp caus.gv.png /media/sf_local_pc


logmesh2Files = LogMesh2/*.yml
logMesh2: 
	$(PROG) --samerank="getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $(logmesh2Files)
	cp caus.gv.png /media/sf_local_pc

logmesh3Files = LogMesh3/*.yml
logMesh3: 
	$(PROG) --doit=each --gen_wf $(logmesh3Files)
	$(PROG) --samerank="getAllLogmeshValues" $(logmesh3Files)
	cp caus.gv.png /media/sf_local_pc



metropolisFiles = Metropolis/*.yml
metropolis: 
	$(PROG) --doit=each --gen_wf $(metropolisFiles)
	$(PROG) --samerank="updateDatabase" $(metropolisFiles)
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

readBook2files = readbook2/readbook*.yml
readBook2: 
	$(PROG) --doit=each --gen_wf --gen_taxo $(readBook2files)
	$(PROG) $(readBook2files)
	cp caus.gv.png /media/sf_local_pc


clean:
	rm -f jupyter/*.gv jupyter/*.gv.png *.gv *.png
	rm -f Materials2/*.gv sample/*.gv.png 

