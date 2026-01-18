# PulseVector

PulseVector is an experimental system exploring how decisions compound over time when made under real constraints.

It uses finance and accounting as the surface layer, not as the objective.

---

## Context

In many development and leadership environments, decisions are discussed abstractly.

Outcomes are explained after the fact, often separated from the structure that produced them.

PulseVector explores a different pattern:
- decisions occur sequentially
- constraints persist
- trade-offs remain visible
- consequences accumulate

The system does not optimize or advise.
It records.

---

## Archetypes

The entry point into PulseVector is an archetype selection.

Participants begin from a particular lens, such as:
- banker
- accountant
- financial modeler
- controller

Each archetype reflects tendencies rather than skills:
- what is prioritized
- what is deferred
- how risk is interpreted
- how pressure is handled

No archetype is neutral.

---

## The Ledger

All actions ultimately resolve into a live accounting ledger.

Cash, obligations, timing, and recognition are not abstracted into scores.

They are recorded directly using double-entry accounting.

The ledger is not explained upfront.
It is observed over time.

---

## Quickstart — Archetype Demo

The archetype demo initializes a PulseVector operator profile.
It is the first surface external users interact with.

### Requirements
- Python 3.10+
- (Optional GUI) Tkinter  
  - Included with Python on most macOS and Windows installations  
  - Linux users may need to install `python3-tk`

### Setup

```bash
git clone <your-repo-url>
cd pulsevector

python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
