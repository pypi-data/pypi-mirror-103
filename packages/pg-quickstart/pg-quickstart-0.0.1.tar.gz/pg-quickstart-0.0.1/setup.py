from setuptools import setup, find_packages

setup(
    name="pg-quickstart",
    version="0.0.1",
    author="Jeremy Crow",
    author_email="jeremy.crow95@gmail.com",
    description="A collection of tools for students and beginner developers to setup, deploy and utilise a remote relational database",
    url="https://github.com/je-c/pg-quickstart",
    packages=find_packages(exclude=["tests*"]),
    package_data={"pixel_reshaper": ["data/*.csv"]},
    install_requires=["pandas", "psycopg2", "SQLAlchemy"],
    setup_requires=["wheel"],
    python_requires=">=3.6",
    license="MIT License",
    keywords=[
        "beginner databasing",
        "sql",
        "remote database",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Database :: Database Engines/Servers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
    ],
    #long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
)