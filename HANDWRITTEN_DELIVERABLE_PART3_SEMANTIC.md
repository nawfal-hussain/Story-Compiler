# PART 3: SEMANTIC ANALYSIS
## Handwritten Deliverable Guide - StoryScript Compiler

---

## 1. SYNTAX-DIRECTED DEFINITIONS (SDD)

### SDD for Type Checking and Symbol Table Construction

```
┌──────────────────────────────────────────────────────────────────┐
│ PRODUCTION                    │  SEMANTIC RULES                  │
├───────────────────────────────┼──────────────────────────────────┤
│ 1. program → STORY STRING     │ symtab.new_scope()               │
│    declarations scenes        │ program.title = STRING.value     │
│    END STORY                  │ check_all_scenes_defined()       │
│                               │ program.symtab = symtab          │
├───────────────────────────────┼──────────────────────────────────┤
│ 2. character_decl →           │ IF symtab.lookup(ID.name):       │
│    CHARACTER ID STRING        │    ERROR("Duplicate character")  │
│                               │ ELSE:                            │
│                               │    symtab.insert(ID.name,        │
│                               │        type='character',         │
│                               │        value=STRING.value)       │
├───────────────────────────────┼──────────────────────────────────┤
│ 3. variable_decl →            │ IF symtab.lookup(ID.name):       │
│    SET ID ASSIGN value        │    ERROR("Duplicate variable")   │
│                               │ ELSE:                            │
│                               │    symtab.insert(ID.name,        │
│                               │        type=value.type,          │
│                               │        value=value.val)          │
├───────────────────────────────┼──────────────────────────────────┤
│ 4. scene → SCENE ID           │ IF symtab.lookup_scene(ID.name): │
│    statements END SCENE       │    ERROR("Duplicate scene")      │
│                               │ ELSE:                            │
│                               │    symtab.insert_scene(ID.name)  │
│                               │    scene.name = ID.name          │
├───────────────────────────────┼──────────────────────────────────┤
│ 5. say_stmt →                 │ IF NOT symtab.lookup(ID.name):   │
│    ID SAY STRING              │    ERROR("Undefined character")  │
│                               │ stmt.type = 'say'                │
│                               │ stmt.character = ID.name         │
├───────────────────────────────┼──────────────────────────────────┤
│ 6. choice_stmt →              │ IF NOT symtab.lookup_scene(ID):  │
│    CHOICE STRING ARROW ID     │    ERROR("Undefined scene")      │
│                               │ stmt.type = 'choice'             │
│                               │ stmt.target = ID.name            │
├───────────────────────────────┼──────────────────────────────────┤
│ 7. goto_stmt → GOTO ID        │ IF NOT symtab.lookup_scene(ID):  │
│                               │    ERROR("Undefined scene")      │
│                               │ stmt.type = 'goto'               │
│                               │ stmt.target = ID.name            │
├───────────────────────────────┼──────────────────────────────────┤
│ 8. set_stmt →                 │ IF NOT symtab.lookup(ID.name):   │
│    SET ID ASSIGN expr         │    WARNING("Implicit var decl")  │
│                               │ type_check(expr)                 │
│                               │ symtab.update(ID, expr.type)     │
├───────────────────────────────┼──────────────────────────────────┤
│ 9. if_stmt →                  │ type_check(condition)            │
│    IF condition statements    │ IF condition.type != 'boolean':  │
│    ELSE statements ENDIF      │    TRY_COERCE_TO_BOOLEAN()       │
│                               │ stmt.type = 'if'                 │
├───────────────────────────────┼──────────────────────────────────┤
│ 10. expr → value binop value  │ IF value1.type != value2.type:   │
│                               │    ERROR("Type mismatch")        │
│                               │ IF value1.type NOT IN [int]:     │
│                               │    ERROR("Invalid operation")    │
│                               │ expr.type = value1.type          │
├───────────────────────────────┼──────────────────────────────────┤
│ 11. condition →               │ IF expr1.type != expr2.type:     │
│     expr1 relop expr2         │    TRY_TYPE_COERCION()           │
│                               │ condition.type = 'boolean'       │
│                               │ condition.value = COMPUTE()      │
├───────────────────────────────┼──────────────────────────────────┤
│ 12. value → ID                │ entry = symtab.lookup(ID.name)   │
│                               │ IF NOT entry:                    │
│                               │    ERROR("Undefined identifier") │
│                               │ value.type = entry.type          │
│                               │ value.val = entry.value          │
├───────────────────────────────┼──────────────────────────────────┤
│ 13. value → NUMBER            │ value.type = 'integer'           │
│                               │ value.val = NUMBER.value         │
├───────────────────────────────┼──────────────────────────────────┤
│ 14. value → STRING            │ value.type = 'string'            │
│                               │ value.val = STRING.value         │
├───────────────────────────────┼──────────────────────────────────┤
│ 15. value → TRUE | FALSE      │ value.type = 'boolean'           │
│                               │ value.val = TRUE/FALSE           │
└───────────────────────────────┴──────────────────────────────────┘
```

