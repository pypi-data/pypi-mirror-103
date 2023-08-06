import setuptools

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "README.md not found."

setuptools.setup(
    name="python_console_creator",
    version="1.0.2",
    author="megat69",
    description="Makes creating a console a simple task !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/megat69/Lib_ConsoleCreator",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)