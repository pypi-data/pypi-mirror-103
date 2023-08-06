import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaudible", # Replace with your own username
    version="1.1.0b3",
    author="Jasper Zheng (Shuoyang)",
    author_email="s.zheng14@student.liverpool.ac.uk",
    description="A Python library for sending and receiving data using audible sound.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jasper-zheng/PyAudible",
    project_urls={
        "Bug Tracker": "https://github.com/jasper-zheng/PyAudible/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["numpy", "scipy", "pyaudio"],
)