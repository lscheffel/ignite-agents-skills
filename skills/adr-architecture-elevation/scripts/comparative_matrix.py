#!/usr/bin/env python3
"""
Comparative Evaluation Matrix Helper

Supports Phase 4: scoring, weighting, visualization, and sensitivity analysis.
"""

import argparse
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class Criterion(Enum):
    CORRECTNESS = "correctness"
    COMPLEXITY = "complexity"
    ROBUSTNESS = "robustness"
    TESTABILITY = "testability"
    OPERABILITY = "operability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    COST = "cost"
    REVERSIBILITY = "reversibility"
    OPERATIONAL_COMPLEXITY = "operational_complexity"


# Default weights (must sum to 1.0)
DEFAULT_WEIGHTS = {
    Criterion.CORRECTNESS: 0.25,
    Criterion.COMPLEXITY: 0.01,  # Inverse - lower is better
    Criterion.ROBUSTNESS: 0.20,
    Criterion.TESTABILITY: 0.10,
    Criterion.OPERABILITY: 0.15,
    Criterion.PERFORMANCE: 0.05,
    Criterion.SECURITY: 0.10,
    Criterion.MAINTAINABILITY: 0.08,
    Criterion.COST: 0.04,
    Criterion.REVERSIBILITY: 0.02,
    Criterion.OPERATIONAL_COMPLEXITY: 0.01,  # Inverse - lower is better
}

# Criteria where LOWER score is better (inverse weighting)
INVERSE_CRITERIA = {Criterion.COMPLEXITY, Criterion.OPERATIONAL_COMPLEXITY}


@dataclass
class Score:
    criterion: Criterion
    alternative: str
    value: int  # 1-5
    evidence: str
    weight: float


@dataclass
class AlternativeResult:
    name: str
    scores: Dict[Criterion, Score]
    weighted_total: float


