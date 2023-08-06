from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="urlshrink",
    version="0.54",
    description="url smallifier",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/urlshrink",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords="smoll url bean",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'urlshrink = urlshrink.__main__:main'
        ]
    },
    install_requires=[
        "loguru", "dataset", "flask", "hashids", "qrcode[pil]"
    ],
    package_data={
        "urlshrink": ["templates/*.html"]
    },
    long_description_content_type="text/markdown"
)
