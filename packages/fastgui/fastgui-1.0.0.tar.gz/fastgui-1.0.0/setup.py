import setuptools

setuptools.setup(
    name='fastgui',
    version='1.0.0',
    description='Gui tool to test py programs.',
    py_modules=['fastgui'],
	packages=setuptools.find_packages(),

    long_description='',
    author='userElaina',
    author_email='userElaina@google.com',
    url='https://github.com/userElaina',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='gui elaina fast',
    install_requires=[
		'tk',
	],
    package_data={
        'fastgui': ['1.ico'],
    },
    python_requires='>=3.6',
)