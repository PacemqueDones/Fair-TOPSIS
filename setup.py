from setuptools import setup, find_packages

setup(
    name="fair-topsis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "matplotlib"
    ],
    description="Framework para seleção de modelos fair utilizando TOPSIS",
    author="Anderson Lucas de Paula Costa",
)