class ComparativeMatrix:
    def __init__(self, weights: Optional[Dict[Criterion, float]] = None):
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.alternatives: Dict[str, Dict[Criterion, Score]] = {}
        self._validate_weights()

    def _validate_weights(self):
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def add_score(self, alternative: str, criterion: Criterion, value: int, evidence: str):
        if alternative not in self.alternatives:
            self.alternatives[alternative] = {}
        weight = self.weights.get(criterion, 0.0)
        self.alternatives[alternative][criterion] = Score(
            criterion=criterion,
            alternative=alternative,
            value=value,
            evidence=evidence,
            weight=weight
        )

    def calculate_totals(self) -> Dict[str, AlternativeResult]:
        results = {}
        for alt_name, scores in self.alternatives.items():
            total = 0.0
            for criterion, score in scores.items():
                # Apply inverse weighting for complexity criteria
                effective_value = score.value
                if criterion in INVERSE_CRITERIA:
                    effective_value = 6 - score.value  # Invert 1-5 to 5-1
                total += effective_value * score.weight * 5  # Normalize to 25 max per criterion
            results[alt_name] = AlternativeResult(
                name=alt_name,
                scores=scores,
                weighted_total=total
            )
        return results

    def get_winner(self) -> Optional[str]:
        results = self.calculate_totals()
        if not results:
            return None
        return max(results.items(), key=lambda x: x[1].weighted_total)[0]

    def check_vetos(self) -> List[str]:
        """Check for any criterion scored 1 (Critical) - automatic veto."""
        vetos = []
        for alt_name, scores in self.alternatives.items():
            for criterion, score in scores.items():
                if score.value == 1:
                    vetos.append(f"{alt_name}: {criterion.value} scored 1 (Critical)")
        return vetos

    def sensitivity_analysis(self, variation: float = 0.1) -> Dict[str, List[str]]:
        """Test how winner changes with ±weight variations."""
        original_winner = self.get_winner()
        results = {"original_winner": original_winner, "variations": {}}
        
        for criterion in self.weights:
            # Test increasing this weight
            modified_weights = self.weights.copy()
            modified_weights[criterion] *= (1 + variation)
            # Renormalize
            total = sum(modified_weights.values())
            modified_weights = {k: v/total for k, v in modified_weights.items()}
            
            matrix = ComparativeMatrix(modified_weights)
            matrix.alternatives = self.alternatives
            new_winner = matrix.get_winner()
            results["variations"][f"{criterion.value}+{int(variation*100)}%"] = new_winner
            
            # Test decreasing this weight
            modified_weights = self.weights.copy()
            modified_weights[criterion] *= (1 - variation)
            total = sum(modified_weights.values())
            modified_weights = {k: v/total for k, v in modified_weights.items()}
            
            matrix = ComparativeMatrix(modified_weights)
            matrix.alternatives = self.alternatives
            new_winner = matrix.get_winner()
            results["variations"][f"{criterion.value}-{int(variation*100)}%"] = new_winner
        
        return results

    def export_csv(self, path: Path):
        """Export matrix to CSV for spreadsheet analysis."""
        results = self.calculate_totals()
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            # Header
            criteria = list(Criterion)
            header = ["Alternative"] + [c.value for c in criteria] + ["Weighted Total"]
            writer.writerow(header)
            
            for alt_name, result in results.items():
                row = [alt_name]
                for c in criteria:
                    score = result.scores.get(c)
                    row.append(score.value if score else "")
                row.append(f"{result.weighted_total:.2f}")
                writer.writerow(row)

    def export_json(self, path: Path):
        """Export full matrix with evidence to JSON."""
        data = {
            "weights": {k.value: v for k, v in self.weights.items()},
            "alternatives": {}
        }
        for alt_name, scores in self.alternatives.items():
            data["alternatives"][alt_name] = {
                c.value: {"value": s.value, "evidence": s.evidence, "weight": s.weight}
                for c, s in scores.items()
            }
        data["results"] = {
            name: {"weighted_total": r.weighted_total}
            for name, r in self.calculate_totals().items()
        }
        data["winner"] = self.get_winner()
        data["vetos"] = self.check_vetos()
        data["sensitivity"] = self.sensitivity_analysis()
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def render_markdown(self) -> str:
        """Render matrix as markdown table."""
        results = self.calculate_totals()
        criteria = list(Criterion)
        
        lines = ["# Comparative Evaluation Matrix\n"]
        
        # Weight row
        weight_row = "| Criterion | Weight |" + " | ".join(results.keys()) + " | Winner |"
        lines.append(weight_row)
        lines.append("|" + "---|" * (len(results) + 3))
        
        for criterion in criteria:
            row = f"| {criterion.value} | {self.weights.get(criterion, 0):.0%} |"
            scores = []
            for alt_name in results:
                score = results[alt_name].scores.get(criterion)
                row += f" {score.value if score else '—'} |"
                scores.append((alt_name, score.value if score else 0))
            
            # Determine winner for this criterion (higher is better, except inverse)
            if scores:
                if criterion in INVERSE_CRITERIA:
                    winner = min(scores, key=lambda x: x[1])[0]
                else:
                    winner = max(scores, key=lambda x: x[1])[0]
                row += f" {winner} |"
            lines.append(row)
        
        # Total row
        total_row = "| **WEIGHTED TOTAL** | **100%** |"
        for alt_name in results:
            total_row += f" **{results[alt_name].weighted_total:.2f}** |"
        total_row += f" **{self.get_winner()}** |"
        lines.append(total_row)
        
        # Vetos
        vetos = self.check_vetos()
        if vetos:
            lines.append("\n## ⚠️ Vetoes (Critical Scores)")
            for v in vetos:
                lines.append(f"- {v}")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Comparative Evaluation Matrix Tool")
    parser.add_argument("--input", help="JSON input file with scores")
    parser.add_argument("--output", help="Output file (markdown, csv, or json)")
    parser.add_argument("--format", choices=["md", "csv", "json"], default="md")
    parser.add_argument("--weights", help="JSON file with custom weights")
    parser.add_argument("--sensitivity", action="store_true", help="Run sensitivity analysis")
    args = parser.parse_args()

    weights = None
    if args.weights:
        with open(args.weights) as f:
            raw = json.load(f)
        weights = {Criterion(k): v for k, v in raw.items()}

    matrix = ComparativeMatrix(weights)

    if args.input:
        with open(args.input) as f:
            data = json.load(f)
        for alt_name, scores in data.get("alternatives", {}).items():
            for criterion_name, score_data in scores.items():
                matrix.add_score(
                    alt_name,
                    Criterion(criterion_name),
                    score_data["value"],
                    score_data.get("evidence", "")
                )

    if args.output:
        path = Path(args.output)
        if args.format == "csv":
            matrix.export_csv(path)
        elif args.format == "json":
            matrix.export_json(path)
        else:
            path.write_text(matrix.render_markdown())
    else:
        print(matrix.render_markdown())
        if args.sensitivity:
            print("\n## Sensitivity Analysis")
            sens = matrix.sensitivity_analysis()
            print(f"Original winner: {sens['original_winner']}")
            for var, winner in sens['variations'].items():
                print(f"  {var}: {winner}")


if __name__ == "__main__":
    main()
