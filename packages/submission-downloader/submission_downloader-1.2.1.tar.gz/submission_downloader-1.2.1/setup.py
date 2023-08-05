import setuptools

with open("README.md", "r") as fh:
    long_description_md = fh.read()

setuptools.setup(
    name="submission_downloader",
    version="1.2.1",
    author="Anthony Chen",
    description="Downloads your submissions in bulk from the DMOJ website and any compatible forks.",
    long_description=long_description_md,
    long_description_content_type="text/markdown",
    url="https://github.com/slightlyskepticalpotat/submission-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.22.0",
    ],
    python_requires='>=3.8',
)

