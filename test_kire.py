"""
Test script for Kuczynski Inference Rule Engine (KIRE)
Demonstrates how KIRE converts phenomena into savage Kuczynski deductions
"""
from kuczynski_engine import kuczynski_think, KuczynskiEngine

print("=" * 80)
print("KUCZYNSKI INFERENCE RULE ENGINE (KIRE) - TEST SUITE")
print("=" * 80)

# Initialize engine
kire = KuczynskiEngine()
print(f"\n✓ Loaded {len(kire.rules)} inference rules\n")

# Test cases
test_phenomena = [
    "Neuralink brain-computer interface promises perfect memory instant knowledge telepathic communication merging with AI",
    "Male feminist declares support for gender equality and women's rights",
    "Empirical observation is the only valid source of knowledge",
    "Democracy requires equality and consensus among citizens",
    "Possible worlds semantics provides the best account of modal logic",
    "Probability is just relative frequency of events over time"
]

for i, phenomenon in enumerate(test_phenomena, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}: {phenomenon[:70]}...")
    print('=' * 80)
    
    # Run KIRE
    fired_rules = kire.deduce(phenomenon, max_rules=5)
    
    print(f"\n✓ KIRE fired {len(fired_rules)} rules\n")
    
    # Show deductions
    for j, rule in enumerate(fired_rules, 1):
        print(f"{j}. [{rule['id']}] (strength: {rule['strength']})")
        print(f"   → {rule['conclusion'][:120]}...")
        print()
    
    # Show formatted output
    print("\nFORMATTED OUTPUT:")
    print("-" * 80)
    formatted = kire.format_chain(fired_rules)
    print(formatted[:500] + "...\n" if len(formatted) > 500 else formatted + "\n")

print("\n" + "=" * 80)
print("KIRE TEST SUITE COMPLETE")
print("=" * 80)

# Quick function demo
print("\n\nQUICK FUNCTION DEMO:")
print("-" * 80)
result = kuczynski_think("artificial intelligence consciousness computational theory of mind", max_rules=3)
print(result)
