# NCC-Paper-Generator
NCC Paper Generator

Installing dependencies
```bash
pip install -r requirements.txt
```

Setup data
- data_template is template for the data file
- data is file with actual data of questions according to template

- Dummy data is for testing purposes
- Dummy data can be generated using `python generate_dummy_data.py` where the parameters can be changed in the file

Running the program
```bash
python generator.py
```

*The contraints which are set as per C certificate can be changed in tne contraints variable in generator.py*