# ML Preprocessing Skeleton

## Purpose

This folder contains the initial preprocessing and feature-engineering package for the sensor-fusion model pipeline.

## Current status

This is a skeletal pipeline only. It is intentionally designed to prepare the raw hardware data for future training and evaluation. It does not claim a finished ML model.

## Contents

- `feature_pipeline.py` — validation, session-boundary detection, motion features, electrical features
- `__init__.py` — package marker

## Planned workflow

1. Load real CSV files from `data/raw/tamper_experiments/`
2. Validate required columns
3. Detect resets and session boundaries
4. Compute motion features from MPU6050 values
5. Include electrical measurements as feature inputs
6. Prepare a fused table for EDA and modeling
7. Train a baseline Random Forest after enough real data exists

## TODO

- [TODO] Add session-aware event segmentation.
- [TODO] Add class-balance checks.
- [TODO] Add outlier detection and feature visualization.
- [TODO] Add train/test split and baseline model training.
