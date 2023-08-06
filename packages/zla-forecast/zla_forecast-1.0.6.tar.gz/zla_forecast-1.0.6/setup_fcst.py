import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zla_forecast", # Replace with your own username
    version="1.0.6",
    author="zlakeaw",
    author_email="zla.naratip@gmail.com",
    description="zla_fcst for get picture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['numpy','pandas','pyodbc','datetime',''],
    python_requires='>=3.6',
)