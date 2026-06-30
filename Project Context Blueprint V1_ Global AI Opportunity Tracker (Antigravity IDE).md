### Project Context Blueprint: Global AI Opportunity Tracker (Antigravity IDE)

#### 1\. Project Mission and Scope

The "Global AI Opportunity Tracker" is a production-quality, modular backend designed to automate the lifecycle of AI-related professional opportunities. The core objective is to transform raw web data from fragmented sources into a structured, actionable data pipeline.**Target Platforms:**

* **Primary:**  Unstop, Hack2Skill, Devpost, Kaggle.  
* **Categories:**  Conferences, Workshops, Research Programs, and Scholarships.**Primary Functional Stages:**  
1. **Scraping:**  Targeted automated data extraction via Patchright.  
2. **Normalization:**  Standardizing raw data into unified internal formats.  
3. **Structuring via LLM:**  Utilizing Large Language Models (LLMs) to clean, categorize, and validate information.  
4. **Storage:**  Persistence into a structured database.  
5. **FastAPI Exposure:**  Providing high-performance RESTful access to the processed data.

#### 2\. Core Development Philosophy

We adhere to a rigorous architectural standard to ensure the system remains maintainable and focused.

* **Build infrastructure only until it is "good enough":**  We avoid speculative engineering. We implement the minimum stable infrastructure required to satisfy current requirements and let real-world constraints drive future iterations.  
* **Small Iterative Development:**  Every module must strictly follow the  **Design → Implement → Test → Refactor**  lifecycle.  
* **Composition over Inheritance:**  We prefer classes that own specific components over deep, complex inheritance chains. For example, the system utilizes a BrowserManager to manage lifecycle logic rather than inheriting browser capabilities into the scrapers.  
* **Single Responsibility Principle:**  Every class must answer exactly one question. The BrowserManager handles the lifecycle; it does not concern itself with cookies, stealth, or specific scraping logic.  
* **Type Safety:**  The project requires Python 3.13+, mandatory type hints, Pydantic models for all data structures, and Google-style docstrings.

#### 3\. Completed Development Phases (Phases 0–2)

The foundational infrastructure is established and considered immutable.

* x  **Phase 0: Research and Architecture**  (Technology selection, planning, and modular design).  
* x  **Phase 1: Foundation**  (Poetry setup, Logger, Configuration,  **Environment Variables** , Constants, and Project Structure).  
* x  **Phase 2: Browser Engine Core**  (Patchright integration and lifecycle management).**Current Browser Engine State:**  
* **BrowserManager:**  Solely responsible for the browser lifecycle (start, close, new page). It utilizes read-only properties for the browser and context to maintain encapsulation.  
* **BrowserFactory:**  A static utility responsible strictly for the instantiation of Patchright objects (start\_playwright, launch\_browser, create\_context).**Deferred Browser Layer Features:**  The following features are intentionally omitted and  **must not**  be implemented until a specific scraper requirement justifies the complexity:  
* Session management and storage state.  
* Proxy support and User-Agent management.  
* Screenshots and downloads.  
* Advanced stealth improvements and multiple contexts.

#### 4\. Technical Architecture and File Structure

