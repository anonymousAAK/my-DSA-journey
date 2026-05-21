## Summary
<one-paragraph description of the change>

## Type
- [ ] Bug fix (correctness, broken file, smart quotes)
- [ ] New topic file
- [ ] Documentation improvement
- [ ] Test coverage extension
- [ ] Infrastructure (CI, scripts, harness)
- [ ] Other (describe)

## Checklist
- [ ] `./scripts/build_all.sh all` passes locally
- [ ] `python tests/harness/harness.py --all` passes locally
- [ ] `python scripts/quality_check.py --quiet` exits 0
- [ ] If adding a topic file: cross-language counterparts present in python/, cpp/, rust/, web/
- [ ] If adding a topic file: fixture in `tests/cases/` and ref in `tests/refs/`
- [ ] If touching a per-week README: existing Tradeoff Matrix / Anti-patterns / Reflection Prompts sections preserved

## Test plan
<how a reviewer can verify your change works>
