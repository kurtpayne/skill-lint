# Examples

## Example 1: Readability feedback

Input:
- Long, dense paragraphs with overloaded sentences.

Output:
- Lower `readability` score and quality gate warning under strict policy.

## Example 2: Complexity warning

Input:
- Excessive nested conditions and branching instructions.

Output:
- Lower `complexity` score.

## Example 3: Completeness failure

Input:
- Missing key sections such as Overview, Inputs, Outputs, Examples.

Output:
- Lower `completeness` score and possible policy failure.

## Example 4: Safe auto-fix

Input heading:
- `#Heading`

Auto-fix result:
- `# Heading`

## Example 5: Strict quality policy in CI

```bash
skilllint scan . --policy src/skilllint/policies/strict.yaml --format text
```

If quality thresholds are missed, command exits `2`.
