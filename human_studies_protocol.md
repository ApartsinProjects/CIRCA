# CIRCA: minimal human studies required for acceptance

Two human-annotation studies are the remaining evidence blockers flagged by both the
Fable and GPTConsult reviews. They are sized to be *sufficient for acceptance* while
keeping rater burden low. All tooling is built; each study is one Excel workbook to be
filled by a trained annotator (CS student), then scored by a script.

Compliance: the MIMIC-derived workbooks contain surrogate-filled note text and must stay
local (they are gitignored via `*.xlsx`). Only aggregate results (kappa, precision/recall,
prevalence) go into the paper. The ACI-Bench sheets are public.

Annotators: computer-science students trained on the CIR annotation guidelines (not
clinicians). This is stated factually in §6/§8.1.

---

## Study A. Exhaustive, blinded, whole-note gold

**Question it answers.** What fraction of prospective intents do the source anchors plus
the three models miss (the completeness ceiling), and what is the models' true whole-note
precision / recall / F1 and the true prevalence of the sparse fields? The current
benchmark uses sampled, anchor-derived gold, so it cannot measure these.

**Design.** A trained annotator (a CS student) reads each whole note and lists every prospective intent
**from scratch, blind to the source anchors and the model outputs.**

**Sample (minimal): 24 notes**, stratified across both note distributions:
4 each from CLIP, MedDec, ap_parsing, PaniniQA (16 MIMIC) + 8 ACI-Bench (public).
This spans the discharge, assessment-and-plan, instruction, and dialogue settings and is
enough for a first completeness-ceiling and precision/recall estimate.

**Materials.** `human_studies/study_A_wholenote_gold.xlsx` — one worksheet per note: the
full note text (read-only) followed by a blank intent table with drop-downs
(span, action, type, target, request-intent, modality, time, condition, prospective).
Build: `python tools/build_study_A_wholenote.py --per-mimic 4 --aci 8`.

**Scoring.** `python tools/score_study_A.py` yields:
- **candidate completeness ceiling** = fraction of exhaustive human intents present in the
  released candidate pool (released gold + cached model extractions); the complement is the
  intents both anchors and models miss;
- **whole-note precision / recall / F1** per model on the exhaustive gold (for notes with
  cached model output, i.e. the test-split notes);
- **true sparse-field prevalence** (time, condition), which calibrates the Figure 1
  fill-rate caveat.

**Where it lands in the paper.** A short subsection (or additions to §8.2) reporting true
precision/recall/F1 on the exhaustive subset and the completeness ceiling; it removes the
"precision is only a lower bound" and "completeness ceiling is unmeasured" limitations.

---

## Study B. Second-rater inter-annotator reliability (Cohen's kappa)

**Question it answers.** Is the schema, and especially the two novel axes, reproducibly
annotatable? The current gold uses a single rater who saw a pre-filled label, so no
inter-rater reliability exists.

**Design.** A **second** trained annotator (CS student) independently labels a stratified sample with
**no pre-filled label** (blind to the first rater and to the models). Fields: prospective
(Y/N inclusion), action, type, request-intent, modality.

**Sample (minimal): 220 intents**, oversampling the rare axis values so kappa is
estimable on them. As generated: request-intent proposal 6 / option 10 / plan 65 /
order 139; modality conditional 48 / optional 51 / prohibited 14 / considered 6 /
recommended 14 / planned 24 / ordered 63.

**Materials.** `human_studies/study_B_second_rater.xlsx` — one row per intent: the span in
`[[ ]]` with +/-160 characters of context and blank drop-downs; the first-rater gold is in
a hidden column for scoring only. Build: `python tools/build_study_B_secondrater.py --n 220`.

**Scoring.** `python tools/score_study_B.py` yields per-field raw agreement and Cohen's
kappa (action, type, request-intent, modality), a linearly-weighted kappa for the ordered
modality scale, the prospective-inclusion agreement, and the top confusions.

**Where it lands in the paper.** §8.1 gains an inter-rater reliability paragraph and a
small kappa table; it removes the "single annotator, no reliability" limitation.

---

## Effort and sequence

- Study B is the lighter lift (220 short span judgments) and closes the reliability gap
  most reviewers weight heavily; run it first.
- Study A is 24 full-note reads; heavier but it is what converts "precision is a lower
  bound" into a real precision/recall/F1 plus the completeness ceiling.
- Both are independent of any further model compute; only a rater's time is needed.
- After each workbook is filled, run its scorer; results are written to
  `var/gold/study_B_kappa.json` and `var/gold/study_A_wholenote.json` for insertion.
