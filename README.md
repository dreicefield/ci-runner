# Overview
Tool to run workflows/pipelines on your local machine

# Limitations (There is many of them as this is still work in progress)
- Only Jenkinsfiles in .yaml format are supported at the moment
- Jenkinsfile support is still very limited, e.g.
- - default environment variables are not created or passed to runners
- - no support for credentials
- - only one global agent is supported (no local stage agents)
-
