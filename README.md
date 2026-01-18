# pulsevector-sim

# PulseVector Senior Ops Simulator

**A CLI-based operations and finance simulation engine that trains both tactical execution (Excel-level work) and strategic judgment (CFO-level decision-making).**

---

## 🚀 Overview

PulseVector Senior Ops Simulator is a **Node.js / TypeScript** simulation designed to model the real-world responsibilities of a high-performing **senior operator**—someone who must simultaneously:

- Execute **technical work** (Excel analysis, data validation, logic checks)
- Make **strategic decisions** (cash management, debt, working capital, risk sequencing)

The design philosophy is inspired by chess:

> You cannot rely only on positioning without tactics.  
> You cannot rely only on tactics without a plan.

This simulator enforces mastery of **both**.

---

## 🎯 Key Features

### Dual-Skill Gameplay
- **Strategic layer**:  
  - Cash, AR/AP, inventory, debt, deferred revenue  
  - Payment terms, collections posture, spend controls, financing decisions
- **Tactical layer**:  
  - Excel-style missions (XLOOKUP, IF/AND logic, pivot table interpretation)
  - Data integrity reviews under time pressure

You cannot progress by strategy alone—technical competence is required.

---

### Debt-Induced Stress System
Debt is intentionally **not overpowered**.

A dynamic **Debt Stress Meter (0–100)** increases with:
- High leverage relative to revenue capacity
- Low cash runway
- AR aging deterioration
- Missed payments or covenant flags

Stress directly impacts:
- Sales close rates
- Vendor terms
- Interest rates
- Event severity

---

### Company Credit Score (Primary Game Metric)
The main score of the game is a **projected company credit score (0–1000)**, derived from:

- Liquidity and runway
- Leverage and coverage
- Working capital quality
- Profitability and volatility
- Behavioral signals (missed payroll, late vendors, covenant issues)

The credit score determines:
- Financing availability and cost
- Customer and vendor behavior
- Long-term optionality

You are not optimizing profit—you are optimizing **solvency, credibility, and flexibility**.

---

## 🕹️ Gameplay Loop

Each simulated day:
1. Review operational state (cash, AR/AP, inventory, debt, stress)
2. Receive **tickets / missions**
   - CFO / ops incidents
   - Excel-style technical challenges
3. Choose a limited set of **strategic levers**
4. Resolve missions and observe consequences
5. Advance to the next day

Poor decisions compound. Good decisions create optionality.

---

## 🧩 Excel / Technical Missions

Examples include:
- Identifying broken `XLOOKUP` logic
- Correcting flawed `IF` / `AND` conditions
- Interpreting misleading pivot tables
- Catching data consistency issues

Mission performance affects:
- XP progression
- Error rates
- Downstream financial outcomes

---

## 🏗️ Architecture

### Stack
- **Node.js + TypeScript**
- CLI-first (terminal-based)
- Modular, event-driven engine
- XLSX export via `xlsx` (SheetJS)

### Design Goals
- CLI today
- Web UI tomorrow
- Native Excel interoperability
- Power BI / Azure readiness

### Data Outputs
Normalized tables suitable for BI tools:
- Daily KPIs
- Mission results
- Journal-style event logs
- Credit score history
- Stress metrics

---

## 📦 Project Status

🚧 **Active Development**

Current focus:
- Core engine stabilization
- Mission generation system
- Excel challenge framework
- Credit score and stress tuning

This project is intentionally opinionated and evolving.

---

## 🧠 Why This Exists

This simulator exists to train a skill set that is rarely taught explicitly:

> **Operating as a senior professional who must think tactically and strategically under constraint.**

It reflects real-world truths:
- Senior contributors still do technical work
- Strategic decisions are made with incomplete information
- Debt buys time but costs credibility
- Small technical errors can cascade into major financial issues

---

## ⚠️ Disclaimer

This project is for **training and experimentation purposes only**.  
It does not constitute financial, accounting, or investment advice.

---

## 📄 License

MIT License

Copyright (c) 2026 PulseVector

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
