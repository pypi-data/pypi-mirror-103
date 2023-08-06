# Ezpub [cli-environment]
## Tool to help developer to publish package to PyPI
### [Beta-development]

## Installation
```
pip3 install Ezpub-karjakak
```
## Usage
**Create token for variable environment and save it for publish with twine [token key-in in tkinter simpledialog for showing in hidden].**
```
ezpub -t None
```
**Delete saved token.**
```
ezpub -t d
```
**Create save token.**
```
ezpub -t %VARTOKEN%
```
**Building the package and create [build, dist, and package.egg-info] for uploading to PyPI.**  
```
ezpub -b "\package-path"
```
**TAKE NOTE:**
* **Ezpub will try to move existing [build, dist, and package.egg-info] to created archive folder and create new one.**
    * **If Exception occured, user need to remove them manually.**   

**Pubish to PyPI.**
```
ezpub -p "\package-path\dist\*"
```
**TAKE NOTE:**
* **If token is not created yet, it will start process "-t" automatically.**

## Links
* **https://packaging.python.org/tutorials/packaging-projects/**
* **https://twine.readthedocs.io/en/latest/**