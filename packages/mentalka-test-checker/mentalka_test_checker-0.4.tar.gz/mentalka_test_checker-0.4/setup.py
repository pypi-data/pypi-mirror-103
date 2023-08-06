from setuptools import setup


setup(
    name='mentalka_test_checker',                       # package name
    version='0.4',                                      # version
    author="Salim",
    author_email="cvwisework@gmail.com",
    description='OCR system for table-test check',      # short description
    long_description='''OCR system for table-test check. Use 
    result, scans, rects, blank_type, qr_code = check_test(image)
    painted_image = paint(image, all_marks, rects, blank_type)
    ''',
    long_description_content_type = 'text/x-rst',
    url='https://github.com/SalimMaxHigh/test_checker',                           # package URL
    install_requires=['h5py==2.10.0',
                      'scipy==1.4.1',
                      'opencv-python',
                      'numpy==1.18.5',
                      'scikit-image==0.17.2',
                      'imutils==0.5.3',
                      'tensorflow==2.3',
                      'Keras==2.4.3'],                # list of packages this package depends
                                                        # on.
    packages=['mentalka_test_checker'],                                   # List of module names that installing
                                                        # this package will provide.
) 
