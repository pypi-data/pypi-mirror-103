from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Creates splash screens for GUIs'
with open("readme.md", "r") as fh:
    long_description = fh.read()
# Setting up
setup(
    name="tksplash",
    version=VERSION,
    author="MrHola21 (Gautam Singh)",
    author_email="projpy6969@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Guis', 'GUI', 'Gui', 'splash screen'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
