import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonbot",
    version="0.4",
    author="Flampt",
    description="Simple api wrapper for Python Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlamptX/pythonbot-api-wrapper",
    project_urls={
        "Python Bot": "https://python-bot.web.app",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)