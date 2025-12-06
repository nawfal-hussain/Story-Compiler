"""
Story Compiler
Compiler Construction Project

Nawfal Hussain 22k-4372
Mustafa Shahzad 22k-4166
Muhammad Alyan 22k-4582
"""

KEYWORDS = ['STORY', 'END', 'SCENE', 'CHARACTER', 'SAY', 'CHOICE', 'GOTO']

def tokenize(code):
    """Break code into tokens."""
    tokens = []
    i = 0
    line = 1
    
    while i < len(code):
        char = code[i]
        
        if char in ' \t':
            i += 1
            continue
        
        if char == '\n':
            line += 1
            i += 1
            continue
        
        if char == '#':
            while i < len(code) and code[i] != '\n':
                i += 1
            continue
        
        if char == '"':
            i += 1
            string_value = ""
            while i < len(code) and code[i] != '"':
                string_value += code[i]
                i += 1
            i += 1
            tokens.append(('STRING', string_value, line))
            continue
        
        if char.isalpha() or char == '_':
            word = ""
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                word += code[i]
                i += 1
            if word.upper() in KEYWORDS:
                tokens.append((word.upper(), word.upper(), line))
            else:
                tokens.append(('ID', word, line))
            continue
        
        if char == '-' and i + 1 < len(code) and code[i + 1] == '>':
            tokens.append(('ARROW', '->', line))
            i += 2
            continue
        
        i += 1
    
    tokens.append(('EOF', 'EOF', line))
    return tokens


def print_tokens(tokens):
    print("\nToken Stream:")
    print("="*50)
    for i, (token_type, value, line) in enumerate(tokens):
        print(f"{i+1:3}. [{token_type:10}] {repr(value):20} (line {line})")
    print("="*50)


if __name__ == "__main__":
    test_code = '''
STORY "Test"
CHARACTER hero "The Hero"
SCENE start
    hero SAY "Hello!"
END SCENE
END STORY
'''
    tokens = tokenize(test_code)
    print_tokens(tokens)
