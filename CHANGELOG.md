# Changelog

## 6.1.1 - Unreleased

- Fixed `AlterField` operations that require a `USING` cast when a column's
  data type changes (e.g. `TextField` to `JSONField`).

## 6.1 - 2026-08-07

Initial release for Django 6.1.x and CockroachDB 24.3.x, 25.2.x, 25.4.x,
26.2.x, and 26.3.x.
