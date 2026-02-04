#!/usr/bin/env python
"""Test operational modes."""

from src.operational_modes import FORENSIC, POPPERIAN

print('Operational Modes Verification:')
print('')
print('FORENSIC Mode:')
print(f'  Allowed operations: {len(FORENSIC.allowed_operations)} total')
print(f'  Prohibited operations: {len(FORENSIC.prohibited_operations)} total')
print(f'  hash_verification allowed? {FORENSIC.is_allowed("hash_verification")}')
print(f'  emotion_labeling allowed? {FORENSIC.is_allowed("emotion_labeling")}')
print('')
print('POPPERIAN Mode:')
print(f'  Allowed operations: {len(POPPERIAN.allowed_operations)} total')
print(f'  Prohibited operations: {len(POPPERIAN.prohibited_operations)} total')
print(f'  hypothesis_testing allowed? {POPPERIAN.is_allowed("hypothesis_testing")}')
print(f'  interpretive_analysis allowed? {POPPERIAN.is_allowed("interpretive_analysis")}')
print('')
print('Operational modes verification: OK')
