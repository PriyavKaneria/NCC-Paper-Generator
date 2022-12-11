# NCC-Paper-Generator
NCC Paper Generator

## [Demo](https://drive.google.com/file/d/1i5w5tFFe1fhWBiPHV32BkcRCA3w6NpRt/view?usp=sharing)

Installing dependencies
```bash
pip install -r requirements.txt
```

Setup data
- data_template is template for the data file
- data is file with actual data of questions according to template

- Dummy data is for testing purposes
- Dummy data can be generated using `python dummy_data_generator.py` where the parameters can be changed in the file

- pyvips needs to be setup for image processing of Hindi text - [Documentation article to help setup](https://www.infinitycodex.in/how-to-put-hindi-text-on-images-using)

Running the program
```bash
python generator.py
```

*The contraints which are set as per C certificate can be changed in tne contraints variable in generator.py*
