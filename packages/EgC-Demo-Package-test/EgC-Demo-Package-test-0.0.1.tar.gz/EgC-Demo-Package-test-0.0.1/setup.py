import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
def parse_json_dependencies_requirement(strPathJson):
    
    import json
    #dependencies_dict = pd.read_json(strPathJson)
    
    with open(strPathJson, "r") as read_file:
        dependencies_dict = json.load(read_file)
    
    install_requires = dependencies_dict['install_requires']
    extras_require = dependencies_dict['extras_require']
    
    extras_require['all'] = set(vv for value in extras_require.values() for vv in value)
    
    return install_requires, extras_require

setuptools.setup(
    name="EgC-Demo-Package-test", # Replace with your python folder name 
    version="0.0.1",
    install_requires=parse_json_dependencies_requirement('requirements.json')[0],
    extras_require=parse_json_dependencies_requirement('requirements.json')[1],
    author="liu1stu",# Replace with your own username
    author_email="weihan.liu1994@hotmail.com",# Replace with your own username
    description="A small example package from EGC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EgC-Team/EngineeringGoesCloud",
    #packages=["src","src.demo"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
