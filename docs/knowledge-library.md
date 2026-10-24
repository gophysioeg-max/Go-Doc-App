# Go Doc Knowledge Library and Build Resources

Everything Go Doc needs to build the knowledge layer described in the
[Self-Assessment & Knowledge Assistant spec](https://claude.ai/artifact/S86EMtwTbRC2v4wdXaDJfV):
the sources that go into the knowledge base, and the material to learn how to build it.

As of 24 Oct 2026. Owner of the source list: Michael (decision K5). Licences: decision K4.

## How to read this list

| Mark | Meaning |
| --- | --- |
| **P0** | Needed before the physio assistant launches (Phase 2) |
| **P1** | Add in the first 3 months after launch |
| **P2** | Add when the specialty is offered or asked for |
| **Ingest** | Goes into the clinical tier (chunked, embedded, cited) |
| **Reference** | Read by Michael to write patient articles and triage rules; not ingested |
| **Licence** | Ingest only after written permission from the publisher (decision K4) |

Order of authority when sources disagree: clinical practice guideline → systematic review → textbook.
Guidelines are ingested first because they are free or cheap to licence and are revised more often than textbooks.

"Free to read" is not the same as "free to put in a commercial AI product". Every source below needs its reuse terms checked
before ingest, including WHO and NICE material; until then it is **Reference** only.

Editions were checked on 24 Oct 2026 against publisher and retailer listings found by web search. Confirm each one
on the publisher page before buying.

## Clinical practice guidelines

| Source | Covers | Priority | Access and licence |
| --- | --- | --- | --- |
| [JOSPT clinical practice guidelines](https://www.jospt.org/) (CPG section; APTA Orthopaedics and Sports) | Low back pain, neck pain, hip OA, hip pain, knee ligament and meniscus injuries, patellofemoral pain, ankle sprain, Achilles tendinopathy, heel pain, shoulder adhesive capsulitis, lateral elbow pain, carpal tunnel, hamstring strain | P0 | Many free to read; ask JOSPT for AI-use permission |
| [APTA clinical practice guidelines list](https://www.apta.org/patient-care/evidence-based-practice-resources/cpgs) | Index of APTA and academy CPGs: neurology (stroke and locomotor training, vestibular hypofunction, Parkinson disease, concussion, outcome measures), paediatrics (torticollis and others), geriatrics, women's health, cardiopulmonary | P0 | Mixed; check per guideline |
| [NICE NG59: Low back pain and sciatica in over 16s](https://www.nice.org.uk/guidance/ng59) (2016, updated 2020) | Back pain, sciatica | P0 | NICE copyright; free to read, commercial reuse needs NICE permission |
| [NICE NG226: Osteoarthritis in over 16s](https://www.nice.org.uk/guidance/ng226) (2022) | Knee, hip and hand OA | P0 | As above |
| [NICE NG236: Stroke rehabilitation in adults](https://www.nice.org.uk/guidance/ng236) (2023) | Stroke rehab | P1 | As above |
| [WHO guideline on non-surgical management of chronic primary low back pain in adults](https://www.who.int/publications/i/item/9789240081789) (2023) | Chronic low back pain in primary and community care | P0 | Usually CC BY-NC-SA 3.0 IGO: non-commercial, so ask WHO before ingest |
| [WHO Package of Interventions for Rehabilitation](https://www.who.int/teams/noncommunicable-diseases/sensory-functions-disability-and-rehabilitation/rehabilitation/service-delivery/package-of-interventions-for-rehabilitation) | 20 conditions across 8 modules: MSK, neuro, paediatrics, older people, cardiopulmonary | P0 | As above |
| [World Guidelines for Falls Prevention](https://pmc.ncbi.nlm.nih.gov/articles/PMC9523684/) (Age and Ageing, 2022) | Falls risk, balance, older adults | P1 | Open access; check the article licence |
| Mona's home PT program and other Go Doc programs | Go Doc's own protocols | P0 | Owned by Go Doc; ingest first |

## Textbooks by specialty

All textbooks are **Ingest after licence** (decision K4) and **Reference** until then.

### Screening and red flags: the safety base

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Goodman & Snyder's Differential Diagnosis for Physical Therapists: Screening for Referral](https://shop.elsevier.com/books/goodman-and-snyder-s-differential-diagnosis-for-physical-therapists/heick/978-0-323-72204-9) (Heick, Lazaro) | 7th, 2022 | Elsevier | P0 |
| [Pharmacology in Rehabilitation](https://www.fadavis.com/) (Ciccone): Reference only, because the AI never advises on drugs | 5th, 2016; an updated 5th may exist (2022) | F.A. Davis | P2 |

### Orthopaedics and musculoskeletal

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Magee's Orthopedic Physical Assessment](https://shop.elsevier.com/books/magee-s-orthopedic-physical-assessment/manske/978-0-443-12864-6) (Manske, Magee) | 8th, 2026 | Elsevier | P0 |
| [Netter's Orthopaedic Clinical Examination: An Evidence-Based Approach](https://www.us.elsevierhealth.com/netters-orthopaedic-clinical-examination-9780323695350.html) (Cleland, Koppenhaver, Su) | 4th, 2021 | Elsevier | P0 |
| [Dutton's Orthopaedic: Examination, Evaluation and Intervention](https://www.mhprofessional.com/dutton-s-orthopaedic-examination-evaluation-and-intervention-sixth-edition-9781264259076-usa) | 6th, 2023 | McGraw Hill | P0 |
| [Therapeutic Exercise: Foundations and Techniques](https://www.fadavis.com/) (Kisner, Colby, Borstad) | 8th, 2022 | F.A. Davis | P0 |
| [Neumann's Kinesiology of the Musculoskeletal System](https://shop.elsevier.com/books/neumann-s-kinesiology-of-the-musculoskeletal-system/neumann/978-0-323-71859-2) | 4th, 2024 | Elsevier | P1 |
| [Grieve's Modern Musculoskeletal Physiotherapy](https://shop.elsevier.com/books/grieves-modern-musculoskeletal-physiotherapy/falla/978-0-7020-8089-0) (Falla et al.) | 5th, 2024 | Elsevier | P1 |
| [Petty's Musculoskeletal Examination and Assessment](https://shop.elsevier.com/books/pettys-musculoskeletal-examination-and-assessment/ryder/978-0-323-87471-7) (Ryder, Barnard) | 6th, 2023 | Elsevier | P1 |
| [Petty's Principles of Musculoskeletal Treatment and Management](https://shop.elsevier.com/books/pettys-principles-of-musculoskeletal-treatment-and-management/barnard/978-0-323-87228-7) (Barnard, Ryder) | 4th, 2023 | Elsevier | P1 |
| [Clinical Reasoning in Musculoskeletal Practice](https://www.us.elsevierhealth.com/clinical-reasoning-in-musculoskeletal-practice-9780702059766.html) (Jones, Rivett) | 2nd, 2019 | Elsevier | P1 |
| [Maitland's Vertebral Manipulation, Vol 1](https://shop.elsevier.com/books/maitlands-vertebral-manipulation/hengeveld/978-0-7020-4066-5) (Hengeveld, Banks) | 8th, 2013 | Elsevier | P2 |
| [The Lumbar Spine: Mechanical Diagnosis and Therapy](https://www.optp.com/enrichment/pdp/801-2) (McKenzie, May) | 2nd, 2003 | Spinal Publications | P2 |
| [Clinical Neurodynamics](https://www.uk.elsevierhealth.com/clinical-neurodynamics-9780750654562.html) (Shacklock) | 1st, 2005 | Elsevier | P2 |
| [Diagnosis and Treatment of Movement Impairment Syndromes](https://shop.elsevier.com/books/diagnosis-and-treatment-of-movement-impairment-syndromes/sahrmann/978-0-8016-7205-7) (Sahrmann) | 1st, 2002 | Elsevier | P2 |

### Post-surgical rehabilitation

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Clinical Orthopaedic Rehabilitation: A Team Approach](https://shop.elsevier.com/books/clinical-orthopaedic-rehabilitation/giangarra/978-0-443-28631-5) (Giangarra, Manske) | 4th, 2018; 5th due Jul 2027 | Elsevier | P0 |
| [Rehabilitation for the Postsurgical Orthopedic Patient](https://uk.elsevierhealth.com/rehabilitation-for-the-postsurgical-orthopedic-patient-9780323077477.html) (Maxey, Magnusson) | 3rd, 2013 | Elsevier | P1 |
| [Rehabilitation of the Hand and Upper Extremity](https://shop.elsevier.com/books/rehabilitation-of-the-hand-and-upper-extremity-2-volume-set/macdermid/978-0-443-41190-8) (Skirven et al.) | 7th, 2021; 8th due 2029 | Elsevier | P2 |
| [Orthotics and Prosthetics in Rehabilitation](https://eu.elsevierhealth.com/orthotics-and-prosthetics-in-rehabilitation-9780443113697.html) (Chui et al.) | 5th, 2025 | Elsevier | P2 |

### Sports

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Brukner & Khan's Clinical Sports Medicine: Managing Injuries](https://www.mheducation.com.au/clinical-sports-medicine-managing-injuries-6th-edition-9781761000027-aus) and *Foundations of Clinical Practice* | 6th, 2025–26 (now split into separate books) | McGraw Hill Australia | P1 |

### General rehabilitation

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [O'Sullivan & Schmitz's Physical Rehabilitation](https://www.fadavis.com/) (Fulk, Chui) | 8th, 2024 | F.A. Davis | P0 |
| [Practical Evidence-Based Physiotherapy](https://www.asia.elsevierhealth.com/practical-evidence-based-physiotherapy-9780323848398.html) (Herbert et al.) | 3rd, 2022 | Elsevier | P2 (reference for Michael) |

### Neurology

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Umphred's Neurological Rehabilitation](https://www.us.elsevierhealth.com/umphreds-neurological-rehabilitation-9780443112928.html) (Lazaro) | 8th, 2025 | Elsevier | P0 |
| [Physical Management for Neurological Conditions](https://eu.elsevierhealth.com/physical-management-for-neurological-conditions-9780323881326.html) (Lennon, Ramdharry, Verheyden) | 5th, 2024 | Elsevier | P0 |
| [Motor Control: Translating Research into Clinical Practice](https://shop.lww.com/) (Shumway-Cook, Woollacott et al.) | 6th, 2022 | Wolters Kluwer | P1 |
| [Stroke Rehabilitation: A Function-Based Approach](https://shop.elsevier.com/books/stroke-rehabilitation/gillen/978-0-323-63994-1) (Gillen, Nilsen) | 5th, 2020 | Elsevier | P1 |
| [Neuroscience: Fundamentals for Rehabilitation](https://shop.elsevier.com/books/neuroscience/lundy-ekman/978-0-323-79267-7) (Lundy-Ekman) | 6th, 2022 | Elsevier | P1 |
| [Vestibular Rehabilitation](https://search.worldcat.org/oclc/885123823) (Herdman, Clendaniel) | 4th, 2014 | F.A. Davis | P1 |
| [Bobath Concept: Theory and Clinical Practice in Neurological Rehabilitation](https://www.wiley-vch.de/de/fachgebiete/medizin-und-gesundheit/bobath-concept-978-1-4051-7041-3) (Raine et al.) | 1st, 2009 | Wiley-Blackwell | P2 |

### Paediatrics

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Campbell's Physical Therapy for Children](https://shop.elsevier.com/books/campbells-physical-therapy-for-children/palisano/978-0-323-79796-2) (Palisano, Orlin, Schreiber) | 6th, 2022 | Elsevier | P0 |
| [Tecklin's Pediatric Physical Therapy](https://shop.lww.com/p/9781975141592) | 6th, 2022 | Wolters Kluwer | P1 |
| [Meeting the Physical Therapy Needs of Children](https://www.fadavis.com/) (Effgen, Fiss) | 3rd, 2021 | F.A. Davis | P2 |

### Older adults, balance and falls

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Guccione's Geriatric Physical Therapy](https://tienda.elsevier.com/books/gucciones-geriatric-physical-therapy/avers/978-0-323-60912-8) (Avers, Wong) | 4th, 2020 | Elsevier | P0 (many Go Doc patients are older) |

### Cardiopulmonary

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Cardiovascular and Pulmonary Physical Therapy: Evidence to Practice](https://www.elsevier.com/books/cardiovascular-and-pulmonary-physical-therapy/frownfelter/978-0-323-62471-8) (Frownfelter, Dean) | 6th, 2022 | Elsevier | P2 |
| [Essentials of Cardiopulmonary Physical Therapy](https://shop.elsevier.com/books/essentials-of-cardiopulmonary-physical-therapy/hillegass/978-0-323-72212-4) (Hillegass) | 5th, 2022 | Elsevier | P2 |
| [Cardiorespiratory Physiotherapy: Adults and Paediatrics](https://www.uk.elsevierhealth.com/cardiorespiratory-physiotherapy-adults-and-paediatrics-9780702047312.html) (Main, Denehy) | 5th, 2016 | Elsevier | P2 |

### Pelvic floor and women's health

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Evidence-Based Physical Therapy for the Pelvic Floor](https://shop.elsevier.com/books/evidence-based-physical-therapy-for-the-pelvic-floor/bo/978-0-7020-8308-2) (Bø et al.) | 3rd, 2024 | Elsevier | P2 |
| Women's Health in Physical Therapy (Irion & Irion) | 1st, 2010; dated, look for a newer title | LWW | P2 |

### Pain

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [Mechanisms and Management of Pain for the Physical Therapist](https://uk.elsevierhealth.com/mechanisms-and-management-of-pain-for-the-physical-therapist-9780443117220.html) (Sluka) | 3rd, 2025 | Elsevier | P0 |
| [Explain Pain](https://noigroup.com/product/explain-pain-second-edition/) (Butler, Moseley) | 2nd, 2013 | NOI Group | P0 (the model for how patient articles explain pain) |

### Exercise prescription and modalities

| Title | Edition | Publisher | Priority |
| --- | --- | --- | --- |
| [ACSM's Guidelines for Exercise Testing and Prescription](https://shop.lww.com/) | 12th, 2025 | Wolters Kluwer | P0 |
| [Electrotherapy: Evidence-Based Practice](https://shop.elsevier.com/books/electrotherapy/watson/978-0-443-10179-3) (Watson) | 12th, 2008; dated | Elsevier | P2 |

### Notes on the textbook list

- **P0 total: 14 textbooks.** That covers screening, ortho, post-op, neuro, paediatrics, older adults, pain and exercise prescription.
- **Dated but still standard:** Sahrmann, McKenzie, Maitland, Shacklock, Watson and Vestibular Rehabilitation have no newer edition. Use them for technique, and let guidelines win on evidence.
- **Due soon:** Clinical Orthopaedic Rehabilitation 5th (Jul 2027). Licence the 4th now and replace it when the 5th comes out.

## Reference databases (not ingested)

| Resource | Used for | Access |
| --- | --- | --- |
| [PEDro](https://pedro.org.au/) | Finding trials, reviews and guidelines when a source is challenged | Free |
| [Shirley Ryan AbilityLab Rehabilitation Measures Database](https://www.sralab.org/rehabilitation-measures) | Outcome measures for milestones and before/after values | Free to read |
| [Cochrane Library](https://www.cochranelibrary.com/) | Systematic reviews | Abstracts free |
| [PubMed](https://pubmed.ncbi.nlm.nih.gov/) | Primary research | Free |
| [Physiopedia](https://www.physio-pedia.com/) | Quick reading for Michael | Licence unclear (pages differ), so never ingested |

## Patient tier: how to write it

The patient tier is written by Go Doc, not copied. Use these as models for tone and structure, then write in Egyptian Arabic:

- *Explain Pain* (above) for explaining pain without fear.
- The WHO EMRO [Unified Medical Dictionary](https://umd.emro.who.int/WHODictionary/) for consistent Arabic medical terms.
- Patient leaflets from NICE guidelines ("Information for the public" on each guideline page) for what a patient needs to know.

## Learning to build it

### 1. Foundations: how RAG systems work

| Resource | Type | Why |
| --- | --- | --- |
| Chip Huyen, *AI Engineering* (O'Reilly) | Book | The best single overview: RAG, evaluation, guardrails, cost |
| Jay Alammar and Maarten Grootendorst, *Hands-On Large Language Models* (O'Reilly) | Book | Embeddings, semantic search and RAG with diagrams and code |
| John Berryman and Albert Ziegler, *Prompt Engineering for LLMs* (O'Reilly) | Book | How to structure prompts and context for reliable answers |
| [Anthropic: Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) | Article | Chunking + contextual embeddings + BM25 + reranking; the retrieval design this project should copy |
| [Anthropic courses on GitHub](https://github.com/anthropics/courses) | Course | API fundamentals, prompt engineering, real-world prompting, tool use |
| [Anthropic Academy](https://anthropic.skilljar.com) | Course | Free courses on building with the Claude API |
| [Claude cookbooks](https://github.com/anthropics/anthropic-cookbook) | Code | RAG, contextual retrieval, citations and evaluation notebooks |
| [DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/) | Course | Search for "RAG", "evaluating RAG", "embeddings", "vector databases" |

### 2. Claude API features this project uses

| Feature | Docs | Used for |
| --- | --- | --- |
| Citations | [docs](https://platform.claude.com/docs/en/build-with-claude/citations) | Every answer quotes its source passage (safety rule "No source, no answer") |
| Prompt caching | [docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Cache the fixed system prompt and safety rules; cuts cost and latency per message |
| Structured outputs | [docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | The pre-visit brief and the diagnosis/medication output check as validated JSON |
| PDF support | [docs](https://platform.claude.com/docs/en/build-with-claude/pdf-support) | Reading guideline PDFs during ingestion |
| Streaming | [docs](https://platform.claude.com/docs/en/build-with-claude/streaming) | Chat answers appear as they are written |
| Batch processing | [docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing) | Generating chunk context for contextual retrieval at half price |
| Embeddings | [docs](https://platform.claude.com/docs/en/build-with-claude/embeddings) | Anthropic has no embedding model of its own; this page lists recommended providers |
| TypeScript SDK | [repo](https://github.com/anthropics/anthropic-sdk-typescript) | Supabase Edge Functions run TypeScript (Deno) |
| Python SDK | [repo](https://github.com/anthropics/anthropic-sdk-python) | The ingestion script |

### 3. Stack: GitHub, Vercel, Supabase, Expo

| Resource | Used for |
| --- | --- |
| [Supabase AI & Vectors](https://supabase.com/docs/guides/ai) | pgvector setup, semantic and hybrid search, RAG with permissions |
| [pgvector](https://github.com/pgvector/pgvector) | Vector column types and indexes (HNSW) |
| [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) | "Physio sees assigned patients only"; patients cannot read the clinical tier |
| [Supabase Edge Functions](https://supabase.com/docs/guides/functions) | The chat, assistant and triage APIs |
| [Supabase phone login](https://supabase.com/docs/guides/auth/phone-login) | Phone and one-time code sign-in |
| [Supabase Storage](https://supabase.com/docs/guides/storage) | Source files, exercise videos, before/after photos |
| [Next.js docs](https://nextjs.org/docs) | Web apps for patient, physio and admin |
| [Vercel docs](https://vercel.com/docs) | Deploys from GitHub `main`, preview per pull request, environment variables |
| [Expo docs](https://docs.expo.dev) | Patient and physio mobile apps, push notifications |
| [GitHub Actions](https://docs.github.com/actions) | Tests and the safety test set on every pull request |

### 4. Arabic language

| Resource | Used for |
| --- | --- |
| [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Compare embedding models on Arabic retrieval before choosing (decision K3) |
| [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) | Arabic normalisation and dialect handling (alef/yaa forms, diacritics, Arabic-Indic digits) |
| [WHO EMRO Unified Medical Dictionary](https://umd.emro.who.int/WHODictionary/) | Consistent Arabic terms in patient articles |

### 5. Getting text out of books and PDFs

| Resource | Used for |
| --- | --- |
| [Docling](https://github.com/docling-project/docling) | PDF to structured text with headings, tables and page numbers |
| [PyMuPDF](https://pymupdf.readthedocs.io) | Fast page-level text extraction with page numbers for citations |

### 6. Testing that it is safe and correct

| Resource | Used for |
| --- | --- |
| [Ragas](https://docs.ragas.io) | Retrieval and answer-faithfulness metrics |
| [promptfoo](https://www.promptfoo.dev) | Regression tests in CI: red-flag phrases, diagnosis wording, medication refusals |
| [Anthropic: define success criteria and build evals](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | How to write an eval set |

The safety test set (decision K12) is written by Michael: at least one message per red flag in each of the 10 patterns,
in Arabic, English and Franco-Arabic, plus diagnosis-seeking and medication questions. It runs on every pull request.

### 7. Medical AI, regulation and privacy

| Resource | Used for |
| --- | --- |
| [WHO: Ethics and governance of AI for health (2021)](https://www.who.int/publications/i/item/9789240029200) | Principles to cite in the legal review |
| [WHO: Guidance on large multi-modal models (2024)](https://www.who.int/publications/i/item/9789240084759) | Risks specific to chat models in health |
| [FDA: Clinical Decision Support Software guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software) | Why the physio assistant (professional reviews the basis) is lower risk than patient-facing advice |
| [IMDRF: Software as a Medical Device](https://www.imdrf.org/working-groups/software-medical-device-samd) | Risk categories regulators use for health software |
| Egypt Personal Data Protection Law (Law 151 of 2020) and its executive regulations | Health data consent and retention; confirm in the legal review (K6) |
| Egyptian Drug Authority rules on medical devices and software | Whether the patient chat counts as a device; confirm in the legal review (K6) |

## Next steps

1. Michael confirms the P0 list and marks anything Go Doc already owns.
2. Omar emails the publishers of P0 textbooks asking for commercial AI-use licences (template to draft).
3. While waiting: ingest the free P0 guidelines and Mona's program, and build the physio assistant on them.
4. Run the embedding comparison on 50 real Arabic and English questions (K3).
5. Write the safety test set before any patient-facing code.
