# Minimal makefile for Sphinx documentation
#

# https://github.com/deepcharles/ruptures/pull/26

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    =
SPHINXBUILD   = python3 -msphinx
SPHINXPROJ    = mozhi
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

docs:
	mkdir -p source/mozhi/
	touch source/mozhi/temp.rst
	rm source/mozhi/*.rst
	sphinx-apidoc -E -M -d 2 -f ../mozhi/ -o source/mozhi/
	cd source/mozhi/ && sed -i '' -e 's/ package//g' *
	cd source/mozhi/ && sed -i '' -e 's/Submodules//g' *
	cd source/mozhi/ && sed -i '' -e 's/Subpackages//g' *
	@make clean
	@make html
	git add -f build/
	git add .
