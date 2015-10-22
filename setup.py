from setuptools import setup

setup(
    name='namesparser',
    version='1.0.0',
    url='https://github.com/gwu-libraries/namesparser',
    author='Justin Littman',
    author_email='justinlittman@gmail.com',
    py_modules=['namesparser'],
    description="Complement to nameparser for parsing lists of names.",
    platforms=['POSIX'],
    test_suite='tests',
    install_requires=['nameparser'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
    ],
)
