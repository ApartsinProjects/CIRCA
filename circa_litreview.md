A strong Related Work arc is to move from what prior datasets extract, to what semantic distinctions they miss, then to how CIRCA harmonizes, constructs, and evaluates the resulting resource. I would organize the section into five larger blocks while preserving the nine themes below:

A. Extracting prospective clinical actions (1–2) → B. Representing epistemic and directive force (3–4) → C. Standards and harmonization (5) → D. Dataset construction and benchmarking (6–8) → E. Privacy-preserving preprocessing (9).

One important positioning point: do not describe all prior work as “intent extraction.” Much of it extracts recommendations, orders, medications, temporal events, or assertions. CIRCA's novelty is partly that it makes prospective clinical intent itself the organizing unit and separates what action is mentioned from how strongly/authoritatively it is being requested.

1. Clinical action, order, and follow-up-recommendation extraction

Why it matters to CIRCA: This is the closest task lineage: prior resources typically identify one restricted class of prospective action—medication decisions, follow-up recommendations, orders, or instructions—whereas CIRCA tries to unify these as instances of a common prospective-intent schema.

Works to cite

CLIP original corpus/publication. [verify exact authors, title, venue, year, identifier]
I would cite the exact release paper or repository associated with the particular CLIP version that CIRCA ingests rather than infer bibliographic metadata from the dataset name.

vs CIRCA: CLIP contributes one action-oriented annotation regime; CIRCA re-expresses its labels in a corpus-independent representation and evaluates whether that representation transfers beyond the source task.

MedDec original corpus/publication. [verify exact authors, title, venue, year, identifier]

vs CIRCA: MedDec focuses on a particular class of clinical decisions; CIRCA treats medication decisions as only one realization of a broader prospective-intent construct and adds normalized target/time/condition plus authority and modality.

ap_parsing original publication/repository. [verify exact authors, title, venue, year, identifier]

PaniniQA original publication/repository. [verify exact authors, title, venue, year, identifier]

SIMORD original publication/repository. [verify exact authors, title, venue, year, identifier]
If SIMORD is your derived annotation layer over ACI-Bench rather than an independently published corpus, say that explicitly and cite ACI-Bench instead of presenting SIMORD as an external dataset.

Yim et al. ACI-BENCH: a Novel Ambient Clinical Intelligence Dataset for Benchmarking Automatic Visit Note Generation. Scientific Data, 2023. arXiv identifier [verify].

vs CIRCA: ACI-Bench supplies dialogue-derived clinical material and generated/reference notes rather than an intent ontology; CIRCA uses this substantially different discourse distribution to test whether intent extraction transfers beyond conventional EHR notes.

Additional follow-up/recommendation literature worth citing

There is a substantial radiology literature on automatically identifying follow-up recommendations. One particularly relevant paper is:

Large-Scale Evaluation of Machine Learning Models in Identifying Follow-Up Recommendations in Radiology Reports. [authors/venue/year/identifier verify].

I would verify and include this because it provides perhaps the cleanest contrast: recommendation detection is a narrow prospective-action task; CIE requires exhaustive extraction plus structured semantics across action types and note genres.

2. Prospective versus retrospective information; follow-up and care-plan NLP

Why it matters to CIRCA: Clinical NLP has sophisticated temporal-event machinery, but “future” is not equivalent to “intended”: the patient will return, should return, we may repeat CT, and CT was scheduled have different prospective semantics despite all referring forward in time.

Works to cite

Styler IV, Bethard S, Finan S, et al. Temporal Annotation in the Clinical Domain. Transactions of the Association for Computational Linguistics, 2014. ACL Anthology: Q14-1012 [verify identifier].

vs CIRCA: THYME-style temporal annotation determines temporal properties and relations of clinical events; CIRCA asks the orthogonal question of whether a mention encodes a prospective clinical commitment/recommendation and with what authority and strength.

