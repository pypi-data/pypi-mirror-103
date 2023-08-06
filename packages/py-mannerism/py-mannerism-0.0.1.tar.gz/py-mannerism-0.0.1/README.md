# Python Library

This project consists of code for creating minimal python library and deploying it to Pypi.

## Operating on This Library

### Installing and Using Library

#### Installing

You can simply run this command to install this library:

`pip install py-mannerism`

or add the library to requirements.txt:

`py-mannerism=0.0.1`

#### Using the library

You can use the library with this code (remember, that this is not real solving-problem library).

```python
from pylib.commons import Mannerism

mannerism = Mannerism('Unis Badri')

print(mannerism.create())
```

it will show this text:

`Hi Unis Badri, how are you today?`

### Developing with Library

This library is intended to fasten the library development, you can look at this as starter kit for library development. So you can add you own structure and library and doing your own library development on it.

These are some useful information when developing library with this repository.

#### Running Unit Test

`pytest`

#### Running Code Coverage

`pytest --cov-report html --cov-report term --cov=pylib tests/`

#### Running Static Analysis

To run static analysis using flake8, run this command:

`flake8 --config=.flake8 --count --statistics pylib/`

#### Adding Status Check for Pull Request

You can add status check to the target branch on Pull Request in the .github/workflows/onpush-ci.yml. The name of the workflow Status Checks will be:

```
build-ci (3.6)
build-ci (3.7)
build-ci (3.8)
```

Please refer to github documentation to create status check in github repository.

## Other Library Project

I create other library projects in various programming language. The purpose of these projects are to ease engineers to create their own library.

- [Python Library](https://github.com/namikazebadri/PythonLibrary)
- [Ruby Library](https://github.com/namikazebadri/RubyLibrary)
- [Java Library](https://github.com/namikazebadri/JavaLibrary)
- [Node Library](https://github.com/namikazebadri/NodeLibrary)
- [PHP Library](https://github.com/namikazebadri/PHPLibrary)
- [Go Library](https://github.com/namikazebadri/GoLibrary)
- [Rust Library](https://github.com/namikazebadri/RustLibrary)
- [Elixir Library](https://github.com/namikazebadri/ElixirLibrary)

Any suggestions can be sent to my email at [unis.badri@elementcreativestudio.com](mailto:unis.badri@elementcreativestudio.com) or [uzumaki.unis@gmail.com](mailto:uzumaki.unis@gmail.com).