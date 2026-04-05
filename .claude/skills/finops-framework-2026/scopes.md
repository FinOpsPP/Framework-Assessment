# FinOps Scopes (Updated in 2026)

> Source: [finops.org/framework/scopes](https://www.finops.org/framework/scopes/)

---

## Definition

A FinOps Scope is "a defined segment of spending across technology categories, aligned to business constructs — such as product, cost center, or environment — that guide the application of FinOps to maximize technology value."

---

## Core Principles

### Decision-Focused Structure
Scopes establish decision context and shared reference points. They determine which personas engage, which capabilities apply, and which domains define success.

### Business-Driven, Not Technology-Driven
Scopes reflect decision contexts rather than infrastructure boundaries. Multiple products, cost centers, or environments may fall within a single scope when decisions cut across them. Conversely, distinct business objectives can create multiple scopes within one spending area.

### Customization Within Common Framework
Organizations tailor how capabilities (data ingestion, allocation, forecasting, etc.) apply across different scopes. While capability goals remain consistent, inputs, KPIs, maturity levels, and success measures vary by scope.

---

## Scope Governance

- Create scopes only when distinct business outcomes or decision contexts require them
- Keep scopes **few, simple, and purposeful** to avoid overhead
- Common capabilities, personas, and domains often apply across scopes with minimal variation
- New scopes should NOT be introduced simply because a topic interests practitioners
- Use the "Five Whys" technique to understand what business question drives the need

---

## Lifecycle

### Initiation
Scopes are initiated in response to specific business questions and leadership expectations — not generic analytical interests.

**Example progression (Five Whys):**
1. "What are we spending on AI?" →
2. Deeper investigation reveals: "We need visibility into infrastructure investments supporting key products driving market differentiation" →
3. Result: Scope addresses strategic need, not just spending visibility

### Evolution
As organizations mature, scopes evolve:
- Initially: default scopes aligned to cloud usage and adoption goals
- Maturing: targeted scopes within specific footprints defined by business context
- Advanced: scopes spanning multiple technology categories for cross-technology investment decisions

### Duration
Scopes "flex in duration and intensity to match the business objective being served."

### Conclusion
When scopes achieve their outcomes or become irrelevant, practices should adapt by adjusting or discontinuing them.

---

## Managing Scope Interactions

Technology usage may fall within multiple scopes simultaneously when different business outcomes apply. Practitioners must intentionally manage these overlaps — deciding whether to adjust scope boundaries or explicitly account for contributions to metrics like forecast variance.

---

## Relationship to Technology Categories

| | Scopes | Technology Categories |
|---|---|---|
| **Represents** | "Why" — business context | "What" — technical domain |
| **Driven by** | Business questions & objectives | Technology procurement models |
| **Examples** | Product line profitability, cost center optimization | Public Cloud, SaaS, AI |
| **Duration** | Flexible, tied to business need | Persistent categories |

Scopes can span multiple technology categories when business objectives require cross-technology investment decisions (e.g., an AI scope that touches Public Cloud, Data Center, and SaaS).

---

## Relationship to Framework Elements

Scopes determine engagement levels for:
- **Personas** — which roles participate based on accountability needs
- **Capabilities** — which FinOps practices apply and their priority
- **Domains** — how success is measured within each scope

Inclusion or exclusion of framework elements should reflect organizational maturity, business priorities, and innovation timelines.

---

## Example: Defining a FinOps Scope for AI

From the 2026 framework announcement:
- **Business strategy**: Market differentiation through AI-powered products
- **Technology strategy**: Multi-category investment (Public Cloud GPU instances, colocated data center for training, SaaS AI platforms)
- **Scope definition**: AI product infrastructure investment
- **Personas engaged**: Engineering leads, FinOps practitioners, product managers, executive sponsors
- **Key capabilities**: Usage Optimization, Architecting & Workload Placement, Executive Strategy Alignment, Forecasting
- **Cadence**: Monthly review with quarterly strategic alignment
- **Maturity target**: Walk (structured processes with regular reviews)
