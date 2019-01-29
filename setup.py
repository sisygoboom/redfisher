import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redfisher",
    version="1.1",
    author="@sisygoboom",
    author_email="chrisgraneyward@gmail.com",
    description="Find promising new steem users who are acting in ways that benefit the community.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sisygoboom/redfisher",
    packages=setuptools.find_packages(),
    install_requires=['beem==0.20.17', 'click'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)