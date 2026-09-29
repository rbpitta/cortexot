"""Backward-compatible import path; Phase 1 uses simulator.main for OPC-UA."""

from simulator.simulator_app import create_app

app = create_app()
