import setuptools

setuptools.setup(
    name='userElainaTestSetup1',
    version='1.6.0',
    description='Some small tols like syntactic sugar.',
    # py_modules=['userElainaTestSetup1'],
	packages=['userElainaTestSetup1'],
    # ckages=find_packages(exclude=['contrib','docs','tests']),

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