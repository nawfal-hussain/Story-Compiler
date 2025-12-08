# StoryScript Compiler

## CS4031 Compiler Construction Project

---

## Current Status

✓ Phase 1: Lexical Analysis  
✓ Phase 2: Syntax Analysis  
✓ Phase 3: Semantic Analysis

Next: IR Generation

---

## Usage

```bash
python compiler.py
```

---

## Language Features

### Supported Statements
- `CHARACTER` declarations
- `SET` variable assignments
- `SAY` dialogue
- `CHOICE` branching
- `GOTO` jumps
- `IF/ELSE/ENDIF` conditionals

### Operators
- Comparison: `>`, `<`, `==`
- Assignment: `=`

---

## Semantic Validation

The compiler now validates:
- Character references
- Scene targets
- Variable declarations
