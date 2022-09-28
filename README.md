# error-code-tools
## How to clone?
Since there is a xcal-common submodule, after you clone error-code-tools, you still need to clone submodule by following command:
```bash
cd error-code-tools
git submodule init
git submodule update
```

## How to use this tool?
Prerequisites:
- Install Qt5
- ```export PYTHONPATH="$(pwd)"``` to make sure the PYTHONPATH is pointing to src root, or ```common``` module won't be located

1. Use UI to output errorMessage.json file.
2. Use generatePyErrorFile command line to generate python error file 'error.py'. For example:
```bash
python3 generatePyErrorFile.py <path to errorMessage.json>
```
3. Put error-code-tools artifacts errorMessage.json and error.py into xcal-common directory(submodule).
There are two test cases in xcal-common/py directory. 
test_error.py can be used to check whether the error.py file is ok. 
test_utils.py can be used to check error.py, utils.py and errorMessage.json is ok. 
If test failed, check the error messages and scripts to check what happens. May fix the problems by hand or improve the program.
For now, test_error.py will always fill since the input has some problems. You need to comment the invalid error code items in error.py by hand.
For example:
```bash
python3 <path to test_error.py>
python3 <path to test_utils.py>
```