Sun W, Rumshisky A, Uzuner O. Evaluating Temporal Relations in Clinical Text: 2012 i2b2 Challenge. Journal of the American Medical Informatics Association, 2013. DOI: 10.1136/amiajnl-2013-001628 [verify].

vs CIRCA: i2b2 temporal relations establish when events occur relative to other events or document time; CIRCA represents what clinicians intend to happen, with time as one attribute rather than the defining label.

Bethard S, Derczynski L, Savova G, Pustejovsky J, Verhagen M. SemEval-2015 Task 6: Clinical TempEval. SemEval, 2015. ACL Anthology [verify exact identifier].

Bethard S, Savova G, Chen W-T, Derczynski L, Pustejovsky J, Verhagen M. SemEval-2016 Task 12: Clinical TempEval. SemEval, 2016. ACL Anthology [verify exact identifier].

Zaki-Metias KM, et al. Follow-up of Imaging Findings / FIND program paper. Journal of Digital Imaging, 2023. [verify exact title, DOI].

Mabotuwana T, et al. Radiology recommendation/follow-up tracking work. [verify exact title, venue, year].

Positioning sentence

I would explicitly write something equivalent to:

Temporal annotation distinguishes past, present, and future events, but prospective intent is not reducible to future temporality: CIRCA additionally models whether an event is proposed, planned, ordered, optional, conditional, or prohibited.

That distinction is conceptually important.

3. Assertion, negation, uncertainty, hedging, factuality, and modality

Why it matters to CIRCA: Existing clinical NLP already recognizes that event extraction without assertion status is inadequate; CIRCA builds on that idea but distinguishes epistemic/assertional status from deontic or clinical-action strength.

Works to cite

Chapman WW, Bridewell W, Hanbury P, Cooper GF, Buchanan BG. A Simple Algorithm for Identifying Negated Findings and Diseases in Discharge Summaries. Journal of Biomedical Informatics, 2001. DOI: 10.1006/jbin.2001.1029.

vs CIRCA: NegEx distinguishes asserted from negated clinical findings; CIRCA's modality axis instead distinguishes degrees and kinds of prospective force, such as recommended, considered, optional, or prohibited.

Harkema H, Dowling JN, Thornblade T, Chapman WW. ConText: An Algorithm for Determining Negation, Experiencer, and Temporal Status from Clinical Reports. Journal of Biomedical Informatics, 2009. DOI: 10.1016/j.jbi.2009.05.002.

vs CIRCA: ConText adds contextual properties to clinical concepts but does not represent the directive force or authority of prospective clinical actions.

Uzuner Ö, South BR, Shen S, DuVall SL. 2010 i2b2/VA Challenge on Concepts, Assertions, and Relations in Clinical Text. Journal of the American Medical Informatics Association, 2011. DOI: 10.1136/amiajnl-2011-000203.

Vincze V, Szarvas G, Farkas R, Móra G, Csirik J. The BioScope Corpus: Biomedical Texts Annotated for Uncertainty, Negation and Their Scopes. BMC Bioinformatics, 2008. DOI: 10.1186/1471-2105-9-S11-S9.

Saurí R, Pustejovsky J. FactBank: A Corpus Annotated with Event Factuality. Language Resources and Evaluation, 2009. DOI: 10.1007/s10579-009-9089-9 [verify].

Peng Y, Wang X, Lu L, Bagheri M, Summers R, Lu Z. NegBio: A High-Performance Tool for Negation and Uncertainty Detection in Radiology Reports. AMIA/JAMIA-related proceedings, 2018 [verify exact venue/identifier].

Important conceptual distinction for the paper

Do not equate CIRCA modality with the standard clinical-NLP term assertion status.

For example:

“No pulmonary embolism” → negated fact

“Do not restart warfarin” → positively asserted prospective intent, with prohibited modality

That example makes the need for the CIRCA axis immediately clear.

4. Speech acts, request authority, orders, and FHIR RequestIntent

