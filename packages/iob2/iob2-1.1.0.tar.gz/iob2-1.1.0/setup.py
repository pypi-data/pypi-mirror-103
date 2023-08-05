import ezpip
from setuptools import setup

with ezpip.packager(develop_dir = "./_develop_iob2") as p:
    setup(
        name = "iob2",
        version = "1.1.0",
        description = "A library for manipulating, loading, and saving corpus in iob2 format.",
        author = "bib_inf",
        author_email = "contact.bibinf@gmail.com",
        url = "https://github.co.jp/",
        packages = p.packages,
        install_requires = ["relpath", "sout", "seqeval==0.0.12"],
        long_description = p.long_description,
        long_description_content_type = "text/markdown",
        license = "CC0 v1.0",
        classifiers = [
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries',
            'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
        ]
    )
