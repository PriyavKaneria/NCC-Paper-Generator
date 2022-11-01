import random
from openpyxl import load_workbook

# LOAD EXCEL
workbook = load_workbook(filename='dummy_data.xlsx', data_only=True)
sheet = workbook.active

# LOAD DATA
questions = {}
for question in sheet.iter_rows(1, values_only=True, max_row=2501):
    # print(question)
    subject = question[0].split('.')[0]
    category = question[1]
    type = question[2]
    name = question[3]
    marks = question[9]
    if subject not in questions:
        questions[subject] = {}
    if category not in questions[subject]:
        questions[subject][category] = {}
    if type not in questions[subject][category]:
        questions[subject][category][type] = []
    questions[subject][category][type].append([name, marks])

# GIVEN PAPER CONSTRAINTS
constraints = {
    'Drill': {
        'Und': {
            'VSA': 5,
            'LA1': 1,
            'ET': 3
        },
        'Hot': {
            'VSA': 3,
            'LA1': 2,
        },
        'Rem': {
            'SA': 2,
        },
        'App': {
            'SA': 3,
            'LA1': 1,
        },
        'Emd': {
            'LA2': 3,
        }
    },
    'WT': {
        'Und': {
            'VSA': 5,
        },
        'Hot': {
            'VSA': 5,
            'LA1': 2,
            'LA2': 2,
            'ET': 3
        },
        'App': {
            'SA': 5,
            'ET': 1
        },
        'Emd': {
            'VSA': 1,
            'LA1': 2,
        }
    },
    'PD': {
        'Und': {
            'SA': 5,
            'LA1': 2,
        },
        'Hot': {
            'SA': 5,
            'ET': 1
        },
        'App': {
            'LA1': 2,
            'LA2': 3,
            'ET': 2
        },
        'Emd': {
            'VSA': 7,
            'LA1': 2,
        }
    },
    'LD': {
        'Hot': {
            'LA1': 1,
        },
        'Rem': {
            'VSA': 5,
        },
        'App': {
            'SA': 1,
        },
    },
    'DM': {
        'Und': {
            'ET': 1
        },
        'Hot': {
            'LA1': 1,
        },
        'App': {
            'LA2': 1,
        },
        'Emd': {
            'SA': 3,
        }
    },
    'SSCD': {
        'Und': {
            'SA': 5,
        },
        'Hot': {
            'LA1': 4,
        },
        'App': {
            'VSA': 5,
        },
        'Emd': {
            'LA2': 2,
        }
    },
    'HH': {
        'Und': {
            'LA1': 2,
        },
        'Hot': {
            'LA2': 2,
            'ET': 1
        },
        'Rem': {
            'VSA': 1,
            'SA': 2,
        },
        'App': {
            'SA': 5,
        },
    },
    'EAC': {
        'Hot': {
            'VSA': 2,
            'LA1': 1,
        },
        'Rem': {
            'VSA': 5,
            'SA': 1,
        },
        'Emd': {
            'VSA': 2,
            'SA': 2,
            'LA1': 1,
        }
    },
    'OT': {
        'Und': {
            'ET': 1
        },
        'App': {
            'SA': 1,
            'LA1': 1,
            'LA2': 1,
        }
    },
    'GA': {
        'App': {
            'LA1': 1,
            'ET': 2
        },
    }
}

total_marks = 0
for subject in constraints:
    paperData = ''
    question_paper = open("question_paper_" + subject + ".txt", "w")
    print(subject)
    print('-' * len(subject))
    paperData += subject + '\n' + ('-' * len(subject)) + '\n'
    subject_marks = 0
    question_count = 1
    for category in constraints[subject]:
        print(category)
        for type in constraints[subject][category]:
            no_of_questions = constraints[subject][category][type]
            selected_questions = random.sample(
                questions[subject][category][type], no_of_questions)
            for question in selected_questions:
                print(
                    f"Question {question_count}. {question[0]}", '\t\t', question[1])
                paperData += f"Question {question_count}. {question[0]}\t\t{question[1]} Marks\n"
                question_count += 1
                subject_marks += question[1]
    print()
    print(f"Total marks for {subject}: {subject_marks}")
    paperData += f"\nTotal marks for {subject}: {subject_marks}\n"
    total_marks += subject_marks
    print('-----------------------------------------------------')
    print()
    paperData += '-----------------------------------------------------\n'
    paperData += '-----------------------------------------------------\n'
    question_paper.write(paperData)
print('-----------------------------------------------------')
print(f"Total marks: {total_marks}")
