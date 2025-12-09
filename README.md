# Story Compiler

## CS4031 Compiler Construction Project

---

## Usage

```bash
python compiler.py
```

---

## Intermediate Representation

The compiler generates three-address code (TAC) using quadruples.

**Quadruple Format:** `(operation, arg1, arg2, result)`

**Operations:**
- `PROGRAM` - Program header
- `CHAR` - Character declaration
- `SET` - Variable assignment
- `LABEL` - Code label
- `SAY` - Dialogue output
- `CHOICE` - User choice
- `GOTO` - Unconditional jump
- `IF_FALSE` - Conditional jump
- `COPY` - Value copy

---

## Example Output

```
#    Op           Arg1            Arg2            Result    
---- ------------ --------------- --------------- ----------
0    PROGRAM      Test            -               -         
1    CHAR         hero            Hero            -         
2    SET          health          100             -         
3    LABEL        scene_start     -               -         
```
