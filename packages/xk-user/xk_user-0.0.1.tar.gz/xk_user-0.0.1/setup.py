from setuptools import setup, find_packages

setup(
    name="xk_user",
    version="0.0.1",
    description="xing kuang SDK",
    long_description="eds sdk for python",
    license="MIT Licence",

    url="http://test.com",
    author="zhanglei",
    author_email="test@gmail.com",

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["protobuf==3.15.8",
                      "grpcio==1.37.0",
                      "grpcio-tools==1.37.0",
                      "six==1.15.0"],

    scripts=[],

)
