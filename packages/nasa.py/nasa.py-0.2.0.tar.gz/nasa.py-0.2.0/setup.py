from setuptools import setup, find_packages
import os


extras_require = {
    'speedups': ['aiohttp[speedups]'],
}




DESCRIPTION = "An async ready wrapper for the NASA Open API's"

# Setting up
setup(
    name="nasa.py",
    version="0.2.0",
    author="quiktea",
    author_email="wishymovies@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(),
    extras_require = extras_require,
    install_requires=['aiohttp'],
    keywords=['python', 'nasa', 'api', 'mars', 'rover'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        "GitHub" : "https://github.com/quiktea/nasa.py"
    }
)