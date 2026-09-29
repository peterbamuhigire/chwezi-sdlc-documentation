# Uganda Regulatory Framework

## Primary Legislation

| Act | Key Requirements for Software Systems |
|---|---|
| Data Protection and Privacy Act 2019 (No. 9 of 2019) | PII collection consent; special personal data (incl. financial info); PDPO registration; data subject rights (30-day response); immediate breach notification; DPIA for high-risk processing; DPO designation; 10-year imprisonment for Part VII offences |
| Data Protection and Privacy Regulations 2021 | PDPO registration (Form 2); DPIA content requirements; DPO qualifications and tasks; breach notification content; data protection register |
| Uganda Income Tax Act (Cap 340) | PAYE calculation and remittance; 7-year financial record retention; WHT (6%) on local service supplier payments; PAYE employer obligations |
| Uganda NSSF Act | Employer contribution (10%) and employee contribution (5%) of gross salary; monthly remittance in prescribed format |
| PPDA Act (Cap 305) | All procurement classified by category; threshold-based approval matrix; full documentation on file before payment released; public procurement register |
| Uganda Companies Act | 7-year company record retention; director obligations; annual returns |
| Electronic Signatures Act | Legal recognition of electronic records and signatures |
| Computer Misuse Act 2011 (principal Act only; see the note below) | Unauthorised computer access; data interference offences; system-generated evidence admissibility |

**Computer Misuse Act: legal currency (checked 29 Sep 2026; factual reporting, not legal advice).** On 17 Mar 2026 the Constitutional Court declared the whole Computer Misuse (Amendment) Act 2022 void (quorum defect: Rule 24(3) of the Rules of Procedure; Articles 88 and 89 of the Constitution). Per secondary reports it also struck ss.11, 23 and 26 to 29 of the principal Act (2023 revised edition numbering) and criminal libel (Penal Code ss.162 and 163); s.25 was struck earlier, on 11 Jan 2023. The Attorney General halted prosecutions under the struck provisions. The rest of the principal Act remains in force. In an SRS, cite the principal Act without 2022-amendment obligations, and verify every section number against the judgment on ULII before it appears in a requirement. Sources (accessed 29 Sep 2026): CPJ, 19 Mar 2026, https://cpj.org/2026/03/uganda-declares-criminal-defamation-unconstitutional-strikes-down-cybercrime-law/ ; The Independent (Uganda), https://www.independent.co.ug/court-castrates-computer-misuse-act-2022-amendment-declared-illegal/ ; Daily Monitor, 26 Mar 2026, https://www.monitor.co.ug/uganda/news/national/ag-halts-arrests-based-on-nullified-computer-misuse-law-5403596 . Register records `UG-CMA-*`: https://github.com/peterbamuhigire/social-media-skills/blob/main/docs/source-registers/source-register.json .

## Regulatory Bodies

| Body | Role for Software Systems |
|---|---|
| PDPO (within NITA-U) | Receives breach notifications; registers data controllers; investigates complaints; issues DPIA guidance; can direct data subject notification; can impose fines and refer for criminal prosecution |
| URA (Uganda Revenue Authority) | EFRIS system-to-system API for fiscal receipting; PAYE remittance; WHT returns; TIN validation |
| PPDA | Procurement documentation compliance; audit of procurement records |
| OAG | Annual audit of government entities; 7-year audit trail required; trial balance and GL exportable in auditable formats |
| NSSF Uganda | Monthly employer contribution schedule in prescribed format |
| NIRA | NIN validation API for farmer and employee registration |
| ICPAU | IFRS for SMEs adoption; financial reporting standards |
| UNBS | Product quality standards; CoA requirements for domestic sales |

## DPPA 2019 — Full Section Reference

### Part I — Preliminary

**Section 1 — Application:** Applies to any person, institution, or public body collecting, processing, holding, or using personal data within Uganda; and outside Uganda if processing Ugandan citizens' data.

**Section 2 — Definitions (key):**
- *Personal data* — information from which a person can be identified: nationality, age, marital status, educational level, occupation, identification number, identity data, or any opinion about the individual
- *Special personal data* — religious/philosophical beliefs, political opinions, sexual life, **financial information**, health status, medical records
- *Data controller* — determines purposes and manner of processing
- *Data collector* — collects personal data (distinct role unique to Uganda Act)
- *Data processor* — processes data on behalf of controller (not an employee of controller)
- *Data subject* — individual from whom data is collected
- *Consent* — freely given, specific, informed, unambiguous indication of the data subject's wish
- *Processing* — collection, organisation, adaptation, retrieval, use, disclosure, alignment, combination, blocking, erasure, or destruction

### Part II — Principles (Section 3)

Data collectors, processors, and controllers shall be **accountable to the data subject** for data collected, processed, held, or used.

