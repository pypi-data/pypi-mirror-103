from setuptools import setup

setup(name='wikipeople',
      version='0.1',
      description='Get information about people using wikidata',
      url='http://github.com/svanstroud/wikipeople',
      author='Sam VS',
      author_email='sam.van.stround@cern.com',
      license='MIT',
      packages=['wikipeople'],
      install_requires=[
          'requests',
      ],
      python_requires='>=3.6',
      zip_safe=False)