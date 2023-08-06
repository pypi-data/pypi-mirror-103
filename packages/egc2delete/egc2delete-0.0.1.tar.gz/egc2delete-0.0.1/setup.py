import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
def parse_json_dependencies_requirement(strPathJson):
    
    import json
    
    with open(strPathJson, "r") as read_file:
        dependencies_dict = json.load(read_file)
    
    install_requires = dependencies_dict['install_requires']
    extras_require = dependencies_dict['extras_require']
    
    extras_require['all'] = set(pckg for feature in extras_require.values() for pckg in feature)
    
    return install_requires, extras_require


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="egc2delete", # Replace with custom python folder name 
    version="0.0.1",
    
    install_requires=parse_json_dependencies_requirement('requirements.json')[0],
    extras_require=parse_json_dependencies_requirement('requirements.json')[1],

    author="EgC-Team", # Replace with custom PyPI authoring name
    author_email="mail@engineering-goes-cloud.de",# Replace with custom contact
    
    description="A small example package from EGC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/EgC-Team/EngineeringGoesCloud",

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

