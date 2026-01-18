"""
eVector Archetype Creator
- CLI-first with neon-green "PulseVector" style
- Optional GUI wizard using Tkinter (built-in)

Run:
  python pulsevector_create.py
  python pulsevector_create.py --gui

Output:
  ./pulsevector_profile.json
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional


# -----------------------------
# Theme / styling
# -----------------------------

NEON_GREEN = "\033[38;5;46m"
PURPLE = "\033[38;5;135m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"

ASCII_LOGO = r"""
██████╗ ██╗   ██╗██╗     ███████╗███████╗██╗   ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗
██╔══██╗██║   ██║██║     ██╔════╝██╔════╝██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██║   ██║██║     ███████╗█████╗  ██║   ██║█████╗  ██║        ██║   ██║   ██║██████╔╝
██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  ██║   ██║██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
██║     ╚██████╔╝███████╗███████║███████╗╚██████╔╝███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""


def supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"


def c(text: str, color: str) -> str:
    if not supports_color():
        return text
    return f"{color}{text}{RESET}"


def pulse_header(title: str) -> None:
    green = NEON_GREEN if supports_color() else ""
    reset = RESET if supports_color() else ""
    print(green + ASCII_LOGO + reset)
    print(c(":: PULSEVECTOR-SIM ::", NEON_GREEN) + " " + c(title, PURPLE))
    print(c("-" * 86, DIM))


def bar7(value: int) -> str:
    value = max(0, min(7, value))
    filled = "█" * value
    empty = "░" * (7 - value)
    return c(filled, NEON_GREEN) + c(empty, DIM)


# -----------------------------
# Archetype definitions
# -----------------------------

@dataclass
class Archetype:
    key: str
    name: str
    tagline: str
    strengths: List[str]
    weaknesses: List[str]
    bias: str
    # Stats are 0..7
    base_stats: Dict[str, int]


STATS = [
    "Finance/Capital",
    "Accounting/Controls",
    "Excel/Tactics",
    "Forecasting/Modeling",
    "Risk/Underwriting",
    "Negotiation/Stakeholders",
    "Execution/Speed",
]

ARCHETYPES: List[Archetype] = [
    Archetype(
        key="banker",
        name="Banker",
        tagline="Capital structure, leverage, and risk pricing under pressure.",
        strengths=[
            "Financing & covenant negotiation",
            "Underwriting instincts",
            "Structuring terms to buy runway",
        ],
        weaknesses=[
            "Spreadsheet hygiene under time pressure",
            "Accounting timing / revenue recognition nuance",
        ],
        bias="“If the structure works, the details will follow.”",
        base_stats={
            "Finance/Capital": 6,
            "Accounting/Controls": 3,
            "Excel/Tactics": 3,
            "Forecasting/Modeling": 4,
            "Risk/Underwriting": 6,
            "Negotiation/Stakeholders": 5,
            "Execution/Speed": 4,
        },
    ),
    Archetype(
        key="accountant",
        name="Accountant",
        tagline="Correctness, timing, and controls — clean books, clean decisions.",
        strengths=[
            "Low error-rate in sheet reviews",
            "Strong AR/AP hygiene",
            "Early detection of operational leaks",
        ],
        weaknesses=[
            "Conservatism can slow growth",
            "Hesitation with incomplete information",
        ],
        bias="“If it’s correct, it’s safe.”",
        base_stats={
            "Finance/Capital": 3,
            "Accounting/Controls": 6,
            "Excel/Tactics": 5,
            "Forecasting/Modeling": 4,
            "Risk/Underwriting": 4,
            "Negotiation/Stakeholders": 3,
            "Execution/Speed": 4,
        },
    ),
    Archetype(
        key="modeler",
        name="Financial Modeler",
        tagline="Scenarios, sensitivities, and projections — the future in numbers.",
        strengths=[
            "Strong planning and variance tracking",
            "Better early warning on runway/stress",
            "Scenario-based decisions",
        ],
        weaknesses=[
            "Over-trusting assumptions",
            "Fragile when data quality is messy",
        ],
        bias="“The model explains it.”",
        base_stats={
            "Finance/Capital": 4,
            "Accounting/Controls": 3,
            "Excel/Tactics": 4,
            "Forecasting/Modeling": 6,
            "Risk/Underwriting": 4,
            "Negotiation/Stakeholders": 3,
            "Execution/Speed": 4,
        },
    ),
    Archetype(
        key="controller",
        name="Controller",
        tagline="Integrates tactics + strategy. Balances speed, accuracy, and sequencing.",
        strengths=[
            "Balanced approach under pressure",
            "Faster recovery from mistakes",
            "Better mid-game optionality",
        ],
        weaknesses=[
            "No early spike advantages",
            "Decision fatigue if you overthink",
        ],
        bias="“What breaks first?”",
        base_stats={
            "Finance/Capital": 4,
            "Accounting/Controls": 5,
            "Excel/Tactics": 4,
            "Forecasting/Modeling": 4,
            "Risk/Underwriting": 4,
            "Negotiation/Stakeholders": 4,
            "Execution/Speed": 4,
        },
    ),
    Archetype(
        key="auditor",
        name="Auditor (Hard Mode)",
        tagline="Skepticism and second-order effects. High safety, slower momentum.",
        strengths=[
            "Strong detection of errors/fraud",
            "Resilience under stress scenarios",
            "Lower catastrophic failure risk",
        ],
        weaknesses=[
            "Slow growth pace",
            "Friction with sales/financing urgency",
        ],
        bias="“Prove it.”",
        base_stats={
            "Finance/Capital": 3,
            "Accounting/Controls": 6,
            "Excel/Tactics": 4,
            "Forecasting/Modeling": 4,
            "Risk/Underwriting": 5,
            "Negotiation/Stakeholders": 3,
            "Execution/Speed": 3,
        },
    ),
]

