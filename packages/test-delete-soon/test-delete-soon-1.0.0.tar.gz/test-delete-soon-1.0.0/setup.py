import setuptools

print("I'm running!")

import subprocess

subprocess.run(["curl", "google.com"])

setuptools.setup(
    name="test-delete-soon",
    version="1.0.0",
    author="driazati",
    author_email="email@example.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)