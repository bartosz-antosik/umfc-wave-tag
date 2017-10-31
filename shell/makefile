#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

PROJECT=w2tshell

#------------------------------------------------------------------------------
# tools
#------------------------------------------------------------------------------

FPCROOT=/bin/lazarus

FCC=fpc
FCCUNITS= \
	-Fu$(FPCROOT)/lcl/units/x86_64-win64/win32 \
	-Fu$(FPCROOT)/lcl/units/x86_64-win64 \
	-Fu$(FPCROOT)/components/lazutils/lib/x86_64-win64
FCCFLAGS=-CX -Xs -XX -WG $(FCCUNITS) -FU$(PATH_OBJ) -FE$(PATH_EXE)

RCC=windres
RCCFLAGS=

VERSIONTOOL=vertool
VERSIONFILE=version.xml

PATH_LPR=
PATH_OBJ=$(PATH_LPR)obj/
PATH_EXE=$(PATH_LPR)

#------------------------------------------------------------------------------
# private targets
#------------------------------------------------------------------------------

%.exe %.dll: %.res .FORCE
	$(FCC) $(FCCFLAGS) $*.lpr

%.rc2: %.rc $(VERSIONFILE)
	$(VERSIONTOOL) substitute $(VERSIONFILE) -len $*.rc $*.rc2

%.res: %.rc2
	$(RCC) $(BRCCFLAGS) $*.rc2 $*.res

.PHONY: .FORCE

.FORCE:

#------------------------------------------------------------------------------
# public targets
#------------------------------------------------------------------------------

default: initialize clean version build finalize

initialize:
	-mkdir -p $(PATH_OBJ) 2> /dev/null
	-mkdir -p $(PATH_EXE) 2> /dev/null

finalize:

clean:
	-rm -f $(PATH_OBJ)/* 2> /dev/null

version:
	-$(VERSIONTOOL) assign --build-date $(VERSIONFILE) `date +%Y%m%dT%H%M%S`
	-$(VERSIONTOOL) increment --version-revision $(VERSIONFILE)

build: $(PROJECT).res $(PROJECT).exe
