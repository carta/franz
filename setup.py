from setuptools import setup


__version__ = "0.0.9"


setup(
    name="franz",
    version=__version__,
    url="https://github.com/eshares/franz",
    download_url="https://github.com/eshares/franz/tarball/{version}".format(
        version=__version__,
    ),
    author="Carta, Inc.",
    author_email="engineering@carta.com",
    description=(
        "Event broker built on top of kafka and rabbitmq; used to handle micro"
        " services message exchange."
    ),
    long_description=open('README.md').read(),
    license="MIT",
    keywords="microservices broker event kafka rabbitmq",
    install_requires=[
        "kafka-python==1.3.5",
        "bson==0.5.0",
        "pika==0.11.0",
    ],
    packages=[
        "franz",
        "franz.kafka",
        "franz.rabbitmq",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=True,
)
