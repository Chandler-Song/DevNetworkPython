# General Notes

## Stack
- Windows 10
- VSCode 1.45.1
- PowerShell 7.0.1
- Python 3.8.3
- PIP 20.1

## Python Modules
Modules can be be installed by running **installModules.ps1** in PowerShell. This will create an embedded **venv** environment and install all necessary modules with correct versions without polluting the global namespace.

# Running
To run the tool you need to setup a configuration file **[something].yml** and run **main.py** with the **-c** or **--config** parameter pointing to the physical location of the configuration file.

An example configuration file using the explained parameters and values below is included in the repository.

*$ python main.py -c config.yml*

## Configuration

#### repositoryUrl (str)
The URL to the GitHub repository you want to analyse.  
*Ex: "https://github.com/eclipse/rt.equinox.bundles"*

#### repositoryShortname (str)
The user/project part of the repository URL. Must be exact.  
*Ex: "eclipse/rt.equinox.bundles"*

#### repositoryPath (str)
The physical path to the local clone of the repository.
If the directory does not exist, it will be created and the repository will be automatically cloned to this path.   
*Ex: "D:\Repos\rt.equinox.bundles"*

#### analysisOutputPath (str)
The physical path to the desired output directory.  
*Ex: "D:\Repos\analysisOutput\eclipse-rt.equinox.bundles"*

#### aliasPath (str)
The physical path to the list of author aliases.  
*Ex: "D:\Repos\analysisOutput\aliases\eclipse-rt.equinox.bundles.yml"*

#### aliasSimilarityMaxDistance (float)
For documentation on changing this value see:  
https://github.com/luozhouyang/python-string-similarity#metric-longest-common-subsequence  
*Ex: 0.25*