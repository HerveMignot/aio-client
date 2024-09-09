# How to build a pip install package

Instructions to build an installable package using pip. This is useful for sharing your package with others or for installing it on a different machine.


## Command to build the package

In the package root folder, use the following command:

```bash
$ pip install -q build
$ python -m build
```

This will create a `dist` folder with the package inside. The package will be named `<package_name>-<version>.tar.gz`. The version is specified in the `pyproject.toml` file.

### Use package file for installation

To install the package from the file, use the following command:	
```bash
$ pip install <package_name>-<version>.tar.gz
```

### Use git to install package

To install the package from a git repository, use the following command:
```bash
$ pip install git+https://github.com/<username>/<repo>.git@<branch>#egg=<package_name>
```


## Upload package to PyPI

A PyPI account is required. You can create one [here](https://pypi.org/account/register/).
To pusblish the package to PyPI, use the following command:

```bash
$ pip install -q twine
$ twine upload dist/*
```

