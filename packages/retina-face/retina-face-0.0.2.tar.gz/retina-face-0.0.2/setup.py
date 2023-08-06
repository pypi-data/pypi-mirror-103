import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="retina-face", #pip install retina-face
    version="0.0.2",
    author="Sefik Ilkin Serengil",
    author_email="serengil@gmail.com",
    description="RetinaFace: Deep Face Detection Framework in TensorFlow for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serengil/retinaface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8.5',
    install_requires=["numpy>=1.19.5", "gdown>=3.10.1", "Pillow>=5.2.0", "opencv-python>=4.5.1.48", "tensorflow>=1.9.0"]
)
