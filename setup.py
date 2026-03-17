from setuptools import setup, find_packages

setup(
    name="fair-topsis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20"
    ],
    include_package_data=True,
    description="Framework para seleção de modelos fair utilizando TOPSIS",
    author="Anderson Lucas de Paula Costa",
)