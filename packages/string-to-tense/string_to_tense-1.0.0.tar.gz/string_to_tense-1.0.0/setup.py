from setuptools import find_packages, setup


classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Financial and Insurance Industry',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='string_to_tense',
    version='1.0.0',
    author='Vinit Ganorkar',
    auther_email='vinit777ganorkar@gmail.com',
    description='Forword Looking Sentence Identification',
    long_description=open('README.txt').read(),
    licence='MIT',
    classifiers = classifiers,
    packages=find_packages(),
    install_requires=['spacy>=3.0.5', 'pandas>=1.0.5'],
    package_data={'string_to_tense': ['model_checkpoint/*.pkl',
                                      'pattern/text/en/*slp',
                                      'pattern/text/en/*txt',
                                      'pattern/text/en/wordnet/*txt',
                                      'pattern/text/en/wordlist/*txt']},
    include_package_data=True
)
