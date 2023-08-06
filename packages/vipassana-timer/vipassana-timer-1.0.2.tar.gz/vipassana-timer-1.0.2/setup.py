import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vipassana-timer",
    version="1.0.2",
    author="toxicologist",
    license='MIT',
    author_email="toxiccologist@gmail.com",
    description="A small meditation timer for vipassana",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toxicologist/vipassana-timer",
    project_urls={
        "Bug Tracker": "https://github.com/toxicologist/vipassana-timer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["meditation", "vipassana", "timer", "countdown"],
    packages=['meditate'],
    include_package_data=True,
    package_data={
        'meditate': [
            'data/bell.wav'
        ]
    },
    entry_points={
        "console_scripts": [
            "meditate=meditate:main"
        ],
    },
    python_requires="~=3.5",
    install_requires=[
        'simpleaudio',
        'argparse',
        'humanize'
    ],
)
