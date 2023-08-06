import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="similarity_model_trainer_2021", # Replace with your own username
    version="0.1.3",
    author="Author",
    author_email="",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'data': ['similarity_model_trainer_2021/Normailzer/tables/chars.csv',
                           'similarity_model_trainer_2021/Normailzer/tables/specialWords.csv',
                           'similarity_model_trainer_2021/Tokenizer/frequency_bigramdictionary2_fa_243_342.txt',
                           'similarity_model_trainer_2021/Tokenizer/LM/dic_bi.pickle',
                           'similarity_model_trainer_2021/Tokenizer/LM/dic_uni.pickle']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)