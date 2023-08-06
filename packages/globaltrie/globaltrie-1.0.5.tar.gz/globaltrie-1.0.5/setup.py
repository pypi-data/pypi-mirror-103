from setuptools import setup, find_packages

setup(
    name='globaltrie',
    version='1.0.5',
    author="dajkatal",
    author_email="<dajkatal@gmail.com>",
    description="Client to access server Trie",
    long_description_content_type="text/markdown",
    long_description="A client that lets you access and interact with a Trie hosted on a server.",
    url="https://github.com/dajkatal/Global-Trie",
    packages=find_packages(),
    entry_points = {
        "console_scripts": ['globaltrie = globaltrie.client_cli:main']
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)