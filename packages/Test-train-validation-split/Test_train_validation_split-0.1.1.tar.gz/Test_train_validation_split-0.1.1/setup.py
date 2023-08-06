from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README  
setup(
  name = 'Test_train_validation_split',         
  packages = ['test_train_validation_split_by_rajeev'],
  version = '0.1.1',      
  license='MIT',        
  description = 'A python package to split Directory into Training, Testing and Validation Directory',
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'RAJEEV SINGLA',                   
  author_email = 'rajeevsingla780@gmail.com',  
  url = 'https://github.com/rajeevsingla780/Test_train_validation_split',   # Provide either the link to your github or to your website
  include_package_data=True,    
  classifiers=[
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  entry_points={
        "console_scripts": [
            "test_train_split=test_train_validation_split_by_rajeev.split_train_validation:main",
        ]
    },
)