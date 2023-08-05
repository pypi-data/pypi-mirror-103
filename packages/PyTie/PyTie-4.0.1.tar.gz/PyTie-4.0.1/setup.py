import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyTie", 
    version="4.0.1",
    author="Raquel Theodoro Amancio da Silva",
    author_email="ratheodoro@gmail.com",
    description="Well tie in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raquelsilva/pytie",
    packages=["pytie"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
   	    "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.7',
    install_requires = [
        "numpy",
        "lasio",
        "pandas",
        "matplotlib",
        "scipy",
        ]
)