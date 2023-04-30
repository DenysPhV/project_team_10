from setuptools import setup, find_namespace_packages
# Нужно доработать выкидывает ошибку "error in project-team-10 setup command: 'NoneType' object has no attribute 'group'"
setup(
    name='project-team-10',
    version='1.0.0',
    description='Package with scripts for using CLI Bot assistant',
    url='https://github.com/DenysPhV/project-team-10',
    author='team-10',
    # keywords="README.md",
    license="LICENSE",
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
        ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ["project-team-10=project-team-10.main:personal_assistant"]}
    )