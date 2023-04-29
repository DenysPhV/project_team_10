from setuptools import setup, find_namespace_packages

setup(
    name='project-team-10',
    version='1.0.0',
    description='Package with scripts for using CLI Bot assistant',
    url='https://github.com/DenysPhV/project-team-10',
    author1='outgoing_team',
    readme="README.md",
    license="LICENSE",
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
        ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ["CLIbot=project-team-10.main:personal_assistant"]}
    # CLIbot - command that shall be executed in the terminal
    # after "=" - the path to the file where the function is located -> goit_team5_personal_assistant.main
    # after ":" - the function that shall be performed -> personal_assistant
    )