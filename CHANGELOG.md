# Changelog

## 6.0.1 - 2026-07-29

- Confirmed support for CockroachDB 26.1.x and 26.2.x (no code changes
  required).

- Added support for CockroachDB 26.3.x. This version of CockroachDB reports
  itself as PostgreSQL 18 (increased from version 13 in prior versions).
  Several Django feature flags are adjusted to account for behavioral
  differences between PostgreSQL and CockroachDB to maintain correct behavior.

## 6.0 - 2025-12-05

Initial release for Django 6.0.x and CockroachDB 24.1.x, 24.3.x, 25.2.x,
25.3.x, and 25.4.x.
