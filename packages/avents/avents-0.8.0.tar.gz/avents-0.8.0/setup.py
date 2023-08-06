#!/Users/sam/PycharmProjects/avents/venv/bin/python

from setuptools import setup

setup(
    name="avents",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    version=open("VERSION", "r").read(),
    packages=["avents"],
    python_requires=">=3.9",
    license_files=("LICENSE",),
    include_package_data=True,
    zip_safe=True,
    include_dirs=False,
    url="https://gitlab.cloud-technology.io/Open-Source/async-events",
    project_urls={
        "Documentation": "https://gitlab.cloud-technology.io/Open-Source/async-events/docs/",
        "Tracker": "https://gitlab.cloud-technology.io/Open-Source/async-events/issues/",
    },
    license="BSD 3-Clause",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Price Hiller",
    author_email="philler3138@gmail.com",
    description="An asynchronous event library",
)
