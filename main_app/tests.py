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


