# K-Digital Asset Policy Intelligence (K-DAPI)

K-DAPI is an Agent Skill for analysing overseas digital-asset and tokenisation business models, comparing them with Korean law and policy, and identifying conditions, opportunities and constraints for Korean financial institutions and fintech firms.

Its core workflow is:

> overseas business model → foreign regulation → Korean regulation → gap analysis → adoption conditions → business implications

## Capabilities

- Analyse English PDFs, official URLs, or a research question
- Separate enacted law, effective law, draft rules, policy announcements and guidance
- Link major claims to Evidence IDs and confidence classifications
- Produce a Korean research report and an English executive summary
- Validate structured evidence and reports without mandatory third-party Python packages
- Fetch HTML, text and PDF sources, compare excerpts, and record document hashes (`pypdf` is required for PDF extraction)
- Validate normalised legal claim types against source status, jurisdiction and the report analysis date

This skill does not provide legal or investment advice.

## Install

After the repository is public:

```bash
npx skills add junjunny/k-digital-asset-policy-intelligence@k-digital-asset-policy-intelligence
```

Alternatively, clone the repository and copy the folder containing `SKILL.md` into a supported agent's skills directory.

## Example prompt

```text
Use $k-digital-asset-policy-intelligence to analyse this tokenised bond,
compare it with Korea's token securities framework as of 2026-11-16,
and produce a Korean report plus an English executive summary.
```

## Validate

```bash
python3 -m pip install -r requirements.txt
python3 scripts/verify_evidence.py examples/hong-kong-digital-green-bond/evidence.json --output /tmp/kdapi-verification.json
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json
python3 scripts/validate_report.py examples/tokenization-case-study/report.json
python3 -m unittest discover -s tests -v
```

The included [case study](examples/tokenization-case-study/report-ko.md) compares the EIB's sterling digital bond with Korea's forthcoming token-securities framework. Its evidence metadata and English summary are reproducible companion files.

The independent [Hong Kong digital green bond case](examples/hong-kong-digital-green-bond/report-ko.md) exercises the full research workflow with newly collected HKMA and SFC sources, including PDF content verification.

## Licence

MIT. Regulatory information is time-sensitive; contributions should preserve the analysis date, official source URL, legal status and Evidence ID.

