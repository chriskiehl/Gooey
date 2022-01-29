# Release Checklist 


 - [ ] Release commit is tagged 
 - [ ] The next release-branch is created 
 - [ ] CONTRIBUTING.md has been updated to point at the next release branch
 - [ ] Release is created on Github 
 - [ ] All tests pass on 2.7 and 3.x 
 - [ ] All warnings are resolved (run tests with `PYTHONWARNINGS=default`)
 - [ ] All Gooey Examples run and work as expected 
 - [ ] All new features have corresponding examples 
 - [ ] All new features have README updates 
 - [ ] Wx Inspection tool is removed from the runner
 - [ ] all debug prints removed  
 - [ ] setup.py version is updated 
 - [ ] __init__.py version is updated
 - [ ] types check (for the most part) `./venv/Scripts/python.exe -m mypy /path/to/python_bindings/types.py`
 - [ ] pip install of release branch works.   
     - [ ] All Gooey Examples run and work as expected
 - [ ] pypi is updated 
 - [ ] pypi pip install tested 2.7 & 3.x
     - [ ] All Gooey Examples run and work as expected
 - [ ] Release notes written: 
     - [ ] major features 
     - [ ] bug fixes
     - [ ] language additions
     - [ ] breaking changes  
     - [ ] contributors 
  


 