We maintain a strict "Downward-only dependencies" rule: upper layers (Scrapers) depend on lower layers (Browser Engine), but lower layers must never have knowledge of upper layers.**Explicit Contracts:**  To maintain modular boundaries, we implement explicit contracts between layers (e.g., RawOpportunity from the Scraper vs. ParsedOpportunity for the LLM). This prevents tight coupling and ensures independent testability.  
global-ai-opportunity-tracker-backend/  
├── .env.example  
├── .gitignore  
├── LICENSE  
├── README.md  
├── poetry.lock  
├── pyproject.toml  
├── docs/  
├── examples/  
│   └── browser/  
│       └── basic\_browser.py  
├── scraper/  
│   ├── \_\_init\_\_.py  
│   ├── core/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── browser/  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── config.py  
│   │   │   ├── factory.py  
│   │   │   ├── manager.py  
│   │   │   ├── models.py  
│   │   │   ├── protocols.py  
│   │   │   ├── session.py  
│   │   │   └── stealth.py  
│   │   ├── exceptions/  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── browser.py  
│   │   ├── manager/  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── scraper\_manager.py  
│   │   └── scheduler/  
│   │       ├── \_\_init\_\_.py  
│   │       └── job\_scheduler.py  
│   ├── data/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── outputs/  
│   │   └── screenshots/  
│   ├── exporters/  
│   │   └── \_\_init\_\_.py  
│   ├── parsers/  
│   │   └── \_\_init\_\_.py  
│   └── scrapers/  
│       ├── \_\_init\_\_.py  
│       ├── base/  
│       │   ├── \_\_init\_\_.py  
│       │   └── base\_scraper.py  
│       ├── devpost/  
│       │   └── \_\_init\_\_.py  
│       ├── hack2skill/  
│       │   └── \_\_init\_\_.py  
│       ├── kaggle/  
│       │   └── \_\_init\_\_.py  
│       └── unstop/  
│           └── \_\_init\_\_.py  
├── shared/  
│   ├── \_\_init\_\_.py  
│   ├── config/  
│   │   ├── \_\_init\_\_.py  
│   │   └── settings.py  
│   ├── constants/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── browser.py  
│   │   ├── files.py  
│   │   ├── formats.py  
│   │   ├── llm.py  
│   │   ├── logging.py  
│   │   └── scraper.py  
│   ├── database/  
│   │   └── \_\_init\_\_.py  
│   ├── exceptions/  
│   │   └── \_\_init\_\_.py  
│   ├── llm/  
│   │   └── \_\_init\_\_.py  
│   ├── logger/  
│   │   └── \_\_init\_\_.py  
│   ├── models/  
│   │   └── \_\_init\_\_.py  
│   └── utils/  
│       └── \_\_init\_\_.py  
└── tests/  
    ├── scraper/  
    │   ├── browser/  
    │   ├── parsers/  
    │   └── scrapers/  
    └── shared/  
        ├── config/  
        └── logger/

#### 5\. Phase 3 Directive: The Scraper Framework

The immediate goal is building the BaseScraper abstraction. This class defines the contract for all website-specific implementations.**BaseScraper Responsibilities:**

* Composition and ownership of the BrowserManager instance.  
* Orchestration of the browser/page lifecycle.  
* High-level navigation (goto).  
* Defining the abstract scrape() contract.  
* Providing the capacity for "Waiting helpers" (though implementation is deferred).**BaseScraper Prohibitions (MUST NOT contain):**  
* Parsing logic, HTML selectors, or extraction logic.  
* LLM cleaning or structuring code.  
* Database interaction or storage logic.**Version 1 API Specification:**  Concrete scrapers must only interact with self.page and self.browser\_manager. To maintain strict encapsulation, the BaseScraper  **must not**  expose a direct browser property.

class BaseScraper(ABC):  
    @property  
    def page(self) \-\> Page:  
        """Access the current Patchright page."""  
        ...

    @property  
    def browser\_manager(self) \-\> BrowserManager:  
        """Access the browser lifecycle manager."""  
        ...

    async def start(self) \-\> None:  
        """Initialize browser and create a new page."""  
        ...

    async def stop(self) \-\> None:  
        """Close page and browser resources."""  
        ...

    async def goto(self, url: str) \-\> None:  
        """Navigate to a target URL."""  
        ...

    @abstractmethod  
    async def scrape(self):  
        """Abstract method for website-specific extraction logic."""  
        ...

#### 6\. Mandatory Coding Rules and Workflow Constraints

* **Context Integrity:**  The IDE must never assume the contents of existing files. You  **must**  request the user to paste the relevant file (e.g., manager.py) before suggesting any modifications.  
* **Technology Stack:**  Strictly use  **Patchright**  (not Playwright) and  **LiteLLM**  for future provider abstractions.  
* **Deferred Complexity:**  Implementation of retries, pagination, rate limiting, and screenshots is strictly forbidden in Phase 3\.  
* **No Redundant Logging:**  Redundant navigation logging or click/locator wrappers are forbidden in Version 1\. BrowserManager already logs lifecycle events; extra logging should only be added if it proves necessary in Phase 4\.

#### 7\. Implementation Roadmap

1. **Phase 3: Scraper Framework**  (Current: base\_scraper.py)  
2. **Phase 4: Website Scrapers**  (Implementation of Unstop, Hack2Skill, etc.)  
3. **Phase 5: LLM Pipeline**  (Integration with LiteLLM, Gemini, Groq)  
4. **Phase 6: Exporters**  
5. **Phase 7: Database**  
6. **Phase 8: Scheduler**  
7. **Phase 9: FastAPI Backend**  
8. **Phase 10: DeploymentInstruction to IDE:**  Phases 0-2 are immutable foundations. Do not suggest architectural changes to existing core modules. Focus exclusively on the Phase 3 implementation of base\_scraper.py within the established architectural constraints.

