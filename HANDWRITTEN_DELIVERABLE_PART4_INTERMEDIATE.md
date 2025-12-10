# PART 4: INTERMEDIATE CODE & OPTIMIZATION
## Handwritten Deliverable Guide - StoryScript Compiler

---

## 1. THREE-ADDRESS CODE (TAC)

### TAC Instruction Format

```
┌─────────────────────────────────────────────────────────────┐
│ THREE-ADDRESS CODE GENERAL FORM:                            │
│                                                              │
│   result = operand1 operator operand2                       │
│                                                              │
│ At most ONE operator per instruction                        │
│ At most THREE addresses (result, op1, op2)                  │
└─────────────────────────────────────────────────────────────┘
```

### TAC Instruction Types for StoryScript

```
┌────────────────────┬─────────────────────────────────────────┐
│ INSTRUCTION TYPE   │ FORMAT                                  │
├────────────────────┼─────────────────────────────────────────┤
│ Assignment         │ x = y                                   │
│ Arithmetic         │ x = y + z                               │
│ Arithmetic         │ x = y - z                               │
│ Comparison         │ x = y > z                               │
│ Comparison         │ x = y < z                               │
│ Comparison         │ x = y == z                              │
│ Conditional Jump   │ if condition goto L                     │
│ Conditional Jump   │ ifFalse condition goto L                │
│ Unconditional Jump │ goto L                                  │
│ Label              │ L:                                      │
│ Function Call      │ param x                                 │
│                    │ call f, n                               │
│ Copy               │ x = y                                   │
└────────────────────┴─────────────────────────────────────────┘
```

---

## 2. QUADRUPLES (Use Simple Core Example)

### Format: (operator, arg1, arg2, result)

### Example 1: SET score = 0

```
┌────┬──────────┬──────────┬──────────┬──────────┐
│ #  │ OPERATOR │   ARG1   │   ARG2   │  RESULT  │
├────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ COPY     │ 0        │ -        │ score    │
└────┴──────────┴──────────┴──────────┴──────────┘
```

### Example 2: SET score = score + 1

```
┌────┬──────────┬──────────┬──────────┬──────────┐
│ #  │ OPERATOR │   ARG1   │   ARG2   │  RESULT  │
├────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ +        │ score    │ 1        │ t1       │
│ 1  │ COPY     │ t1       │ -        │ score    │
└────┴──────────┴──────────┴──────────┴──────────┘
```

### Example 3: IF score > 0 GOTO win

```
┌────┬──────────┬──────────┬──────────┬──────────┐
│ #  │ OPERATOR │   ARG1   │   ARG2   │  RESULT  │
├────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ >        │ score    │ 0        │ t1       │
│ 1  │ IF_FALSE │ t1       │ -        │ L1       │
│ 2  │ GOTO     │ win      │ -        │ -        │
│ 3  │ LABEL    │ L1       │ -        │ -        │
└────┴──────────┴──────────┴──────────┴──────────┘
```

---

## 3. TRIPLES (Use Simple Core Example)

### Format: (operator, arg1, arg2) - Result implicit by position

### Example 1: SET score = score + 1

```
┌────┬──────────┬──────────┬──────────┐
│ #  │ OPERATOR │   ARG1   │   ARG2   │
├────┼──────────┼──────────┼──────────┤
│ 0  │ +        │ score    │ 1        │
│ 1  │ =        │ score    │ (0)      │
└────┴──────────┴──────────┴──────────┘

Note: (0) refers to result of instruction 0
```

### Example 2: IF score > 0

```
┌────┬──────────┬──────────┬──────────┐
│ #  │ OPERATOR │   ARG1   │   ARG2   │
├────┼──────────┼──────────┼──────────┤
│ 0  │ >        │ score    │ 0        │
│ 1  │ IF_FALSE │ (0)      │ L1       │
│ 2  │ GOTO     │ win      │ -        │
│ 3  │ LABEL    │ L1       │ -        │
└────┴──────────┴──────────┴──────────┘
```

---

## 4. POSTFIX NOTATION (RPN)

### Conversion Table

