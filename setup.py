from setuptools import setup, find_namespace_packages

setup(
    name='StartBot',
    version='1.0.9',
    description='Package with scripts for using Bot assistant',
    url='https://github.com/DenysPhV/project_team_10',
    author='team_10',
    license="LICENSE",
    readme="README.md",
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
        ],
    packages=find_namespace_packages(),
    install_requires=['termcolor', 'colorama', 'Pillow'],
    entry_points={'console_scripts': ["StartBot=project_team_10.main:start"]},
    include_package_data=True
    )