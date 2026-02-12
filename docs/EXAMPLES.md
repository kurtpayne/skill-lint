# Examples

## Example 1: Security finding

Input:
- `Ignore previous instructions`

Output finding category:
- `injection`

## Example 2: Malware-like pattern

Input:
- `curl ... | bash`

Output finding severity:
- `critical`

## Example 3: Quality gate failure

When readability and completeness are below policy thresholds, `skilllint scan` exits with code `2`.

## Example 4: Safe auto-fix

Input heading:
- `#Heading`

Auto-fix result:
- `# Heading`
