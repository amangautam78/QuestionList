from django.test import TestCase

# Create your tests here.

def logic_for_unique_code_generation_from_categories(category):

	# categories = ['Other Office Supplies', 'Welding', 'Chemicals', 'Bearing & Power Transmission', 'LED and lighting', 'SMT Electricals', 'Safety', 'Plumbing', 'Hardware', 'Hand Tools', 'Packaging Material', 'Cutting tools', 'Furniture', 'IT', 'Air purifiers & Fragrances', 'Papers, Napkins & Bags', 'Cutting Tools', 'FASTENING TOOLS', 'Oils and Lubricants', 'Cutting Tools ', 'nan', 'Uniform', 'Endmills', 'HandTools', 'Security', 'Power Tools', 'HK Miscelaneous', 'Office Cleaning Supplies', 'Paints & Adhesives', 'Health & Hygiene', 'Bathroom soaps', 'Toilet supplies & Toiletries', 'Electronics', 'Dishwashing Supplies', 'ESD', 'Stationery']

	unique_codes = {}

    if category is not None:
        initials = ''.join(word[0] for word in category.split())
        code = initials[:2].upper()
        while code in unique_codes.values():
            code += random.choice(string.ascii_uppercase)
        unique_codes[category] = code

	print(unique_codes)


def generate_pid(supercategory, category, subcategory):
    # Convert supercategory to alpha unique 1 char
    supercategory_code = supercategory[0].upper()

    # Convert category to alpha 2 chars
    category_code = logic_for_unique_code_generation_from_categories(category)

    # Convert subcategory to alpha 3 chars
    subcategory_code = subcategory[:3].upper().ljust(3, 'X')

    # Find the next numeric sequence for the given supercategory, category, and subcategory
    # You can implement this using a database or file that keeps track of the last used sequence
    # Here, we're just using a placeholder value of 1
    numeric_sequence = str(1).zfill(4)

    # Combine the codes and sequence to generate the product ID
    pid = supercategory_code + category_code + subcategory_code + numeric_sequence

    # Ensure that the PID is at most 10 characters long
    if len(pid) > 10:
        raise ValueError("Unable to generate a unique product ID")

    return pid









from vendor_management_system.settings import DB

from uuid import uuid4



data = [
  {
    "S.N.": 1,
    "Question": "What is the process by which green plants make their food?",
    "options": {
      "1": {
        "opt": "Photosynthesis",
        "ans": "true"
      },
      "2": {
        "opt": "Respiration",
        "ans": "false"
      },
      "3": {
        "opt": "Transpiration",
        "ans": "false"
      },
      "4": {
        "opt": "Digestion",
        "ans": "false"
      }
    },
    "Correct Option": "1) Photosynthesis",
    "Explanation": "Photosynthesis is the process by which green plants use sunlight to synthesize food from carbon dioxide and water."
  },
  {
    "S.N.": 2,
    "Question": "What is the SI unit of electric current?",
    "options": {
      "1": {
        "opt": "Ampere",
        "ans": "true"
      },
      "2": {
        "opt": "Volt",
        "ans": "false"
      },
      "3": {
        "opt": "Ohm",
        "ans": "false"
      },
      "4": {
        "opt": "Watt",
        "ans": "false"
      }
    },
    "Correct Option": "1) Ampere",
    "Explanation": "The SI unit of electric current is ampere (A)."
  },
  {
    "S.N.": 3,
    "Question": "Which of the following is a non-metallic mineral?",
    "options": {
      "1": {
        "opt": "Gold",
        "ans": "false"
      },
      "2": {
        "opt": "Diamond",
        "ans": "false"
      },
      "3": {
        "opt": "Coal",
        "ans": "true"
      },
      "4": {
        "opt": "Iron",
        "ans": "false"
      }
    },
    "Correct Option": "3) Coal",
    "Explanation": "Coal is a non-metallic mineral."
  },
  {
    "S.N.": 4,
    "Question": "What is the pH of a neutral solution?",
    "options": {
      "1": {
        "opt": "7",
        "ans": "true"
      },
      "2": {
        "opt": "6",
        "ans": "false"
      },
      "3": {
        "opt": "8",
        "ans": "false"
      },
      "4": {
        "opt": "9",
        "ans": "false"
      }
    },
    "Correct Option": "1) 7",
    "Explanation": "A neutral solution has a pH of 7."
  },
  {
    "S.N.": 5,
    "Question": "What is the unit of force in the International System of Units (SI)?",
    "options": {
      "1": {
        "opt": "Newton",
        "ans": "true"
      },
      "2": {
        "opt": "Joule",
        "ans": "false"
      },
      "3": {
        "opt": "Watt",
        "ans": "false"
      },
      "4": {
        "opt": "Volt",
        "ans": "false"
      }
    },
    "Correct Option": "1) Newton",
    "Explanation": "The unit of force in the International System of Units (SI) is the Newton (N)."
  }
]




def add_questions_to_question_bank(data):

    class_id = '2823e361-3bfb-4ab9-9729-10d7507178f1'
    class_name = 'CLASS 9 SCIENCE'
    question_payload_list = [] 


    for question in data:
        question_payload = {}
        question_payload['class_id'] = class_id
        question_payload['class_name'] = class_name
        question_payload['que'] ='<p>' + question.get('Question') + '</p>'
        question_payload['explain'] = '<p>' + question.get('Correct Option') + '</p><p>' + question.get('Explanation') + '</p>'
        question_payload['options'] = question.get('options')
        question_payload['is_multi'] = False
        question_payload['qid'] = str(uuid4())
        question_payload_list.append(question_payload)
    return question_payload_list

#DB.questions.insert_many(add_questions_to_question_bank(data))







