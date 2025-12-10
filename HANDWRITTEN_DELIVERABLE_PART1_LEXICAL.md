# PART 1: LEXICAL ANALYSIS
## Handwritten Deliverable - StoryScript Compiler

---

## 1. REGULAR EXPRESSIONS FOR TOKENS

### Token Patterns with Domain Mapping

```
┌─────────────────────────────────────────────────────────────┐
│  TOKEN       │  PATTERN (Regex)        │  DOMAIN            │
├──────────────┼─────────────────────────┼────────────────────┤
│  KEYWORD     │  STORY|END|SCENE|IF|... │  Reserved words    │
│  ID          │  [a-zA-Z_][a-zA-Z0-9_]* │  Identifiers       │
│  NUMBER      │  [0-9]+                 │  Integer literals  │
│  STRING      │  "[^"]*"                │  String literals   │
│  ASSIGN      │  =                      │  Assignment        │
│  GREATER     │  >                      │  Comparison        │
│  PLUS        │  \+                     │  Arithmetic        │
│  ARROW       │  ->                     │  Choice pointer    │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. DFA DIAGRAMS

### DFA for IDENTIFIER

```
     [a-zA-Z_]        [a-zA-Z0-9_]
(q0) ---------> (q1) -------------> ((q1))
START          ACCEPT     Loop back
```

### DFA for NUMBER

```
           [0-9]          [0-9]
(q0) -------> (q1) --------> ((q1))
START        ACCEPT    Loop back
```

### DFA for STRING

```
         "           any char         "
(q0) ------> (q1) ---------> (q1) ------> ((q2))
START       Reading         Loop    ACCEPT
```

---

## 3. TRANSITION TABLES

### Identifier Transition Table

```
┌───────┬──────────┬───────────┬───────────┐
│ State │ [a-zA-Z_]│ [0-9]     │ Other     │
├───────┼──────────┼───────────┼───────────┤
│  q0   │   q1     │   ERROR   │   ERROR   │
│  q1   │   q1     │   q1      │   ACCEPT  │
└───────┴──────────┴───────────┴───────────┘
```

### Number Transition Table

```
┌───────┬──────────┬───────────┐
│ State │  [0-9]   │   Other   │
├───────┼──────────┼───────────┤
│  q0   │   q1     │   ERROR   │
│  q1   │   q1     │   ACCEPT  │
└───────┴──────────┴───────────┘
```

---

## 4. TOKEN STREAMS (Use Simple Core Example)

### Example 1: SET score = 0

```
┌────┬────────────┬──────────┬──────┐
│ #  │ TOKEN_TYPE │  VALUE   │ LINE │
├────┼────────────┼──────────┼──────┤
│  1 │ SET        │ SET      │  1   │
│  2 │ ID         │ score    │  1   │
│  3 │ ASSIGN     │ =        │  1   │
│  4 │ NUMBER     │ 0        │  1   │
└────┴────────────┴──────────┴──────┘
```

### Example 2: host SAY "Hello!"

```
┌────┬────────────┬──────────┬──────┐
│ #  │ TOKEN_TYPE │  VALUE   │ LINE │
├────┼────────────┼──────────┼──────┤
│  1 │ ID         │ host     │  1   │
│  2 │ SAY        │ SAY      │  1   │
│  3 │ STRING     │ Hello!   │  1   │
└────┴────────────┴──────────┴──────┘
```

### Example 3: CHOICE "Play" -> game

```
┌────┬────────────┬──────────┬──────┐
│ #  │ TOKEN_TYPE │  VALUE   │ LINE │
├────┼────────────┼──────────┼──────┤
│  1 │ CHOICE     │ CHOICE   │  1   │
│  2 │ STRING     │ Play     │  1   │
│  3 │ ARROW      │ ->       │  1   │
│  4 │ ID         │ game     │  1   │
└────┴────────────┴──────────┴──────┘
```

### Example 4: SET score = score + 1

```
┌────┬────────────┬──────────┬──────┐
│ #  │ TOKEN_TYPE │  VALUE   │ LINE │
├────┼────────────┼──────────┼──────┤
│  1 │ SET        │ SET      │  1   │
│  2 │ ID         │ score    │  1   │
│  3 │ ASSIGN     │ =        │  1   │
│  4 │ ID         │ score    │  1   │
│  5 │ PLUS       │ +        │  1   │
│  6 │ NUMBER     │ 1        │  1   │
└────┴────────────┴──────────┴──────┘
```

### Example 5: IF score > 0

```
┌────┬────────────┬──────────┬──────┐
│ #  │ TOKEN_TYPE │  VALUE   │ LINE │
├────┼────────────┼──────────┼──────┤
│  1 │ IF         │ IF       │  1   │
│  2 │ ID         │ score    │  1   │
│  3 │ GREATER    │ >        │  1   │
│  4 │ NUMBER     │ 0        │  1   │
└────┴────────────┴──────────┴──────┘
```

### Example 6: GOTO win

```
┌────┬────────────┬──────────┬──────┐
│ #  │ TOKEN_TYPE │  VALUE   │ LINE │
├────┼────────────┼──────────┼──────┤
│  1 │ GOTO       │ GOTO     │  1   │
│  2 │ ID         │ win      │  1   │
└────┴────────────┴──────────┴──────┘
```

---

## 5. ERROR CASES AND COVERAGE NOTES

### Lexical Error Handling (required edge cases)

```
Unrecognized character:  @  → ERROR at line X, column Y
Unterminated string:     "Hello  → ERROR: missing closing quote
Bad arrow:               - >     → Emit '-' then ERROR('> expected')
```

### Token Stream Coverage Summary

- 6 micro examples above span all token kinds (keywords, IDs, numbers, strings, operators, arrow).
- Quiz story (24 lines) adds STORY/END/SCENE/IF/ELSE/GOTO/CHOICE paths; first tokens:
     - STORY "Quiz" | CHARACTER host "Host" | SET score = 0 | SCENE start ...
     - (Remaining tokens follow the same patterns; no extra token classes appear.)
- The same token set applies to `examples/test1_simple.story`, `test2_adventure.story`, and `test3_mystery.story`; no additional lexical classes are needed.

---

END OF PART 1: LEXICAL ANALYSIS
