from setuptools import setup,find_packages

setup(
    name='userElainaTestSetup1',
    version='1.2.0',
    description='Some small tols like syntactic sugar.',
    py_modules=['userElainaTestSetup2'],
    # ckages=find_packages(exclude=['contrib','docs','tests']),

    long_description='',
    author='userElaina',
    author_email='userElaina@google.com',
    url='https://github.com/userElaina',
    classifiers=[
        # 'Development Status :: 1 - Test',
        # 'Intended Audience :: Saya',
        # 'License :: OSI Approved :: 996 License',
        'Programming Language :: Python :: 3',
        # 'Operating System :: Windows 11',
    ],
    keywords='qwq saya elaina test',
    install_requires=[
		'Pillow',
	],
    package_data={
        'userElainaTestSetup2': ['2.txt'],
    },
    # data_files=[
	# 	('userElainaTestSetup2', []),
	# ],
    python_requires='>=3.6',
)