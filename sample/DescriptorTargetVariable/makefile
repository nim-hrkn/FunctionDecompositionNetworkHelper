PROG= ../../prog/cauFirst.py # --no_wf --no_taxo --no_connect_invis 

FILES = bottom_wf.yml  middle_taxo.yml  topmost_taxo.yml  topmost_wf.yml


default:  descriptorTargetvariableRelation.png

descriptorTargetvariableRelation.png: $(FILES)
	$(PROG) $^
	mv caus.gv.png descriptorTargetvariableRelation.png

workflow: $(FILES)
	for i in $^ ; do \
	$(PROG) --doit=each --gen_wf --gen_taxo $$i; \
	done

clean:
	rm -f *.png *.gv