### Part III — Data Collection and Processing

**Section 6 — DPO:** Every institution's head shall designate a DPO responsible for compliance.

**Section 7 — Lawful Processing Bases:**
- Prior consent (unless exception applies)
- Authorised or required by law
- Public duty of a public body
- National security
- Prevention/detection/prosecution of offences
- Performance of a contract
- Medical purposes
- Legal obligation

**Section 8 — Children:** Consent of parent/guardian required unless: compliance with law, or research/statistical purposes. Data controllers must establish age verification systems.

**Section 9 — Special Personal Data:** Collection and processing of special personal data prohibited unless lawfully justified. Exception: data collected under Uganda Bureau of Statistics Act 1998.

**Section 13 — Right to be Informed:** Must inform data subject before collection of: purpose, right to access and request rectification.

**Section 16 — Right to Rectification/Erasure:** Data subject may request:
- Correction or deletion of inaccurate, irrelevant, excessive, out-of-date, incomplete, misleading, or unlawfully obtained data
- Destruction of data the controller no longer has authority to retain
- Controller must comply or reject in writing; failure to comply within 30 days → data subject may complain to PDPO

**Section 17 — Purpose Limitation:** Further processing compatible if: historical, statistical, or research purposes, provided identity is not revealed in published form.

**Section 18 — Retention:**
- Retain only as long as necessary for original purpose
- At expiry: destroy, delete, or de-identify
- Destruction must prevent reconstruction in intelligible form
- Exception: historical, statistical, or research retention

**Section 19 — Cross-border Transfers:** Processing or storage outside Uganda permitted only if:
- Destination country has adequate protection (at least equivalent to the Act), OR
- Data subject has consented

**Section 20 — Security Obligations:**
- Adopt appropriate technical and organisational measures to prevent loss, damage, unauthorised destruction, and unlawful access
- Identify foreseeable risks, establish safeguards, verify effectiveness, update in response to new risks
- Observe generally accepted information security practices

**Section 21 — Data Processor Contracts:** Data controller must not permit processing unless data processor has established required security measures. Written contract must require confidentiality and security measures.

**Section 23 — Data Breach Notification:**
- **Immediately** notify PDPO of unauthorised access/acquisition
- PDPO then determines whether data subject notification is required
- If PDPO directs notification: registered mail, email, website, or mass media publication
- Notification content: nature of breach, data involved, categories and approximate number of affected data subjects, likely consequences, remedial measures taken/proposed, DPO contact details
- PDPO provides guidance to controller on managing the breach

### Part IV — Rights of Data Subjects

**Section 14 — Right of Access:** Data subject may request copy of personal data held about them.

**Section 15 — Right to Object:** Data subject may object to collection or processing; controller must stop unless processing falls under Section 7(2) exceptions.

**Section 16 — Right to Rectification/Erasure:** See above.

### Part V — PDPO Registration

**Section 29 — Register:** PDPO maintains a public Data Protection Register. All data controllers must register.

### Part VI — Offences and Penalties

**Section 31 — Unlawful Data Disclosure:** Offence to knowingly disclose personal data in contravention of the Act.

**Section 32 — Unlawful Destruction/Concealment/Alteration:** Offence to destroy, delete, conceal, or alter personal data to prevent lawful access.

**Section 37 — Individual Penalties:** Up to 245 currency points (UGX 4.9M ≈ USD 1,300).

**Section 38 — Corporate Penalties:** Corporation liable; court may additionally order fine not exceeding 2% of annual gross turnover.

**Part VII — Imprisonment:** Prison term not exceeding 10 years for certain offences.

## PPDA Compliance Requirements

Every purchase order must:
1. Be classified by category (goods/services/works/consultancy)
2. Meet applicable threshold approval level
3. Have full documentation on file (RFQ, evaluation, approval, LPO, GRN, invoice, payment)
4. Be recorded in the PPDA procurement register

No payment may be released until all required PPDA documentation is filed.

## URA EFRIS Requirements

Every commercial invoice and POS receipt must:
1. Be submitted to URA EFRIS via system-to-system API in real time on posting
2. Receive a Fiscal Document Number (FDN) from EFRIS
3. Print the FDN on the physical/digital document
4. Store the FDN in the database linked to the document
5. Implement retry queue for failed submissions (exponential backoff)
6. Never block user workflow pending EFRIS response — submit asynchronously

## OAG Audit Trail Requirements

- All financial records retained for 7 years (Income Tax Act + Companies Act)
- Trial balance, GL detail, and audit trail exportable in formats suitable for OAG review
- GL hash chain or equivalent integrity mechanism to detect tampering
- Every GL entry: timestamp, user ID, IP address, before/after values, document reference