---

## 2. SYNTAX-DIRECTED TRANSLATION (SDT)

### SDT with Embedded Actions (Essential Rules Only)

```
character_decl → CHARACTER ID STRING
                 { if (symtab.lookup(ID.name))
                       error("Duplicate");
                   symtab.insert(ID.name, 'character', STRING.value);
                 }

set_stmt → SET ID { check_or_create(ID); }
           ASSIGN expr
           { symtab.update(ID, expr.type, expr.value); }

if_stmt → IF condition
          { if (cond.type != 'boolean') coerce();
            emit("IF_FALSE", cond.result, else_label);
          }
          statements
          { emit("GOTO", end_label);
            emit("LABEL", else_label);
          }
          ENDIF
          { emit("LABEL", end_label); }

expr → value₁ binop value₂
       { if (value₁.type != value₂.type) error();
         temp = new_temp();
         emit(binop.op, value₁.result, value₂.result, temp);
         expr.result = temp;
       }
```

---

## 3. L-ATTRIBUTED vs S-ATTRIBUTED

### S-Attributed (Synthesized Only)

```
Production: expr → expr₁ + term
Rule: expr.value = expr₁.value + term.value  [SYNTHESIZED]

Attribute flow: BOTTOM-UP only (children to parent)
```

### L-Attributed (Inherited + Synthesized)

```
Production: statements → stmt statements₁
Rules:
  statements₁.scope = statements.scope  [INHERITED - passed down]
  statements.valid = stmt.valid AND statements₁.valid  [SYNTHESIZED]

Attribute flow: TOP-DOWN (inherited) and BOTTOM-UP (synthesized)
```

**Key Difference:**
- S-Attributed: Only synthesized (↑)
- L-Attributed: Both inherited (↓) and synthesized (↑)
│                         │ expr.type = 'integer'            │
├─────────────────────────┼──────────────────────────────────┤
│ value → ID              │ value.type = lookup_type(ID)     │
│                         │ value.name = ID.name             │
└─────────────────────────┴──────────────────────────────────┘

All attributes flow BOTTOM-UP (from children to parent)
```

### L-Attributed Grammar (Inherited + Synthesized)

**Example: Type Propagation with Declaration**

```
Production: decl → type var_list

Attributes:
  var_list.dtype = type.name   [INHERITED - passed down]
  decl.symtab = var_list.symtab [SYNTHESIZED - passed up]

Parse Tree with Attribute Flow:

           decl
          /     \
       type    var_list (dtype=int)  ← INHERITED from type
        |         |
       int    [var₁, var₂]
                  ↓
          Each var gets dtype=int
