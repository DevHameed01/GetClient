# GetClient: Product Requirements Document

**Product:** GetClient, AI powered lead generation and outbound prospecting SaaS **Document type:** Product Requirements Document (PRD) **Version:** 1.0 **Status:** Initial product specification **Product model:** Multi tenant SaaS **Primary interaction model:** Human in the loop AI automation

## 1. Product Overview

### 1.1 Introduction

GetClient is an AI powered prospecting and client acquisition platform. It helps businesses, freelancers, agencies and sales professionals discover potential customers, qualify leads, research businesses and generate highly personalised cold outreach messages.

Traditional cold outreach demands heavy manual effort. A salesperson or business owner must identify prospects, investigate their businesses, understand their needs, find relevant contact channels, develop a suitable pitch and manage communication. This becomes unmanageable across hundreds or thousands of prospects.

GetClient uses AI assisted research, lead qualification, business intelligence and contextual message generation to turn prospecting into an organised, efficient workflow. It does not blindly automate outreach. The AI researches, identifies opportunities and prepares messages. The user reviews, edits, approves or rejects them before anything is sent through a permitted channel.

**Core product proposition:** GetClient helps businesses find the right people to sell to, understand their businesses and approach them with relevant, personalised messages.

### 1.2 Product Vision

To become an intelligent client acquisition platform that reduces the time and complexity of finding, understanding and approaching potential customers, and to function as a central prospecting workspace where users manage their entire outbound acquisition process.

### 1.3 Product Mission

Help businesses spend less time searching for customers and more time building meaningful business relationships.

### 1.4 Problem Statement

Businesses struggle with five major problems:

1. Finding suitable potential customers.
2. Identifying which prospects are genuinely relevant.
3. Understanding a prospect's business before making contact.
4. Writing personalised outreach at scale.
5. Organising outreach activity and managing responses.

Existing approaches force users to combine several disconnected tools: lead databases, email automation and generic AI writers. GetClient brings these activities into one integrated workflow.

### 1.5 Proposed Solution

GetClient provides a unified system that:

- Discovers potential customers from permitted sources.
- Collects relevant business information.
- Filters and qualifies prospects.
- Researches individual businesses and their offerings.
- Identifies opportunities and service gaps.
- Generates context aware outreach messages.
- Provides an approval and editing interface.
- Supports permitted outreach channels.
- Tracks communication history and prospect outcomes.
- Provides analytics to evaluate acquisition performance.

## 2. Target Audience

GetClient serves individuals and organisations that depend on outbound prospecting to acquire customers.

### 2.1 Primary User Segments

| Segment | Description |
| --- | --- |
| A. Freelancers | Independent professionals seeking clients: graphic designers, video editors, motion designers, web developers, copywriters, consultants, digital marketers. |
| B. Creative and digital agencies | Agencies looking for businesses that may benefit from their services. |
| C. Small and medium sized businesses | Businesses seeking new customers, partnerships or commercial opportunities. |
| D. Sales professionals | Individuals responsible for identifying prospects and managing outbound pipelines. |
| E. Startup founders | Founders looking for customers, investors, partners or early adopters. |

### 2.2 User Personas

| Persona | Need |
| --- | --- |
| Independent Freelancer | Identify businesses that need their services and approach them without spending hours researching each company. |
| Agency Owner | A consistent stream of qualified opportunities, with prospect research and message preparation delegated to AI. |
| Sales Representative | Manage prospect lists, research leads, prepare personalised outreach and track outcomes. |
| Business Development Manager | A repeatable prospecting process that can be shared across a team. |

## 3. Product Objectives

### 3.1 Primary Objectives

1. Reduce the time required to discover potential customers.
2. Improve the relevance and quality of qualified leads.
3. Automate repetitive prospect research.
4. Generate genuinely personalised outreach messages.
5. Give users control over outbound communication.
6. Centralise prospect management.
7. Improve the organisation and consistency of outbound acquisition.

### 3.2 Secondary Objectives

1. Support multiple social and professional platforms.
2. Support different industries and business categories.
3. Allow multiple users to collaborate.
4. Provide performance analytics.
5. Eventually support AI assisted follow up and conversation management.

## 4. Core Product Modules

### 4.1 User Authentication and Account Management

Users must be able to create accounts, authenticate and manage their profiles.

**Functional requirements**

- User registration and email verification.
- Login, logout and password reset.
- Profile management and account settings.
- Subscription management.
- Organisation and workspace management.

**Multi tenant architecture.** GetClient must support multiple independent users and organisations. Each organisation has its own business profile, service catalogue, Ideal Customer Profile (ICP), prospect database, outreach campaigns, message templates, communication history, team members, and subscription and usage limits. Data belonging to one organisation must never be accessible to another without explicit authorisation.

### 4.2 Business Profile Configuration

Before using the prospecting engine, users configure their business so GetClient understands what they sell and who they want to sell to.

