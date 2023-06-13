import setuptools
from pathlib import Path

# note: build this package with the following commands: #TODO: automate this
'''
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
'''
base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text(encoding="utf-8")

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="aichat-cli",
    version="0.4.7",
    author="TheLime1",
    license="GPLv3",
    description="A CLI app that allows you to have interactive conversations with different AI bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    url="https://github.com/TheLime1/aichat-cli"
)
