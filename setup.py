from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name='genehomology',
    version='0.1.0',
    description='batch cross-species homologous gene sequence alignment',
    long_description='A command-line tool for calculating BLAST homology scores between cross-species gene and protein sequences.',
    author='GeneHomology Team',
    author_email='guojing@ioz.ac.cn',
    url='https://github.com/JingGuo1997/GeneHomology',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'genehomology=genehomology.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    keywords='bioinformatics, gene, homology, blast, sequence-analysis',
) 