import os

import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="pyrefinebio",
    version=os.getenv("VERSION"),
    author="Childhood Cancer Data Lab",
    author_email="ccdl@alexslemonade.org",
    description="A python client for the refine.bio API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexsLemonade/refinebio-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",  # not sure if this is actually true - we should probably test on windows!
    ],
    python_requires=">=3.6",
    install_requires=["iso8601", "PyYAML", "requests", "Click", "pytimeparse"],
    entry_points="""
        [console_scripts]
        refinebio=pyrefinebio.script:cli
    """,
)
