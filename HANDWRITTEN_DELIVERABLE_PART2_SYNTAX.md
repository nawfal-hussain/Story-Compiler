# PART 2: SYNTAX ANALYSIS (PARSING)
## Handwritten Deliverable Guide - StoryScript Compiler

---

## 1. CONTEXT-FREE GRAMMAR (CFG) FOR STORYSCRIPT

### Complete Grammar Productions

```
1.  <program> → STORY STRING <declarations> <scenes> END STORY

2.  <declarations> → <declaration> <declarations>
3.  <declarations> → ε

4.  <declaration> → <character_decl>
5.  <declaration> → <variable_decl>

6.  <character_decl> → CHARACTER ID STRING

7.  <variable_decl> → SET ID ASSIGN <value>

8.  <scenes> → <scene> <scenes>
9.  <scenes> → <scene>

10. <scene> → SCENE ID <statements> END SCENE

11. <statements> → <statement> <statements>
12. <statements> → ε

13. <statement> → <say_stmt>
14. <statement> → <choice_stmt>
15. <statement> → <goto_stmt>
16. <statement> → <set_stmt>
17. <statement> → <if_stmt>

18. <say_stmt> → ID SAY STRING

19. <choice_stmt> → CHOICE STRING ARROW ID

20. <goto_stmt> → GOTO ID

21. <set_stmt> → SET ID ASSIGN <expression>

22. <if_stmt> → IF <condition> <statements> ENDIF
23. <if_stmt> → IF <condition> <statements> ELSE <statements> ENDIF

24. <condition> → <expression> <relop> <expression>
25. <condition> → <value>

26. <expression> → <value> <binop> <value>
27. <expression> → <value>

28. <value> → ID
29. <value> → NUMBER
30. <value> → STRING
31. <value> → TRUE
32. <value> → FALSE

33. <relop> → GREATER
34. <relop> → LESS
35. <relop> → EQUALS

36. <binop> → PLUS
37. <binop> → MINUS
```

### Grammar Classification

```
Type: Context-Free Grammar (CFG)
Parsing Strategy: Recursive Descent (LL parsing)
Ambiguity: Unambiguous
Left Recursion: None (suitable for top-down parsing)
```

---

## 2. PARSING TABLES

### FIRST and FOLLOW Sets

```
┌─────────────────┬─────────────────────────────┬────────────────────────┐
│ Non-terminal    │ FIRST                       │ FOLLOW                 │
├─────────────────┼─────────────────────────────┼────────────────────────┤
│ <program>       │ {STORY}                     │ {$}                    │
│ <declarations>  │ {CHARACTER, SET, ε}         │ {SCENE}                │
│ <declaration>   │ {CHARACTER, SET}            │ {CHARACTER, SET, SCENE}│
│ <character_decl>│ {CHARACTER}                 │ {CHARACTER, SET, SCENE}│
│ <variable_decl> │ {SET}                       │ {CHARACTER, SET, SCENE}│
│ <scenes>        │ {SCENE}                     │ {END}                  │
│ <scene>         │ {SCENE}                     │ {SCENE, END}           │
│ <statements>    │ {ID, CHOICE, GOTO, SET, IF} │ {END, ELSE, ENDIF}     │
│ <statement>     │ {ID, CHOICE, GOTO, SET, IF} │ {ID, CHOICE, GOTO,...} │
│ <say_stmt>      │ {ID}                        │ {ID, CHOICE, GOTO,...} │
│ <choice_stmt>   │ {CHOICE}                    │ {ID, CHOICE, GOTO,...} │
│ <goto_stmt>     │ {GOTO}                      │ {ID, CHOICE, GOTO,...} │
│ <set_stmt>      │ {SET}                       │ {ID, CHOICE, GOTO,...} │
│ <if_stmt>       │ {IF}                        │ {ID, CHOICE, GOTO,...} │
│ <condition>     │ {ID, NUMBER, STRING, TRUE,  │ {ID, CHOICE, GOTO,...} │
│                 │  FALSE}                     │                        │
│ <expression>    │ {ID, NUMBER, STRING, TRUE,  │ {GREATER, LESS,...}    │
│                 │  FALSE}                     │                        │
│ <value>         │ {ID, NUMBER, STRING, TRUE,  │ {PLUS, MINUS, GREATER} │
│                 │  FALSE}                     │                        │
│ <relop>         │ {GREATER, LESS, EQUALS}     │ {ID, NUMBER,...}       │
│ <binop>         │ {PLUS, MINUS}               │ {ID, NUMBER,...}       │
└─────────────────┴─────────────────────────────┴────────────────────────┘
```

### LL(1) Parsing Table (Partial - Key Productions)