Why it matters to CIRCA: CIRCA's request-intent axis concerns the institutional/directive status of an action—proposal versus plan versus order versus option—which is closer to speech-act/deontic semantics and the FHIR Request pattern than to ordinary clinical assertion classification.

Works/standards to cite

HL7 International. FHIR Release 4: RequestIntent ValueSet. HL7 FHIR R4, 2019. Official standard; no DOI.

vs CIRCA: FHIR defines RequestIntent primarily for already-structured request resources; CIRCA adapts this distinction into an annotation/extraction axis for free clinical text.

HL7 International. FHIR Release 4: Request Pattern / ServiceRequest / MedicationRequest. HL7 FHIR R4, 2019. Official standard; no DOI.

vs CIRCA: FHIR specifies how computational requests are represented after structuring; CIRCA addresses the upstream NLP problem of recovering those semantics from narrative text.

Austin JL. How to Do Things with Words. Oxford University Press, 1962. ISBN rather than DOI.

Searle JR. Speech Acts: An Essay in the Philosophy of Language. Cambridge University Press, 1969.

Bunt H, Petukhova V, Traum D, Alexandersson J. Dialogue Act Annotation with ISO 24617-2. [exact title/venue/year verify].

ISO 24617-2. Language Resource Management—Semantic Annotation Framework—Part 2: Dialogue Acts. ISO standard, original 2012; revised versions [verify].

This is one of CIRCA's strongest novelty gaps

I do not know a strong, widely used clinical-NLP corpus that explicitly annotates something equivalent to the FHIR RequestIntent distinction across heterogeneous clinical prose.

That absence is worth stating carefully:

Prior clinical NLP commonly annotates assertion, uncertainty, temporality, or individual order types, whereas standardized request authority is primarily represented downstream in structured interoperability standards such as FHIR.

Avoid saying “no prior work” unless you have searched systematically.

5. Mapping clinical NLP to FHIR/OMOP and cross-schema harmonization

Why it matters to CIRCA: CIRCA is not merely merging label names; it attempts to construct a common semantic representation that can be projected into an operational healthcare standard.

Works to cite

Hong N, et al. NLP2FHIR: A Framework/Pipeline for Transforming Clinical Text into FHIR Resources. [exact title, venue, year, identifier verify].

vs CIRCA: NLP2FHIR's central goal is converting NLP-derived clinical information into FHIR-compatible resources; CIRCA concentrates on a specific semantic object—prospective clinical intent—and introduces an annotation schema and multi-corpus benchmark around it.

This is an important citation, but I would verify the exact NLP2FHIR paper metadata before submission.

Bender D, Sartipi K. HL7 FHIR: An Agile and RESTful Approach to Healthcare Information Exchange. IEEE CBMS, 2013. DOI: 10.1109/CBMS.2013.6627810 [verify].

vs CIRCA: This motivates FHIR as the interoperability target but does not address extraction from narrative clinical language.

Mandel JC, Kreda DA, Mandl KD, Kohane IS, Ramoni RB. SMART on FHIR: A Standards-Based, Interoperable Apps Platform for Electronic Health Records. Journal of the American Medical Informatics Association, 2016. DOI: 10.1093/jamia/ocv189.

Voss EA, Makadia R, Matcho A, et al. Feasibility and Utility of Applications of the Common Data Model to Multiple, Disparate Observational Health Databases. Journal of the American Medical Informatics Association, 2015. DOI: 10.1093/jamia/ocu023 [verify].

Hripcsak G, Duke JD, Shah NH, et al. Observational Health Data Sciences and Informatics (OHDSI): Opportunities for Observational Researchers. Studies in Health Technology and Informatics, 2015. DOI/identifier [verify].

Kahn MG, Callahan TJ, Barnard J, et al. A Harmonized Data Quality Assessment Terminology and Framework for the Secondary Use of Electronic Health Record Data. eGEMs, 2016. DOI [verify].

Distinction worth emphasizing

There are actually three different harmonization problems:

