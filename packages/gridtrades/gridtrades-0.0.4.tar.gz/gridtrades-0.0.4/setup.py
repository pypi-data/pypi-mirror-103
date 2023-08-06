import setuptools

setuptools.setup(
    name="gridtrades",  #库的名字
    version="0.0.4",    #库的版本号，后续更新时候只要改版本号就行了
    author="",  #你的名字
    author_email="",    #你的邮箱
    description="", #介绍
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
#注：没有进行注释的地方不要修改，以免引发错误