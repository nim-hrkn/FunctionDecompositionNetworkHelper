

PROG= ../prog/cauFirst.py # --no_wf --no_taxo --no_connect_invis --concentrate
CONVERT= ../prog/unitfiletest.py 

default: decisionTree

MaterialsDir = Materials2

#------------------------
TargetValuePrediction= $(MaterialsDir)/TheoreticalTargetValuePrediction_*.yml
MaterialsList= $(MaterialsDir)/MaterialsList_*.yml
Prediction:  $(TargetValuePrediction)  $(MaterialsList)  Materials2/Richer_DB.yml
	$(CONVERT) $^
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG) --samerank="updateMaterialsList,get_NewMaterialSatisfyingSelectionCriterion"  $^
	cp caus.gv.png $(MaterialsDir)/Prediction.png

#---------------------------
AtomicProperty= $(MaterialsDir)/AtomicProperty_Caus*.yml
AtomicCoordinate2Descriptor= $(MaterialsDir)/AtomicCoordinate2Descriptor_*.yml
CrystalTarget= $(MaterialsDir)/CrystalTargetToDescriptor_*.yml
DescriptorGeneration: $(CrystalTarget)  $(AtomicProperty)  $(AtomicCoordinate2Descriptor)
	$(PROG) $^
	cp caus.gv.png $(MaterialsDir)/DescriptorGeneration.png

#------------------------
atomicproperty:
	for i in Materials2/AtomicProperty_*.yml; do \
	  $(PROG) --doit=each --gen_wf --gen_taxo $$i; \
    done
	$(PROG) Materials2/AtomicProperty_*.yml 
	cp caus.gv.png $(MaterialsDir)/atomicproperty.png

Importance= Materials2/Importance_*.yml
Group= Materials2/Group_*.yml
Understanding: Materials2/Understand_Taxo.yml Materials2/SparseModeling.yml Materials2/LinearModel_Taxo.yml Materials2/EXSparseModel*.yml  $(Importance) $(Group)
	$(CONVERT) $^
	$(PROG) a.yml
	mv caus.gv.png a.png 
	$(PROG)  $^
	cp caus.gv.png $(MaterialsDir)/Understanding.png

#---------------------------
distributionDir=  Distribution
SeparatedDistribution: $(distributionDir)/*.yml
	$(PROG)   $^
	cp caus.gv.png $(distributionDir)
#---------------------------

decisionTreeDir= DecisionTree
decisionTree: $(decisionTreeDir)/EnsembleTree.yml
	$(PROG) --samerank="updateDecisionTreeNodeForNewSearch,generateDecisionTreeModel,getInitialStatusForDecisionTreeConstruction"   $^
	cp caus.gv.png $(decisionTreeDir)

decisionTree2Dir= DecisionTree2
decisionTree2: $(decisionTree2Dir)/EnsembleTree.yml
	$(PROG) --doit=each --gen_wf  $^
	$(PROG) --samerank="generateDecisionTreeModel"  $^
	cp caus.gv.png $(decisionTree2Dir)


PredictionAbilityDir = PredictionAbility
predictionAbility: $(PredictionAbilityDir)/*.yml
	$(PROG) $^
	cp caus.gv.png $(PredictionAbilityDir)
	
steepestDescentDir = SteepestDescent
steepestDescent: $(steepestDescentDir)/*.yml
	$(PROG) --doit=each --gen_wf $^
	$(PROG) --samerank="getStablePosition,getStablerPosition" $^
	cp caus.gv.png $(steepestDescentDir)

steepestDescent0Dir = SteepestDescent0
steepestDescent0: $(steepestDescent0Dir)/*.yml
	$(PROG) --samerank="initializePositionForceDatabase,getStablePosition,updatePositionForNewSearch" $^
	cp caus.gv.png $(steepestDescent0Dir)


logmeshDir = LogMesh
logMesh: $(logmeshDir)/*.yml
	$(PROG) --samerank="getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $^
	cp caus.gv.png $(logmeshDir)

logmesh0Dir = LogMesh0
logMesh0: $(logmesh0Dir)/*.yml
	$(PROG) --samerank="InitializeCounter,updateLoopCounterForNewExecution,getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $^
	cp caus.gv.png $(logmesh0Dir)


logmesh2Dir = LogMesh2
logMesh2: $(logmesh2Dir)/*.yml
	$(PROG) --samerank="getLogmeshValueSet,InitializeLogmeshValueDatabase,updateLogmeshSet" $^
	cp caus.gv.png $(logmesh2Dir)

logmesh3Dir = LogMesh3
logMesh3:  $(logmesh3Dir)/*.yml
	$(PROG) --doit=each --gen_wf $^
	$(PROG) --samerank="getAllLogmeshValues" $^
	cp caus.gv.png $(logmesh3Dir)


metropolisDir = Metropolis
metropolis: $(metropolisDir)/*.yml
	$(PROG) --doit=each --gen_wf $^
	$(PROG) --samerank="updateDatabase" $^
	cp caus.gv.png $(metropolisDir)

optDir = Optimization
optimization: $(optDir)/*.yml
	$(PROG) --samerank="getTheBestVariable,updateVariableForNewSearch" $^
	cp caus.gv.png $(optDir)

umldir= UMLbook
umlfig11_1: $(umldir)/fig11_1.yml
	$(PROG) $^
	cp caus.gv.png $(umldir)/fig11_1.png

umlfig11_5: $(umldir)/fig11_5.yml
	$(PROG) $^
	cp caus.gv.png $(umldir)/fig11_5.png

umlfig11_6: $(umldir)/fig11_6.yml
	$(PROG) $^
	cp caus.gv.png $(umldir)/fig11_6.png

umlfig11_11: $(umldir)/fig11_11.yml
	$(PROG) $^
	cp caus.gv.png $(umldir)/fig11_11.png

umlfig11_12: $(umldir)/fig11_12.yml
	$(PROG) $^
	cp caus.gv.png $(umldir)/fig11_12.png

umlfig16_1: UMLbook/fig16_1.yml 
	$(PROG) $^
	cp caus.gv.png $(umldir)/fig16_1.png

readBook2dir = readbook2
readBook2: $(readBook2dir)/readbook*.yml
	$(PROG) --doit=each --gen_wf --gen_taxo $^
	$(PROG) $^
	cp caus.gv.png $(readBook2dir)

clean:
	rm -f jupyter/*.gv jupyter/*.gv.png *.gv *.png
	rm -f Materials2/*.gv sample/*.gv.png 



