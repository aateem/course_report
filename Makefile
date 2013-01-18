# set TARGET to the name of the main file without the .tex
# (the default value 'document' is overridden by the command line value)
TARGET=main

# latex output filetype (pdf or dvi)
OUTPUT = pdf

# directory for latex auxiliary and temporary files
AUX_DIR = temp

PARAMS = --output-directory=$(AUX_DIR) --output-format=$(OUTPUT)
TEX = pdflatex $(PARAMS)
# directories and files to exclude from compressing into tar
EXCLUDE_PATTERN = --exclude=$(AUX_DIR) --exclude=graphics

makedoc :
	mkdir -p $(AUX_DIR)
	# check for bibliography file and execute bibtex if needed
	@if [ -f *.bib ] ; \
		then echo "processing bibliography..." ; \
		$(TEX) $(TARGET).tex ; bibtex $(AUX_DIR)/$(TARGET) ; $(TEX) $(TARGET).tex \
		else echo "no bibliography found." ; \
		fi
	# run latex several times until all references are resolved from *.aux files
	@echo "rebuilding until all references resolved..."
	@while ($(TEX) $(TARGET).tex ; \
		grep -q "Rerun to get cross" $(AUX_DIR)/$(TARGET).log ); do true; \
		done
ifeq ($(OUTPUT), 'dvi')
	@mv $(AUX_DIR)/$(TARGET).dvi ./
	@dvips $(TARGET).dvi
	@ps2pdf $(TARGET).ps
else
	@mv $(AUX_DIR)/$(TARGET).pdf ./
endif

clean :
	rm -r $(AUX_DIR)

cleanall :
	rm -r $(AUX_DIR) *.pdf *.ps *.dvi *.tar.gz

# create compressed archive with complete file set
# (tex, styles, bibliography and final documents)
tarball:
	tar -czvf $(TARGET).tar.gz $(EXCLUDE_PATTERN) * 