import setuptools

setuptools.setup(
    name='userElainaTestSetup1',
    version='1.8.1',
    description='Some small tols like syntactic sugar.',
    py_modules=['aaa'],
	# packages=['userElainaTestSetup1'],   
	packages=setuptools.find_packages(),
    # ckages=setuptools.find_packages(exclude=['qwq2']),

    long_description='',
    author='userElaina',
    author_email='userElaina@google.com',
    url='https://github.com/userElaina',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='qwq saya elaina test',
    install_requires=[
		'Pillow',
	],
    package_data={
        'userElainaTestSetup1': ['1.txt'],
    },
    # data_files=[
	# 	('userElainaTestSetup2', []),
	# ],
    python_requires='>=3.6',
)