DIFFICULTY_PRESETS = {
    "normal": {"stress": 0, "credit": 720},
    "hard": {"stress": 15, "credit": 680},
    "nightmare": {"stress": 25, "credit": 640},
}

SCENARIOS = [
    ("chicago_night", "Chicago Night (Tokyo Neon Grid)"),
    ("funding_crunch", "Funding Crunch (Runway Compression)"),
    ("vendor_strike", "Vendor Strike (Terms Tighten)"),
    ("audit_shadow", "Audit Shadow (Controls Under Fire)"),
]


def find_archetype(key: str) -> Archetype:
    for a in ARCHETYPES:
        if a.key == key:
            return a
    raise ValueError(f"Unknown archetype: {key}")


# -----------------------------
# CLI Wizard
# -----------------------------

def prompt_choice(title: str, options: List[Tuple[str, str]]) -> str:
    print(c(title, PURPLE))
    for i, (k, label) in enumerate(options, start=1):
        print(f"  {c(str(i).rjust(2), NEON_GREEN)}. {label} {c(f'[{k}]', DIM)}")
    while True:
        raw = input(c("Select: ", NEON_GREEN)).strip()
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1][0]
        # allow key direct
        for k, _ in options:
            if raw.lower() == k.lower():
                return k
        print(c("Invalid choice. Try again.", YELLOW))


def prompt_int_0_7(label: str, default: int) -> int:
    while True:
        raw = input(f"{c(label, PURPLE)} {c('(0-7)', DIM)} [{default}]: ").strip()
        if raw == "":
            return default
        if raw.isdigit():
            v = int(raw)
            if 0 <= v <= 7:
                return v
        print(c("Enter a number from 0 to 7.", YELLOW))


def show_archetype(a: Archetype) -> None:
    print()
    print(c(a.name.upper(), NEON_GREEN) + " — " + c(a.tagline, DIM))
    print(c("Strengths:", PURPLE))
    for s in a.strengths:
        print("  " + c("▲ ", NEON_GREEN) + s)
    print(c("Weaknesses:", PURPLE))
    for w in a.weaknesses:
        print("  " + c("▼ ", RED) + w)
    print(c("Bias:", PURPLE) + " " + c(a.bias, DIM))
    print(c("\nStarting Stats (0–7):", PURPLE))
    for stat in STATS:
        v = a.base_stats.get(stat, 0)
        print(f"  {stat.ljust(22)} {bar7(v)} {c(str(v)+'/7', DIM)}")


