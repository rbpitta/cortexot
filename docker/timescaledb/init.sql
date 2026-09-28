-- CortexOT TimescaleDB bootstrap (Phase 0)
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Application schema placeholder for later phases
CREATE SCHEMA IF NOT EXISTS cortexot;

COMMENT ON SCHEMA cortexot IS 'CortexOT application objects (tables/hypertables added in Phase 1+)';
