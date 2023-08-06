from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ocitoollib',
    package_dir={"":"."},
    packages=find_packages(where="."),
    version='0.2.0',
    description='ocitool Python library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='James Jeong',
    author_email='james1.jeong@gmail.com',
    license='MIT',
    install_requires=['oci'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    python_requires=">=3.6",
)
