from setuptools import setup, find_packages

setup(
    name="ci-runner",
    version="0.1.0",
    description="General pipeline execution engine",
    python_requires=">3.6.0",
    packages=find_packages(where="src"),
    package_dir={'': "src"},
    include_package_data=True,
    install_requires=[
        "click==7.1.2",
        "networkx==2.5.1",
        #"pyyaml==5.2",
    ],
    entry_points={
        "console_scripts": ["ci=ci.cli:main"],
    },
    url='https://github.com/dreicefield/ci-runner',
)
