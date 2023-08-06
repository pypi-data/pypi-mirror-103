from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name='universities_exercise_api_v1',
    version='0.0.3',
    description='A simple api for working with universities data',
    py_modules=['universities_api', 'requests_utils'],
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=['requests>=2.25.1'],
    url='https://github.com/omerl2322/pip_package_exercise',
    author='Omer Levy',
    author_email='omerl2322@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown'

)