**Required information:** business name, description, industry, website, location, products and services, target market, unique selling proposition, and preferred communication style.

**AI business understanding.** The AI analyses the submitted information and builds an internal business profile containing:

- Business positioning.
- Main offerings.
- Target audience.
- Core value proposition.
- Customer problems the business solves.
- Differentiating factors.

Users can review and edit this profile.

### 4.3 Ideal Customer Profile (ICP) Builder

The ICP Builder lets users describe the businesses or individuals they want to approach.

**Configuration parameters:** industry, business category, geographic location, company size, estimated business maturity, target audience, business characteristics, required services or technologies, preferred prospect type, and exclusion criteria.

**Example.** Industry: Hospitality. Location: United Kingdom. Business type: independent hotels. Company size: small to medium. Service offered: website development and digital marketing. Preferred prospects: businesses with outdated websites and weak online presentation.

GetClient uses these parameters to guide discovery and qualification. Users can save multiple ICP configurations.

### 4.4 Lead Discovery Engine

The Lead Discovery Engine identifies potential customers based on the user's ICP. It is one of GetClient's most important modules.

**Supported discovery sources** (subject to access permissions):

- Search engine results.
- Public business websites.
- Authorised business directories.
- Licensed business data providers.
- Instagram official APIs and separately licensed providers approved for that use.
- X (Twitter) official APIs and separately licensed providers approved for that use.
- LinkedIn official APIs and separately licensed providers approved for that use.
- User submitted prospect lists and uploaded CSV files.
- Other approved data providers.

Instagram, X, and LinkedIn are separate discovery and enrichment sources. Each source has its own integration, access approval, search capabilities, data fields, permissions, quotas, rate limits, retention rules, and terms. A platform's availability as an outreach channel does not imply that it supports prospect discovery or enrichment.

**Discoverable record types:** users must eventually be able to search for and discover both companies and founders where a platform's official API or a contractually licensed provider permits the requested search. Companies and founders are distinct records. A founder may be related to one or more companies through explicit, attributable company-founder relationships; discovery of a profile must not by itself be treated as proof that the person founded or currently leads a company.

**Discovery parameters:** target record type (company, founder, or both), industry, location, business category, company size where available, keywords, relevant public activity, and source-specific criteria supported by the selected provider. The interface must distinguish criteria a provider supports from filters GetClient cannot apply at source.

**The system must:**

1. Accept discovery parameters and a requested record type.
2. Search only sources enabled for the organisation and permitted for the specific use.
3. Identify relevant companies and/or founders without conflating the two entity types.
4. Collect only fields the source permits GetClient to access, display, and retain.
5. Extract contact information only when the source licence and applicable law permit it.
6. Preserve source, source record/profile URL or identifier, and retrieval timestamp for each returned or enriched field.
7. Detect duplicates separately for companies, founders, and source-specific profiles; represent uncertain matches for review rather than silently merging identities.
8. Link companies and founders only with attributable relationship evidence and a retrieval timestamp.
9. Enforce source-specific rate limits, quotas, retention/deletion periods, and restrictions on export, reuse, and downstream display.
10. Return results with their entity type, source, freshness, and any material limitations.

**Company and founder information**

Company and founder are separate canonical entities. Company records hold business attributes; founder records hold person attributes. Company-founder relationship records link them and retain the relationship type/title, source evidence, and observation time. Prospect pipeline status may reference either entity or a company-founder relationship, without duplicating or merging their canonical records.

Social profiles and observations must be represented independently of these canonical entities. A social profile identifies a source-platform account and the entity it is associated with, if known. Each social-derived field or activity observation must retain, at minimum, its platform/source, provider or API where applicable, source profile/item URL or stable source identifier where permitted, retrieval timestamp, and applicable retention/expiry rule. Keep provenance per field, not only once on the parent company or founder. Store raw provider payloads only when explicitly permitted and necessary; otherwise retain only permitted normalized fields and provenance.

| Entity or field | Notes |
| --- | --- |
| Company | Canonical business record; includes name, website, description, industry, and location when verified and permitted |
| Founder | Separate person record; includes only permitted, relevant professional information |
| Company-founder relationship | Explicit link between a company and founder; includes relationship type, supporting source, and observation time |
| Social profile | Platform-specific profile URL/identifier associated with a company or founder, with match confidence and source provenance |
| Social field/activity observation | One permitted public business/profile field or relevant public activity item, with source and retrieval timestamp for that specific value |
| Prospect pipeline record | Workflow state referencing a company, founder, or relationship; not a substitute for either canonical entity |

Social profile links, public business information, and relevant activity may be used to enrich existing company and founder records only through supported, permitted access. Enrichment must add provenance and a retrieval timestamp per field and must not overwrite independently sourced values without preserving their provenance and history.

