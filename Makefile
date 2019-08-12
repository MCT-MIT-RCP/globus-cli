PYTHON_VERSION=python3
VIRTUALENV=.venv
CLI_VERSION=$(shell grep '^__version__' globus_cli/version.py | cut -d '"' -f2)

.PHONY: build release localdev test clean showvars help travis

help:
	@echo "These are our make targets and what they do."
	@echo "All unlisted targets are internal."
	@echo ""
	@echo "  help:      Show this helptext"
	@echo "  showvars:  Show makefile variables"
	@echo "  localdev:  Setup local development env with a 'pip install -e' and include dev tools"
	@echo "  test:      Run the full suite of tests on py2 and py3"
	@echo "  release:   Build, upload to pypi, and create a signed git tag"
	@echo "  clean:     Remove typically unwanted files, mostly from [build] and [test]"


showvars:
	@echo "CLI_VERSION=$(CLI_VERSION)"


$(VIRTUALENV):
	virtualenv --python=$(PYTHON_VERSION) $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip install -U pip setuptools
	$(VIRTUALENV)/bin/pip install 'tox<4'
	$(VIRTUALENV)/bin/pip install -e .
localdev: $(VIRTUALENV)

release: $(VIRTUALENV)
	$(VIRTUALENV)/bin/tox -e upload
	git tag -s "$(CLI_VERSION)" -m "v$(CLI_VERSION)"

# default for local testing
test: $(VIRTUALENV)
	$(VIRTUALENV)/bin/tox -e py2-lint,py3-lint,py2,py3

autoformat: $(VIRTUALENV)
	$(VIRTUALENV)/bin/tox -e autoformat

clean:
	-rm -r $(VIRTUALENV)
	-rm -r .tox
	-rm -r dist
	-rm -r build
	-rm -r *.egg-info
	find . -name '*.pyc' -delete
