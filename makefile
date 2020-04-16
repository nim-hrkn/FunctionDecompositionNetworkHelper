
Importance= sample/Importance_*.yml
AtomCrystTarget= sample/AtomCrystTarget_*.yml
TargetValuePrediction= sample/TargetValuePrediction_*.yml
Group= sample/Group_*.yml

PROG= prog/cauFirst.py

Importance:
	$(PROG) $(Importance)
AtomCrystTarget:
	$(PROG) $(AtomCrystTarget)
TargetValuePrediction:
	$(PROG) $(TargetValuePrediction)
Group:
	$(PROG) $(Group)


clean:
	rm -f sample/*.gv sample/*.png *.gv *.png
