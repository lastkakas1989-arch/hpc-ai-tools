from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hpc-ai-tools",
    version="1.0.0",
    author="Attaxu",
    author_email="last.kakas.1989@gmail.com",
    description="HPC/AI content generation and publishing tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/last-kakas-1989/hpc-ai-tools",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hpc-ai-tools=hpc_ai_tools.cli:main",
        ],
    },
    include_package_data=True,
)