```

**L-Attributed Examples in StoryScript:**

```
┌────────────────────────────────────────────────────────────────┐
│ PRODUCTION                  │ SEMANTIC RULES                   │
├─────────────────────────────┼──────────────────────────────────┤
│ statements → stmt stmts     │ stmts.scope = statements.scope   │
│                             │     [INHERITED - scope info]     │
│                             │ statements.symtab =              │
│                             │     merge(stmt.symtab,           │
│                             │           stmts.symtab)          │
│                             │     [SYNTHESIZED]                │
├─────────────────────────────┼──────────────────────────────────┤
│ scene → SCENE ID stmts      │ stmts.scene_name = ID.name       │
│                             │     [INHERITED]                  │
│                             │ scene.valid = check_stmts(stmts) │
│                             │     [SYNTHESIZED]                │
└─────────────────────────────┴──────────────────────────────────┘
```

### Classification Table

```
┌─────────────────────────────┬──────────────┬──────────────┐
│ GRAMMAR RULE                │ S-ATTR?      │ L-ATTR?      │
├─────────────────────────────┼──────────────┼──────────────┤
│ expr → expr + term          │ YES          │ YES          │
│ value → NUMBER              │ YES          │ YES          │
│ scene → SCENE ID stmts      │ NO           │ YES          │
│  (passes scope to stmts)    │              │              │
│ program → decls scenes      │ NO           │ YES          │
│  (passes symtab to scenes)  │              │              │
└─────────────────────────────┴──────────────┴──────────────┘

Note: All S-Attributed grammars are L-Attributed,
      but not all L-Attributed are S-Attributed.
```

---

## 4. L-ATTRIBUTED WALK (Quiz Story)

1. Enter `STORY "Quiz"` → `symtab.new_scope()`, record title.
2. `CHARACTER host "Host"` → insert `{host: character, "Host"}`.
3. `SET score = 0` → insert `{score: int, 0}`; type=int via NUMBER.
4. `SCENE start` → insert scene; statements validated with inherited scope.
5. `SCENE game` → compute `score > 0`; type-check ints; branches to `win` or `start` (scene existence validated).
6. `SCENE win` → SAY checked against characters table.

---

## 5. ANNOTATED PARSE TREES WITH ATTRIBUTES

### Annotated Parse Tree 1: Variable Declaration

```
Input: SET health = 100

                <variable_decl>
                [type: int, value: 100, scope: global]
                    /    |    |    \
                   /     |    |     \
                 SET    ID  ASSIGN  <value>
                        |           [type: int, value: 100]
                   [name: health]   |
                   [scope: global]  |
                                 NUMBER
                                 [lexval: 100]
                                 [type: int]

Semantic Actions:
1. Check if 'health' already in symbol table → NO
2. Evaluate value: type=int, value=100
3. Insert into symtab: {health: {type:'int', value:100, scope:'global'}}
```

### Annotated Parse Tree 2: Conditional Expression

```
Input: IF dream_level > 0

                <if_stmt>
                [cond_type: boolean, result: L1]
                    /       |        \
                   /        |         \
                 IF    <condition>   <stmts> ...
                       [type: boolean]
                       [result: t1]
                       /      |      \
                      /       |       \
                  <expr>   <relop>  <expr>
               [type: int]    |    [type: int]
               [result:       >    [result: 0]
                dream_level] [op: >]
                    |                  |
                  <value>           <value>
                [type: int]        [type: int]
                [name:             [value: 0]
                 dream_level]         |
                    |               NUMBER
                   ID               [lexval: 0]
              [lexeme:
               dream_level]

Semantic Actions:
1. Lookup 'dream_level' in symtab → Found, type=int
2. Check types: int > int → Valid comparison
3. Result type: boolean
4. Generate: t1 = dream_level > 0
5. Generate: IF_FALSE t1 GOTO else_label
```

### Annotated Parse Tree 3: Arithmetic Expression

```
Input: SET count = count + 1

                <set_stmt>
                [var: count, type: int, result: t2]
                    /    |    |     \
                   /     |    |      \
                 SET    ID  ASSIGN  <expr>
                        |           [type: int, result: t2]
                   [name: count]    /    |    \
                                   /     |     \
                              <value> <binop> <value>
                           [type: int]  |  [type: int]
                           [result:    +   [value: 1]
                            count]  [op: +]    |
                               |             NUMBER
                              ID             [lexval: 1]
                         [lexeme: count]

