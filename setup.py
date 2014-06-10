from distutils.core import setup

setup(
    name="Python Brandstem",
    version="1.0",
    packages=['PythonBrandStem','PythonBrandStem.client'],
    license="MIT",
    requires=['requests(>=1.0,<3.0)'],
    install_requires=['requests>=1.0,<3.0'],
)
