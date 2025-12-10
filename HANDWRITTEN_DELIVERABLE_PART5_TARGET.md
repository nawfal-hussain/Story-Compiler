# PART 5: TARGET CODE GENERATION
## Handwritten Deliverable Guide - StoryScript Compiler

---


## 1. TAC → PYTHON MAPPING (Instruction Subset)

```
TAC                   Python
------------------------------------------------
LABEL L               def L(): ... ; return next
SAY c, "txt"          print(f"{c}: txt")
CHOICE "t", tgt       choices.append(("t", tgt))
GOTO tgt              return tgt
IF_FALSE t goto L     if not t: return L
x = y + z             x = y + z
```

---

## 2. TARGET CODE — QUIZ STORY (24 lines)

```python
characters = {"host": "Host"}
state = {"score": 0}
choices = []

def scene_start():
   print(f"{characters['host']}: Hello!")
   choices.clear(); choices.append(("Play", "game"))
   return choices[0][1]

def scene_game():
   print(f"{characters['host']}: Answer?")
   state['score'] = state['score'] + 1
   if state['score'] > 0:
      return "win"
   else:
      return "start"

def scene_win():
   print(f"{characters['host']}: You win!")
   return None

scene_table = {
   "start": scene_start,
   "game": scene_game,
   "win": scene_win,
}

current = "start"
while current:
   current = scene_table[current]()
```

---


### Memory Layout

```
┌─────────────────────────────────────────────────────┐
│                   MEMORY LAYOUT                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  CHARACTER TABLE                     │          │
│  │  {player: "Bernardo Silva", ...}     │          │
│  └──────────────────────────────────────┘          │
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  VARIABLE TABLE                      │          │
│  │  {health: 100, score: 50, ...}       │          │
│  └──────────────────────────────────────┘          │
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  SCENE TABLE                         │          │
│  │  {start: func_ptr, ...}              │          │
│  └──────────────────────────────────────┘          │
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  CALL STACK                          │          │
│  │  [scene_start, scene_press, ...]     │          │
│  └──────────────────────────────────────┘          │
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  CHOICE BUFFER                       │          │
│  │  [("Press", scene_press), ...]       │          │
│  └──────────────────────────────────────┘          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 11. EXECUTION TRACE EXAMPLE

### Execution Flow for test1_simple.story

```
EXECUTION TRACE:
═══════════════════════════════════════════════════════

1. INITIALIZATION PHASE
   ├─ Load characters table
   │  ├─ player = "Bernardo Silva"
   │  ├─ ronaldo = "Cristiano Ronaldo"
   │  └─ narrator = "Narrator"
   │
   ├─ Load variables table
   │  └─ (none)
   │
   └─ Set entry point: scene_start

2. EXECUTION PHASE
   ├─ Execute scene_start()
   │  ├─ Print: narrator: "World Cup Final..."
   │  ├─ Print: narrator: "85th minute..."
   │  ├─ Print: player: "The defender..."
   │  ├─ Add choice: "Press" -> scene_press
   │  ├─ Add choice: "Mark" -> scene_mark
   │  ├─ Display choices
   │  ├─ Wait for input: 1
   │  └─ Return: scene_press
   │
   ├─ Execute scene_press()
   │  ├─ Print: player: "I'm closing..."
   │  ├─ Print: narrator: "The pressure..."
   │  ├─ Add choice: "Pass" -> scene_pass_ronaldo
   │  ├─ Add choice: "Shoot" -> scene_shoot_glory
   │  ├─ Wait for input: 1
   │  └─ Return: scene_pass_ronaldo
   │
   ├─ Execute scene_pass_ronaldo()
   │  ├─ Print: player: "Cristiano!"
   │  ├─ Print: narrator: "Perfect pass..."
   │  ├─ Print: narrator: "GOOOOAL!"
   │  └─ Return: scene_celebration
   │
   └─ Execute scene_celebration()
      ├─ Print: narrator: "Portugal wins..."
      ├─ Print: ronaldo: "We did it..."
      ├─ Print: player: "This is what..."
      ├─ Print: narrator: "History is made!"
      └─ Return: None (END)

3. TERMINATION PHASE
   └─ Print: "=== THE END ==="

TOTAL SCENES EXECUTED: 4
CHOICES MADE: 2
EXECUTION TIME: ~30 seconds (user input dependent)
```

---

## 12. PERFORMANCE METRICS

### Code Generation Statistics

```
┌──────────────────────────┬─────────┬─────────┬─────────┐
│ TEST CASE                │   TC1   │   TC2   │   TC3   │
├──────────────────────────┼─────────┼─────────┼─────────┤
│ Source Lines             │   71    │   70    │   73    │
│ Target Lines (Python)    │  125    │  140    │  158    │
│ Expansion Factor         │  1.76x  │  2.0x   │  2.16x  │
│ Number of Functions      │    8    │    7    │    7    │
│ Number of Characters     │    3    │    2    │    4    │
│ Number of Variables      │    0    │    1    │    2    │
│ Number of Scenes         │    8    │    7    │    7    │
│ Average Scene Size       │  15.6   │  20.0   │  22.5   │
│ Generated Instructions   │  ~100   │  ~110   │  ~125   │
└──────────────────────────┴─────────┴─────────┴─────────┘
```

---

## NOTES FOR HANDWRITTEN SUBMISSION:

1. **Show complete target code** - At least 2 full test cases
2. **Include all sections** - Data, code, main execution
END OF PART 5: TARGET CODE GENERATION