lexical/terminological normalization;

reconciling heterogeneous annotation ontologies;

mapping the unified representation to a healthcare interoperability standard.

CIRCA does all three. Prior NLP2FHIR work mainly addresses (3); OMOP/CDM work mainly addresses structured-data harmonization; CIRCA's unusual contribution is combining (2) and (3) around a new NLP task.

6. LLM-as-annotator, model consensus, and disagreement-based human triage

Why it matters to CIRCA: The dataset methodology relies on several models proposing/validating labels and uses agreement or uncertainty to determine where expensive human adjudication is most valuable.

Works to cite

Gilardi F, Alizadeh M, Kubli M. ChatGPT Outperforms Crowd-Workers for Text-Annotation Tasks. Proceedings of the National Academy of Sciences, 2023. DOI: 10.1073/pnas.2305016120.

vs CIRCA: Gilardi et al. establish that LLMs can perform annotation competitively in conventional text-labeling tasks; CIRCA uses multiple LLMs in a substantially more structured clinical extraction setting and does not equate model consensus with gold without human validation.

Snow R, O'Connor B, Jurafsky D, Ng AY. Cheap and Fast—But Is It Good? Evaluating Non-Expert Annotations for Natural Language Tasks. EMNLP, 2008. ACL Anthology: D08-1027.

vs CIRCA: Snow et al. motivate aggregation of noisy annotators; CIRCA effectively substitutes heterogeneous model annotators for part of the crowd and separately validates the resulting consensus.

Dawid AP, Skene AM. Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm. Applied Statistics, 1979. DOI: 10.2307/2346806.

Ratner A, Bach SH, Ehrenberg H, Fries J, Wu S, Ré C. Snorkel: Rapid Training Data Creation with Weak Supervision. Proceedings of the VLDB Endowment, 2017. DOI: 10.14778/3157794.3157797.

Seung HS, Opper M, Sompolinsky H. Query by Committee. COLT, 1992. [identifier verify].

Settles B. Active Learning Literature Survey. University of Wisconsin–Madison Computer Sciences Technical Report 1648, 2009.

How I would position your method

Avoid describing three-LLM consensus as automatically yielding “gold.” A more defensible framing is:

model-assisted candidate annotation → agreement/disagreement characterization → targeted human validation → validated gold subset.

That connects cleanly to annotator aggregation, weak supervision, and disagreement sampling without claiming that LLM votes constitute independent human evidence.

7. Clinical NLP datasets and LLM benchmarks: EHR notes and clinical dialogue

Why it matters to CIRCA: CIRCA spans both conventional clinical documentation and dialogue-derived/ambient clinical text, making heterogeneity of source distribution part of the benchmark rather than an incidental detail.

Works to cite

Johnson AEW, Pollard TJ, Shen L, et al. MIMIC-III, a Freely Accessible Critical Care Database. Scientific Data, 2016. DOI: 10.1038/sdata.2016.35.

vs CIRCA: MIMIC-III provides the underlying clinical records but no exhaustive CIR-style intent labels; CIRCA adds harmonized prospective-intent annotation over MIMIC-derived material.

Yim et al. ACI-BENCH: a Novel Ambient Clinical Intelligence Dataset for Benchmarking Automatic Visit Note Generation. Scientific Data, 2023. [identifier verify].

vs CIRCA: ACI-Bench benchmarks documentation generation from clinical dialogue; CIRCA instead uses dialogue-associated material to evaluate structured extraction of future clinical actions.

Johnson AEW, Bulgarelli L, Shen L, et al. MIMIC-IV, a Freely Accessible Electronic Health Record Dataset. Scientific Data, 2023. DOI: 10.1038/s41597-022-01899-x [verify].

Uzuner Ö, South BR, Shen S, DuVall SL. 2010 i2b2/VA Challenge on Concepts, Assertions, and Relations in Clinical Text. JAMIA, 2011. DOI: 10.1136/amiajnl-2011-000203.