**Unsupported capabilities and provider dependencies:** general-purpose search across every Instagram account/post, unrestricted public-member or company search on LinkedIn, and unlimited/bulk X profile or post search must not be assumed. Platform APIs may not expose these capabilities, may restrict them to approved products or account types, or may limit results and retention. If native APIs do not support the required company/founder discovery or enrichment, evaluate a third-party licensed provider whose contract explicitly permits this SaaS use, the specific social-derived fields, customer-facing display, retention, and any export or outreach workflow. A third-party provider does not waive the originating platform's restrictions or applicable law.

**Initial discovery record fields**

| Field | Notes |
| --- | --- |
| Company ID / Founder ID | System generated; different entity types have separate identifiers |
| Company-founder relationship | Optional attributed relationship linking the separate records |
| Business/person attributes | Each attribute retains its own source and retrieval timestamp |
| Social profile links | Platform-specific profile references; retain only as permitted |
| Relevant social activity | Public, relevant activity only where the platform/provider permits access and storage |
| Discovery source and timestamp | Source-level job provenance; does not replace per-field provenance |
| Research status | Applies to the referenced record or relationship |
| Qualification status | Applies to the prospect pipeline record |

The system must distinguish verified information from inferred information. It must not fabricate contact information or claim to have verified information it has not checked.

### 4.5 Lead Qualification and Filtering Engine

Finding a business does not make it a good prospect. GetClient evaluates each discovered prospect against the user's ICP.

**Qualification criteria:** industry relevance, geographic relevance, business size, service compatibility, evidence of potential need, business activity, availability of relevant contact channels, and other user defined criteria.

**Lead scoring.** Each prospect receives a score from 0 to 100. The model is configurable. Suggested default:

| Criterion | Weight |
| --- | --: |
| Industry relevance | 25 |
| Service compatibility | 25 |
| Evidence of potential need | 20 |
| Geographic relevance | 10 |
| Business activity | 10 |
| Contactability | 10 |
| **Total** | **100** |

**Qualification categories**

| Score | Category |
| --- | --- |
| 80 to 100 | High priority |
| 60 to 79 | Potentially qualified |
| 40 to 59 | Needs further review |
| 0 to 39 | Low priority |

Scores are prioritisation estimates, not predictions of guaranteed conversion.

**Filtering.** Users can filter by qualification score, industry, location, business size, research status, contact availability, discovery source and qualification category. Users must be able to manually override AI qualification decisions.

### 4.6 Brand Intelligence and Business Research Engine

This module differentiates GetClient from ordinary lead generation tools. It understands the individual prospect before any outreach is generated. For every qualified prospect, the system researches available and permitted business information.

**Research sources:** official business websites, About pages, product and service pages, public business announcements, public case studies, publicly accessible social content where collection is permitted, and other authorised sources.

**Information to extract**

1. What does the business do?
2. What products or services does it offer?
3. Who does it serve?
4. How does it position itself?
5. What makes it different?
6. What is its brand identity?
7. What is its communication style?
8. What business challenges are visibly evidenced?
9. What opportunities might exist for the user's services?

**Opportunity identification.** The AI compares the prospect's public information against the user's service offerings.

*Example.* User's business: video production and motion design. Prospect: a solar energy company. Observed evidence: the company publishes product photographs, its website has technical product descriptions, and there is little explanatory product video. Potential opportunity: explanatory product videos and visual storytelling that make its products easier for customers to understand.

The system must distinguish between **verified observations**, **reasonable interpretations** and **unverified assumptions**, and must never present assumptions as established business problems.

**Research report.** Each prospect has a report containing business overview, products and services, target audience, brand positioning, relevant observations, potential service opportunities, supporting evidence, source URLs and research confidence. Users can inspect it before approving generated outreach.

### 4.7 AI Personalisation and Message Generation Engine

This is the primary content generation module. It creates individual outreach messages from actual prospect research and the user's business profile.

**Inputs**

1. User's business profile.
2. User's service catalogue.
3. Prospect's business profile.
4. Prospect research report.
5. Identified opportunities.
6. Selected communication platform.
7. Desired message tone.
8. User's outreach objective.
9. Message length preference.
10. Relevant communication history.

**The AI must:**

- Understand the prospect's business.
- Identify a relevant point of connection.
- Select an appropriate service offering and explain its relevance.
- Generate a natural opening.
- Avoid generic introductions, fabricated observations, exaggerated compliments and aggressive sales language.
- Respect platform specific message limits and adapt structure to the selected channel.

**Supported tones:** Professional, Conversational, Friendly, Direct, Consultative, Casual, and Custom.

**Generation modes**

| Mode | Purpose |
| --- | --- |
| 1. Initial outreach | Generates a first contact message. |
| 2. Opportunity based outreach | Focuses on an identified opportunity within the prospect's business. |
| 3. Service based outreach | Introduces a specific service relevant to the prospect. |
| 4. Partnership outreach | Establishes business relationships or collaborations. |

**Multiple drafts.** The system can optionally generate several variations, for example short and direct, conversational, and detailed and consultative. Users select their preferred draft.

