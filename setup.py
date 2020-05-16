import setuptools

with open("README.md", "r") as file:
    readme_description = file.read()

setuptools.setup(
    name="File_convention-DEV-ONI", # Replace with your own username
    version="0.0.1",
    author="Matthew Gonzales",
    author_email="eng.matthew.gonzales@gmail.com",
    description="for testing",
    long_description=readme_description,
    long_description_content_type="text/markdown",
    url="github-repo-here",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