Henry S, Buchan K, Filannino M, Stubbs A, Uzuner Ö. 2018 n2c2 Shared Task on Adverse Drug Events and Medication Extraction in Electronic Health Records. Journal of the American Medical Informatics Association, 2020. DOI: 10.1093/jamia/ocz166 [verify].

Ben Abacha A, et al. Overview of the MEDIQA-Chat 2023 Shared Task on the Summarization and Generation of Doctor-Patient Conversations. ClinicalNLP/ACL, 2023. ACL identifier [verify].

The strongest point here is not simply that CIRCA is “another clinical NLP benchmark,” but that its common schema is deliberately tested across different annotation histories and different discourse distributions.

8. Cross-corpus, domain-shift, and transfer evaluation

Why it matters to CIRCA: A harmonized schema is much more convincing if models trained on one source genuinely transfer to another; otherwise harmonization may only create a common file format without creating a common learnable task.

Works to cite

Gururangan S, Marasović A, Swayamdipta S, et al. Don't Stop Pretraining: Adapt Language Models to Domains and Tasks. ACL, 2020. arXiv:2004.10964.

vs CIRCA: Gururangan et al. demonstrate the importance of domain adaptation at the representation level; CIRCA measures transfer at the task/schema level across independently constructed clinical corpora.

Alsentzer E, Murphy JR, Boag W, Weng W-H, Jin D, Naumann T, McDermott M. Publicly Available Clinical BERT Embeddings. ClinicalNLP, 2019. ACL Anthology: W19-1909.

vs CIRCA: ClinicalBERT addresses adaptation to clinical language broadly; CIRCA's cross-corpus evaluation tests whether task semantics themselves survive differences in institution, source genre, and original annotation ontology.

Gu Y, Tinn R, Cheng H, et al. Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing. ACM Transactions on Computing for Healthcare, 2021. arXiv:2007.15779.
PubMedBERT.

Han X, Eisenstein J. Unsupervised Domain Adaptation of Contextualized Embeddings for Sequence Labeling. EMNLP-IJCNLP, 2019. ACL identifier [verify].

Blitzer J, Dredze M, Pereira F. Biographies, Bollywood, Boom-boxes and Blenders: Domain Adaptation for Sentiment Classification. ACL, 2007. ACL Anthology identifier [verify].

Lehman E, et al. Do We Still Need Clinical Language Models? CHIL, 2023. arXiv:2302.08091 [verify].

I would make this a visible contribution rather than a generic benchmark paragraph

Your TF-IDF+logistic-regression cross-corpus experiment is particularly useful here. It tests a different proposition from the LLM leaderboard:

whether CIRCA's harmonized labels create enough corpus-independent signal that even a conventional classifier trained on one corpus can recover the task in another.

That is evidence about the schema, not merely about model quality.

9. De-identification and surrogate/synthetic PHI replacement

Why it matters to CIRCA: Clinical LLM pipelines often require not merely detecting PHI but replacing redacted identifiers with realistic surrogates so that text remains linguistically and temporally usable by downstream models without reintroducing patient identity.

Works to cite

Carrell D, Malin B, Aberdeen J, et al. Hiding in Plain Sight: Use of Realistic Surrogates to Reduce Exposure of Protected Health Information in Clinical Text. Journal of the American Medical Informatics Association, 2013. DOI: 10.1136/amiajnl-2012-001034 [verify].

vs CIRCA: This is highly relevant if your preprocessing replaces MIMIC-style placeholders with synthetic names/dates/etc.; CIRCA uses surrogate reconstruction as an enabling preprocessing step rather than treating de-identification as its NLP contribution.

Yeniterzi R, Aberdeen J, Bayer S, Wellner B, Hirschman L, Malin B. Effects of Personal Identifier Resynthesis on Clinical Text De-identification. Journal of the American Medical Informatics Association, 2010. DOI [verify].

