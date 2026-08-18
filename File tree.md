# File Tree: global-ai-opportunity-tracker-backend

**Root Path:** `d:\Programming\Python\Global AI opportunity Tracker\global-ai-opportunity-tracker-backend`

```
├── 📁 .agents
│   ├── 📁 rules
│   │   ├── 📝 agent-progress.md
│   │   └── 📝 graphify.md
│   └── 📁 workflows
│       ├── 📝 agent-session.md
│       └── 📝 graphify.md
├── 📁 .github
│   └── ⚙️ .gitkeep
├── 📁 .state
│   ├── 📝 CURRENT_CONTEXT.md
│   ├── 📝 CURRENT_PHASE.md
│   ├── 📝 DECISIONS.md
│   ├── 📝 DEVELOPMENT_STATUS.md
│   ├── 📝 KNOWN_ISSUES.md
│   └── 📝 TASK_QUEUE.md
├── 📁 docs
│   ├── 📁 architecture
│   │   └── ⚙️ .gitkeep
│   ├── 📁 deployment
│   │   └── ⚙️ .gitkeep
│   ├── 📁 phases
│   │   ├── 📝 PHASE_00.md
│   │   ├── 📝 PHASE_01.md
│   │   ├── 📝 PHASE_02.md
│   │   ├── 📝 PHASE_03.md
│   │   ├── 📝 PHASE_04.md
│   │   ├── 📝 PHASE_05.md
│   │   ├── 📝 PHASE_06.md
│   │   ├── 📝 PHASE_07.md
│   │   ├── 📝 PHASE_08.md
│   │   ├── 📝 PHASE_09.md
│   │   └── 📝 PHASE_10.md
│   ├── 📁 research
│   │   └── ⚙️ .gitkeep
│   ├── 📁 scraper
│   │   └── ⚙️ .gitkeep
│   ├── 📝 ARCHITECTURE.md
│   ├── 📝 CODEBASE_GUIDE.md
│   ├── 📝 COMPONENT_LIBRARY.md
│   ├── 📝 DEVELOPMENT_WORKFLOW.md
│   ├── 📝 FEATURES_AND_FLOWS.md
│   ├── 📝 PROJECT_OVERVIEW.md
│   └── 📝 ROADMAP.md
├── 📁 examples
│   ├── 📁 browser
│   │   └── 🐍 basic_browser.py
│   ├── 📁 llm
│   │   ├── ⚙️ .gitkeep
│   │   └── 🐍 test_llm_connection.py
│   └── 📁 scraper
│       ├── ⚙️ .gitkeep
│       ├── 🐍 debug_devpost_selectors.py
│       ├── 🐍 debug_unstop_pagination.py
│       ├── 🐍 debug_unstop_selectors.py
│       ├── 🐍 run_devpost.py
│       └── 🐍 run_unstop.py
├── 📁 graphify-out
│   ├── 📁 2026-08-15
│   │   ├── ⚙️ .graphify_analysis.json
│   │   ├── ⚙️ .graphify_labels.json
│   │   ├── 📝 GRAPH_REPORT.md
│   │   ├── ⚙️ cost.json
│   │   ├── ⚙️ graph.json
│   │   └── ⚙️ manifest.json
│   ├── 📁 2026-08-16
│   │   ├── ⚙️ .graphify_analysis.json
│   │   ├── ⚙️ .graphify_labels.json
│   │   ├── 📝 GRAPH_REPORT.md
│   │   ├── ⚙️ cost.json
│   │   ├── ⚙️ graph.json
│   │   └── ⚙️ manifest.json
│   ├── ⚙️ .graphify_analysis.json
│   ├── ⚙️ .graphify_ast.json
│   ├── ⚙️ .graphify_detect.json
│   ├── ⚙️ .graphify_extract.json
│   ├── ⚙️ .graphify_labels.json
│   ├── ⚙️ .graphify_python
│   ├── ⚙️ .graphify_root
│   ├── ⚙️ .graphify_semantic.json
│   ├── 📝 GRAPH_REPORT.md
│   ├── ⚙️ cost.json
│   ├── 🌐 graph.html
│   ├── ⚙️ graph.json
│   ├── ⚙️ manifest.json
│   ├── 📄 step3.ps1
│   └── 📄 step_full.ps1
├── 📁 scraper
│   ├── 📁 core
│   │   ├── 📁 browser
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 config.py
│   │   │   ├── 🐍 factory.py
│   │   │   ├── 🐍 manager.py
│   │   │   ├── 🐍 models.py
│   │   │   ├── 🐍 protocols.py
│   │   │   ├── 🐍 session.py
│   │   │   └── 🐍 stealth.py
│   │   ├── 📁 exceptions
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 browser.py
│   │   ├── 📁 manager
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 scraper_manager.py
│   │   └── 📁 scheduler
│   │       ├── 🐍 __init__.py
│   │       └── 🐍 job_scheduler.py
│   ├── 📁 data
│   │   ├── 📁 outputs
│   │   │   ├── ⚙️ devpost_opportunities.json
│   │   │   └── ⚙️ unstop_opportunities.json
│   │   └── 🐍 __init__.py
│   ├── 📁 exporters
│   │   └── 🐍 __init__.py
│   ├── 📁 parsers
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 base_parser.py
│   │   ├── 🐍 normalizer.py
│   │   ├── 🐍 opportunity_parser.py
│   │   ├── 🐍 parser_utils.py
│   │   ├── 🐍 selector_engine.py
│   │   ├── 🐍 selector_parser.py
│   │   └── 🐍 site_parser.py
│   └── 📁 scrapers
│       ├── 📁 base
│       │   ├── 🐍 __init__.py
│       │   └── 🐍 base_scraper.py
│       ├── 📁 devpost
│       │   ├── 📁 profiles
│       │   │   └── ⚙️ devpost_selectors.json
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 profile_manager.py
│       │   └── 🐍 scraper.py
│       ├── 📁 hack2skill
│       │   └── 🐍 __init__.py
│       ├── 📁 kaggle
│       │   └── 🐍 __init__.py
│       └── 📁 unstop
│           ├── 📁 profiles
│           │   ├── ⚙️ .gitkeep
│           │   ├── ⚙️ competitions.json
│           │   └── ⚙️ hackathon_listing.json
│           ├── 🐍 __init__.py
│           ├── 🐍 parser.py
│           ├── 🐍 profile_manager.py
│           └── 🐍 scraper.py
├── 📁 shared
│   ├── 📁 config
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 settings.py
│   ├── 📁 constants
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 browser.py
│   │   ├── 🐍 files.py
│   │   ├── 🐍 formats.py
│   │   ├── 🐍 llm.py
│   │   ├── 🐍 logging.py
│   │   └── 🐍 scraper.py
│   ├── 📁 database
│   │   └── 🐍 __init__.py
│   ├── 📁 exceptions
│   │   └── 🐍 __init__.py
│   ├── 📁 llm
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 client.py
│   │   ├── 🐍 exceptions.py
│   │   ├── 🐍 manager.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 parser.py
│   │   ├── 🐍 prompt_builder.py
│   │   ├── 🐍 providers.py
│   │   ├── 🐍 selector_profile.py
│   │   ├── 🐍 templates.py
│   │   └── 🐍 validator.py
│   ├── 📁 logger
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 filters.py
│   │   ├── 🐍 formatters.py
│   │   ├── 🐍 handlers.py
│   │   └── 🐍 logger.py
│   ├── 📁 models
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 enums.py
│   │   ├── 🐍 location.py
│   │   ├── 🐍 metadata.py
│   │   ├── 🐍 opportunity.py
│   │   ├── 🐍 organizer.py
│   │   ├── 🐍 prize.py
│   │   └── 🐍 timeline.py
│   ├── 📁 utils
│   │   └── 🐍 __init__.py
│   └── 🐍 __init__.py
├── 📁 tests
│   ├── 📁 scraper
│   │   ├── 📁 browser
│   │   │   └── ⚙️ .gitkeep
│   │   ├── 📁 parsers
│   │   │   └── ⚙️ .gitkeep
│   │   ├── 📁 scrapers
│   │   │   ├── ⚙️ .gitkeep
│   │   │   └── 🐍 test_base_scraper.py
│   │   └── ⚙️ .gitkeep
│   └── 📁 shared
│       ├── 📁 config
│       │   └── ⚙️ .gitkeep
│       ├── 📁 logger
│       │   └── ⚙️ .gitkeep
│       └── ⚙️ .gitkeep
├── ⚙️ .aiexclude
├── ⚙️ .antigravityignore
├── ⚙️ .env.example
├── ⚙️ .gitignore
├── 📄 LICENSE
├── 📝 Project Context Blueprint V1_ Global AI Opportunity Tracker (Antigravity IDE).md
├── 📝 README.md
├── 📝 context.md
├── 🌐 devpost_page.html
├── 📄 poetry.lock
├── ⚙️ pyproject.toml
├── 🌐 unstop_listing_component.html
└── 🌐 unstop_page.html
```