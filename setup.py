import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="echo_mailer",
    version="0.0.1",
    author="Echo Void",
    author_email="void-echo@outlook.com",
    description="A simple mail sender for python. Send mail with smtp. Central server is needed.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/void-echo/echo_mailer/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requires=[
        'flask',
        'flask_cors',
        'requests',
        'echo_logger'
    ],
)
