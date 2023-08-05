from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="introduce",
    version="0.0.6",
    description="자기소개 라이브러리",
    license="GPL-V3",
    author="Jung Ji-Hyo",
    author_email="cord0318@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/cord0318/python_introduce",
    install_requires=["pillow"],
    packages=find_packages(),
    keywords=["korea", "auto", "pillow", "introduce", "introduction"],
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        #'Development Status :: 3 - Alpha',
        "Development Status :: 5 - Production/Stable",
    ],
)