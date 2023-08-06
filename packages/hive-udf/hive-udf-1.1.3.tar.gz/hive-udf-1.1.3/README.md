# hive-udf

Hive UDF (user-defined functions) in Python.

This package provides a single function `make_udf` for
working with Hive UDF written in Python.
Please see the source code for documentation.

[This blog post](https://zpz.github.io/blog/hive-udf/) describes how the code arrived at the current shape after addressing multiple very tricky problems. If you want to understand the code, read this post.

Some test code is included, along with several example UDF modules, which are used in the tests. The user is encouraged to run these tests in their Hive setup to confirm that things work as expected.

This package is ready for production use.