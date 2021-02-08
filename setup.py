from setuptools import setup, find_packages

setup(
    name="a2t",
    use_scm_version=True,
    packages=['a2t'],
    setup_requires=["setuptools_scm"],
    install_requires=[],
    python_requires=">=3.7.0",
)