vs CIRCA: This is probably the most directly relevant precedent for replacing de-identified identifiers with realistic synthetic values while retaining text utility.

Neamatullah I, Douglass MM, Lehman L-WH, et al. Automated De-Identification of Free-Text Medical Records. BMC Medical Informatics and Decision Making, 2008. DOI: 10.1186/1472-6947-8-32.

Stubbs A, Kotfila C, Uzuner Ö. Automated Systems for the De-identification of Longitudinal Clinical Narratives: Overview of 2014 i2b2/UTHealth Shared Task Track 1. Journal of Biomedical Informatics, 2015. DOI: 10.1016/j.jbi.2015.06.007 [verify].

Dernoncourt F, Lee JY, Uzuner Ö, Szolovits P. De-identification of Patient Notes with Recurrent Neural Networks. Journal of the American Medical Informatics Association, 2017. DOI: 10.1093/jamia/ocw156.

Uzuner Ö, Luo Y, Szolovits P. Evaluating the State-of-the-Art in Automatic De-identification. Journal of the American Medical Informatics Association, 2007. DOI [verify].

For CIRCA, distinguish de-identification from resynthesis/surrogation. If you replace [**First Name**] with “John,” the second literature is the more specific precedent.

Highest-priority must-cite set

If space allows only about 10–12 references, I would prioritize these:

The original papers/releases for all five CIRCA source corpora — CLIP, MedDec, ap_parsing, PaniniQA, and SIMORD/ACI-Bench. These are non-negotiable because CIRCA's construction depends directly on them.

Uzuner et al., 2011 — 2010 i2b2/VA concepts/assertions/relations. Establishes the clinical assertion-status lineage.

Harkema et al., 2009 — ConText. Clear contrast between established contextual semantics and CIRCA's prospective modality.

Styler et al., 2014 — Temporal Annotation in the Clinical Domain. Essential for explaining why prospective intent is more than future temporality.

HL7 FHIR R4 RequestIntent / Request pattern, 2019. Essential because your request-intent axis is explicitly adapted from it.

NLP2FHIR, Hong et al. [verify exact citation]. Probably the closest interoperability precedent.

Gilardi et al., 2023 — ChatGPT Outperforms Crowd-Workers for Text-Annotation Tasks. Strong anchor for LLM annotation.

Snow et al., 2008 — Cheap and Fast—But Is It Good? Strong anchor for annotator aggregation.

ACI-Bench, Yim et al., 2023 [verify metadata]. Essential for the dialogue/ambient distribution.

Johnson et al., 2016 — MIMIC-III. Required for the MIMIC provenance.

Gururangan et al., 2020 — Don't Stop Pretraining. Good anchor for domain shift/adaptation, particularly if you discuss cross-corpus transfer.

Carrell et al., 2013 — Hiding in Plain Sight or Yeniterzi et al., 2010 — identifier resynthesis, if surrogate PHI replacement is methodological enough to mention in the main paper.

Areas where the literature link is weakest

The clearest citation gap is Theme 4: clinical request authority. FHIR gives you a strong structured-data precedent, and speech-act theory gives a strong linguistic precedent, but I do not know of a canonical clinical-NLP corpus that systematically annotates proposal vs plan vs order vs option from free clinical narrative. That gap may be genuine and is potentially one of CIRCA's more defensible innovations.

A second, narrower gap is exhaustive cross-action prospective-intent extraction. There is ample work on radiology follow-up recommendations, medication decisions, orders, temporal events, and care-plan elements, but I do not know a canonical benchmark whose primary unit is every prospective clinical action across heterogeneous action types and clinical genres, with both structured attributes and separate authority/modality axes.

The bibliographic details I would verify most carefully before submission are the CLIP, MedDec, ap_parsing, PaniniQA, SIMORD, NLP2FHIR, ACI-Bench, and radiology follow-up papers. I am confident about the conceptual relevance of those literatures, but not sufficiently confident in the exact metadata of those particular entries to fabricate it.