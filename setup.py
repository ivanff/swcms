import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swcms_social",
    version="0.0.1",
    author="Ivan Fedoseev",
    author_email="agestart@gmail.com",
    description="Collect of Django apps, shared part of likeis and posticas",
    license='MIT',
    long_description=long_description,
    url="https://github.com/ivanff/swcms-social",
    packages=setuptools.find_packages(),
    install_requires=(
            'django>=2.0',
            'django-ckeditor>=5.4.0',
            'rest_framework>=3.7.7',
    ),
    classifiers=(
        'Development Status :: 4 - Alpha',
        'Environment :: Web Environment',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Framework :: Django',
    ),
    include_package_data = True,
)
