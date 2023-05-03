from setuptools import setup, find_namespace_packages

setup(
    name='project_team_10',
    version='1.0.5',
    description='Package with scripts for using Bot assistant',
    url='https://github.com/DenysPhV/project_team_10',
    author='team-10',
    license="LICENSE",
    readme="README.md",
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
        ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ["StartBot=project_team_10.main:main"]}
    )