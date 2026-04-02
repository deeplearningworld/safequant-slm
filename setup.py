from setuptools import setup, find_packages

setup(
    name="safequant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["torch", "transformers", "bitsandbytes", "accelerate", "reportlab"],
    entry_points={"console_scripts": ["safequant=safequant.cli:main"]},
)