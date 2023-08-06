import setuptools

long_description = """
Q. What is Yokaranda?
A. See yokaranda.com
"""

# see https://packaging.python.org/specifications/core-metadata/
setuptools.setup(
    name="yokr",
    version="0.3.02",
    author="Gadi Solotorevsky",
    author_email="gadi.solotorevsky@yokaranda.com",
    description="A client for Yokaranda SaaS",
    long_description=long_description,
    long_description_content_type='text/plain',
    license='BSD-3-Clause',
    url="https://yokaranda.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[           
        'requests',
      ],
    package_data={
        '': ['README.md', 'dev_requirements.txt', 'yokr/create_tables.sql']
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