**Message quality requirements.** Every message must be relevant to the individual prospect, use accurate information, avoid unsupported claims, have a clear objective, sound natural, avoid repetitive template language, and respect the selected platform's requirements.

**Personalisation evidence.** The interface must explain why a message was generated, shown beside the message. Example: "Personalisation reason: The prospect recently introduced a new product range and its website contains detailed technical specifications. The message focuses on improving product communication through explanatory video content."

### 4.8 Human Approval and Message Review Dashboard

No message is sent automatically by default. The user retains control over all outbound communication.

**Review actions:** Approve, Reject, Edit, Regenerate, Save as draft, Copy message, Open prospect profile, Review supporting research.

**Approval states:** Draft, Awaiting approval, Approved, Rejected, Scheduled, Sent, Failed, Replied, Archived.

**Editing.** Users can edit generated messages directly and the system preserves the edited version. On regeneration, the AI considers the user's corrections and feedback.

**Learning from corrections.** GetClient maintains a user specific preference profile. For example, if a user consistently removes phrases such as "I hope this message finds you well", the system learns to avoid them. It learns from explicit feedback and approved edits without silently changing critical business facts or overriding user instructions.

### 4.9 Outreach Management and Platform Integrations

**Initial target communication platforms:** Instagram, X, LinkedIn and Email. These are outreach targets; their inclusion here does not grant discovery or enrichment access. Discovery/enrichment integrations for Instagram, X, and LinkedIn are separate source adapters governed by the lead discovery requirements above.

Each platform has an independent integration module handling authentication, authorisation, account connections, available API operations, message formatting, sending permissions, delivery status, error handling and rate limits.

**Platform restrictions.** GetClient must not depend on unauthorised scraping, browser automation or prohibited messaging automation. Each integration uses official APIs, authorised providers or explicitly permitted workflows.

Social discovery and enrichment must not be implemented through scraping, browser automation, session-cookie reuse, or circumvention of API access controls. Platform-specific API permissions, approved product eligibility, scopes, commercial licensing, rate limits, retention, display, export, and deletion requirements must be reviewed before enabling each capability and revalidated when platform terms or APIs change. No capability is considered supported merely because a profile or post is publicly viewable in a browser.

Where automated sending is not permitted, GetClient provides a human assisted workflow:

1. Open the prospect's profile or communication channel.
2. Display the approved message.
3. Let the user copy it.
4. Let the user send it manually.
5. Record the outreach activity.

**Platform specific approach**

| Platform | Approach |
| --- | --- |
| Instagram | Use separately permissioned official API capabilities or a licensed provider for discovery/enrichment only when the applicable terms allow it. Do not assume arbitrary account or founder search is available. Support human assisted DM preparation where sending APIs are unavailable. |
| X | Use authorised API capabilities for separately scoped search/enrichment and sending. Search access, fields, quotas, and retention depend on the granted tier and terms. Automated unsolicited bulk DMs must not be supported. |
| LinkedIn | Use only approved APIs/products or providers with explicit rights for the intended search, enrichment, and display. Broad member/company search is not assumed to be available. No unauthorised profile scraping or automated messaging. |
| Email | Support authorised email integrations, subject generation, sending permissions and unsubscribe management. Must support applicable consent, privacy and anti spam requirements. |

**Sending controls.** The platform must provide explicit user approval, sending limits, duplicate contact prevention, suppression lists, unsubscribe and opt out handling, delivery tracking where supported, error reporting and audit logs. No automated sending occurs without user authorisation and platform permission.

### 4.10 CRM and Prospect Management

GetClient includes an internal prospect management system so users do not need another CRM to understand their outreach.

**Prospect pipeline stages**

1. Discovered
2. Qualified
3. Researched
4. Message generated
5. Awaiting approval
6. Approved
7. Contacted
8. Responded
9. Interested
10. Negotiation
11. Converted
12. Not interested
13. Archived

Users can move prospects between stages manually.

**Prospect history.** Each prospect has a chronological timeline of discovery events, research updates, generated messages, message edits, approval decisions, outreach attempts, replies, follow up activities, notes and status changes.

**Search and organisation.** Users can search and filter prospects, create custom lists, add tags and notes, export permitted data, archive prospects and identify duplicates.

### 4.11 Follow up Management

The platform eventually helps users manage conversations after initial outreach.

**Initial capabilities:** follow up reminders, follow up message generation, communication history, suggested next actions and follow up status.

**AI follow up intelligence.** The AI considers previous communication before suggesting a follow up. It must not generate repetitive messages or contact anyone who has opted out. Automated follow up sending remains subject to user approval and channel permissions.

### 4.12 Analytics and Reporting

Users have a dashboard showing prospecting performance.

**Core metrics:** total prospects discovered, qualified prospects, research completion rate, messages generated, approved and sent, delivery rate where available, response rate, positive response rate, meetings booked, converted prospects, and conversion rate.

