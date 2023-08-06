from distutils.core import setup

setup(
    name='aggdirect-ocr',  # How you named your package folder (MyLib)
    packages=['aggdirect_ocr'],
    version='0.1.29',
    description='The core of OCR modeling',
    author='Suchita Bhinge',
    author_email='',
    url='',  # Provide either the link to your github or to your website
    keywords=['OCR', 'AGGDIRECT'],  # Keywords that define your package best

    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires=">=3.8",
    install_requires=[
        'apscheduler==3.7.0',
        'boto3==1.17.57',
        'numpy==1.19.2',
        'TensorFlow==2.4.1',
        'pyyaml==5.4.1'
    ],
    package_data={'aggdirect_ocr': ['config/*.yaml', 'models/*', 'training_data/*']}
)
