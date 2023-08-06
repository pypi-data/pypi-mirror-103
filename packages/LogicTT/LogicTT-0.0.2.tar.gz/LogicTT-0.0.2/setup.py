import setuptools

with open("README.md", "r", encoding="utf-8") as rm:
    README = rm.read()

setuptools.setup(
    name="LogicTT",
    packages=["LogicTT"],
    version="0.0.2",
    license="MIT",
    description="Logic Truth Table Generator",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Warith Adetayo",
    author_email="warithadetayo.awa@gmail.com",
    url="https://github.com/SpecialDude/LogicTT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3"
)
