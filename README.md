# Story Compiler

## CS4031 Compiler Construction Project

---

## Current Status

✓ Phase 1: Lexical Analysis  
✓ Phase 2: Syntax Analysis  
✓ Phase 3: Semantic Analysis  
✓ Phase 4: IR Generation  
✓ Phase 5: Optimization

Next: Code Generation

---

## Optimization

The compiler implements constant folding:
- Evaluates constant expressions at compile time
- Reduces arithmetic operations where possible
- Tracks constant values through the symbol table

**Example:**
```
SET x = 5
SET y = 10
SET result = x + y
```
becomes:
```
result = 15
```

---

## Test Results

Running sample programs shows successful optimization of constant arithmetic expressions.