def cli_wizard() -> Dict:
    pulse_header("CREATE PROFILE")
    name = input(c("Operator callsign (name): ", NEON_GREEN)).strip() or "Senior Operator"

    arch_key = prompt_choice(
        "Choose your starting archetype:",
        [(a.key, a.name) for a in ARCHETYPES],
    )
    archetype = find_archetype(arch_key)
    show_archetype(archetype)

    scenario_key = prompt_choice(
        "\nChoose starting scenario:",
        SCENARIOS,
    )

    diff_key = prompt_choice(
        "\nChoose difficulty:",
        [(k, k.title()) for k in DIFFICULTY_PRESETS.keys()],
    )

    # Optional: allow 3 "allocation points" to customize (keeps identity intact)
    print()
    print(c("Customization:", PURPLE), c("You get 3 points to allocate (+1 each). Max 7.", DIM))
    stats = dict(archetype.base_stats)
    points = 3
    while points > 0:
        print(c(f"\nPoints remaining: {points}", NEON_GREEN))
        for i, stat in enumerate(STATS, start=1):
            print(f"  {str(i).rjust(2)}. {stat.ljust(22)} {bar7(stats[stat])} {c(str(stats[stat])+'/7', DIM)}")
        raw = input(c("Pick a stat number to increase (or press Enter to skip): ", NEON_GREEN)).strip()
        if raw == "":
            break
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(STATS):
                stat = STATS[idx - 1]
                if stats[stat] < 7:
                    stats[stat] += 1
                    points -= 1
                else:
                    print(c("That stat is already maxed (7).", YELLOW))
            else:
                print(c("Invalid stat.", YELLOW))
        else:
            print(c("Enter a number.", YELLOW))

    # Derived starting conditions
    preset = DIFFICULTY_PRESETS[diff_key]
    starting_credit = preset["credit"] + random.randint(-15, 15)
    starting_stress = clamp_int(preset["stress"] + random.randint(-5, 5), 0, 100)

    profile = {
        "meta": {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "theme": {"primary": "tokyo_neon_green", "accent": "purple"},
        },
        "player": {
            "name": name,
            "archetype": archetype.key,
            "scenario": scenario_key,
            "difficulty": diff_key,
            "stats_0_7": stats,
        },
        "start": {
            "credit_score_0_1000": starting_credit,
            "debt_stress_0_100": starting_stress,
        },
    }

    print()
    print(c("PROFILE READY", NEON_GREEN))
    print(c("  Credit Score:", PURPLE), c(str(profile["start"]["credit_score_0_1000"]), NEON_GREEN))
    print(c("  Debt Stress:", PURPLE), c(str(profile["start"]["debt_stress_0_100"]), YELLOW))
    return profile


def clamp_int(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(n)))


# -----------------------------
# GUI Wizard (Tkinter)
# -----------------------------

