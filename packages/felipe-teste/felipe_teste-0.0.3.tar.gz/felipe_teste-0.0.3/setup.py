from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ray", "NanoFilt"]

# teste
setup(
    name="felipe_teste",
    version="0.0.3",
    author="Felipe Marcelo",
    author_email="felipemarcelo@usp.br",
    description="A teste package",
    long_description=readme,
    url="https://github.com/sfmpds/felipe_teste/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
