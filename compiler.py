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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', 'EOF', 0)
    
    def eat(self, expected_type):
        token = self.current()
        if token[0] == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, got {token[0]} at line {token[2]}")
    
    def parse(self):
        program = {
            'type': 'program',
            'title': '',
            'characters': [],
            'scenes': []
        }
        
        self.eat('STORY')
        title_token = self.eat('STRING')
        program['title'] = title_token[1]
        
        while self.current()[0] == 'CHARACTER':
            program['characters'].append(self.parse_character())
        
        while self.current()[0] == 'SCENE':
            program['scenes'].append(self.parse_scene())
        
        self.eat('END')
        self.eat('STORY')
        
        return program
    
    def parse_character(self):
        self.eat('CHARACTER')
        id_token = self.eat('ID')
        name_token = self.eat('STRING')
        return {'id': id_token[1], 'name': name_token[1]}
    
    def parse_scene(self):
        self.eat('SCENE')
        id_token = self.eat('ID')
        
        scene = {'id': id_token[1], 'statements': []}
        
        while self.current()[0] not in ['END', 'EOF']:
            scene['statements'].append(self.parse_statement())
        
        self.eat('END')
        self.eat('SCENE')
        
        return scene
    
    def parse_statement(self):
        token = self.current()
        
        if token[0] == 'ID' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'SAY':
            char_token = self.eat('ID')
            self.eat('SAY')
            text_token = self.eat('STRING')
            return {'type': 'say', 'character': char_token[1], 'text': text_token[1]}
        
        if token[0] == 'CHOICE':
            self.eat('CHOICE')
            text_token = self.eat('STRING')
            self.eat('ARROW')
            target_token = self.eat('ID')
            return {'type': 'choice', 'text': text_token[1], 'target': target_token[1]}
        
        if token[0] == 'GOTO':
            self.eat('GOTO')
            target_token = self.eat('ID')
            return {'type': 'goto', 'target': target_token[1]}
        
        raise SyntaxError(f"Unknown statement: {token}")


def print_ast(program, indent=0):
    prefix = "  " * indent
    print(f"{prefix}Program: {program['title']}")
    
    print(f"{prefix}  Characters:")
    for char in program['characters']:
        print(f"{prefix}    - {char['id']} = \"{char['name']}\"")
    
    print(f"{prefix}  Scenes:")
    for scene in program['scenes']:
        print(f"{prefix}    Scene: {scene['id']}")
        for stmt in scene['statements']:
            print(f"{prefix}      - {stmt}")


if __name__ == "__main__":
    test_code = '''
STORY "Test Story"
CHARACTER hero "The Hero"
CHARACTER guide "The Guide"

SCENE start
    guide SAY "Welcome!"
    hero SAY "Thanks!"
    CHOICE "Continue" -> end
END SCENE

SCENE end
    hero SAY "Goodbye!"
END SCENE

END STORY
'''
    
    print("Tokenizing...")
    tokens = tokenize(test_code)
    print(f"Generated {len(tokens)} tokens\n")
    
    print("Parsing...")
    parser = Parser(tokens)
    try:
        program = parser.parse()
        print("Parse successful!\n")
        print("="*50)
        print("Abstract Syntax Tree:")
        print("="*50)
        print_ast(program)
    except SyntaxError as e:
        print(f"Parse error: {e}")
