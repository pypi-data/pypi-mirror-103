import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requires = ['requests>=2.25.1']

setuptools.setup(
    name="pyrconsole",
    version="0.0.2",
    author="Guifang Zhou",
    author_email="guifang03@126.com",
    description="Python RConsole",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gzhou/pyrconsole",
    project_urls={
        "Bug Tracker": "https://github.com/gzhou/pyrconsole/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"pyr": "pyr"},
    packages=['pyr'],
    install_requires = requires,
    python_requires=">=3.6",
)