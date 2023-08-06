# Speedup-Work-Lib

This repo is a library for speed up work

## Useful command:

pip freeze > requirements.txt
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*

Copyright 2021
