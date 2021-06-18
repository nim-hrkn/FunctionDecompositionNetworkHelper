PROG= ../../prog/cauFirst.py # --no_wf --no_taxo --no_connect_invis 

FILES =  top_taxo3.yml  top_wf3_whitebox_regressionmodel.yml


default:  MaterialExploration.png

MaterialExploration.png: $(FILES)
	$(PROG) --splines=true --samerank="Obtain updated material database,Obtain new materials with physical property values equal to or above the threshold value,Obtain new materials with physical property values below the threshold value" $^
	mv caus.gv.png descriptorTargetvariableRelation.png

workflow: $(FILES)
	for i in $^ ; do \
	$(PROG) --doit=each --gen_wf --gen_taxo $$i; \
	done

clean:
	rm -f *.png *.gv

