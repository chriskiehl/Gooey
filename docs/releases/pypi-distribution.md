# Testing PyPi distribution before upload

The release workflow now builds and uploads Gooey to PyPI when a version tag is pushed (see the release checklist in [.github/ISSUE_TEMPLATE/release_checklist.md](../../.github/ISSUE_TEMPLATE/release_checklist.md)). The steps below are for checking a build locally.

The 1.0.4 release was botched when uploading to PyPi as it pulled in the 1.0.3 artifacts sitting in my dev directory.  This meant that the 1.0.4 version was now clobbered on PyPi and could no longer be used. More care is needed when deploying. 


### How to test locally before uploading

1\. build the wheel

```
python -m build
``` 

this will output the wheel to the `dist/` directory. 

2/. Copy the file location. 

Copy the absolute path to the .gz output file. It will look something like this:  

```
dist/Gooey-1.0.4.tar.gz
```

3\. In a different virtual environment, install the local wheel 

```
cd ~/projects/GooeyExamples
virtualenv venv 
source ./venv/Scripts/activate
pip install /path/to/local/dist/Gooey-1.0.4.tar.gz
``` 

If everything installs OK, you're good to upload.

```
twine upload dist/*
```

 