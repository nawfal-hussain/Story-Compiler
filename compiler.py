"""
Story Compiler
Compiler Construction Project

Nawfal Hussain 22k-4372
Mustafa Shahzad 22k-4166
Muhammad Alyan 22k-4582
"""

KEYWORDS = ['STORY', 'END', 'SCENE', 'CHARACTER', 'SAY', 'CHOICE', 'GOTO', 'SET', 'IF', 'ELSE', 'ENDIF']

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
        
        if char.isdigit():
            number = ""
            while i < len(code) and code[i].isdigit():
                number += code[i]
                i += 1
            tokens.append(('NUMBER', int(number), line))
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
        
        if char == '=' and i + 1 < len(code) and code[i + 1] == '=':
            tokens.append(('EQUALS', '==', line))
            i += 2
            continue
        if char == '-' and i + 1 < len(code) and code[i + 1] == '>':
            tokens.append(('ARROW', '->', line))
            i += 2
            continue
        if char == '>':
            tokens.append(('GREATER', '>', line))
            i += 1
            continue
        if char == '<':
            tokens.append(('LESS', '<', line))
            i += 1
            continue
        if char == '=':
            tokens.append(('ASSIGN', '=', line))
            i += 1
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
            'variables': [],
            'scenes': []
        }
        
        self.eat('STORY')
        title_token = self.eat('STRING')
        program['title'] = title_token[1]
        
        while self.current()[0] in ['CHARACTER', 'SET']:
            if self.current()[0] == 'CHARACTER':
                program['characters'].append(self.parse_character())
            else:
                program['variables'].append(self.parse_variable())
        
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
    
    def parse_variable(self):
        self.eat('SET')
        id_token = self.eat('ID')
        self.eat('ASSIGN')
        value = self.parse_value()
        return {'id': id_token[1], 'value': value}
    
    def parse_value(self):
        token = self.current()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return {'type': 'number', 'value': token[1]}
        elif token[0] == 'ID':
            self.eat('ID')
            return {'type': 'variable', 'name': token[1]}
        else:
            raise SyntaxError(f"Unexpected value: {token}")
    
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
        
        if token[0] == 'SET':
            self.eat('SET')
            id_token = self.eat('ID')
            self.eat('ASSIGN')
            value = self.parse_value()
            return {'type': 'set', 'variable': id_token[1], 'value': value}
        
        if token[0] == 'IF':
            self.eat('IF')
            condition = self.parse_condition()
            
            then_stmts = []
            while self.current()[0] not in ['ELSE', 'ENDIF', 'EOF']:
                then_stmts.append(self.parse_statement())
            
            else_stmts = []
            if self.current()[0] == 'ELSE':
                self.eat('ELSE')
                while self.current()[0] not in ['ENDIF', 'EOF']:
                    else_stmts.append(self.parse_statement())
            
            self.eat('ENDIF')
            return {'type': 'if', 'condition': condition, 'then': then_stmts, 'else': else_stmts}
        
        raise SyntaxError(f"Unknown statement: {token}")
    
    def parse_condition(self):
        left = self.parse_value()
        
        if self.current()[0] in ['GREATER', 'LESS', 'EQUALS']:
            op_token = self.current()
            self.pos += 1
            right = self.parse_value()
            return {'type': 'comparison', 'op': op_token[1], 'left': left, 'right': right}
        
        return left


def semantic_analysis(program):
    errors = []
    symbol_table = {
        'characters': {},
        'variables': {},
        'scenes': {}
    }
    
    for char in program['characters']:
        symbol_table['characters'][char['id']] = char['name']
    
    for var in program['variables']:
        symbol_table['variables'][var['id']] = var['value']
    
    for scene in program['scenes']:
        symbol_table['scenes'][scene['id']] = True
    
    for scene in program['scenes']:
        for stmt in scene['statements']:
            if stmt['type'] == 'say':
                if stmt['character'] not in symbol_table['characters']:
                    errors.append(f"Undefined character: {stmt['character']}")
            
            if stmt['type'] == 'choice':
                if stmt['target'] not in symbol_table['scenes']:
                    errors.append(f"Undefined scene: {stmt['target']}")
            
            if stmt['type'] == 'goto':
                if stmt['target'] not in symbol_table['scenes']:
                    errors.append(f"Undefined scene: {stmt['target']}")
    
    return symbol_table, errors


def print_symbol_table(symbol_table):
    print("\n" + "="*50)
    print("Symbol Table")
    print("="*50)
    
    print("\nCharacters:")
    for id, name in symbol_table['characters'].items():
        print(f"  {id} -> {name}")
    
    print("\nVariables:")
    for id, val in symbol_table['variables'].items():
        print(f"  {id} = {val}")
    
    print("\nScenes:")
    for scene_id in symbol_table['scenes']:
        print(f"  {scene_id}")
    
    print("="*50)


if __name__ == "__main__":
    import sys
    
    test_code = '''
STORY "Adventure"
CHARACTER hero "Hero"
SET health = 100

SCENE start
    hero SAY "Let's begin!"
    IF health > 50
        GOTO win
    ELSE
        GOTO lose
    ENDIF
END SCENE

SCENE win
    hero SAY "Victory!"
END SCENE

SCENE lose
    hero SAY "Defeat..."
END SCENE

END STORY
'''
    
    print("Phase 1: Tokenizing...")
    tokens = tokenize(test_code)
    print(f"  Generated {len(tokens)} tokens")
    
    print("\nPhase 2: Parsing...")
    parser = Parser(tokens)
    try:
        program = parser.parse()
        print("  Parse successful")
    except SyntaxError as e:
        print(f"  Error: {e}")
        sys.exit(1)
    
    print("\nPhase 3: Semantic Analysis...")
    symbol_table, errors = semantic_analysis(program)
    if errors:
        for err in errors:
            print(f"  Error: {err}")
    else:
        print("  Analysis complete")
        print_symbol_table(symbol_table)
