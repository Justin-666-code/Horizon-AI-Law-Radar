# Validation

## Automated

```powershell
python scripts/apply_radar_preferences.py `
  --input data/config.github.json `
  --preferences data/radar-preferences.json `
  --output data/config.json

python -m pytest tests/test_radar_preferences.py tests/test_personal_radar.py -q
```

Expected:

- Generated configuration reports `policy primary_only`.
- Tests pass.
- Digest order is
  `ai-foundations, ai-research, tech-blog, tech-news, law-governance`.
- Engineering limit is `3`; total daily limit remains `10`.

## Manual Review

- Read `tech-blog/match.md` and confirm it describes deliverables and product
  judgment rather than generic engineering prestige.
- Read `law-governance/enrichment.md` and confirm AI safety, intellectual
  property, and digital government are classified independently.
- Confirm no prompt teaches the user to train a frontier model or adds law
  admissions, civil-service exams, or generic legal news.

## Definition of Done

The generated configuration and all focused tests pass, and the profile prompts
make the route-aware behavior explicit without changing the source policy or the
delivery pipeline.
