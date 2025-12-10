# HANDWRITTEN DELIVERABLE - INDEX
## StoryScript Compiler (CS4031)

**Scope anchor**: All parts use the 24-line Quiz story from `SIMPLE_CORE_EXAMPLE.md` as the running example. Goals are to keep handwriting minimal while meeting the professor's checklist.

## Part 1 - Lexical Analysis (`HANDWRITTEN_DELIVERABLE_PART1_LEXICAL.md`)
- Token definitions for Quiz story: keywords, identifiers, numbers, strings, punctuation, operators.
- Regex patterns + short DFA sketches for identifier, number, string, and arrow (`->`).
- One token stream for the Quiz story; brief error notes (bad char, unterminated string).

## Part 2 - Syntax Analysis (`HANDWRITTEN_DELIVERABLE_PART2_SYNTAX.md`)
- Compact CFG tailored to the Quiz story (program, scene, statement, expr, condition).
- FIRST/FOLLOW highlights for non-terminals that appear in the Quiz story.
- One LL-style parse table slice for the key productions.
- One parse tree + leftmost derivation for a Quiz scene (with SAY and CHOICE).

## Part 3 - Semantic Analysis (`HANDWRITTEN_DELIVERABLE_PART3_SEMANTIC.md`)
- SDD/SDT snippets for scene definitions, SAY, CHOICE, and simple expressions.
- L-attributed walk for the Quiz story (symbol table entries for characters/scenes; type notes for strings/ints).
- One annotated parse tree fragment showing attribute flow.
- Minimal semantic errors covered: undefined scene, duplicate scene, type mismatch in SET.

## Part 4 - Intermediate Code (`HANDWRITTEN_DELIVERABLE_PART4_INTERMEDIATE.md`)
- TAC conventions used for the Quiz story (quadruple format, labels, temporaries).
- Full TAC listing for the Quiz story (labels for scenes, SAY/CHOICE/GOTO, simple SET/copy).
- One tiny DAG/RPN illustration for an expression; note on constant folding (if any).

## Part 5 - Target Code (`HANDWRITTEN_DELIVERABLE_PART5_TARGET.md`)
- Target language: Python.
- Full Python translation of the Quiz TAC (data + code + main loop) only.
- TAC->Python mapping table for the small instruction set used.

END OF INDEX
