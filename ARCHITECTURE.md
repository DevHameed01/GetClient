# GetClient Architecture

## Status and scope

This document records the current foundation and the proposed architecture for company and founder discovery. The social discovery and enrichment capabilities below are requirements, not implemented features. No social platform API, scraping workflow, or discovery result is currently part of the application.

The product requirements are in [GetClient Product Requirements Document](./GetClient%20Product%20Requirements%20Document.md).

## Current implementation

The repository currently has a React/TypeScript/Vite frontend and a Python/FastAPI backend. The backend persists users, organizations, memberships, authentication sessions, business profiles, and services. Existing API routes cover health, authentication, workspace management, and business-profile reads/updates. There are no company, founder, social-profile, discovery-run, or social-observation models or API integrations.

## Target discovery architecture

### Independent source adapters

Discovery, enrichment, and outreach are separate capabilities. Instagram, X, and LinkedIn each require independent adapters and configuration; authorization to use one platform for messaging does not authorize its data for search or enrichment.

Proposed integration boundaries:

```text
backend/app/
  api/
    discovery.py
    companies.py
    founders.py
  models/
    company.py
    founder.py
    company_founder_relationship.py
    social_profile.py
    social_data_observation.py
    discovery_run.py
  services/
    discovery/
      orchestration.py
      source_capabilities.py
      matching.py
      provenance.py
      retention.py
  integrations/
    discovery/
      social/
        instagram/
        x/
        linkedin/
      licensed_providers/
```

This is a proposed module layout, not a requirement to create every file at once. Each adapter should declare its supported record types, query filters, fields, access requirements, request limits, retention rules, and permitted downstream uses. The discovery orchestrator should report unavailable filters or sources rather than silently pretending to search them.

Long-running discovery and enrichment should use the existing planned background-job direction. Jobs need tenant scope, source and capability selection, status, timestamps, quota usage, and auditable errors. Provider credentials belong on the backend, must be protected as secrets, and must never be exposed to the browser.

### Separate entities and relationships

- **Company** is a canonical business identity and holds company attributes.
- **Founder** is a separate canonical person identity and holds only relevant, permitted professional attributes.
- **Company-founder relationship** is an independently stored, attributable link with relationship type/title, source evidence, observed/retrieved time, and any validity period. A name match or social-profile association alone is not proof of a founder relationship.
- **Prospect/pipeline record** references a company, founder, or relationship; it does not merge those entities.
- **Social profile** represents a platform-specific account associated with a company or founder, including a match status/confidence and source identity.

Use tenant ownership and authorization checks for tenant-managed records. If shared/global identity resolution is later introduced, it must be designed explicitly with access controls and source-license rules; do not make discovered data globally visible by default.

### Field-level provenance

Represent social-sourced values and activity as source-attributed observations rather than untraceable overwrites. For every social-derived field, store at minimum:

- Subject entity and field name.
- Value or normalized value, only if retention is permitted.
- Platform and provider/API source.
- Source profile/item URL or stable identifier, where permitted.
- Retrieval timestamp.
- Evidence type and verification/match status.
- Applicable license/policy identifier, retention deadline, and deletion state where needed.

A company or founder may have multiple observations of the same field from different sources or times. Preserve history and provenance when selecting a current value. Discovery-run timestamps alone do not satisfy the per-field provenance requirement. Do not retain raw responses by default; store them only where the provider explicitly allows it and a documented need exists.

Retention enforcement must be source-aware and automatic: expire or delete data when the provider's policy or contract requires it, including derived/indexed copies and queued exports where applicable. Users should be able to see source and freshness in the product. Audit events must record discovery/enrichment access without logging credentials or unnecessary personal data.

## Social source capabilities and unsupported searches

The following are design constraints; actual scopes, product eligibility, fields, terms, and limits must be checked against current official documentation and the applicable account agreement before implementation.

| Source | Intended capability, if authorized | Do not assume |
| --- | --- | --- |
| Instagram | Search or enrich eligible business/professional profiles and relevant public business information/activity only where the granted official API or licensed provider expressly supports it. | General search over arbitrary Instagram accounts, posts, or founders; access to personal accounts; permission to retain or reuse content for lead lists. |
| X (Twitter) | Search/enrich profiles or public activity only through API products and endpoints available under the approved access tier and its terms. | Unlimited, bulk, historical, or unrestricted search; stable access to profile/activity fields; indefinite retention or export rights. |
| LinkedIn | Search/enrich company or member information only through approved LinkedIn products, partner permissions, or a separately licensed provider with explicit rights. | General-purpose member or company search via a standard public API; scraping or browser automation as a fallback. |

Public visibility is not authorization. Do not scrape websites or social platforms, automate browsers, reuse user session cookies, bypass API controls, or use an intermediary to circumvent source restrictions. Do not promise platform coverage or search filters until they are verified for the production credentials and target markets.

Where official APIs do not expose the requested company/founder search or enrichment, mark the capability unsupported or assess a licensed provider. A provider contract must explicitly cover GetClient's customer-facing, multi-tenant SaaS use, the specific social-derived fields, storage and refresh, end-user display, export/deletion, and intended research/outreach uses. A downstream license does not override restrictions imposed by the originating platform or applicable privacy law. Record the provider as the immediate source and retain upstream provenance where available and contractually permitted.

## Source compliance and operational controls

Before enabling an adapter, document and review:

1. Approved API product, scopes, account eligibility, and permitted query/subject types.
2. Commercial-use and multi-tenant display rights.
3. Allowed fields and source attribution/display requirements.
4. Rate limits, quotas, pricing, and retry guidance.
5. Cache, retention, refresh, deletion, and export restrictions.
6. Privacy-law basis, notice, rights handling, and outreach restrictions.
7. Unsupported searches and a safe user-visible explanation.

Enforce limits centrally per provider credential and tenant as applicable; honor provider retry instructions and stop on authorization or policy errors. Keep discovery credentials and API keys in backend secret storage, restrict access, rotate them, and redact them from logs.

## API and frontend boundary

The frontend submits a tenant-scoped discovery request and renders only results and filters reported by the backend as available. It must not hold provider secrets or call providers directly. API results should identify entity type, source, field provenance, retrieval time, freshness/expiry, and partial or unsupported-source status. Empty or failed results must not be presented as evidence that no matching companies or founders exist.
