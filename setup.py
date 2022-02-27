from setuptools import setup

setup(
    name="ci-runner",
    version="0.1.0",
    description="General pipeline execution engine",
    python_requires=">3.6.0",
    # install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": ["ci=ci.cli:main"],
    },
)