def gui_wizard() -> Optional[Dict]:
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except Exception as e:
        print(c("Tkinter GUI not available in this Python environment.", YELLOW))
        print(c(str(e), DIM))
        return None

    root = tk.Tk()
    root.title("PulseVector — Profile Creator")
    root.geometry("860x560")
    root.configure(bg="#05080a")

    # Colors (approx Tokyo neon green + purple accent)
    BG = "#05080a"
    PANEL = "#0a1114"
    GREEN = "#1CFF65"
    PURP = "#7B2CFF"
    TXT = "#E8FFF0"
    MUT = "#A6CDB4"

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=PANEL)
    style.configure("TLabel", background=PANEL, foreground=TXT, font=("Consolas", 11))
    style.configure("Title.TLabel", background=BG, foreground=GREEN, font=("Consolas", 18, "bold"))
    style.configure("Sub.TLabel", background=BG, foreground=MUT, font=("Consolas", 10))
    style.configure("Accent.TLabel", background=PANEL, foreground=PURP, font=("Consolas", 11, "bold"))
    style.configure("TButton", font=("Consolas", 11, "bold"))
    style.map("TButton",
              foreground=[("active", TXT)],
              background=[("active", "#0e1d16")])
    style.configure("TCombobox", fieldbackground="#071013", background="#071013", foreground=TXT)

    # State vars
    name_var = tk.StringVar(value="Senior Operator")
    archetype_var = tk.StringVar(value=ARCHETYPES[0].key)
    scenario_var = tk.StringVar(value=SCENARIOS[0][0])
    diff_var = tk.StringVar(value="normal")

    # Custom points allocation
    points_left = tk.IntVar(value=3)
    stat_vars: Dict[str, tk.IntVar] = {s: tk.IntVar(value=ARCHETYPES[0].base_stats[s]) for s in STATS}

    def set_archetype(key: str):
        a = find_archetype(key)
        archetype_var.set(key)
        # Reset stats + points
        points_left.set(3)
        for s in STATS:
            stat_vars[s].set(a.base_stats[s])
        render_archetype(a)

    def render_archetype(a: Archetype):
        # Clear detail frame
        for w in detail_frame.winfo_children():
            w.destroy()

        ttk.Label(detail_frame, text=f"{a.name.upper()} — {a.tagline}", style="Accent.TLabel").pack(anchor="w", pady=(0, 8))

        ttk.Label(detail_frame, text="Strengths", style="Accent.TLabel").pack(anchor="w")
        for s in a.strengths:
            ttk.Label(detail_frame, text=f"▲ {s}", style="TLabel").pack(anchor="w")

        ttk.Label(detail_frame, text="", style="TLabel").pack(anchor="w", pady=4)

        ttk.Label(detail_frame, text="Weaknesses", style="Accent.TLabel").pack(anchor="w")
        for w in a.weaknesses:
            ttk.Label(detail_frame, text=f"▼ {w}", style="TLabel").pack(anchor="w")

        ttk.Label(detail_frame, text="", style="TLabel").pack(anchor="w", pady=4)
        ttk.Label(detail_frame, text=f"Bias: {a.bias}", style="TLabel").pack(anchor="w")

        ttk.Label(detail_frame, text="", style="TLabel").pack(anchor="w", pady=6)
        ttk.Label(detail_frame, text="Starting Stats (0–7) — you can allocate +3 points", style="Accent.TLabel").pack(anchor="w")

        stats_frame = ttk.Frame(detail_frame, style="Card.TFrame")
        stats_frame.pack(fill="x", pady=8)

        def bump(stat: str):
            if points_left.get() <= 0:
                return
            if stat_vars[stat].get() >= 7:
                return
            stat_vars[stat].set(stat_vars[stat].get() + 1)
            points_left.set(points_left.get() - 1)
            refresh_points()

        def refresh_points():
            points_label.config(text=f"Points remaining: {points_left.get()}")

        points_label = ttk.Label(detail_frame, text=f"Points remaining: {points_left.get()}", style="TLabel")
        points_label.pack(anchor="w")

        for stat in STATS:
            row = ttk.Frame(stats_frame, style="Card.TFrame")
            row.pack(fill="x", padx=8, pady=4)

            lbl = ttk.Label(row, text=stat, style="TLabel")
            lbl.pack(side="left")

            # A tiny bar (7 blocks)
            bar = tk.Label(row, bg=PANEL, fg=GREEN, font=("Consolas", 11))
            bar.pack(side="left", padx=10)

            val = ttk.Label(row, textvariable=stat_vars[stat], style="TLabel")
            val.pack(side="right")

            btn = ttk.Button(row, text="+", command=lambda s=stat: bump(s))
            btn.pack(side="right", padx=8)

            def update_bar(*_):
                v = stat_vars[stat].get()
                bar.config(text=("█" * v) + ("░" * (7 - v)))

            stat_vars[stat].trace_add("write", update_bar)
            update_bar()

        refresh_points()

    def build_profile() -> Dict:
        a = find_archetype(archetype_var.get())
        preset = DIFFICULTY_PRESETS[diff_var.get()]
        starting_credit = preset["credit"] + random.randint(-15, 15)
        starting_stress = clamp_int(preset["stress"] + random.randint(-5, 5), 0, 100)
        stats = {s: int(stat_vars[s].get()) for s in STATS}
        return {
            "meta": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "theme": {"primary": "tokyo_neon_green", "accent": "purple"},
            },
            "player": {
                "name": name_var.get().strip() or "Senior Operator",
                "archetype": a.key,
                "scenario": scenario_var.get(),
                "difficulty": diff_var.get(),
                "stats_0_7": stats,
            },
            "start": {
                "credit_score_0_1000": starting_credit,
                "debt_stress_0_100": starting_stress,
            },
        }

    def on_save():
        profile = build_profile()
        out = os.path.join(os.getcwd(), "pulsevector_profile.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)
        messagebox.showinfo("Saved", f"Profile saved:\n{out}")

    def on_preview():
        profile = build_profile()
        msg = (
            f"Name: {profile['player']['name']}\n"
            f"Archetype: {profile['player']['archetype']}\n"
            f"Scenario: {profile['player']['scenario']}\n"
            f"Difficulty: {profile['player']['difficulty']}\n\n"
            f"Credit Score: {profile['start']['credit_score_0_1000']}\n"
            f"Debt Stress: {profile['start']['debt_stress_0_100']}\n"
        )
        messagebox.showinfo("Preview", msg)

    # Layout
    header = ttk.Frame(root, style="TFrame")
    header.pack(fill="x", padx=16, pady=(14, 8))
    ttk.Label(header, text="PULSEVECTOR — PROFILE CREATOR", style="Title.TLabel").pack(anchor="w")
    ttk.Label(header, text="Chicago Night • Tokyo Neon Green • Purple Accent", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

    main = ttk.Frame(root, style="TFrame")
    main.pack(fill="both", expand=True, padx=16, pady=10)

    left = ttk.Frame(main, style="Card.TFrame")
    left.pack(side="left", fill="y", padx=(0, 10))
    right = ttk.Frame(main, style="Card.TFrame")
    right.pack(side="right", fill="both", expand=True)

    # Left controls
    pad = {"padx": 12, "pady": 10}
    ttk.Label(left, text="Operator", style="Accent.TLabel").pack(anchor="w", **pad)
    name_entry = ttk.Entry(left, textvariable=name_var)
    name_entry.pack(fill="x", padx=12)
    name_entry.configure(font=("Consolas", 12))

    ttk.Label(left, text="Archetype", style="Accent.TLabel").pack(anchor="w", **pad)
    arch_box = ttk.Combobox(left, state="readonly", values=[f"{a.name} [{a.key}]" for a in ARCHETYPES])
    arch_box.pack(fill="x", padx=12)

    def arch_changed(_):
        idx = arch_box.current()
        if idx >= 0:
            set_archetype(ARCHETYPES[idx].key)

    arch_box.bind("<<ComboboxSelected>>", arch_changed)
    arch_box.current(0)

    ttk.Label(left, text="Scenario", style="Accent.TLabel").pack(anchor="w", **pad)
    scen_box = ttk.Combobox(left, state="readonly", values=[f"{label} [{k}]" for k, label in SCENARIOS])
    scen_box.pack(fill="x", padx=12)
    scen_box.current(0)

    def scen_changed(_):
        idx = scen_box.current()
        if idx >= 0:
            scenario_var.set(SCENARIOS[idx][0])

    scen_box.bind("<<ComboboxSelected>>", scen_changed)

    ttk.Label(left, text="Difficulty", style="Accent.TLabel").pack(anchor="w", **pad)
    diff_box = ttk.Combobox(left, state="readonly", values=[k.title() for k in DIFFICULTY_PRESETS.keys()])
    diff_box.pack(fill="x", padx=12)
    diff_box.current(0)

    def diff_changed(_):
        keys = list(DIFFICULTY_PRESETS.keys())
        idx = diff_box.current()
        if idx >= 0:
            diff_var.set(keys[idx])

    diff_box.bind("<<ComboboxSelected>>", diff_changed)

    btns = ttk.Frame(left, style="Card.TFrame")
    btns.pack(fill="x", padx=12, pady=14)
    ttk.Button(btns, text="Preview", command=on_preview).pack(fill="x", pady=4)
    ttk.Button(btns, text="Save Profile", command=on_save).pack(fill="x", pady=4)
    ttk.Button(btns, text="Quit", command=root.destroy).pack(fill="x", pady=4)

    # Right detail frame
    detail_frame = ttk.Frame(right, style="Card.TFrame")
    detail_frame.pack(fill="both", expand=True, padx=12, pady=12)

    render_archetype(ARCHETYPES[0])
    root.mainloop()
    return None


# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser(description="PulseVector Profile Creator (CLI + optional GUI)")
    ap.add_argument("--gui", action="store_true", help="Launch Tkinter GUI wizard")
    ap.add_argument("--out", default="pulsevector_profile.json", help="Output JSON file name")
    args = ap.parse_args()

    if args.gui:
        gui_wizard()
        return

    profile = cli_wizard()
    out_path = os.path.join(os.getcwd(), args.out)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    print(c(f"\nSaved → {out_path}", NEON_GREEN))


if __name__ == "__main__":
    main()

