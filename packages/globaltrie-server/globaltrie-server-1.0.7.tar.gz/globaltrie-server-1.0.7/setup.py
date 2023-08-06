from setuptools import setup, find_packages

setup(
    name='globaltrie-server',
    version='1.0.7',
    author="dajkatal",
    author_email="<dajkatal@gmail.com>",
    description="CLI to host Trie Server",
    long_description_content_type="text/markdown",
    long_description="CLI to host a server with the Trie data structure, allowing multiple clients to concurrently interact with it.",
    url="https://github.com/dajkatal/Global-Trie",
    packages=find_packages(),
    install_requires=['dill'],
    entry_points = {
        "console_scripts": ['trieserver = globaltrieserver.server_cli:main']
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