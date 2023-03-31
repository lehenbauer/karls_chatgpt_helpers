from setuptools import setup, find_packages

setup(
    name="karls_gpt_helpers",
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here, e.g.
        # "numpy>=1.21",
        'openai',
        'pyyaml'
    ],
    entry_points={
        "console_scripts": [
            "chatgpt = scripts.chatgpt:__main__",
            "gptshell = scripts.gptshell:__main__",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