**Campaign analytics.** Users can evaluate which ICPs produce the best leads, which industries respond most, which message styles and channels perform best, and which services attract the most interest.

Metrics must be calculated from actual recorded activity, never assumed delivery or response events.

## 5. Core User Workflow

| Step | Stage | Description |
| --- | --- | --- |
| 1 | Account creation | The user creates a GetClient account. |
| 2 | Business configuration | The user provides information about their business, products and services. |
| 3 | ICP configuration | The user defines the businesses or individuals to target. |
| 4 | Prospect discovery | The user selects company, founder, or both and starts a campaign. GetClient searches only the selected, permitted sources and reports source limitations. |
| 5 | Social enrichment | Where permitted, separate Instagram, X, and LinkedIn adapters add profile links, public business information, and relevant activity to company/founder records with field-level source and retrieval timestamps. |
| 6 | Lead qualification | The AI evaluates and ranks discovered prospects. The user reviews them. |
| 7 | Business research | GetClient investigates selected prospects and generates research reports. |
| 8 | Message generation | The AI prepares personalised outreach messages. |
| 9 | Human review | The user reviews research and messages, then approves, edits, regenerates or rejects. |
| 10 | Outreach | The user sends approved messages through permitted integrations or human assisted workflows. |
| 11 | Tracking | GetClient records outreach activity and updates prospect statuses. |
| 12 | Follow up and conversion | The user manages responses, follow ups and conversions from the prospect dashboard. |

## 6. Functional Requirements Summary

| Module | Priority | MVP |
| --- | --- | --- |
| Authentication | Critical | Yes |
| Business profile | Critical | Yes |
| ICP builder | Critical | Yes |
| Lead discovery | Critical | Yes |
| Social company discovery (Instagram, X, LinkedIn) | Medium | Later; gated by official API access or explicit provider licensing |
| Social founder discovery (Instagram, X, LinkedIn) | Medium | Later; gated by official API access or explicit provider licensing |
| Social enrichment with field-level provenance | Medium | Later; gated by source permissions and retention terms |
| Lead qualification | Critical | Yes |
| Business research | Critical | Yes |
| Message generation | Critical | Yes |
| Approval dashboard | Critical | Yes |
| Prospect CRM | High | Yes |
| Email integration | High | Limited |
| Instagram integration | Medium | Separate discovery/enrichment and outreach capabilities; API access and fields subject to platform permission |
| X integration | Medium | Separate discovery/enrichment and outreach capabilities; API access and fields subject to platform permission |
| LinkedIn integration | Medium | Separate discovery/enrichment and outreach capabilities; API access and fields subject to platform permission |
| Follow up intelligence | Medium | Basic |
| Analytics | Medium | Basic |
| Team collaboration | Low | Later |
| Advanced AI learning | Low | Later |

## 7. MVP Scope

The first release proves the central proposition: GetClient can find relevant businesses, qualify them, understand their context and generate personalised outreach that users find valuable.

**The MVP includes:**

1. User authentication.
2. Business profile configuration.
3. ICP builder.
4. Lead discovery through at least one permitted source.
5. Prospect data collection.
6. Duplicate detection.
7. AI lead qualification.
8. Business research.
9. Opportunity identification.
10. Personalised message generation.
11. Human approval dashboard.
12. Prospect management.
13. Manual outreach handoff.
14. Basic analytics.

**MVP exclusions** (must not delay the first release):

- Fully autonomous multi platform messaging.
- Advanced sales forecasting.
- Complex team permissions.
- Enterprise CRM integrations.
- AI voice calling.
- Fully autonomous negotiation.
- Advanced predictive lead scoring.
- Extensive custom workflow builders.
- Native mobile applications.

## 8. Technical Architecture

### 8.1 Recommended Technology Stack

The initial architecture prioritises modularity, maintainability and reasonable infrastructure cost.

| Layer | Technology |
| --- | --- |
| Frontend | React, TypeScript, Tailwind CSS, React Router, TanStack Query |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy |
| Database | PostgreSQL |
| Background processing | Redis, Celery or an equivalent job system |
| AI layer | Model agnostic service connecting to OpenAI compatible APIs, other hosted LLM providers, and local models through Ollama where appropriate. Must not be tightly coupled to one provider. |
| Research and data collection | Search APIs, authorised data providers, website content extraction from permitted sources, official platform APIs |
| Infrastructure | Docker, cloud hosted backend, managed PostgreSQL, object storage where required, centralised application logging |

### 8.2 Backend Module Structure

A proposed starting structure, not a requirement to implement every module immediately.

