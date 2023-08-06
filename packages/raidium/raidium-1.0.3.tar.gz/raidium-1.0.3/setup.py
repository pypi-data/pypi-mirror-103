import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="raidium",
    version="1.0.3",
    author="k3rry1xrd",
    author_email="Mrslashkaopenko@google.com",
    description="Модуль для Накрутки Прослушиваний в Вашем Альбоме в Социальной Сети ВКонтакте.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrshowtv/vk-listener",
    project_urls={
        "Bug Tracker": "https://github.com/mrshowtv/vk-listener",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["raidium"],
    install_requires=['selenium'],
    python_requires=">=3.0",
)