from setuptools import setup, find_packages

setup(
    name="a2t",
    use_scm_version=True,
    packages=find_packages(".", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    setup_requires=["setuptools_scm"],
    install_requires=[],
    python_requires=">=3.7.0",
)