```
getclient/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   ├── auth.py, users.py, businesses.py, icp.py
│   │   │   ├── prospects.py, discovery.py, research.py
│   │   │   └── messages.py, outreach.py, analytics.py
│   │   ├── core/
│   │   │   ├── security.py, permissions.py, tenant_context.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── discovery/, qualification/, intelligence/
│   │   │   └── personalisation/, outreach/
│   │   ├── integrations/
│   │   │   ├── discovery/social/instagram/, discovery/social/x/, discovery/social/linkedin/
│   │   │   ├── discovery/licensed_providers/
│   │   │   └── outreach/email/, outreach/instagram/, outreach/linkedin/, outreach/x/
│   │   ├── workers/
│   │   └── database/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/, pages/, layouts/, hooks/
│   │   └── services/, context/, types/
│   └── package.json
├── infrastructure/
├── documentation/
├── docker-compose.yml
└── README.md
```

### 8.3 Architectural Principles

1. Modular backend services.
2. Separation of AI logic from business logic.
3. Multi tenant data isolation.
4. Independent platform integrations.
5. Asynchronous processing for long running research tasks.
6. Model provider independence.
7. Centralised error handling.
8. Auditable user actions.
9. Secure credential management.
10. API first architecture.
11. Treat social discovery, social enrichment, and outreach as separate permissioned capabilities, even when they use the same platform.
12. Keep provider adapters isolated so each source's access rules, field mapping, rate limits, and retention controls are enforced independently.

## 9. Database Requirements

The initial database supports the following entities. All organisation owned records must carry tenant ownership references. Credentials and external access tokens must be stored securely and never exposed to the frontend.

| Entity | Purpose |
| --- | --- |
| Users | Individual accounts |
| Organisations | Tenant workspaces |
| Memberships | User to organisation relationships |
| BusinessProfiles | User business information |
| Services | Products and services offered |
| ICPs | Target customer configurations |
| Campaigns | Prospect discovery campaigns |
| Companies | Canonical business identities and business attributes |
| Founders | Canonical person identities for founders, separate from companies |
| CompanyFounderRelationships | Attributed links between companies and founders, including relationship type and observation time |
| Prospects | Pipeline records referencing a company, founder, or company-founder relationship |
| SocialProfiles | Platform-specific profile identities associated with a company or founder |
| SocialDataObservations | Field-level social attributes and activity with source/provider, source reference, retrieval timestamp, and retention/expiry metadata |
| DiscoveryRuns | Search requests, selected sources, criteria, status, quota use, and timing for auditability |
| LeadScores | Qualification results for prospect pipeline records |
| ResearchReports | Business intelligence reports |
| EvidenceSources | Supporting research sources and field-level provenance references |
| MessageDrafts | Generated outreach messages |
| MessageVersions | Draft revision history |
| Approvals | Human approval records |
| ConnectedAccounts | Authorised external connections |
| OutreachActivities | Communication activity |
| Conversations | Prospect communication history |
| Tasks | Follow ups and reminders |
| SuppressionRecords | Opt outs and do not contact records |
| Subscriptions | Billing and plan information |
| UsageRecords | Resource and quota consumption |

## 10. AI System Design

GetClient uses specialised AI workflows rather than one large prompt performing every task.

### 10.1 AI Components

| Component | Responsibility |
| --- | --- |
| Business Understanding AI | Interprets the user's business profile, services and target customers. |
| Discovery Assistant | Helps construct search queries and discovery parameters. |
| Qualification AI | Evaluates prospect relevance against the ICP. |
| Research AI | Analyses collected business information. |
| Opportunity Detection AI | Identifies opportunities based on available evidence. |
| Personalisation AI | Creates individual outreach messages. |
| Message Review AI | Checks messages for relevance, accuracy, tone and unsupported claims. |
| Follow up Assistant | Determines appropriate follow ups and next actions. |

### 10.2 AI Execution Principles

- Use structured outputs wherever possible and validate model generated data.
- Store research evidence separately from AI conclusions.
- Preserve user corrections.
- Avoid unnecessary repeated model calls and cache reusable research.
- Track AI usage and costs.
- Allow model replacement without rewriting the application.

### 10.3 Human in the Loop Requirement

The system must distinguish AI generated recommendations from user approved actions. AI research is not user approval. Message generation is not permission to send. A user must explicitly approve outbound actions, and the platform must independently enforce the relevant integration permissions.

## 11. Security, Privacy and Compliance

GetClient processes business information, contact information and communication records. Security and compliance are foundational requirements.

**Data security:** secure authentication, role based access control, tenant isolation, encrypted connections, secure credential storage, audit logging, rate limiting, input validation, protection against injection attacks, and secure backup procedures.

**Data privacy:** privacy policy, clear data collection disclosures, user data export, account deletion, data retention controls, contact data deletion, and suppression and opt out management.

**Data collection.** GetClient only collects information through permitted means and must respect applicable privacy laws, platform terms of service, API usage requirements, data provider licensing restrictions and anti spam legislation. Users must be able to identify the source of prospect information and its collection date. For social-derived fields and activity, record provenance and retrieval timestamp per field, apply source-specific expiry/deletion rules, and avoid retaining raw payloads unless expressly allowed. A publicly visible profile or post is not, by itself, permission to collect, retain, enrich, or use it for outreach.

