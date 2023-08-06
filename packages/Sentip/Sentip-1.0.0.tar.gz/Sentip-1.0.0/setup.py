import setuptools
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
with open(f"{HERE}/README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Sentip",
    version="1.0.0",
    author="Panjapol Ampornratana",
    author_email="panjapol.pol@gmail.com",
    keywords = ['NLP', 'THAI'],
    description="Thai Social Data Sentiment Analysis",
    url = 'https://github.com/hhej/Sentip',
    long_description=long_description,
    install_requires=["numpy","pandas","tensorflow","keras","pythainlp","gensim"],
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=["Sentip", "Sentip.utility_data"],
    package_data={'Sentip': ['utility_data/**/*']},
    classifiers=[
        "Natural Language :: Thai",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.7'
)