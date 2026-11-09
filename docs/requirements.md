# Requirements

## Persona

**Jenny, accountant** at a small business (about 5 to 20 staff). She receives 50 to 300
supplier invoices a month as e-invoice XML, PDF and phone photos. She keys them into
accounting software by hand. She wants fewer typing errors and a record of who approved what.

## User stories

| ID | Story | Main acceptance criteria | Priority |
| --- | --- | --- | --- |
| US-01 | As an accountant, I want to upload many files at once | PDF, JPG, PNG, XML accepted; max 10 MB each; wrong types rejected with a reason | Must |
| US-02 | As an accountant, I want e-invoice XML read exactly, without AI | Given valid XML, every field matches the file and Bedrock is never called | Must |
| US-03 | As an accountant, I want PDFs and images read with a confidence per field | Each field has a value and a confidence; unreadable fields stay empty, never guessed | Must |
| US-04 | As an accountant, I want totals, tax rates and tax IDs checked | Errors appear on the field concerned, with a reason in the user's language | Must |
| US-05 | As an accountant, I want a warning for duplicate invoices | Same seller tax ID, series and number is flagged and approval is blocked | Must |
| US-06 | As an accountant, I want a split review screen | Low-confidence and invalid fields are highlighted; keyboard shortcuts approve and move on | Must |
| US-07 | As an accountant, I want to export approved documents to CSV | Only approved documents export; CSV is safe against CSV injection | Must |
| US-08 | As a chief accountant, I want the edit and approval history | Each change records who, when, old and new value; the log is append-only | Should |
| US-09 | As an owner, I want my company's data fully separated | Tenant A asking for tenant B's document ID gets 404 | Must |
| US-10 | As a user, I want English and Vietnamese | First visit: Vietnam IP gives Vietnamese, elsewhere English; the user's choice is remembered and wins; switching keeps typed data | Must |
| US-11 | As a user, I want original files deleted when I am done or uploaded by mistake | Export deletes the originals of that export; "Delete now" deletes any time; unfinished documents expire after 7 days | Must |

## Non-functional requirements

| ID | Type | Measurable requirement |
| --- | --- | --- |
| NFR-01 | Performance | XML processed in under 3 s; one-page image or PDF under 20 s (p95) |
| NFR-02 | Accuracy | On the eval set: tax ID, invoice number, total correct at 95% or more; line items F1 at 85% or more |
| NFR-03 | Cost | Under 0.01 USD per document; infrastructure under 5 USD per month; budget alerts at 5 and 10 USD |
| NFR-04 | Reliability | Each document processed exactly once in effect even if SQS redelivers; 3 failures go to the DLQ with an alarm |
| NFR-05 | Security | No secret in the repo; no `*` in IAM actions or resources; data encrypted at rest and in transit |
| NFR-06 | Privacy | Logs and eval set contain no PII; originals deleted on export, unfinished ones after 7 days; no data leaves Australia when using the `au.` profile |
| NFR-07 | Testing | Python coverage 90% or more, frontend 80% or more; CI blocks merge on red |
| NFR-08 | Accessibility | The review screen is fully usable with a keyboard |

## Out of scope for the MVP

Accounting-software integration, payments, mobile app, OCR for handwriting, multi-currency
conversion.
