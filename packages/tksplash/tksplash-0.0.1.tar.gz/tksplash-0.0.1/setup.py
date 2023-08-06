from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Creates splash screens for GUIs'
# Setting up
setup(
    name="tksplash",
    version=VERSION,
    author="MrHola21 (Gautam Singh)",
    author_email="projpy6969@gmail.com",
    description=DESCRIPTION,
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