```
┌──────────────┬──────────┬───────────┬──────────┬─────────┬──────────┐
│ Non-terminal │ STORY    │ CHARACTER │ SET      │ SCENE   │ ID       │
├──────────────┼──────────┼───────────┼──────────┼─────────┼──────────┤
│ <program>    │ Prod 1   │           │          │         │          │
│ <declars>    │          │ Prod 2    │ Prod 2   │ Prod 3  │          │
│ <declaration>│          │ Prod 4    │ Prod 5   │         │          │
│ <scenes>     │          │           │          │ Prod 8  │          │
│ <scene>      │          │           │          │ Prod 10 │          │
│ <statements> │          │           │ Prod 11  │         │ Prod 11  │
│ <statement>  │          │           │ Prod 16  │         │ Prod 13  │
└──────────────┴──────────┴───────────┴──────────┴─────────┴──────────┘

┌──────────────┬──────────┬──────────┬──────────┬──────────┬─────────┐
│ Non-terminal │ CHOICE   │ GOTO     │ IF       │ END      │ ELSE    │
├──────────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│ <statements> │ Prod 11  │ Prod 11  │ Prod 11  │ Prod 12  │ Prod 12 │
│ <statement>  │ Prod 14  │ Prod 15  │ Prod 17  │          │         │
│ <if_stmt>    │          │          │ Prod 22  │          │         │
└──────────────┴──────────┴──────────┴──────────┴──────────┴─────────┘
```

---

## 3. PARSE TREES (Use Simple Core Example)

### Example 1: host SAY "Hello!"

```
        <say_stmt>
        /    |    \
       ID   SAY  STRING
       |          |
      host    "Hello!"
```

### Example 2: SET score = 0

```
       <set_stmt>
       /   |   |   \
     SET  ID  =  <expr>
          |       |
        score  <value>
                 |
              NUMBER
                 |
                 0
```

### Example 3: CHOICE "Play" -> game

```
      <choice_stmt>
      /    |    |   \
  CHOICE STR  ->   ID
          |         |
       "Play"     game
```

### Example 4: IF score > 0

```
         <if_stmt>
         /    |     \
        IF <cond> <stmts> ENDIF
             |        |
        <expr> > <expr> |
          |        |    |
         ID      NUM  <stmt>
          |        |    |
        score     0  <goto>
                        |
                     GOTO ID
                           |
                          win
```

### Example 5: SET score = score + 1

```
          <set_stmt>
          /   |   |    \
        SET  ID  =   <expr>
             |      /  |  \
           score <val> + <val>
                   |       |
                  ID      NUM
                   |       |
                 score     1
```

---

## 4. LEFTMOST DERIVATIONS (Use Simple Core Example)

### Derivation 1: host SAY "Hello!"

```
<statement> ⇒ <say_stmt>              [Rule 13]
            ⇒ ID SAY STRING           [Rule 18]
            ⇒ host SAY "Hello!"       [Match tokens]
```

### Derivation 2: SET score = 0

```
<set_stmt> ⇒ SET ID ASSIGN <expr>    [Rule 21]
           ⇒ SET score = <expr>      [Match]
           ⇒ SET score = <value>     [Rule 27]
           ⇒ SET score = NUMBER      [Rule 29]
           ⇒ SET score = 0           [Match]
```

### Derivation 3: IF score > 0 GOTO win ENDIF

```
<if_stmt> ⇒ IF <cond> <stmts> ENDIF          [Rule 22]
          ⇒ IF <expr> > <expr> <stmts> ENDIF [Rule 24]
          ⇒ IF ID > NUM <stmts> ENDIF        [Rules 28,29]
          ⇒ IF score > 0 <stmt> ENDIF        [Match]
          ⇒ IF score > 0 <goto> ENDIF        [Rule 15]
          ⇒ IF score > 0 GOTO ID ENDIF       [Rule 20]
          ⇒ IF score > 0 GOTO win ENDIF      [Match]
```



---

## 5. PER-TEST PARSE ARTIFACTS

### Quiz Story (24 lines) – Program-Level Derivation

```
<program>
⇒ STORY STRING <declarations> <scenes> END STORY
⇒ STORY "Quiz" <decl> <scenes> END STORY
⇒ STORY "Quiz" CHARACTER host "Host" SET score = 0 <scenes> END STORY
⇒ STORY "Quiz" ... SCENE start <statements> SCENE game <statements> SCENE win <statements> END STORY
```

### Scene-Level Parse Tree (Quiz: `SCENE start`)

```
          <scene>
     ┌─────┴──────┐
   SCENE         <statements>           END    SCENE
    start    ┌─────┴────────┐                     
             <statement>  <statements>
              (say)          (choice → goto)
```

### Test Case Mapping (examples folder)

- `test1_simple.story`: Uses `<say_stmt>`, `<choice_stmt>`, `<goto_stmt>` only → parsed by Productions 10, 13, 14, 15.
- `test2_adventure.story`: Adds `<set_stmt>` and `<if_stmt>` → Productions 16, 22/23 exercised; same LL(1) table applies.
- `test3_mystery.story`: Uses all constructs including nested choices → Productions 8–37 all reachable; no new grammar rules needed.

### Additional LL(1) Table Slice (control terminals)

```
┌──────────────┬─────────┬──────────┬──────────┬──────────┐
│ Non-terminal │ STRING  │ SAY      │ ARROW    │ ENDIF    │
├──────────────┼─────────┼──────────┼──────────┼──────────┤
│ <say_stmt>   │         │          │          │          │
│ <choice_stmt>│ Prod19  │          │ Prod19   │          │
│ <condition>  │ Prod25  │          │          │          │
│ <statements> │         │          │          │ Prod12   │
└──────────────┴─────────┴──────────┴──────────┴──────────┘
```

---

END OF PART 2: SYNTAX ANALYSIS
