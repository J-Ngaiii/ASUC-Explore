from setuptools import setup, find_packages

setup(
    name="asuc_explore",  # Package name
    version="1.0.0",  # Version of your package
    author="Jonathan Ngai (ASUC Senator 2024-2025)",  # Your name or organization
    author_email="jngai_@berkeley.edu",  # Optional: Your email address
    description="Tools for exploring and analyzing ASUC financial data.",  # Short description
    long_description=open("README.md").read(),  # Optionally include README.md as long description
    long_description_content_type="text/markdown",  # Specify README format
    url="https://github.com/J-Ngaiii/asuc-explore",  # Optional: Link to project repo
    packages=find_packages(),  # Automatically find all packages in the project
    install_requires=[
        "numpy==1.26.4",      # numpy 1.26.4 is required for Python 3.12 compatibility
        "pandas==2.2.3",
        "matplotlib==1.9.2",
        "seaborn==0.13.2",
        "spacy==3.8.2",
        "scikit-learn==1.5.1",  # Ensure scikit-learn 1.5.1 is used (note: incompatible with Python 3.12)
        "rapidfuzz==3.5.2"
    ],
    python_requires='>=3.11,<3.12',
)