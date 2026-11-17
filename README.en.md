# K-Digital Asset Policy Intelligence (K-DAPI)

K-DAPI is an Agent Skill that routes natural-language digital-asset questions to specialised, evidence-led research frameworks. It supports law and policy, coins and projects, blockchain networks, whitepapers, stablecoins, tokenised assets, exchange support policies and business models. Korean context is added only when materially relevant.

Its core workflow is:

> natural-language question → question type and depth → official sources → facts, claims and inferences → Korean context when relevant

## Capabilities

- Start from a natural-language question without requiring a PDF or API key
- Deterministically route 12 question types and request missing identifiers
- Select `QUICK`, `STANDARD`, or `DEEP_RESEARCH` response depth
- Use separate frameworks for regulation, projects, networks, whitepapers, stablecoins, RWA, exchanges and business models
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

## Example prompts

```text
What is the CLARITY Act? Check its current legislative status.
```

```text
Evaluate Ethereum as a network, including consensus, decentralisation, actual use and operational risks.
```

```text
How does USDC maintain its price, and what are its reserve, redemption and depegging risks?
```

```text
Use $k-digital-asset-policy-intelligence to analyse this tokenised bond,
compare it with Korea's token securities framework as of 2026-11-16,
and produce a Korean report plus an English executive summary.
```

## Validate

```bash
python3 -m pip install -r requirements.txt
python3 scripts/route_question.py "What is tokenised securities?"
python3 scripts/verify_evidence.py examples/hong-kong-digital-green-bond/evidence.json --output /tmp/kdapi-verification.json
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json
python3 scripts/validate_report.py examples/tokenization-case-study/report.json
python3 -m unittest discover -s tests -v
```

The included [case study](examples/tokenization-case-study/report-ko.md) compares the EIB's sterling digital bond with Korea's forthcoming token-securities framework. Its evidence metadata and English summary are reproducible companion files.

The independent [Hong Kong digital green bond case](examples/hong-kong-digital-green-bond/report-ko.md) exercises the full research workflow with newly collected HKMA and SFC sources, including PDF content verification.

K-DAPI does not select an unspecified coin or network, force every question into a Korean token-securities analysis, or provide buy/sell and price predictions. See the [general user guide](docs/GENERAL_USER_GUIDE.md) for examples.

## Licence

MIT. Regulatory information is time-sensitive; contributions should preserve the analysis date, official source URL, legal status and Evidence ID.

