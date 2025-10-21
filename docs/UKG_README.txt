UKG Workforce Operating Platform – RAG Demo Context

Company Overview
----------------
UKG (Ultimate Kronos Group) was formed in 2020 from the merger of Ultimate Software and Kronos Incorporated. 
It is one of the world’s largest Workforce Management and Human Capital Management (HCM) providers.

Headquarters: Massachusetts & Florida
Employees: 12,000+
Tagline: "Our purpose is people."
Rebrand Theme: "When Work Works, Everything Works."

The company focuses on AI-driven, people-first innovation that unifies HR, payroll, and workforce management 
under a single Workforce Operating Platform.

Core Products
-------------
1. UKG Pro – For large enterprises; integrates HR, payroll, and talent management with global capabilities.
2. UKG Ready – For SMBs; unified HR, time, and payroll with compliance for 160+ countries.
3. UKG Dimensions – AI-powered workforce optimization and analytics for complex industries.

Specialized Solutions
---------------------
- UKG One View: Global payroll orchestration.
- UKG InTouch DX: Touchscreen-enabled time clock.
- UKG TeleStaff Cloud: Public safety scheduling.
- UKG Virtual Roster Cloud: Casino and resort scheduling.
- EZCall: Healthcare staff scheduling.
- UKG Wallet: Earned wage access.
- UKG Talk: Workforce communication hub.

AI, Data, and Compliance
------------------------
- Predictive analytics for labor and burnout.
- Automated scheduling and compliance monitoring.
- Integration with Google Cloud for Agentic AI collaboration.
- Access to 40,000+ learning courses through OpenSesame.

Payroll & Compliance
--------------------
- Real-time payroll and global compliance in 160+ countries.
- Multi-currency payroll and localized tax compliance.
- Self-service access for pay, benefits, and deductions.

Market Position
---------------
UKG competes with ADP, Workday, and Ceridian. It’s recognized for its people-first design, 
AI-driven insights, and commitment to employee wellbeing.

Vision: Empower organizations to build workplaces where people thrive through intelligent workforce systems.

How to Use in RAG Demo
----------------------
1. Place this file in ./docs/UKG_README.txt or ./docs/UKG_Overview.pdf
2. Ingest using:
   curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '{"input_dir":"./docs"}'
3. Query using:
   curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"query":"What is UKG Ready?"}'
4. Check status:
   curl http://localhost:8000/status/<task_id>

Author: Jorge Rivero
Project: RAG-App (FastAPI + Celery + Redis + Prometheus + FAISS)
Version: 1.0.0
Date: 2025