**Social platform governance.** Instagram, X, and LinkedIn are independent sources and require separate approvals and provider configurations. At implementation time, verify the current official API's permitted search subject, query types, supported profile/business fields, approved account/product eligibility, commercial use, rate limits, display rules, retention/deletion, and export rights. If official APIs do not support the desired company or founder discovery, mark that capability unavailable or procure a provider license that expressly permits the exact use; third-party access must not be used to circumvent a platform's restrictions.

**AI safety and reliability**

- No fabricated business facts.
- No fabricated contact details.
- No false claims about prospect activity.
- Clear distinction between observation and inference.
- Research source traceability.
- Human approval before outbound communication.

## 12. User Interface Requirements

The interface is clean, modern and professional. As a productivity oriented SaaS product, it prioritises information clarity, efficiency and ease of navigation.

**Main dashboard** displays prospecting activity, qualified leads, messages awaiting approval, recent outreach, follow up tasks and acquisition statistics.

**Main navigation:** Dashboard, Find Leads, Prospects, Campaigns, Message Review, Outreach, Analytics, Integrations, Settings.

**Social discovery and enrichment interface.** Users can eventually choose Instagram, X, and LinkedIn independently as discovery or enrichment sources, select companies, founders, or both, and understand which filters are actually supported by each source. Results and enriched fields must show their source and retrieval time. Unsupported or unavailable searches must be clearly disclosed; the interface must not imply that a platform was searched when it was not.

**Prospect detail page** contains business information, contact information, qualification score, research report, identified opportunities, generated messages, communication history, notes and prospect status.

**Message review interface.** This should be one of the most polished parts of GetClient. The user sees the prospect's business information and research alongside the generated message. Editing is immediate and straightforward, and the user never navigates through several pages just to approve a message.

## 13. Non Functional Requirements

| Area | Requirements |
| --- | --- |
| Performance | Normal dashboard requests complete within two seconds under typical MVP load. Long running discovery and research run asynchronously. Users see visible progress updates. Failed background jobs are recoverable where safe. |
| Scalability | Support multiple organisations and growing prospect databases. Allow independent scaling of background workers. Support multiple AI providers and additional discovery and communication integrations. |
| Reliability | Persistent job status, retry handling, duplicate prevention, database transaction integrity, integration failure reporting and audit trails. |
| Maintainability | Modular codebase, documented APIs, automated tests, database migrations, environment based configuration and consistent coding standards. |

## 14. Subscription and Monetisation Model

GetClient operates as a subscription based SaaS platform. The structure below is proposed for validation, not final pricing.

| Plan | Audience | Includes |
| --- | --- | --- |
| Free | Individuals exploring the platform | Limited discovery, AI research and message generation. One workspace. Basic prospect management. |
| Starter | Freelancers and independent professionals | Higher discovery allowance, more AI research, more personalised messages, basic analytics, limited integrations. |
| Professional | Agencies and growing businesses | Higher usage allowances, multiple ICP configurations, advanced lead qualification, more research capacity, campaign management, advanced analytics. |
| Business | Teams | Multiple team members, shared prospect databases, team permissions, collaborative workflows, higher allowances, advanced reporting. |

**Pricing considerations:** AI model consumption, search API costs, third party data costs, infrastructure, storage, email integration costs and customer support. Usage limits should be based on measurable resource consumption rather than arbitrary restrictions.

## 15. Product Success Metrics

| Category | Metrics |
| --- | --- |
| Acquisition | Prospects discovered, percentage qualified, cost per qualified prospect, discovery success rate |
| AI quality | Research accuracy, research completion rate, message approval rate, message edit frequency, message regeneration frequency, user satisfaction with personalisation |
| Outreach | Messages approved, messages successfully sent, response rate, positive response rate, meeting conversion rate, customer acquisition conversion rate |
| Product | Daily and monthly active users, retention, free to paid conversion, subscription churn, average AI cost per user, average cost per qualified lead |

The initial product prioritises research quality, qualification relevance and message approval rates over raw message volume.

## 16. Development Roadmap

| Phase | Scope | Deliverable |
| --- | --- | --- |
| 1. Product foundation | Repository setup, backend and frontend configuration, database setup, authentication, multi tenant foundation, business profile management | Functional application foundation |
| 2. Prospecting engine | ICP builder, discovery source integration, separate company/founder records and relationships, lead collection, prospect database, duplicate detection, lead qualification, filtering; later social discovery/enrichment only where licensed and supported | Users can discover and qualify companies and founders using permitted sources |
| 3. Business intelligence | Website research, business information extraction, research reports, evidence collection, opportunity identification | GetClient understands individual prospect businesses |
| 4. Personalisation engine | AI orchestration, prompt architecture, message generation, tone configuration, multiple drafts, personalisation evidence, message quality checks | Users can generate individualised outreach messages |
| 5. Approval and CRM | Message review dashboard, editing, approval workflow, prospect pipeline, communication history, notes and tags | Users can manage prospects and approve outreach |
| 6. Integrations and outreach | Email integration, permitted platform integrations, human assisted outreach, sending controls, activity tracking, follow up management | Users can execute and track permitted outreach |
| 7. Analytics and monetisation | Performance dashboard, usage tracking, subscription management, billing integration, plan restrictions, operational monitoring | Initial commercially deployable SaaS product |

