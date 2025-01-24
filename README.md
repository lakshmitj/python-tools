# python-tools
python tools

# Virtualenv and requirements.txt
When setting up a new project, list out the Python dependencies in a requirements.txt file, including the version numbers. Commit this file to the repository, so that every new user can replicate the environment your codebase needs to run in.

Users can create a new environment by using virtualenv:

```
# This creates the virtual environment
cd $PROJECT_PATH
virtualenv production-tools

```

and then install the dependencies by referring to the requirements.txt:

```
# This installs the modules
pip install -r requirements.txt

# This activates the virtual environment
source python-tools/bin/activate

```