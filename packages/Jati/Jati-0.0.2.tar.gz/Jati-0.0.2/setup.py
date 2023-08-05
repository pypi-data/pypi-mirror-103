import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jati",
    version="0.0.2",
    author="Janoko",
    author_email="janoko@sandhika.com",
    description="Jati merupakan modul python untuk restAPI dan websocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghuvrons/Jati",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['jati=Jati.CLI:main'],
    },
    python_requires='>=3.7',
    install_requires=[
        "click>=5.1",
        "PyMySQL==1.0.2"
    ]
)

