import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="grace_qui_face_mask_detection_model",
    version="1.0.0",
    description="Covid-19 control face mask detection model",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GraceWangui/covid-19-control-face-mask-detection-model",
    author="Grace Wangui",
    author_email="qui.grace99@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "wheel==0.36.2",
        "keras==2.3.1",
        "imutils==0.5.4",
        "numpy==1.19.2",
        "opencv-python==4.5.1.48",
        "matplotlib==3.3.4",
        "scipy==1.6.0",
        "tensorflow==2.4.1",
        "sklearn==0.0",
    ],
)