from setuptools import setup, find_packages

classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education",
  "Operating System :: Microsoft :: Windows :: Windows 10",
  "License :: Apache License 2.0",
  "Programming Language :: Python :: 3"
]

setup(
    name="Encrypto",
    version="0.0.2",
    description="A Encryption/Decryption Library",
    py_modules=["Encrypto"],
    packages_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"]
)
