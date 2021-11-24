# The Data Tools initiative
Navigating the space of data tools can be daunting. To combat this we need high quality, up-to-date and complete information.

The primary target audience for this list is data professionals trying to find the right tools to help them become more productive. Through this initiative we hope to contribute to a good overview. To limit the scope, only tools targeting a technical audience are welcome. That includes "low-code" tools, but "no-code" tools are not appropriate.

### Technology
The data is stored in the `tools.json` file in this repository which is consumed by a [NocoDB](https://github.com/nocodb/nocodb) instance running on https://alldatatools.com

## Collaboration
Please add your/your favorite **data** tool/product to the list! We want this list to be as inclusive as possible.

## Structure

### Entities
The entities should be either tools or products. The goal is to map all relevant tools a data practitioner might want to use. Both open source and proprietary products/tools are welcome. The goal is to be an exhaustive list.

In addition, the tool should be generally available already. Tools in private alpha/beta/waitlisted/sunsetted are not appropriate for this list.

### Licenses
Licenses should all use the SPDX license format. Find out more on the [LF SPDX licences page](https://spdx.org/licenses/).

### Images
For logos and screenshots please add a folder to the images root folder in lowercase without spaces (use dashes instead if necessary).

### Taxonomy
The current taxonomy is hierarchical (some categories are children of others) and non-exclusive. I.e. a tool can be in multiple categories at the same time.

The initial setup is mostly inspired by the [Firstmark MAD Landscape](https://mattturck.com/data2021/). We hope to evolve this taxonomy over time as understanding of the landscape develops and more consensus is built.

**Note: we encourage everyone to discuss this taxonomy through Pull Requests. Please recommend changes if you feel like it will improve the clarity of the overview of tools.**

- Infrastructure
  - Storage
  - Data lakes
  - Data warehouses
  - Streaming/in-memory
  - RDBMS
  - NoSQL databases
  - NewSQL databases
  - Real-time databases
  - Time series databases
  - Graph databases
  - MPP databases
  - GPU databases
  - Key-value databases
  - ETL / ELT / data transformation
  - Reverse ETL
  - Data integration
  - Data governance & access
  - Data management & prep
  - Privacy & security
  - Data observability
  - Data quality
  - Monitoring
  - Serverless
  - Containers
  - Clusters
  - Formats
  - Orchestration
  - Data versioning
  - Code versioning
  - CI/CD
  - Supply chain security
  - Package management
- Analytics
  - Web/mobile/commerce analytics
  - BI platforms
  - Visualization
  - Data analyst platforms
  - Augmented analytics
  - Data catalog & discovery
  - Metrics store
  - Log analytics
  - Query engine
  - Search
  - Statistical computing
- ML & AI
  - Data Science notebooks
  - Data Science platforms
  - ML platforms
  - Programming libraries/frameworks
  - Data generation & labeling
  - Model building
  - Metric tracking
  - Feature store
  - Deployment & production
  - Computer vision
  - Vector database
  - Speech
  - Drift detection
  - Explainability
  - NLP
  - Model versioning
  - Synthetic media
  - API services
  - GPU libraries


### Exclusions (up for debate)
- Data labeling services. Annotation tools (e.g. Prodigy) are included.
- Search engines (e.g. Elastic, Algolia, Meilisearch)
- Geospatial analysis tools (e.g. ArcGIS)
