from setuptools import setup, find_packages

setup(
    long_description=open("README.md", "r").read(),
    name="npynx",
    version="1.0",
    description="web server",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/npynx",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords="web server",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'npynx = npynx.__main__:main'
        ]
    },
    install_requires=[
        "http_parser", "twisted", "jinja2"
    ],
    long_description_content_type="text/markdown"
)
