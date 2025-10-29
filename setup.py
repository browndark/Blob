"""
Setup do Projeto BLOB
=====================

Script de instalação e configuração do sistema BLOB.
"""

from setuptools import setup, find_packages
import os

# Lê o README para a descrição longa
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'docs', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Sistema de Assistente Virtual Interativo BLOB"

# Lê os requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="blob-assistant",
    version="2.0.0",
    author="Equipe BLOB",
    author_email="blob@example.com",
    description="Sistema de Assistente Virtual Interativo com IA Emocional",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/exemplo/blob-assistant",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "unity": [
            "pythonnet>=2.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "blob=src.main:main",
            "blob-ultra=src.core.blob_ultra_avancado:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai assistant voice recognition chatbot emotional-ai",
)