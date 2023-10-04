import setuptools


setuptools.setup(
    name='negate_hypnotic',
    version='1.0.1',
    author='RimoChan',
    author_email='the@librian.net',
    description='librian',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/negate_hypnotic',
    packages=[
        'negate_hypnotic',
    ],
    package_data={
        'negate_hypnotic': ['web/*']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=open('requirements.txt', encoding='utf8').read().splitlines(),
    python_requires='>=3.7',
)
