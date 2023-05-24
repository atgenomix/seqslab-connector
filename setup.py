#!/usr/bin/env python3

from setuptools import setup
import seqslab


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name="seqslab-connector",
    version=seqslab.__version__,
    description="Atgenomix SeqsLab Connector for Python",
    long_description=long_description,
    url="https://github.com/atgenomix/seqslab-connector",
    author="Allen Chang",
    author_email="allen.chang@atgenomix.com",
    license="Apache License, Version 2.0",
    packages=["seqslab", "seqslab.sqlalchemy", "seqslab.superset"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Database :: Front-Ends",
    ],
    install_requires=[
        "pyhive",
        "thrift",
    ],
    extras_require={
        "sqlalchemy": ["sqlalchemy>=1.3.0"],
        "superset": ["superset>=2.0.1"],
    },
    tests_require=[],
    cmdclass={},
    package_data={
        "": ["*.rst"],
    },
    entry_points={
        "sqlalchemy.dialects": [
            "seqslab.hive = seqslab.sqlalchemy.hive:SeqsLabHiveDialect",
        ],
        "superset.db_engine_specs": [
            "seqslab = seqslab.superset.seqslab:SeqsLabHiveEngineSpec",
        ],
    }
)
