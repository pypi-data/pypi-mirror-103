import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="morpyengine",
    version="0.0.2",
    author="Morgiver",
    author_email="me@morgiver.net",
    description="A small SDL2 Graphic Engine to learn how it work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Morgiver/morpyengine",
    project_urls={
        "Bug Tracker": "https://github.com/Morgiver/morpyengine/issues",
    },
    install_requires=[
        'pysdl2',
        'pysdl2-dll'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)