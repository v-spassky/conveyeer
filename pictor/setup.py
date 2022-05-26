import setuptools

"""
Executed via 'pip install -e .' in same directory.
"""

if __name__ == "__main__":
    setuptools.setup(
        name='pictor',
        version='1.0',
        packages=setuptools.find_packages(),
        install_requires=['Pillow', 'pyyaml', 'pyx'],
    )
