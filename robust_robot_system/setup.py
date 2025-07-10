from setuptools import setup, find_packages

setup(
    name="robust_robot_core",
    version="0.2.0",
    packages=find_packages(include=["core", "core.*"]),
    description="Minimal communication and discovery library for robotics",
    author="Tim Lumpp",
    python_requires=">=3.7",
    install_requires=[
        "pyzmq>=24.0.0",
        "opencv-python>=4.5.0",
    ],
)
