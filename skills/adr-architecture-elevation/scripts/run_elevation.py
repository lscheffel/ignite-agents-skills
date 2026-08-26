#!/usr/bin/env python3
"""
ADR Architecture Elevation — Pipeline Orchestrator

Orchestrates the 8-phase architecture elevation pipeline.
Manages state, coordinates phase execution, produces final report package.
"""

import argparse
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class PhaseStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PhaseResult:
    phase: int
    name: str
    status: PhaseStatus
    output_path: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class ElevationConfig:
    input_dir: Path
    output_dir: Path
    problem_model_hash: Optional[str] = None
    weight_overrides: Optional[Dict[str, float]] = None
    skip_phases: Optional[List[int]] = None
    only_phases: Optional[List[int]] = None


class ElevationPipeline:
    def __init__(self, config: ElevationConfig):
        self.config = config
        self.phases = [
            (1, "Independent Problem Model", self.phase1_problem_model),
            (2, "Existing Decision Set Audit", self.phase2_audit),
            (3, "Architecture Challenge", self.phase3_challenge),
            (4, "Comparative Evaluation", self.phase4_evaluation),
            (5, "Amplification Register", self.phase5_amplification),
            (6, "Decision", self.phase6_decision),
            (7, "Hardened Decision Set", self.phase7_hardened),
            (8, "Re-Audit", self.phase8_reaudit),
        ]
        self.results: List[PhaseResult] = []
        self.state: Dict[str, Any] = {}

    def run(self) -> bool:
        """Execute the full pipeline. Returns True if successful."""
        print("=" * 60)
        print("ADR Architecture Elevation Pipeline")
        print("=" * 60)

        # Setup output directory
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        # Determine which phases to run
        phases_to_run = self._filter_phases()

        for phase_num, phase_name, phase_func in phases_to_run:
            if phase_num in (self.config.skip_phases or []):
                self.results.append(PhaseResult(phase_num, phase_name, PhaseStatus.SKIPPED))
                print(f"\n[SKIP] Phase {phase_num}: {phase_name}")
                continue

            print(f"\n[RUN] Phase {phase_num}: {phase_name}")
            self.results.append(PhaseResult(phase_num, phase_name, PhaseStatus.IN_PROGRESS))

            try:
                result = phase_func()
                self.results[-1] = PhaseResult(
                    phase_num, phase_name, PhaseStatus.COMPLETED,
                    output_path=result.get("output_path"),
                    metadata=result.get("metadata")
                )
                print(f"[OK] Phase {phase_num} completed")
            except Exception as e:
                self.results[-1] = PhaseResult(
                    phase_num, phase_name, PhaseStatus.FAILED, error=str(e)
                )
                print(f"[FAIL] Phase {phase_num} failed: {e}")
                if not self._should_continue_on_failure(phase_num):
                    break

        # Generate executive summary
        self._generate_executive_summary()

        # Print final status
        self._print_summary()
        return all(r.status in (PhaseStatus.COMPLETED, PhaseStatus.SKIPPED) for r in self.results)

    def _filter_phases(self) -> List[tuple]:
        if self.config.only_phases:
            return [(n, name, fn) for n, name, fn in self.phases if n in self.config.only_phases]
        return self.phases

    def _should_continue_on_failure(self, phase_num: int) -> bool:
        # Phases 1-2 are prerequisites; 3-5 can sometimes continue; 6-8 need prior success
        return phase_num <= 2

    def _generate_executive_summary(self):
        """Generate the executive summary document."""
        summary_path = self.config.output_dir / "EXECUTIVE_SUMMARY.md"
        with open(summary_path, "w") as f:
            f.write(self._build_executive_summary())

    def _build_executive_summary(self) -> str:
        decision = "UNKNOWN"
        for r in self.results:
            if r.phase == 6 and r.metadata:
                decision = r.metadata.get("decision", "UNKNOWN")

        return f"""# Architecture Elevation — Executive Summary

## Decision Set
**Original**: [ADR ID / Title]
**Elevated**: HARDENED-v1
**Date**: {datetime.now().strftime('%Y-%m-%d')}

## Verdict
**Decision**: {decision}
**Certification**: PENDING_REAUDIT

## Key Findings
- Phase 1: Independent problem model reconstructed
- Phase 2: Audit completed with findings
- Phase 3: Architecture challenge explored alternatives
- Phase 4: Comparative evaluation scored alternatives
- Phase 5: Amplification register created
- Phase 6: Decision: {decision}
- Phase 7: Hardened decision set produced
- Phase 8: Re-audit pending

## Amplifications Applied
- [To be populated from Phase 5 results]

## Risk Reduction
| Risk | Before | After |
|------|--------|-------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] |

## Complexity Impact
**Original**: [Score]
**Hardened**: [Score]
**Delta**: [+/- with justification]

## Recommendation
[To be populated after Phase 8 re-audit]

## Artifacts Produced
- Phase 1-8 reports: {self.config.output_dir}
- Hardened Decision Set: {self.config.output_dir}/Phase7_Hardened_Decision_Set/
- This Summary: {summary_path}
"""

    def _print_summary(self):
        print("\n" + "=" * 60)
        print("PIPELINE SUMMARY")
        print("=" * 60)
        for r in self.results:
            status_icon = {
                PhaseStatus.COMPLETED: "✅",
                PhaseStatus.FAILED: "❌",
                PhaseStatus.SKIPPED: "⏭️",
                PhaseStatus.IN_PROGRESS: "🔄",
                PhaseStatus.PENDING: "⏳"
            }[r.status]
            print(f"  {status_icon} Phase {r.phase}: {r.name} — {r.status.value}")
            if r.error:
                print(f"      Error: {r.error}")

    # Phase implementations (stubs - would be implemented with actual logic)
    def phase1_problem_model(self) -> Dict:
        output_path = self.config.output_dir / "Phase1_Independent_Problem_Model.md"
        output_path.write_text("# Phase 1 — Independent Problem Model\n\n[Generated by pipeline]")
        self.state["problem_model_path"] = str(output_path)
        return {"output_path": str(output_path), "metadata": {"hash": self._hash_file(output_path)}}

    def phase2_audit(self) -> Dict:
        output_path = self.config.output_dir / "Phase2_Audit_Report.md"
        output_path.write_text("# Phase 2 — Audit Report\n\n[Generated by pipeline]")
        return {"output_path": str(output_path)}

    def phase3_challenge(self) -> Dict:
        output_path = self.config.output_dir / "Phase3_Architecture_Challenge.md"
        output_path.write_text("# Phase 3 — Architecture Challenge\n\n[Generated by pipeline]")
        return {"output_path": str(output_path)}

    def phase4_evaluation(self) -> Dict:
        output_path = self.config.output_dir / "Phase4_Comparative_Evaluation.md"
        output_path.write_text("# Phase 4 — Comparative Evaluation\n\n[Generated by pipeline]")
        return {"output_path": str(output_path)}

    def phase5_amplification(self) -> Dict:
        output_path = self.config.output_dir / "Phase5_Amplification_Register.md"
        output_path.write_text("# Phase 5 — Amplification Register\n\n[Generated by pipeline]")
        return {"output_path": str(output_path)}

    def phase6_decision(self) -> Dict:
        output_path = self.config.output_dir / "Phase6_Decision.md"
        decision = "KEEP + AMPLIFY"
        content = f"""# Phase 6 — Decision

## Decision
**Outcome**: {decision}

## Justification
[Evidence-based rationale referencing Phase 2, 3, 4, 5]
"""
        output_path.write_text(content)
        return {"output_path": str(output_path), "metadata": {"decision": decision}}

    def phase7_hardened(self) -> Dict:
        hardened_dir = self.config.output_dir / "Phase7_Hardened_Decision_Set"
        hardened_dir.mkdir(exist_ok=True)
        
        for artifact in ["ADR-HARDENED.md", "BP-HARDENED.md", "PI-HARDENED.md", "TODO-HARDENED.md"]:
            (hardened_dir / artifact).write_text(f"# {artifact}\n\n[Hardened artifact]")
        
        return {"output_path": str(hardened_dir), "metadata": {"artifacts": 4}}

    def phase8_reaudit(self) -> Dict:
        output_path = self.config.output_dir / "Phase8_Reaudit_Report.md"
        output_path.write_text("# Phase 8 — Re-Audit Report\n\n[Generated by pipeline]")
        return {"output_path": str(output_path)}

    def _hash_file(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description="ADR Architecture Elevation Pipeline")
    parser.add_argument("input_dir", help="Directory containing ADR Decision Set (ADR.md, BP.md, PI.md, TODO.md)")
    parser.add_argument("-o", "--output", default="./architecture-elevation-report", help="Output directory")
    parser.add_argument("--skip", type=int, nargs="*", help="Phase numbers to skip")
    parser.add_argument("--only", type=int, nargs="*", help="Run only specific phases")
    parser.add_argument("--weights", help="JSON file with custom criterion weights")
    args = parser.parse_args()

    config = ElevationConfig(
        input_dir=Path(args.input_dir).resolve(),
        output_dir=Path(args.output).resolve(),
        skip_phases=args.skip,
        only_phases=args.only,
        weight_overrides=json.loads(Path(args.weights).read_text()) if args.weights else None,
    )

    pipeline = ElevationPipeline(config)
    success = pipeline.run()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
