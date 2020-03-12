# coding=utf-8

import io
import re
from setuptools import (
    setup,
    find_packages,
)


EXTRAS_REQUIRE = {
    "tests": [
        "pytest==5.2.1",
        "pytest-cov==2.8.1"
    ],
    "lint": [
        "pylint==2.4.2",
    ]
}

EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"]


with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("src/marshoas/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="marshoas",
    version=version,
    long_description=readme,
    author="Nguyen Khac Thanh",
    author_email="nguyenkhacthanh244@gmail.com",
    url="https://github.com/nkthanh98/marshoas",
    packages=find_packages("src", exclude=["test*", "examples"]),
    package_dir={"": "src"},
    extras_require=EXTRAS_REQUIRE,
    license="MIT",
    python_requires=">=3.5",
    test_suite="tests"
)
