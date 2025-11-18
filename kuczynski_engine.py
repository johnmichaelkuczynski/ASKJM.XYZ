"""
Kuczynski Inference Rule Engine (KIRE)
Converts user input into chain of savage Kuczynski deductions
"""
import json
import re
from typing import List, Dict

class KuczynskiEngine:
    def __init__(self, rules_path='kuczynski_rules_full.json'):
        """Load inference rules once"""
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)
        print(f"✓ KIRE loaded with {len(self.rules)} inference rules")
    
    def deduce(self, phenomenon: str, max_rules: int = 18) -> List[Dict]:
        """
        Execute Kuczynski inference engine on phenomenon
        
        Args:
            phenomenon: User's input text
            max_rules: Maximum number of rules to fire (default 18)
        
        Returns:
            List of fired rules sorted by strength (most savage first)
        """
        activated = []
        text = phenomenon.lower()
        conclusions_text = ""  # Accumulate conclusions for chaining
        
        for rule in self.rules:
            # Search in original phenomenon + accumulated conclusions (chaining)
            search_space = text + " " + conclusions_text
            
            try:
                if re.search(rule["premise"], search_space, re.IGNORECASE):
                    activated.append(rule)
                    conclusions_text += " " + rule["conclusion"].lower()
            except re.error:
                # Skip rules with malformed regex
                continue
        
        # Sort by strength descending (most totalizing/savage claims first)
        activated.sort(key=lambda r: -r["strength"])
        
        return activated[:max_rules]
    
    def format_chain(self, fired_rules: List[Dict]) -> str:
        """Format fired rules as Kuczynski-style prose"""
        if not fired_rules:
            return "No relevant deductions triggered."
        
        lines = []
        for rule in fired_rules:
            year = rule.get('year', 2025)
            conclusion = rule['conclusion']
            lines.append(f"Consider the proposition that {conclusion} ({year})")
        
        return "\n\n".join(lines) + "\n\nThe prophecy is therefore unavoidable."


# Standalone function for quick testing
def kuczynski_think(phenomenon: str, max_rules=18) -> str:
    """Quick inference without instantiating engine"""
    with open('kuczynski_rules_full.json', 'r') as f:
        rules = json.load(f)
    
    activated = []
    text = phenomenon.lower()
    
    for rule in rules:
        try:
            if re.search(rule["premise"], text, re.IGNORECASE):
                activated.append(rule)
        except re.error:
            continue
    
    activated.sort(key=lambda r: -r["strength"])
    
    chain = [f"Consider the proposition that {rule['conclusion']} ({rule.get('year', 2025)})" 
             for rule in activated[:max_rules]]
    
    return "\n\n".join(chain) + "\n\nThe prophecy is therefore unavoidable."
