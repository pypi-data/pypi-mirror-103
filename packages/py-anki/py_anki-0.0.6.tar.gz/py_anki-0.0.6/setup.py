import pathlib
from setuptools import setup, find_packages

CURRENT_PATH = pathlib.Path(__file__).parent
VERSION = '0.0.6' 
DESCRIPTION = 'A simple API for Anki Spaced Repetition'
LONG_DESCRIPTION = (CURRENT_PATH / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

# Setting up
setup(
        name="py_anki", 
        version=VERSION,
        author="Abu Bakar Siddique Arman",
        author_email="arman.bhaai@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESC_TYPE,
        packages=find_packages(),
        download_url="https://pypi.org/project/py-anki/#files",
        url="https://github.com/arman-bhaai/py-anki",
        install_requires=[
            "requests",
        ], 
        license="Custom License",    
        keywords=["py-anki", "py anki", "python","ankiconnect", "python anki","anki api", "arman_bhaai", "arman-bhaai", "Abu Bakar Siddique Arman"],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)