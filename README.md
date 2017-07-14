# conda-forge migration

This repo contains some data that might be useful for migrating to
conda-build-3. Specifically we (conda-forge) should find all of our pure Python
packages and rebrand them as "noarch" python packages. "noarch" packages are
platform and (python) version independent. If we use noarch packages for our pure python packages then we will then require 1/9 of the build time for these packages and we won't clog travis-ci any more than it has to! (Among many other benefits)

## Files in this repo

``find_compiled.py`` Script that I run on my machine where I have a mirror of the conda-forge channel

**csv files**. Files that should be loaded into a pandas dataframe with
``pd.read_csv()``. They contain these three columns: an index, "ext" and "name". 

* ``name``: The name of the conda package
* ``ext``: The set of file extensions that are contained in the conda package
* ``""``: The index that I should have deleted before saving these to csv ¯\_(ツ)_/¯
