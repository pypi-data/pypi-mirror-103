import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartPID",
    version="1.0",                                      
    author="Qi Zhu",                                      
    author_email="2335666965@qq.com",                     
    url="https://mvp.aliyun.com/mvp/detail/450?spm=5176.11535038.header.17.4827755fXaDyyW",
    description=("This library contains three controller algorithms."),                           
    long_description=long_description,                      
    long_description_content_type="text/markdown",          
    packages=setuptools.find_packages(),                   
    classifiers=[                                           
        "Programming Language :: Python :: 3",              
        "License :: OSI Approved :: MIT License",          
        "Operating System :: OS Independent",               
    ],
)

