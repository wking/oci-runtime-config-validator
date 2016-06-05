OCI Runtime Configuration Validator
===================================

Validate configurations against the
[Open Container Runtime Specification][runtime-spec].

Install dependencies with:

```sh
$ pip3 install --user -r requirements.txt
```

Run the tests with:

```sh
$ BUNDLE=/path/to/bundle python3 -m unittest -v
```

[runtime-spec]: https://github.com/opencontainers/runtime-spec