Semantic Actions:
1. Lookup 'count' in symtab → Found, type=int
2. Left operand: count (int)
3. Right operand: 1 (int)
4. Type check: int + int → Valid, result type=int
5. Generate: t1 = count
6. Generate: t2 = t1 + 1
7. Update symtab: count = t2
```

### Annotated Parse Tree 4: SAY Statement with Character Lookup

```
Input: narrator SAY "Hello World"

                <say_stmt>
                [char: narrator, text: "Hello World", valid: true]
                    /       |         \
                   /        |          \
                 ID        SAY       STRING
         [lexeme: narrator] |    [lexval: "Hello World"]
         [type: character]  |    [type: string]
         [display_name:     |
          "Narrator"]       |

Semantic Actions:
1. Lookup 'narrator' in symtab → Found in characters
2. Get display name: "Narrator"
3. Validate string literal → OK
4. Create SAY node with character reference
5. Return: {type: 'say', character: 'narrator', text: "Hello World"}
```

### Annotated Parse Tree 5: CHOICE Statement with Scene Reference

```
Input: CHOICE "Press defender" -> press

                <choice_stmt>
                [text: "Press defender", target: press, valid: true]
                    /      |        |       \
                   /       |        |        \
              CHOICE    STRING   ARROW      ID
                          |                 [lexeme: press]
                  [lexval:                  [type: scene]
                   "Press defender"]        [exists: true]
                  [type: string]

Semantic Actions:
1. Validate string literal → OK
2. Lookup scene 'press' in symtab → Found
3. Create CHOICE node with scene reference
4. Return: {type: 'choice', text: "Press defender", target: 'press'}
```

---

## 6. SYMBOL TABLE (Use Simple Core Example)

### Symbol Table for Quiz Story

```
┌──────────────┬─────────────┬──────────────┬────────┬──────┐
│ NAME         │ TYPE        │ VALUE        │ SCOPE  │ LINE │
├──────────────┼─────────────┼──────────────┼────────┼──────┤
│ CHARACTERS                                                 │
├──────────────┼─────────────┼──────────────┼────────┼──────┤
│ host         │ character   │ "Host"       │ global │  3   │
├──────────────┼─────────────┼──────────────┼────────┼──────┤
│ VARIABLES                                                  │
├──────────────┼─────────────┼──────────────┼────────┼──────┤
│ score        │ integer     │ 0            │ global │  4   │
├──────────────┼─────────────┼──────────────┼────────┼──────┤
│ SCENES                                                     │
├──────────────┼─────────────┼──────────────┼────────┼──────┤
│ start        │ scene       │ scene_start  │ global │  6   │
│ game         │ scene       │ scene_game   │ global │ 11   │
│ win          │ scene       │ scene_win    │ global │ 21   │
└──────────────┴─────────────┴──────────────┴────────┴──────┘
```

---

## 7. SEMANTIC ERROR COVERAGE (Minimal Set)

- Undefined scene: `GOTO finale` where `finale` not in symtab → error before codegen.
- Duplicate scene: second `SCENE start` → reject; keeps first definition only.
- Type mismatch: `SET score = "hi"` when `score` was int → error; no implicit coercion.
- Implicit var warning (allowed): `SET coins = coins + 1` when `coins` unseen → warn + insert int.

---

## 8. SYMBOL TABLES FOR EXAMPLE TEST CASES

### `examples/test1_simple.story`

```
Characters: narrator, player
Variables:  (none)
Scenes: start, press, mark, pass_ronaldo, shoot_glory, celebration
Scope: single global scope; choices jump across scenes only.
```

### `examples/test2_adventure.story`

```
Characters: guide, hero
Variables: torch(int, init=1)
Scenes: start, cave, fork_left, fork_right, exit
Scope: global + per-scene inherited attributes for condition checks.
```

### `examples/test3_mystery.story`

```
Characters: detective, suspect, narrator
Variables: clues(int, init=0), trust(int, init=5)
Scenes: intro, question, accuse, release, ending_good, ending_bad
Scope: global; nested IF/CHOICE still use same symtab entries.
```



---

END OF PART 3: SEMANTIC ANALYSIS
