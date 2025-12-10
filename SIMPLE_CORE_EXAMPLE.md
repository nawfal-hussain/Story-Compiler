# SIMPLE CORE EXAMPLE FOR HANDWRITTEN DELIVERABLE
## Minimal Test Case Covering All Language Features

This single compact example will be used throughout all phases to minimize handwriting.

---

## CORE TEST CASE

```storyscript
STORY "Quiz"

CHARACTER host "Host"
SET score = 0

SCENE start
    host SAY "Hello!"
    CHOICE "Play" -> game
END SCENE

SCENE game
    host SAY "Answer?"
    SET score = score + 1
    IF score > 0
        GOTO win
    ELSE
        GOTO start
    ENDIF
END SCENE

SCENE win
    host SAY "You win!"
END SCENE

END STORY
```

**Why this example?**
- Only 3 scenes (vs 8 in test cases)
- 1 character (vs 3-4)
- 1 variable (vs 0-2)
- Covers: STORY, CHARACTER, SET, SCENE, SAY, CHOICE, GOTO, IF-ELSE, arithmetic, comparison
- Total: 24 lines (vs 70+ in test cases)

---

## ADDITIONAL MICRO EXAMPLES (For specific concepts)

### Example 2: Simple Expression
```
SET x = 5
```

### Example 3: Arithmetic
```
SET y = x + 3
```

### Example 4: Conditional
```
IF x > 2
    GOTO next
ENDIF
```

### Example 5: Choice
```
CHOICE "Yes" -> scene1
```

### Example 6: SAY Statement
```
hero SAY "Test"
```

---

These 6 micro examples cover all required concepts while being easy to handwrite multiple times.
