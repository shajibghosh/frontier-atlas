# Editorial methodology and evidence standards

**Dataset snapshot:** 8 October 2026. **Content status:** research synthesis and curated problem formulations; not an independently peer-reviewed survey.

## Purpose and scope

FrontierAtlas compiles unresolved questions from five scientific domains. Each question is posed narrowly enough to identify a relevant barrier and at least one measurable or mathematically checkable first milestone. The data is not meant to represent a ranking of all unsolved problems, a comprehensive systematic literature search, or proof of priority over existing work.

## Classification system

The `status` field differentiates formal mathematical questions from foundational scientific questions and narrower active research challenges. A hypothesis, a formal theorem, an empirical law, an instrument-limited inference problem, and an unanswered mechanistic question do not share one common proof standard.

- **Formally open:** a mathematically defined existence, regularity, uniqueness, or analogous theorem target.
- **Foundational open question:** a broad mechanistic or conceptual gap lacking an accepted decisive explanation.
- **Active research challenge:** a focused predictive, explanatory, experimental or translational gap with important existing partial results.

Use the exact `status` label stored in the dataset, not an inferred classification. Status can change with subsequent work.

## Per-problem fields

- **Precise question:** an explicit unresolved objective rather than a vague field label.
- **Scientific rationale:** significance of answering that question.
- **Bottleneck:** a specific barrier that obstructs credible progress.
- **Research direction:** a proposal for how to make progress; it is not stated as a published claim unless directly supported.
- **First test:** a constrained experiment, proof target, benchmark or falsification condition.
- **References:** linked primary sources, research papers, scholarly reviews or institutional sources that document context and outstanding limitations.

## What a reference supports

The references constitute a **curated reading list**, not a certified systematic review. One reference may support the existence of a research area or document a partial solution without establishing that every aspect of a problem is unresolved. Research directions and suggested milestones are editorial suggestions unless a cited source explicitly makes the same proposal. Verify each document's title, authors, date, DOI, and claim before scholarly reuse. A valid-looking URL does not establish source quality, peer review, or current availability.

## Evidence-review rubric for contributions

1. Is the problem open *as worded*, as of the claimed snapshot date? Is there a recent claimed or peer-reviewed solution?
2. Does each source specifically support the problem context or bottleneck? Prefer official problem statements and primary or high-quality scholarly references.
3. Does the proposed first test have a well-defined observable, theorem statement or failure criterion?
4. Are missing assumptions, measurement confounding, mathematical identifiability, uncertainty and alternative mechanisms clearly named?
5. Is the question sufficiently distinct from existing entries to avoid duplicate counts?
6. Are biomedical, psychological and genetic proposals consistent with accepted ethics, consent and data governance requirements?

## Types of valid progress

- **Mathematical:** rigorous theorem with assumptions, complete proof, and counterexample searches.
- **Computational:** reproducible benchmark, ablations, baselines, uncertainty estimates, and held-out or prospective evaluation.
- **Experimental:** predeclared endpoints, controls, calibration, error analysis, independent replication.
- **Causal:** declared causal graph, identification assumptions, sensitivity analysis, and justified intervention design.

A better model score is not necessarily an explanation; a simulation is not automatically a theorem; association is not causation.

## Snapshot caveat

Clay's September 2026 Navier–Stokes statement concerning a forced-equation construction is described in the companion catalog. It is not a proof of the separate unforced regularity result. Major claimed breakthroughs should be marked as *under evaluation* until their scope and validation are settled.

## Scope of AI assistance

ChatGPT, powered by OpenAI GPT-6, assisted the synthesis and repository production. This disclosure does **not** mean the references were all inspected line-by-line, nor that the atlas received independent expert fact-checking or peer review.
