import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="circ-spider",  # Replace with your own username
    version="1.0.0",
    author="Akafra",
    author_email="306525121@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.e-nci.com/yangzhongyang/circ_spider.git",
    project_urls={
        "Bug Tracker": "https://git.e-nci.com/yangzhongyang/circ_spider.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'selenium>=3.141.0',
        'Pillow'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
