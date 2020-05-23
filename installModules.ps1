# create virtual environment to avoid polluting global namespace
py -m venv .venv

# activate environment
.venv/Scripts./Activate.ps1

# install modules
pip install 'wheel==0.34.2'
pip install 'networkx==2.4'
pip install 'matplotlib==3.2.1'
pip install 'gitpython==3.1.2'
pip install 'requests==2.23.0'
pip install 'pyyaml==5.3.1'
pip install 'progress==1.5'
pip install 'strsimpy==0.1.4'
pip install 'python-dateutil==2.8.1'