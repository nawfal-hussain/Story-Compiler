# Story Compiler

## CS4031 Compiler Construction Project

---

## Current Status

✓ Phase 1: Lexical Analysis  
✓ Phase 2: Syntax Analysis (Parser)

In Progress: Phase 3 (Semantic Analysis)

---

## Usage

```bash
python compiler.py
```

---

## Language Grammar

```
program    → STORY string characters scenes END STORY
character  → CHARACTER id string
scene      → SCENE id statements END SCENE
statement  → id SAY string
           | CHOICE string -> id
           | GOTO id
```

---

## Features

- Tokenization of source code
- Grammar validation
- AST construction
- Basic error reporting