## 17. Risks and Mitigation

| Risk | Mitigation |
| --- | --- |
| Platform API restrictions | Separate source adapters, capability checks, and permitted fallback workflows; no scraping or access-control circumvention |
| Social data licensing and retention | Per-field provenance, retrieval timestamps, expiry/deletion controls, and provider-specific contracts |
| Unsupported social search | Clearly disclose platform search gaps; evaluate licensed providers with explicit customer-facing rights |
| Inaccurate AI research | Evidence backed research and confidence indicators |
| Generic messages | Prospect specific research and personalisation validation |
| High AI costs | Caching, model selection and usage controls |
| Duplicate prospects | Deduplication and identity matching |
| Poor quality lead sources | Source evaluation and configurable discovery providers |
| Privacy violations | Data governance and compliant collection |
| Spam like outreach | Human approval, sending controls and suppression lists |
| Multi tenant data leakage | Strict tenant isolation and automated security testing |
| Integration failures | Background job monitoring, retries and error reporting |

## 18. Acceptance Criteria

The MVP is not complete until the following conditions are met.

**User management**

- Users can register and authenticate.
- Users can configure their businesses.
- Organisations are isolated from one another.

**Lead discovery**

- Users can create an ICP and initiate discovery.
- The system collects prospects from at least one permitted source.
- Prospects are stored with source information.
- Duplicate prospects are detected.

**Lead qualification**

- Prospects receive qualification scores.
- Users can inspect qualification reasoning.
- Users can manually change qualification decisions.

**Business intelligence**

- The system can research a prospect's business.
- Reports contain source references.
- Observations and inferences are distinguished.
- Users can inspect research before generating outreach.

**Personalisation**

- The system generates prospect specific messages.
- Messages use the user's business profile and are based on prospect research.
- Users can edit and regenerate drafts.
- The system does not invent research findings.

**Approval**

- Messages cannot be sent without the required approval.
- Users can approve, reject and edit messages.
- Approval actions are recorded.

**Prospect management**

- Users can search and filter prospects and track status.
- Communication activities are recorded.
- Suppression records are enforced.

**Reliability**

- Long running jobs execute asynchronously.
- Errors are visible to users.
- Background jobs recover from appropriate failures.
- Sensitive credentials are not exposed to the frontend.

Social discovery requirements below are release gates for any future Instagram, X, or LinkedIn integration; they do not imply that these integrations exist or block the initial MVP:

- Each platform is an independently permissioned discovery/enrichment source; unsupported capabilities are disclosed rather than simulated.
- Every social-derived field and activity observation retains its source and retrieval timestamp and complies with the source-specific retention/deletion policy.
- Company and founder records remain separate and are connected only through attributed company-founder relationships.

## 19. Future Product Opportunities

Outside the initial MVP, these could significantly expand GetClient.

| Opportunity | Description |
| --- | --- |
| A. AI Sales Assistant | Helps users interpret prospect responses, recommend next actions and prepare replies. |
| B. Automated Lead Monitoring | Monitors permitted sources for new businesses matching a user's ICP. |
| C. Website Based Prospect Analysis | Analyses a prospect's website and identifies improvement opportunities. |
| D. AI Proposal Generator | Generates tailored proposals from the prospect's business, needs and past conversations. |
| E. Advanced Conversation Intelligence | Analyses permitted conversation history for buying signals and objections. |
| F. Team Collaboration | Lets multiple team members research, review and manage prospects. |
| G. Advanced CRM Integrations | Connects with external CRM platforms. |
| H. AI Campaign Optimisation | Analyses outreach performance and recommends improvements to ICPs, messaging and targeting. |

## 20. Final Product Definition

GetClient is an AI powered client acquisition platform that combines prospect discovery, lead qualification, business intelligence, personalised outreach generation and prospect management in one SaaS environment.

Its core differentiator is not finding contact information or generating messages. It is understanding the relationship between:

1. What a business offers.
2. Who that business wants to reach.
3. Which prospects are relevant.
4. What those prospects actually do.
5. What opportunities exist between the two businesses.
6. How to communicate those opportunities effectively.

The platform operates as an intelligent prospecting assistant while keeping users in control of their commercial relationships.

**Product philosophy:** Find better prospects. Understand their businesses. Approach them with relevance. Build better client relationships.

**GetClient: Find the right clients. Start better conversations.**
