
Importance= sample/Importance_*.yml
CrystalTarget= sample/CrystalTargetToDescriptor_*.yml
TargetValuePrediction= sample/TargetValuePrediction_*.yml
AtomicProperty= sample/AtomicProperty_Caus*.yml
Group= sample/Group_*.yml
MaterialsList= sample/MaterialsList_*.yml
AtomicCoordinate2Descriptor= sample/AtomicCoordinate2Descriptor_*.yml

PROG= prog/cauFirst.py --no_wf --no_taxo

Importance:
	$(PROG) $(Importance)
CrystalTarget:
	$(PROG) $(CrystalTarget)
TargetValuePrediction:
	$(PROG) $(TargetValuePrediction)
Group:
	$(PROG) $(Group)
AtomicProperty:
	$(PROG) $(AtomicProperty)
MaterialsList:
	$(PROG) $(MaterialsList)
AtomicCoordinate2Descriptor:
	$(PROG) $(AtomicCoordinate2Descriptor)


clean:
	rm -f sample/*.gv sample/*.png *.gv *.png
