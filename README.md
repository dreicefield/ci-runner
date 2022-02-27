# Overview
Tool to run workflows/pipelines on your local machine

# Usage
```shell
> git clone https://github.com/dreicefield/ci-runner.git
> cd ci-runner

# install the project to your local python installation (or do install it globally)
> python3 setip.py install --user

> ci run jenkins --help
Usage: ci run jenkins [OPTIONS]

  Runs jenkinsfile

Options:
  --file TEXT  Jenkinsfile as YAML  [required]
  --help       Show this message and exit.

# Sample usage
> ci run jenkins --file path/to/jenkinsfile.yaml
```


# Limitations (There is many of them as this is still work in progress)
- Only Jenkinsfiles in .yaml format are supported at the moment
- Jenkinsfile support is still very limited, e.g.
- - default environment variables are not created or passed to runners
- - no support for credentials
- - only one global agent is supported (no local stage agents)
-
