# FinOps Technology Categories (NEW in 2026)

> Source: [finops.org/framework/technology-categories](https://www.finops.org/framework/technology-categories/)

Technology categories represent types of technology through which organizations consume and spend on IT resources. Each category has distinct procurement models, pricing structures, cost visibility characteristics, and operational dynamics.

**Categories = "what"** (the technical domain being managed)
**Scopes = "why"** (the business context driving FinOps application)

---

## 1. Public Cloud

> [finops.org/framework/finops-for-public-cloud](https://www.finops.org/framework/finops-for-public-cloud/)

Managing and optimizing cloud-based consumption in support of business outcomes such as cost efficiency, scalability, and delivery velocity.

- **Scope**: IaaS/PaaS services from hyperscalers (AWS, Azure, GCP)
- **Key considerations**: Multi-cloud complexity, commitment-based discounts, reserved instances, savings plans
- **Primary capabilities**: All domains apply; Rate Optimization and Usage Optimization are central
- **KPIs**: Effective savings rate, coverage %, unit cost trends
- **FOCUS alignment**: Native billing data mapped to FOCUS schema

---

## 2. SaaS (Software-as-a-Service)

> [finops.org/framework/finops-for-saas](https://www.finops.org/framework/finops-for-saas/)

Governing and optimizing managed software spending to support organizational value creation.

- **Scope**: Managed software services (Salesforce, ServiceNow, M365, etc.)
- **Key considerations**: License rationalization, utilization tracking, decentralized purchasing models, renewal management
- **Primary capabilities**: Licensing & SaaS, Allocation, KPI & Benchmarking
- **FOCUS alignment**: Vendor-provided or API-derived usage data

---

## 3. Data Center

> [finops.org/framework/finops-for-data-center](https://www.finops.org/framework/finops-for-data-center/)

Improving visibility and decision-making for on-premises infrastructure investments.

- **Scope**: On-premises servers, networking, storage, facilities
- **Key considerations**: Capacity planning, depreciation, power/cooling costs, refresh cycles
- **Primary capabilities**: Allocation, Planning & Estimating, Architecting & Workload Placement
- **Intersects with**: ITAM, Enterprise Architecture

---

## 4. Data Cloud Platforms

> [finops.org/framework/finops-for-data-cloud-platforms](https://www.finops.org/framework/finops-for-data-cloud-platforms/)

Governing and optimizing consumption-based data and analytics spend to support organizational value creation.

- **Scope**: Consumption-based platforms (Snowflake, Databricks, BigQuery, similar)
- **Key considerations**: Query cost optimization, warehouse sizing, pipeline efficiency, workload telemetry
- **Primary capabilities**: Usage Optimization, Reporting & Analytics, Unit Economics
- **FOCUS alignment**: Workload telemetry (queries, jobs, pipelines, platform metadata)

---

## 5. AI

> [finops.org/framework/finops-for-ai](https://www.finops.org/framework/finops-for-ai/)

Addressing the cost complexity, faster development cycle, spend unpredictability, and the need for a greater degree of policy and governance to support innovation.

- **Scope**: AI/ML workloads — training, inference, model serving, fine-tuning
- **Key considerations**: GPU cost management, training vs inference cost split, model selection economics, token-based pricing, rapid iteration cycles
- **Important**: AI spans ACROSS other technology categories — it is not siloed. AI workloads may touch Public Cloud, Data Center, Data Cloud Platforms, and SaaS simultaneously
- **Primary capabilities**: Usage Optimization, Architecting & Workload Placement, Governance/Policy/Risk, Executive Strategy Alignment
- **Unit economics examples**: Cost per token, cost per inference, cost per training run

---

## 6. Private Cloud

Private cloud infrastructure managed within or for the organization.

- **Scope**: Private cloud platforms (OpenStack, VMware private cloud, etc.)
- **Key considerations**: Capacity allocation, chargeback models, hybrid cloud integration

---

## 7. Licenses

Software licensing across the organization.

- **Scope**: Traditional software licenses, enterprise agreements, per-seat/per-core licensing
- **Key considerations**: License compliance, true-up costs, optimization of license tiers
- **Intersects with**: ITAM, SAM (Software Asset Management)

---

## Cross-Category Considerations

Each technology category page on finops.org addresses a consistent structure:
- **FinOps Scopes** — how scopes apply within the category
- **Relevant Capabilities** — which of the 22 capabilities are most applicable
- **Personas** — which roles are most involved
- **KPIs & Measures of Success** — category-specific metrics
- **FOCUS Alignment** — how billing/usage data maps to the FinOps Open Cost and Usage Specification

Organizations often manage multiple technology categories simultaneously. Scopes can span categories when business objectives require cross-technology investment decisions.
