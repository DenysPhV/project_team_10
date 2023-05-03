from setuptools import setup, find_namespace_packages

setup(
    name='project_team_10',
    version='1.0.8',
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
    entry_points={'console_scripts': ["StartBot=project_team_10.main:start"]}
    )