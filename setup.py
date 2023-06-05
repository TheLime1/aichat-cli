import setuptools
from pathlib import Path

# note: build this package with the following command:
# pip wheel --no-deps -w dist .

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="aichat-cli",
    version="0.4.4",
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
    install_requires=[
        'argparse',
        'poe-api==0.4.4',
        'selenium',
        'pyperclip==1.8.2',
        'prompt_toolkit',
        'bardapi==0.1.11',
        'EdgeGPT==0.8.0'
    ],
    url="https://github.com/TheLime1/aichat-cli"
)
