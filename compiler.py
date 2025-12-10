"""
Story Compiler
Compiler Construction Project

Nawfal Hussain 22k-4372
Mustafa Shahzad 22k-4166
Muhammad Alyan 22k-4582
"""

"""
StoryScript Compiler
CS4031 Compiler Construction Project
"""

KEYWORDS = ['STORY', 'END', 'SCENE', 'CHARACTER', 'SAY', 'CHOICE', 'GOTO', 'SET', 'IF', 'ELSE', 'ENDIF', 'TRUE', 'FALSE']

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
        if char == '+':
            tokens.append(('PLUS', '+', line))
            i += 1
            continue
        if char == '-':
            tokens.append(('MINUS', '-', line))
            i += 1
            continue
        
        i += 1
    
    tokens.append(('EOF', 'EOF', line))
    return tokens


def print_tokens(tokens):
    """Display token stream in a nice format."""
    print("\n" + "="*50)
    print("PHASE 1: TOKEN STREAM")
    print("="*50)
    for i, (token_type, value, line) in enumerate(tokens):
        print(f"  {i+1:3}. [{token_type:10}] {repr(value):20} (line {line})")
    print("="*50)


#############################################
# PHASE 2: SYNTAX ANALYSIS (Parser)
#############################################

class Parser:
    """
    Phase 2: Check if tokens follow the grammar rules.
    Build a simple structure (like a tree) of the program.
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.parse_steps = []
    
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
        self.parse_steps.append("program -> STORY string declarations scenes END STORY")
        
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
        
        self.parse_steps.append("  declarations -> (CHARACTER | SET)*")
        while self.current()[0] in ['CHARACTER', 'SET']:
            if self.current()[0] == 'CHARACTER':
                program['characters'].append(self.parse_character())
            else:
                program['variables'].append(self.parse_variable())
        
        self.parse_steps.append("  scenes -> SCENE+")
        while self.current()[0] == 'SCENE':
            program['scenes'].append(self.parse_scene())
        
        self.eat('END')
        self.eat('STORY')
        
        return program
    
    def parse_character(self):
        self.parse_steps.append("    character -> CHARACTER id string")
        self.eat('CHARACTER')
        id_token = self.eat('ID')
        name_token = self.eat('STRING')
        return {'id': id_token[1], 'name': name_token[1]}
    
    def parse_variable(self):
        self.parse_steps.append("    variable -> SET id = value")
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
        elif token[0] == 'TRUE':
            self.eat('TRUE')
            return {'type': 'boolean', 'value': True}
        elif token[0] == 'FALSE':
            self.eat('FALSE')
            return {'type': 'boolean', 'value': False}
        elif token[0] == 'ID':
            self.eat('ID')
            if self.current()[0] in ['PLUS', 'MINUS']:
                op = self.current()[1]
                self.pos += 1
                right = self.parse_value()
                return {'type': 'binary', 'op': op, 'left': token[1], 'right': right}
            return {'type': 'variable', 'name': token[1]}
        elif token[0] == 'STRING':
            self.eat('STRING')
            return {'type': 'string', 'value': token[1]}
        else:
            raise SyntaxError(f"Unexpected value: {token}")
    
    def parse_scene(self):
        self.parse_steps.append("    scene -> SCENE id statements END SCENE")
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
            self.parse_steps.append("      statement -> id SAY string")
            char_token = self.eat('ID')
            self.eat('SAY')
            text_token = self.eat('STRING')
            return {'type': 'say', 'character': char_token[1], 'text': text_token[1]}
        
        if token[0] == 'CHOICE':
            self.parse_steps.append("      statement -> CHOICE string -> id")
            self.eat('CHOICE')
            text_token = self.eat('STRING')
            self.eat('ARROW')
            target_token = self.eat('ID')
            return {'type': 'choice', 'text': text_token[1], 'target': target_token[1]}
        
        if token[0] == 'GOTO':
            self.parse_steps.append("      statement -> GOTO id")
            self.eat('GOTO')
            target_token = self.eat('ID')
            return {'type': 'goto', 'target': target_token[1]}
        
        if token[0] == 'SET':
            self.parse_steps.append("      statement -> SET id = value")
            self.eat('SET')
            id_token = self.eat('ID')
            self.eat('ASSIGN')
            value = self.parse_value()
            return {'type': 'set', 'variable': id_token[1], 'value': value}
        
        if token[0] == 'IF':
            self.parse_steps.append("      statement -> IF condition statements [ELSE statements] ENDIF")
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


def print_parse_tree(parser):
    print("\n" + "="*50)
    print("PHASE 2: PARSE TREE (Derivation)")
    print("="*50)
    for step in parser.parse_steps:
        print(step)
    print("="*50)


def print_ast(program, indent=0):
    prefix = "  " * indent
    print(f"{prefix}Program: {program['title']}")
    
    print(f"{prefix}  Characters:")
    for char in program['characters']:
        print(f"{prefix}    - {char['id']} = \"{char['name']}\"")
    
    print(f"{prefix}  Variables:")
    for var in program['variables']:
        print(f"{prefix}    - {var['id']} = {var['value']}")
    
    print(f"{prefix}  Scenes:")
    for scene in program['scenes']:
        print(f"{prefix}    Scene: {scene['id']}")
        for stmt in scene['statements']:
            print(f"{prefix}      - {stmt}")


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
        symbol_table['variables'][var['id']] = {
            'value': var['value'],
            'type': get_type(var['value'])
        }
    
    for scene in program['scenes']:
        symbol_table['scenes'][scene['id']] = True
    
    for scene in program['scenes']:
        for stmt in scene['statements']:
            if stmt['type'] == 'say':
                if stmt['character'] not in symbol_table['characters']:
                    errors.append(f"Undefined character: {stmt['character']}")
            
            if stmt['type'] == 'choice':
                if stmt['target'] not in symbol_table['scenes']:
                    errors.append(f"Undefined scene in CHOICE: {stmt['target']}")
            
            if stmt['type'] == 'goto':
                if stmt['target'] not in symbol_table['scenes']:
                    errors.append(f"Undefined scene in GOTO: {stmt['target']}")
    
    return symbol_table, errors


def get_type(value):
    if isinstance(value, dict):
        return value.get('type', 'unknown')
    return type(value).__name__


def print_symbol_table(symbol_table):
    print("\n" + "="*50)
    print("PHASE 3: SYMBOL TABLE")
    print("="*50)
    
    print("\n  Characters:")
    print(f"    {'ID':<15} {'Display Name':<20}")
    print(f"    {'-'*15} {'-'*20}")
    for id, name in symbol_table['characters'].items():
        print(f"    {id:<15} {name:<20}")
    
    print("\n  Variables:")
    print(f"    {'ID':<15} {'Type':<10} {'Value':<15}")
    print(f"    {'-'*15} {'-'*10} {'-'*15}")
    for id, info in symbol_table['variables'].items():
        print(f"    {id:<15} {info['type']:<10} {str(info['value']):<15}")
    
    print("\n  Scenes:")
    for scene_id in symbol_table['scenes']:
        print(f"    - {scene_id}")
    
    print("="*50)


def generate_ir(program):
    ir_code = []
    temp_counter = [0]
    label_counter = [0]
    
    def new_temp():
        temp_counter[0] += 1
        return f"t{temp_counter[0]}"
    
    def new_label():
        label_counter[0] += 1
        return f"L{label_counter[0]}"
    
    ir_code.append(('PROGRAM', program['title'], None, None))
    
    for char in program['characters']:
        ir_code.append(('CHAR', char['id'], char['name'], None))
    
    for var in program['variables']:
        value = var['value']
        if isinstance(value, dict) and value['type'] == 'number':
            ir_code.append(('SET', var['id'], value['value'], None))
        elif isinstance(value, dict) and value['type'] == 'boolean':
            ir_code.append(('SET', var['id'], 1 if value['value'] else 0, None))
        else:
            ir_code.append(('SET', var['id'], value, None))
    
    for scene in program['scenes']:
        ir_code.append(('LABEL', f"scene_{scene['id']}", None, None))
        
        for stmt in scene['statements']:
            if stmt['type'] == 'say':
                ir_code.append(('SAY', stmt['character'], stmt['text'], None))
            
            elif stmt['type'] == 'choice':
                ir_code.append(('CHOICE', stmt['text'], f"scene_{stmt['target']}", None))
            
            elif stmt['type'] == 'goto':
                ir_code.append(('GOTO', f"scene_{stmt['target']}", None, None))
            
            elif stmt['type'] == 'set':
                value = stmt['value']
                if isinstance(value, dict):
                    if value['type'] == 'binary':
                        temp = new_temp()
                        ir_code.append((value['op'], value['left'], value['right'], temp))
                        ir_code.append(('COPY', temp, None, stmt['variable']))
                    elif value['type'] == 'number':
                        ir_code.append(('COPY', value['value'], None, stmt['variable']))
                    elif value['type'] == 'boolean':
                        ir_code.append(('COPY', 1 if value['value'] else 0, None, stmt['variable']))
                    else:
                        ir_code.append(('COPY', value, None, stmt['variable']))
            
            elif stmt['type'] == 'if':
                else_label = new_label()
                end_label = new_label()
                
                cond = stmt['condition']
                if cond['type'] == 'comparison':
                    left = cond['left']
                    right = cond['right']
                    left_val = left['name'] if left['type'] == 'variable' else left['value']
                    right_val = right['name'] if right['type'] == 'variable' else right['value']
                    
                    ir_code.append(('IF_FALSE', f"{left_val} {cond['op']} {right_val}", else_label, None))
                else:
                    val = cond['name'] if cond['type'] == 'variable' else cond['value']
                    ir_code.append(('IF_FALSE', val, else_label, None))
                
                for s in stmt['then']:
                    generate_stmt_ir(s, ir_code, new_temp, new_label)
                
                if stmt['else']:
                    ir_code.append(('GOTO', end_label, None, None))
                    ir_code.append(('LABEL', else_label, None, None))
                    for s in stmt['else']:
                        generate_stmt_ir(s, ir_code, new_temp, new_label)
                    ir_code.append(('LABEL', end_label, None, None))
                else:
                    ir_code.append(('LABEL', else_label, None, None))
        
        ir_code.append(('END_SCENE', scene['id'], None, None))
    
    ir_code.append(('END_PROGRAM', None, None, None))
    
    return ir_code


def generate_stmt_ir(stmt, ir_code, new_temp, new_label):
    if stmt['type'] == 'say':
        ir_code.append(('SAY', stmt['character'], stmt['text'], None))
    elif stmt['type'] == 'goto':
        ir_code.append(('GOTO', f"scene_{stmt['target']}", None, None))
    elif stmt['type'] == 'set':
        value = stmt['value']
        if isinstance(value, dict) and value['type'] == 'number':
            ir_code.append(('COPY', value['value'], None, stmt['variable']))


def print_ir(ir_code):
    print("\n" + "="*50)
    print("PHASE 4: THREE-ADDRESS CODE (TAC)")
    print("="*50)
    
    print("\n  Quadruples (op, arg1, arg2, result):")
    print(f"  {'#':<4} {'Op':<12} {'Arg1':<15} {'Arg2':<15} {'Result':<10}")
    print(f"  {'-'*4} {'-'*12} {'-'*15} {'-'*15} {'-'*10}")
    
    for i, (op, arg1, arg2, result) in enumerate(ir_code):
        a1 = str(arg1)[:14] if arg1 is not None else "-"
        a2 = str(arg2)[:14] if arg2 is not None else "-"
        res = str(result)[:9] if result is not None else "-"
        print(f"  {i:<4} {op:<12} {a1:<15} {a2:<15} {res:<10}")
    
    print("\n  TAC Instructions:")
    for op, arg1, arg2, result in ir_code:
        if op == 'LABEL':
            print(f"  {arg1}:")
        elif op == 'GOTO':
            print(f"    goto {arg1}")
        elif op == 'IF_FALSE':
            print(f"    if NOT ({arg1}) goto {arg2}")
        elif op == 'SAY':
            print(f"    SAY({arg1}, \"{arg2}\")")
        elif op == 'CHOICE':
            print(f"    CHOICE(\"{arg1}\", {arg2})")
        elif op == 'COPY':
            print(f"    {result} = {arg1}")
        elif op in ['+', '-']:
            print(f"    {result} = {arg1} {op} {arg2}")
        elif op == 'SET':
            print(f"    {arg1} = {arg2}")
        elif op == 'PROGRAM':
            print(f"  PROGRAM: \"{arg1}\"")
        elif op == 'END_PROGRAM':
            print(f"  END")
    
    print("="*50)


def optimize(ir_code):
    optimized = []
    constants = {}
    optimizations_done = []
    
    for i, (op, arg1, arg2, result) in enumerate(ir_code):
        
        if op in ['+', '-']:
            left_val = constants.get(arg1, arg1)
            right_val = arg2
            if isinstance(right_val, dict) and right_val.get('type') == 'number':
                right_val = right_val['value']
            right_val = constants.get(str(right_val), right_val)
            
            if isinstance(left_val, int) and isinstance(right_val, int):
                if op == '+':
                    new_val = left_val + right_val
                else:
                    new_val = left_val - right_val
                optimized.append(('COPY', new_val, None, result))
                constants[result] = new_val
                optimizations_done.append(f"Constant folding: {arg1} {op} {right_val} = {new_val}")
                continue
        
        if op == 'SET':
            if isinstance(arg2, int):
                constants[arg1] = arg2
        
        if op == 'COPY' and isinstance(arg1, int):
            constants[result] = arg1
        
        optimized.append((op, arg1, arg2, result))
    
    return optimized, optimizations_done


def print_optimization(optimized_ir, optimizations):
    print("\n" + "="*50)
    print("PHASE 5: OPTIMIZATION")
    print("="*50)
    
    if optimizations:
        print("\n  Optimizations performed:")
        for opt in optimizations:
            print(f"    - {opt}")
    else:
        print("\n  No optimizations applied.")
    
    print("\n  Optimized code: (same as TAC if no changes)")
    print("="*50)


def generate_target_code(ir_code, program):
    lines = []
    lines.append("# Generated StoryScript Program")
    lines.append("# Target Code Output")
    lines.append("")
    lines.append("# --- Data Section ---")
    lines.append("characters = {}")
    lines.append("variables = {}")
    lines.append("choices = []")
    lines.append("")
    
    # Initialize characters
    for char in program['characters']:
        lines.append(f"characters['{char['id']}'] = \"{char['name']}\"")
    
    lines.append("")
    
    # Initialize variables
    for var in program['variables']:
        val = var['value']
        if isinstance(val, dict):
            if val['type'] == 'number':
                lines.append(f"variables['{var['id']}'] = {val['value']}")
            elif val['type'] == 'boolean':
                lines.append(f"variables['{var['id']}'] = {val['value']}")
        else:
            lines.append(f"variables['{var['id']}'] = {val}")
    
    lines.append("")
    lines.append("# --- Code Section ---")
    
    for scene in program['scenes']:
        lines.append(f"")
        lines.append(f"def scene_{scene['id']}():")
        lines.append(f"    global choices")
        lines.append(f"    choices = []")
        
        for stmt in scene['statements']:
            if stmt['type'] == 'say':
                lines.append(f"    print(f\"{{characters['{stmt['character']}']}}:  {stmt['text']}\")")
            
            elif stmt['type'] == 'choice':
                lines.append(f"    choices.append((\"{stmt['text']}\", scene_{stmt['target']}))")
            
            elif stmt['type'] == 'goto':
                lines.append(f"    return scene_{stmt['target']}")
            
            elif stmt['type'] == 'set':
                val = stmt['value']
                if isinstance(val, dict):
                    if val['type'] == 'number':
                        lines.append(f"    variables['{stmt['variable']}'] = {val['value']}")
                    elif val['type'] == 'binary':
                        right_val = val['right']
                        if isinstance(right_val, dict) and right_val['type'] == 'number':
                            right_val = right_val['value']
                        lines.append(f"    variables['{stmt['variable']}'] = variables['{val['left']}'] {val['op']} {right_val}")
            
            elif stmt['type'] == 'if':
                cond = stmt['condition']
                if cond['type'] == 'comparison':
                    left = cond['left']
                    right = cond['right']
                    left_str = f"variables['{left['name']}']" if left['type'] == 'variable' else left['value']
                    right_str = f"variables['{right['name']}']" if right['type'] == 'variable' else right['value']
                    lines.append(f"    if {left_str} {cond['op']} {right_str}:")
                else:
                    val = f"variables['{cond['name']}']" if cond['type'] == 'variable' else cond['value']
                    lines.append(f"    if {val}:")
                
                for s in stmt['then']:
                    if s['type'] == 'goto':
                        lines.append(f"        return scene_{s['target']}")
                    elif s['type'] == 'say':
                        lines.append(f"        print(f\"{{characters['{s['character']}']}}:  {s['text']}\")")
                
                if stmt['else']:
                    lines.append(f"    else:")
                    for s in stmt['else']:
                        if s['type'] == 'goto':
                            lines.append(f"        return scene_{s['target']}")
                        elif s['type'] == 'say':
                            lines.append(f"        print(f\"{{characters['{s['character']}']}}:  {s['text']}\")")
        
        # Handle choices at end
        lines.append(f"    if choices:")
        lines.append(f"        print('\\nChoices:')")
        lines.append(f"        for i, (text, _) in enumerate(choices, 1):")
        lines.append(f"            print(f'  {{i}}. {{text}}')")
        lines.append(f"        choice = int(input('Enter choice: '))")
        lines.append(f"        return choices[choice-1][1]")
        lines.append(f"    return None")
    
    lines.append("")
    lines.append("# --- Main ---")
    lines.append(f"print('\\n===  {program['title']}  ===')")
    lines.append("print()")
    lines.append(f"next_scene = scene_{program['scenes'][0]['id']}")
    lines.append("while next_scene:")
    lines.append("    next_scene = next_scene()")
    lines.append("print('\\n=== THE END ===')")
    
    return "\n".join(lines)


def print_target_code(code):
    print("\n" + "="*50)
    print("PHASE 6: TARGET CODE (Python)")
    print("="*50)
    print(code)
    print("="*50)


def run_story(program):
    characters = {}
    variables = {}
    scenes = {}
    
    for char in program['characters']:
        characters[char['id']] = char['name']
    
    for var in program['variables']:
        val = var['value']
        if isinstance(val, dict):
            if val['type'] == 'number':
                variables[var['id']] = val['value']
            elif val['type'] == 'boolean':
                variables[var['id']] = val['value']
        else:
            variables[var['id']] = val
    
    for scene in program['scenes']:
        scenes[scene['id']] = scene
    
    print(f"\n{'='*50}")
    print(f"  {program['title']}")
    print(f"{'='*50}\n")
    
    current_scene = program['scenes'][0]['id']
    
    while current_scene:
        scene = scenes[current_scene]
        choices = []
        next_scene = None
        
        for stmt in scene['statements']:
            if stmt['type'] == 'say':
                char_name = characters.get(stmt['character'], stmt['character'])
                print(f"{char_name}:  {stmt['text']}")
            
            elif stmt['type'] == 'choice':
                choices.append((stmt['text'], stmt['target']))
            
            elif stmt['type'] == 'goto':
                next_scene = stmt['target']
                break
            
            elif stmt['type'] == 'set':
                val = stmt['value']
                if isinstance(val, dict):
                    if val['type'] == 'number':
                        variables[stmt['variable']] = val['value']
                    elif val['type'] == 'boolean':
                        variables[stmt['variable']] = val['value']
                    elif val['type'] == 'binary':
                        left_val = variables.get(val['left'], 0)
                        right_val = val['right']
                        if isinstance(right_val, dict):
                            right_val = right_val.get('value', 0)
                        if val['op'] == '+':
                            variables[stmt['variable']] = left_val + right_val
                        elif val['op'] == '-':
                            variables[stmt['variable']] = left_val - right_val
            
            elif stmt['type'] == 'if':
                cond = stmt['condition']
                condition_met = False
                
                if cond['type'] == 'comparison':
                    left = cond['left']
                    right = cond['right']
                    left_val = variables.get(left['name'], left.get('value', 0)) if left['type'] == 'variable' else left.get('value', 0)
                    right_val = variables.get(right['name'], right.get('value', 0)) if right['type'] == 'variable' else right.get('value', 0)
                    
                    if cond['op'] == '>':
                        condition_met = left_val > right_val
                    elif cond['op'] == '<':
                        condition_met = left_val < right_val
                    elif cond['op'] == '==':
                        condition_met = left_val == right_val
                else:
                    val = variables.get(cond.get('name'), cond.get('value', False))
                    condition_met = bool(val)
                
                branch = stmt['then'] if condition_met else stmt['else']
                for s in branch:
                    if s['type'] == 'goto':
                        next_scene = s['target']
                        break
                    elif s['type'] == 'say':
                        char_name = characters.get(s['character'], s['character'])
                        print(f"{char_name}:  {s['text']}")
                
                if next_scene:
                    break
        
        if next_scene:
            current_scene = next_scene
            continue
        
        if choices:
            print("\nChoices:")
            for i, (text, target) in enumerate(choices, 1):
                print(f"  {i}. {text}")
            
            try:
                choice = int(input("\nEnter choice: "))
                if 1 <= choice <= len(choices):
                    current_scene = choices[choice - 1][1]
                else:
                    print("Invalid choice")
            except (ValueError, EOFError):
                break
        else:
            current_scene = None
    
    print(f"\n{'='*50}")
    print("  THE END")
    print(f"{'='*50}\n")


def compile_story(source_code, show_phases=False, run=True):
    print("StoryScript Compiler")
    print("="*50)
    
    print("\n[Phase 1] Tokenizing...")
    tokens = tokenize(source_code)
    if show_phases:
        print_tokens(tokens)
    print("  ✓ Tokenization complete")
    
    print("\n[Phase 2] Parsing...")
    parser = Parser(tokens)
    try:
        program = parser.parse()
        if show_phases:
            print_parse_tree(parser)
            print("\n" + "="*50)
            print("ABSTRACT SYNTAX TREE (AST)")
            print("="*50)
            print_ast(program)
            print("="*50)
        print("  ✓ Parsing complete")
    except SyntaxError as e:
        print(f"  ✗ Syntax Error: {e}")
        return
    
    print("\n[Phase 3] Semantic Analysis...")
    symbol_table, errors = semantic_analysis(program)
    if show_phases:
        print_symbol_table(symbol_table)
    if errors:
        for err in errors:
            print(f"  ✗ Error: {err}")
        return
    print("  ✓ Semantic analysis complete")
    
    print("\n[Phase 4] Generating IR...")
    ir_code = generate_ir(program)
    if show_phases:
        print_ir(ir_code)
    print("  ✓ IR generation complete")
    
    print("\n[Phase 5] Optimizing...")
    optimized_ir, optimizations = optimize(ir_code)
    if show_phases:
        print_optimization(optimized_ir, optimizations)
    print(f"  ✓ Optimization complete ({len(optimizations)} optimizations)")
    
    print("\n[Phase 6] Generating target code...")
    target_code = generate_target_code(optimized_ir, program)
    if show_phases:
        print_target_code(target_code)
    print("  ✓ Code generation complete")
    
    print("\n" + "="*50)
    print("Compilation Successful!")
    print("="*50)
    
    if run:
        print("\n\nRunning story...\n")
        run_story(program)
    
    return program, target_code


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        show_phases = '--phases' in sys.argv or '-p' in sys.argv
        no_run = '--no-run' in sys.argv or '-n' in sys.argv
        
        try:
            with open(filename, 'r') as f:
                source = f.read()
            compile_story(source, show_phases=show_phases, run=not no_run)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
    else:
        demo_story = '''
STORY "Hello World"

CHARACTER narrator "Narrator"

SET counter = 1

SCENE start
    narrator SAY "Welcome to StoryScript!"
    narrator SAY "This is a simple demo."
    GOTO ending
END SCENE

SCENE ending
    narrator SAY "Goodbye!"
END SCENE

END STORY
'''
        print("No file provided. Running demo...\n")
        compile_story(demo_story, show_phases=True)
