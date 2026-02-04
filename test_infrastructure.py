#!/usr/bin/env python
"""Test infrastructure registry loading."""

from src.infrastructure import registry

print('Infrastructure Registry Verification:')
print('')
print(f'  Compute nodes: {registry.compute_nodes["count"]}')
print(f'  Energy sources: {registry.energy_sources["count"]}')
print(f'  Satellites: {registry.satellite_nervous_system["count"]}')
print(f'  Logic layers: {registry.logic_layers["count"]}')
print('')
print('Registry verification: OK')
