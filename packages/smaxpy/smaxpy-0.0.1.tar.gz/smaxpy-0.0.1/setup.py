from setuptools import setup
import pathlib

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="smaxpy",
    version="0.0.1",
    description="Just a small wrapper to website scraping utilities.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ootiq/smax",
    author="TheBoringDude",
    author_email="iamcoderx@gmail.com",
    license="MIT",
    project_urls={"Bug Tracker": "https://github.com/ootiq/smax/issues"},
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["smaxpy"],
    include_package_data=True,
    install_requires=["requests", "cloudscraper", "bs4"],
)