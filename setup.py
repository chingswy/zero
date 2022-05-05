import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myzero",
    version='0.0.0',
    author="Qing Shuai",
    author_email="s_q@zju.edu.cn",
    url="https://github.com/chingswy/myzero",
    description="Automatic record your paper reading list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'zero=zero.cli:add',
            'zero-a=zero.cli:add',
            'zero-f=zero.cli:find',
            'zero-arxiv=zero.cli:clean_compile_arxiv',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)