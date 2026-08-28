# CIRCA: Clinical Intent Representation, Cross-corpus Annotations

Companion site for the paper **"Clinical Intent Extraction: A FHIR-Aligned Representation and the CIRCA Benchmark"** by Alexander Apartsin (Holon Institute of Technology) and Yehudit Aperstein (Afeka College of Engineering).

## Read the paper

- **HTML** — [circa.html](circa.html) *(source of truth; renders in any browser)*
- **PDF (single-column)** — [circa_1col.pdf](circa_1col.pdf)
- **Word (single-column)** — [circa_1col.docx](circa_1col.docx)

## What CIRCA is

- The **Clinical Intent Extraction (CIE)** task: given a clinical note, extract every prospective clinical action (follow-up, order, referral, instruction) as a structured record.
- The **Clinical Intent Representation (CIR)**: a FHIR-aligned schema that decomposes each action into an action verb, type, coded target, timing, condition, plus two axes prior clinical-note datasets do not jointly represent — **request-intent** (proposal / plan / order / option, aligned to HL7 FHIR RequestIntent) and **modality** (a seven-valued clinical-strength taxonomy).
- The **CIRCA dataset**: 10,011 harmonized intents over 1,185 notes and 942 MIMIC-III patients plus the public ACI-Bench dialogue corpus, harmonized from five heterogeneous source corpora (CLIP, MedDec, ap_parsing, PaniniQA, SIMORD / ACI-Bench).

## Dataset deposit

- **Zenodo:** [10.5281/zenodo.22058593](https://doi.org/10.5281/zenodo.22058593)
- **Package** (annotations + KART mappings + code, no source note text): [circa-cir-v1.zip](circa-cir-v1.zip)

The MIMIC-derived layers ship as stand-off annotations (character offsets + SHA-256) that a credentialed user rehydrates from their own MIMIC-III copy with the included `rebuild.py`; only the public ACI-Bench layer is distributed with its note text. See the deposit's `README.md` and `DATASHEET.md` for the reconstruction procedure and the data-provenance / compliance statement.

## Citation

```
Apartsin A, Aperstein Y. Clinical Intent Extraction: A FHIR-Aligned Representation
and the CIRCA Benchmark. 2026.
Dataset: https://doi.org/10.5281/zenodo.22058593
```

## Compliance

CIRCA never redistributes MIMIC-III text. Model inference during annotation ran on AWS Bedrock under a HIPAA Business Associate Agreement with a zero-retention configuration; the source-corpus data-use agreements govern any reconstructed text.
