from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

replacement_dict = {
    'ا': ['1', 'ا', 'l'],
    'أ': ['2', 'أ', 'i'],
    'إ': ['!', 'إ'],
    'آ': ['1`', 'آ', '`l'],
    'ب': ['].', ').', 'ب'],
    'ت': [':]', ':)', 'ت'],
    'ث': ['.:]', '.:)', 'ث'],
    'ج': ['>.', 'ج'],
    'ح': ['7', 'ح'],
    'خ': ['`7', 'خ', '5'],
    'د': ['>', 'د'],
    'ذ': ['4', 'ذ', '`>'],
    'ر': [')', 'ر'],
    'ز': ['`)', 'ز'],
    'س': ['?', 'س'],
    'ش': ['$', 'ش'],
    'ص': ['9', 'ص'],
    'ض': ['`9', 'ض'],
    'ط': ['6', 'ط'],
    'ظ': ['`6', 'ظ'],
    'ع': ['3', 'ع'],
    'غ': ['`3', 'غ'],
    'ف': [';', 'b.', 'ف'],
    'ق': ['8', 'ق'],
    'ك': ['L^', 'ك'],
    'ل': ['L', 'ل'],
    'م': ['o', 'م'],
    'ن': ['.]', '.)', 'ن'],
    'ه': ['@', 'ه'],
    'و': ['&', 'و', 'g'],
    'ؤ': ['^g', 'ؤ', '^,', '^و'],
    'ي': [']:', '):', 'ي'],
    'ى': [']', ')', 'ى'],
    'ئ': ['2', 'ئ'],
    'ء': ['^', 'ء'],
    'ة': [':@', 'ة']
}

replace_eng_dict = {
    "ا": ["h"],
    "أ": ["H"],
    "إ": ["Y"],
    "آ": ["N"],
    "ب": ["f"],
    "ت": ["j"],
    "ث": ["e"],
    "ج": ["["],
    "ح": ["7", "p"],
    "خ": ["5", "`7", "o"],
    "د": ["]"],
    "ذ": ["4", "`"],
    "ر": ["v"],
    "ز": ["."],
    "س": ["s"],
    "ش": ["a"],
    "ص": ["9", "w"],
    "ض": ["`9", "q"],
    "ط": ["6", "'"],
    "ظ": ["`6", "/"],
    "ع": ["3", "u"],
    "غ": ["`3", "y"],
    "ف": ["t"],
    "ق": ["8", "r"],
    "ك": [";"],
    "ل": ["g"],
    "م": ["l"],
    "ن": ["k"],
    "ه": ["i"],
    "و": [","],
    "ؤ": ["2",  "c"],
    "ي": ["d"],
    "ى": ["n"],
    "ئ": ["z"],
    "ء": ["x"],
    "ة": ["m"]
}

def random_replace(word, replacement_dict):
    """Replace each character in the word with a random character from the replacement dictionary"""
    return ''.join(random.choice(replacement_dict.get(char, [char])) for char in word)

def random_engreplace(word, replace_eng_dict):
    """Replace each character in the word with a random character from the English replacement dictionary"""
    return ''.join(random.choice(replace_eng_dict.get(char, [char])) for char in word)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Process the submitted Arabic text and return transformed versions"""
    try:
        data = request.get_json()
        input_text = data.get('input', '')
        
        # Generate transformed versions
        arabic_result = random_replace(input_text, replacement_dict)
        english_result = random_engreplace(input_text, replace_eng_dict)
        
        return jsonify({
            'result_arabic': arabic_result,
            'result_english': english_result
        })
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)