```
┌────────────────────────┬──────────────────────────────┐
│ INFIX EXPRESSION       │ POSTFIX (RPN)                │
├────────────────────────┼──────────────────────────────┤
│ score + 1              │ score 1 +                    │
│ a + b * c              │ a b c * +                    │
│ (a + b) * c            │ a b + c *                    │
│ score > 0              │ score 0 >                    │
│ (a + b) > (c - d)      │ a b + c d - >                │
└────────────────────────┴──────────────────────────────┘
```

### Evaluation Example: score + 1

```
Postfix:  score 1 +

Stack:
Step 1: Push score     → [score]
Step 2: Push 1         → [score, 1]
Step 3: Apply +        → [score+1]
Result: score+1
```

Conversion Steps (using stack):
Symbol │ Stack      │ Output
───────┼────────────┼─────────
a      │ []         │ a
+      │ [+]        │ a
b      │ [+]        │ a b
*      │ [+, *]     │ a b
c      │ [+, *]     │ a b c
-      │ [-]        │ a b c * + d
d      │ [-]        │ a b c * + d
END    │ []         │ a b c * + d -

Operator Precedence: * > + = -
```

### Postfix for StoryScript Expressions

```
Expression 1: suspects + 1
Postfix: suspects 1 +

Expression 2: pizza_found > 0
Postfix: pizza_found 0 >

Expression 3: health - damage + bonus
Postfix: health damage - bonus +

Expression 4: (score > 50) == TRUE
Postfix: score 50 > TRUE ==
```

---

## 5. DAG DIAGRAMS (Use Simple Core Example)

### Example 1: score + 1

```
       (+)
      /   \
   score    1

Nodes: 3 (operator + 2 operands)
```

### Example 2: SET score = score + 1

```
        (=)
       /   \
    score  (+)
          /   \
      score    1

Note: 'score' appears twice - same DAG node
```

### Example 3: score > 0

```
       (>)
      /   \
   score    0
```

---

## 6. OPTIMIZATION TECHNIQUES (3-4 Required)

### Technique 1: CONSTANT FOLDING

```
Before: SET x = 5 + 10
After:  SET x = 15

TAC Before:          TAC After:
  t1 = 5 + 10          x = 15
  x = t1

Savings: 1 instruction eliminated
```

### Technique 2: COMMON SUBEXPRESSION ELIMINATION (CSE)

```
Before:
  SET a = score + 1
  SET b = score + 1

After:
  SET t = score + 1
  SET a = t
  SET b = t

Savings: 1 addition eliminated
```

### Technique 3: DEAD CODE ELIMINATION

```
Before:
  SET temp = 100    ← Never used
  SET health = 50

After:
  SET health = 50

Savings: 1 assignment eliminated
```

### Technique 4: CONSTANT PROPAGATION

```
Before:
  SET x = 5
  SET y = x + 10

After:
  SET x = 5
  SET y = 15      ← 5 + 10 computed

Combined with folding
```

---

## 7. FULL TAC LISTING (Quiz Story)

```
LABEL start
  SAY host, "Hello!"
  CHOICE "Play", game
  GOTO game            ; single outgoing choice

LABEL game
  SAY host, "Answer?"
  t1 = score + 1
  score = t1
  t2 = score > 0
  IF_FALSE t2 GOTO L_else
  GOTO win
L_else:
  GOTO start

LABEL win
  SAY host, "You win!"
```

---

## 8. OPTIMIZATION COVERAGE PER TEST CASE

```
┌───────────────────────┬──────────┬──────────┬──────────┐
│ Test Case             │ CFold    │ CSE      │ DCE      │
├───────────────────────┼──────────┼──────────┼──────────┤
│ Quiz (24 lines)       │ score>0  │ score+1  │ none     │
│ test1_simple.story    │ choices  │ narrator │ unused t │
│ test2_adventure.story │ torch>0  │ path tag │ temp msg │
│ test3_mystery.story   │ trust-1  │ clue add │ dead goto│
└───────────────────────┴──────────┴──────────┴──────────┘

Key: CFold=constant folding; CSE=common subexpression elimination; DCE=dead code elimination.
```
