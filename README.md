# StoryScript Compiler

## CS4031 – Compiler Construction Project

A mini-compiler for text-based story scripting.

---

## Quick Start

```bash
# Run a story
python compiler.py examples/test1_simple.story

# Show all 6 compilation phases
python compiler.py examples/test2_adventure.story --phases

# Compile only (don't run)
python compiler.py examples/test3_mystery.story --phases --no-run
```

---

## Language Syntax

### Keywords (13 total)
```
STORY, END, SCENE, CHARACTER, SAY, CHOICE, GOTO, SET, IF, ELSE, ENDIF, TRUE, FALSE
```

### Program Structure
```
STORY "Title"

CHARACTER id "Display Name"
SET variable = value

SCENE scene_name
    character SAY "dialogue"
    CHOICE "option" -> target_scene
    GOTO scene_name
    SET variable = value
    IF condition
        statements
    ELSE
        statements
    ENDIF
END SCENE

END STORY
```

### Example Story
```
STORY "Hello World"

CHARACTER hero "The Hero"
SET health = 100

SCENE start
    hero SAY "Hello everyone!"
    IF health > 50
        hero SAY "I feel great!"
        GOTO win
    ELSE
        hero SAY "I need rest..."
        GOTO lose
    ENDIF
END SCENE

SCENE win
    hero SAY "Victory!"
END SCENE

SCENE lose
    hero SAY "Maybe next time..."
END SCENE

END STORY
```

---

## Compilation Phases

### Phase 1: Lexical Analysis
Tokenizes source code into meaningful lexemes.

**Example:**
- Input: `hero SAY "Hello!"`
- Output: `[ID:hero] [SAY:SAY] [STRING:Hello!]`

---

### Phase 2: Syntax Analysis
Validates grammar and constructs parse tree.

**Grammar (simplified):**
```
program    → STORY string characters scenes END STORY
character  → CHARACTER id string
scene      → SCENE id statements END SCENE
statement  → id SAY string
           | CHOICE string -> id
           | GOTO id
           | SET id = value
           | IF condition statements ENDIF
```

**Parse Tree Example:**
```
program
├── STORY "Hello"
├── CHARACTER hero "Hero"
├── SCENE start
│   ├── SAY hero "Hi!"
│   └── GOTO end
└── END STORY
```

---

### Phase 3: Semantic Analysis
Validates semantic correctness and builds symbol table.

**Validation checks:**
- Character declarations
- Scene references
- Variable usage

**Symbol Table:**
| Name | Type | Value |
|------|------|-------|
| hero | character | "The Hero" |
| health | variable | 100 |
| start | scene | - |

---

### Phase 4: Intermediate Representation
Generates three-address code (TAC) using quadruples.

**Format:** `(operator, arg1, arg2, result)`

---

### Phase 5: Optimization
Applies constant folding and propagation.

---

### Phase 6: Code Generation
Produces executable Python code.

---

## Project Files

```
cc_proj/
├── compiler.py          # THE MAIN FILE (all-in-one)
├── examples/
│   ├── test1_simple.story    # Basic dialogue
│   ├── test2_adventure.story # Variables & conditions
│   └── test3_mystery.story   # Multiple scenes
└── README.md
```

**Note:** Everything is in ONE file (`compiler.py`) for simplicity!

---

## Test Cases

### Test 1: Simple Dialogue
Basic character interactions with branching.

### Test 2: Adventure  
Variable manipulation and conditional logic.

### Test 3: Mystery
Multi-scene navigation with state tracking.

## Running with Phases Display

```bash
python compiler.py examples/test2_adventure.story --phases
```

This shows:
1. **Token Stream** - All tokens found
2. **Parse Tree** - Grammar derivation
3. **AST** - Abstract Syntax Tree
4. **Symbol Table** - All symbols
5. **TAC** - Three-Address Code (Quadruples)
6. **Optimizations** - What was optimized
7. **Target Code** - Generated Python

---

## Sample Output

```
StoryScript Compiler
==================================================

[Phase 1] Tokenizing...
  ✓ Tokenization complete

[Phase 2] Parsing...
  ✓ Parsing complete

[Phase 3] Semantic Analysis...
  ✓ Semantic analysis complete

[Phase 4] Generating IR...
  ✓ IR generation complete

[Phase 5] Optimizing...
  ✓ Optimization complete (1 optimizations)

[Phase 6] Generating target code...
  ✓ Code generation complete

==================================================
Compilation Successful!
==================================================
```

---

## For Your Submission

### Handwritten Documents Needed:
1. **Lexical:** Token patterns, DFA for identifiers/numbers/strings
2. **Syntax:** Parse trees for 3 test cases, grammar rules
3. **Semantic:** Symbol tables for each test case

## Documentation

Generated artifacts for each phase:
- Token streams
- Parse trees
- Symbol tables
- Three-address code
- Optimization reports
- Target code
