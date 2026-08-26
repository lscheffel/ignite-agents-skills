#!/usr/bin/env python3
"""
Independent Problem Reconstruction Questionnaire

Guides the challenger through Phase 1: building an independent problem model
without reading the existing ADR first. Ensures fresh reconstruction.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class Goal:
    description: str
    success_criterion: str
    priority: str  # primary, secondary, tertiary


@dataclass
class Constraint:
    description: str
    type: str  # hard, soft
    category: str  # regulatory, budget, timeline, technical, organizational


@dataclass
class Invariant:
    description: str
    rationale: str


@dataclass
class Actor:
    name: str
    type: str  # human, system, external
    responsibilities: List[str]
    interactions: List[str]


@dataclass
class IOFlow:
    name: str
    source_or_consumer: str
    format: str
    frequency: str
    sla: str


@dataclass
class StateEntity:
    name: str
    persistence: str  # persistent, ephemeral, distributed
    consistency: str  # strong, eventual
    access_pattern: str  # read, write, both


@dataclass
class Dependency:
    name: str
    direction: str  # upstream, downstream, lateral
    description: str
    sla: str
    failure_mode: str


@dataclass
class FailureCondition:
    condition: str
    detection: str
    impact: str
    recovery: str


@dataclass
class OperationalRequirement:
    requirement: str
    target: str
    measurement: str


@dataclass
class ProblemModel:
    problem_statement: str
    goals: List[Goal] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    invariants: List[Invariant] = field(default_factory=list)
    non_goals: List[str] = field(default_factory=list)
    actors: List[Actor] = field(default_factory=list)
    inputs: List[IOFlow] = field(default_factory=list)
    outputs: List[IOFlow] = field(default_factory=list)
    state: List[StateEntity] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    failure_conditions: List[FailureCondition] = field(default_factory=list)
    operational_requirements: List[OperationalRequirement] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0"


class ProblemReconstructor:
    def __init__(self):
        self.model = ProblemModel(problem_statement="")
        self.current_section = 0
        self.sections = [
            ("Problem Statement", self._collect_problem_statement),
            ("Goals", self._collect_goals),
            ("Constraints", self._collect_constraints),
            ("Invariants", self._collect_invariants),
            ("Non-Goals", self._collect_non_goals),
            ("Actors", self._collect_actors),
            ("Inputs", self._collect_inputs),
            ("Outputs", self._collect_outputs),
            ("State", self._collect_state),
            ("Dependencies", self._collect_dependencies),
            ("Failure Conditions", self._collect_failure_conditions),
            ("Operational Requirements", self._collect_operational_requirements),
        ]

    def run_interactive(self) -> ProblemModel:
        """Run interactive questionnaire."""
        print("=" * 70)
        print("INDEPENDENT PROBLEM RECONSTRUCTION — Phase 1")
        print("=" * 70)
        print("\nIMPORTANT: Do NOT read the existing ADR before completing this.")
        print("Build your problem model from first principles only.\n")
        
        for i, (name, collector) in enumerate(self.sections, 1):
            self.current_section = i
            print(f"\n{'='*70}")
            print(f"SECTION {i}/12: {name}")
            print(f"{'='*70}")
            collector()
            
            # Show progress
            completed = [s for s in self.sections[:i] if getattr(self.model, s[0].lower().replace(" ", "_") + ("s" if s[0] != "Problem Statement" else ""))]
            print(f"\nProgress: {i}/12 sections completed")
            
            if i < len(self.sections):
                cont = input("\nPress Enter to continue, or 'q' to quit: ")
                if cont.lower() == 'q':
                    break
        
        return self.model

    def _collect_problem_statement(self):
        print("Describe the problem in one paragraph. What is actually being solved?")
        print("Focus on the *problem*, not the solution.")
        self.model.problem_statement = input("Problem statement: ").strip()

    def _collect_goals(self):
        print("Define goals with MEASURABLE success criteria.")
        print("Priority: primary (must), secondary (should), tertiary (nice)")
        
        while True:
            desc = input("\nGoal description (empty to finish): ").strip()
            if not desc:
                break
            criterion = input("  Measurable success criterion: ").strip()
            priority = input("  Priority [primary/secondary/tertiary]: ").strip().lower()
            if priority not in ("primary", "secondary", "tertiary"):
                priority = "secondary"
            self.model.goals.append(Goal(desc, criterion, priority))
            print(f"  Added: [{priority}] {desc}")

    def _collect_constraints(self):
        print("Define constraints. Hard = non-negotiable. Soft = negotiable with trade-off.")
        categories = ["regulatory", "budget", "timeline", "technical", "organizational", "other"]
        
        while True:
            desc = input("\nConstraint description (empty to finish): ").strip()
            if not desc:
                break
            ctype = input("  Type [hard/soft]: ").strip().lower()
            if ctype not in ("hard", "soft"):
                ctype = "hard"
            print(f"  Categories: {', '.join(categories)}")
            category = input("  Category: ").strip().lower()
            if category not in categories:
                category = "other"
            self.model.constraints.append(Constraint(desc, ctype, category))
            print(f"  Added: [{ctype}] {desc}")

    def _collect_invariants(self):
        print("Define invariants — conditions that MUST ALWAYS HOLD.")
        print("Examples: 'No data loss under any failure mode', 'All mutations are idempotent'")
        
        while True:
            desc = input("\nInvariant (empty to finish): ").strip()
            if not desc:
                break
            rationale = input("  Why must this hold? ").strip()
            self.model.invariants.append(Invariant(desc, rationale))
            print(f"  Added: {desc}")

    def _collect_non_goals(self):
        print("Explicitly declare what is OUT OF SCOPE.")
        print("This prevents scope creep and clarifies boundaries.")
        
        while True:
            ng = input("\nNon-goal (empty to finish): ").strip()
            if not ng:
                break
            rationale = input("  Why is this out of scope? ").strip()
            self.model.non_goals.append(f"{ng} — {rationale}")
            print(f"  Added: {ng}")

    def _collect_actors(self):
        print("Identify all actors: humans, systems, external parties.")
        
        while True:
            name = input("\nActor name (empty to finish): ").strip()
            if not name:
                break
            atype = input("  Type [human/system/external]: ").strip().lower()
            if atype not in ("human", "system", "external"):
                atype = "system"
            resp = input("  Responsibilities (comma-separated): ").strip()
            interactions = input("  Interacts with (comma-separated): ").strip()
            self.model.actors.append(Actor(
                name=name,
                type=atype,
                responsibilities=[r.strip() for r in resp.split(",") if r.strip()],
                interactions=[i.strip() for i in interactions.split(",") if i.strip()]
            ))
            print(f"  Added: {name} ({atype})")

    def _collect_inputs(self):
        print("Define all inputs: data, events, triggers coming INTO the system.")
        
        while True:
            name = input("\nInput name (empty to finish): ").strip()
            if not name:
                break
            source = input("  Source: ").strip()
            fmt = input("  Format: ").strip()
            freq = input("  Frequency: ").strip()
            sla = input("  SLA: ").strip()
            self.model.inputs.append(IOFlow(name, source, fmt, freq, sla))
            print(f"  Added: {name} from {source}")

    def _collect_outputs(self):
        print("Define all outputs: deliverables, side effects, state changes GOING OUT.")
        
        while True:
            name = input("\nOutput name (empty to finish): ").strip()
            if not name:
                break
            consumer = input("  Consumer: ").strip()
            fmt = input("  Format: ").strip()
            freq = input("  Frequency: ").strip()
            sla = input("  SLA: ").strip()
            self.model.outputs.append(IOFlow(name, consumer, fmt, freq, sla))
            print(f"  Added: {name} to {consumer}")

    def _collect_state(self):
        print("Define persistent/ephemeral state entities.")
        
        while True:
            name = input("\nState entity name (empty to finish): ").strip()
            if not name:
                break
            persistence = input("  Persistence [persistent/ephemeral/distributed]: ").strip().lower()
            if persistence not in ("persistent", "ephemeral", "distributed"):
                persistence = "persistent"
            consistency = input("  Consistency [strong/eventual]: ").strip().lower()
            if consistency not in ("strong", "eventual"):
                consistency = "eventual"
            access = input("  Access pattern [read/write/both]: ").strip().lower()
            if access not in ("read", "write", "both"):
                access = "both"
            self.model.state.append(StateEntity(name, persistence, consistency, access))
            print(f"  Added: {name} ({persistence}, {consistency})")

    def _collect_dependencies(self):
        print("Define upstream, downstream, and lateral dependencies.")
        
        while True:
            name = input("\nDependency name (empty to finish): ").strip()
            if not name:
                break
            direction = input("  Direction [upstream/downstream/lateral]: ").strip().lower()
            if direction not in ("upstream", "downstream", "lateral"):
                direction = "upstream"
            desc = input("  Description: ").strip()
            sla = input("  SLA: ").strip()
            failure = input("  Failure mode: ").strip()
            self.model.dependencies.append(Dependency(name, direction, desc, sla, failure))
            print(f"  Added: {name} ({direction})")

    def _collect_failure_conditions(self):
        print("Define failure conditions: what fails, how detected, impact, recovery.")
        
        while True:
            condition = input("\nFailure condition (empty to finish): ").strip()
            if not condition:
                break
            detection = input("  How detected: ").strip()
            impact = input("  User/System impact: ").strip()
            recovery = input("  Recovery procedure: ").strip()
            self.model.failure_conditions.append(FailureCondition(condition, detection, impact, recovery))
            print(f"  Added: {condition}")

    def _collect_operational_requirements(self):
        print("Define operational requirements with specific targets.")
        defaults = [
            ("Availability", "99.9%", "Uptime monitoring"),
            ("Latency (p99)", "< 200ms", "APM tracing"),
            ("Throughput", "10k req/s", "Load testing"),
            ("Durability", "11 9s", "Backup verification"),
            ("RTO", "< 5 min", "DR drill"),
            ("RPO", "0", "Replication lag monitoring"),
        ]
        
        print("Default operational requirements (press Enter to accept, or modify):")
        for req, target, measurement in defaults:
            use_default = input(f"  {req} [{target}] — {measurement}? [Y/n]: ").strip().lower()
            if use_default != 'n':
                self.model.operational_requirements.append(OperationalRequirement(req, target, measurement))
        
        # Custom requirements
        while True:
            req = input("\nCustom requirement (empty to finish): ").strip()
            if not req:
                break
            target = input("  Target: ").strip()
            measurement = input("  Measurement: ").strip()
            self.model.operational_requirements.append(OperationalRequirement(req, target, measurement))
            print(f"  Added: {req}")

    def export_markdown(self, path: Path):
        """Export problem model as markdown."""
        lines = [
            "# Phase 1 — Independent Problem Model\n",
            f"**Generated**: {self.model.created_at}",
            f"**Version**: {self.model.version}\n",
            "## Problem Statement",
            self.model.problem_statement or "[Not provided]",
            "",
            "## Goals",
        ]
        
        for priority in ["primary", "secondary", "tertiary"]:
            goals = [g for g in self.model.goals if g.priority == priority]
            if goals:
                lines.append(f"### {priority.capitalize()}")
                for g in goals:
                    lines.append(f"- **{g.description}**")
                    lines.append(f"  - Success criterion: {g.success_criterion}")
                lines.append("")
        
        lines.append("## Constraints")
        for c in self.model.constraints:
            lines.append(f"- **[{c.type.upper()}]** {c.description} ({c.category})")
        lines.append("")
        
        lines.append("## Invariants")
        for inv in self.model.invariants:
            lines.append(f"- {inv.description}")
            lines.append(f"  - Rationale: {inv.rationale}")
        lines.append("")
        
        lines.append("## Non-Goals")
        for ng in self.model.non_goals:
            lines.append(f"- {ng}")
        lines.append("")
        
        lines.append("## Actors")
        lines.append("| Actor | Type | Responsibilities | Interactions |")
        lines.append("|-------|------|------------------|--------------|")
        for a in self.model.actors:
            lines.append(f"| {a.name} | {a.type} | {', '.join(a.responsibilities)} | {', '.join(a.interactions)} |")
        lines.append("")
        
        lines.append("## Inputs")
        lines.append("| Input | Source | Format | Frequency | SLA |")
        lines.append("|-------|--------|--------|-----------|-----|")
        for i in self.model.inputs:
            lines.append(f"| {i.name} | {i.source_or_consumer} | {i.format} | {i.frequency} | {i.sla} |")
        lines.append("")
        
        lines.append("## Outputs")
        lines.append("| Output | Consumer | Format | Frequency | SLA |")
        lines.append("|--------|----------|--------|-----------|-----|")
        for o in self.model.outputs:
            lines.append(f"| {o.name} | {o.source_or_consumer} | {o.format} | {o.frequency} | {o.sla} |")
        lines.append("")
        
        lines.append("## State")
        lines.append("| State Entity | Persistence | Consistency | Access Pattern |")
        lines.append("|--------------|-------------|-------------|----------------|")
        for s in self.model.state:
            lines.append(f"| {s.name} | {s.persistence} | {s.consistency} | {s.access_pattern} |")
        lines.append("")
        
        lines.append("## Dependencies")
        lines.append("| Dependency | Direction | Description | SLA | Failure Mode |")
        lines.append("|------------|-----------|-------------|-----|--------------|")
        for d in self.model.dependencies:
            lines.append(f"| {d.name} | {d.direction} | {d.description} | {d.sla} | {d.failure_mode} |")
        lines.append("")
        
        lines.append("## Failure Conditions")
        lines.append("| Condition | Detection | Impact | Recovery |")
        lines.append("|-----------|-----------|--------|----------|")
        for f in self.model.failure_conditions:
            lines.append(f"| {f.condition} | {f.detection} | {f.impact} | {f.recovery} |")
        lines.append("")
        
        lines.append("## Operational Requirements")
        lines.append("| Requirement | Target | Measurement |")
        lines.append("|-------------|--------|-------------|")
        for o in self.model.operational_requirements:
            lines.append(f"| {o.requirement} | {o.target} | {o.measurement} |")
        
        path.write_text("\n".join(lines))

    def export_json(self, path: Path):
        """Export problem model as JSON."""
        path.write_text(json.dumps(asdict(self.model), indent=2))


def main():
    parser = argparse.ArgumentParser(description="Independent Problem Reconstruction Questionnaire")
    parser.add_argument("-o", "--output", default="./Phase1_Independent_Problem_Model.md", help="Output file")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--non-interactive", action="store_true", help="Load from JSON file instead of interactive")
    parser.add_argument("--input", help="JSON input file for non-interactive mode")
    args = parser.parse_args()

    reconstructor = ProblemReconstructor()

    if args.non_interactive and args.input:
        with open(args.input) as f:
            data = json.load(f)
        reconstructor.model = ProblemModel(**data)
    else:
        reconstructor.run_interactive()

    output_path = Path(args.output)
    if args.format == "json":
        reconstructor.export_json(output_path)
    else:
        reconstructor.export_markdown(output_path)
    
    print(f"\n✅ Problem model saved to: {output_path}")


if __name__ == "__main__":
    main()
