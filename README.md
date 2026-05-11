# ADAS Risk Prediction
## Scenario-Based Driver Intent & Risk Prediction using Synthetic Traffic Simulation and Temporal Deep Learning

---

# Overview

This project is a research-oriented framework for studying highway driving behavior, anticipatory risk prediction, and sim-to-real transfer in Advanced Driver Assistance Systems (ADAS).

The core idea is to generate structured synthetic traffic interaction scenarios using OpenSCENARIO/OpenDRIVE simulation, learn temporal vehicle interaction dynamics using deep learning, and evaluate whether behaviors learned in simulation transfer to real-world traffic trajectories.

Unlike perception-heavy autonomous driving projects, this work focuses primarily on:

- temporal interaction modeling
- driver intent prediction
- dangerous maneuver anticipation
- trajectory-based reasoning
- synthetic-to-real behavioral transfer

The long-term goal is to investigate:

> Can models trained on structured synthetic highway interactions generalize to real-world driving behavior?

---

# Research Motivation

Modern ADAS and autonomous driving systems struggle with:

- early intent prediction
- ambiguous driver behavior
- rare dangerous scenarios
- lack of edge-case training data
- uncertainty estimation in safety-critical settings

Real-world trajectory datasets are valuable but limited in:

- controllability
- scenario diversity
- automatic labeling
- rare-event coverage

Simulation provides a scalable and controllable alternative.

This project explores whether synthetic interaction dynamics generated in simulation can serve as meaningful priors for real-world driving behavior prediction.

---

# Core Research Objectives

The project focuses on four primary research directions:

## 1. Synthetic Traffic Interaction Generation
Programmatically generate structured highway interaction scenarios using OpenSCENARIO and OpenDRIVE.

Examples:
- aggressive cut-ins
- safe merges
- dangerous lane changes
- hesitant merges
- aborted lane changes

---

## 2. Temporal Behavior Learning
Learn interaction dynamics between vehicles over time using sequential deep learning models.

Initial models:
- LSTM
- GRU
- Temporal encoders

Future extensions:
- Transformer encoders
- Graph Neural Networks
- Multi-agent reasoning

---

## 3. Anticipatory Risk Prediction
Predict dangerous maneuvers *before* they fully unfold.

Example task:

> Will a neighboring vehicle perform a dangerous merge within the next 2 seconds?

This shifts the project from reactive classification toward anticipatory behavioral reasoning.

---

## 4. Sim-to-Real Transfer
Evaluate whether synthetic trajectory-based behavior learning transfers to real-world highway interactions.

Real-world validation will use the highD highway trajectory dataset.

---

# Technology Stack

## Simulation

- OpenSCENARIO
- OpenDRIVE
- esmini
- scenariogeneration

## Machine Learning

- PyTorch
- NumPy
- Pandas
- scikit-learn

## Visualization

- Matplotlib
- Plotly

## Infrastructure

- Python
- Git
- GitHub

---

# Project Architecture

```text
adas-risk-prediction/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── configs/
│
├── scenarios/
│   ├── base/
│   ├── generated/
│   └── templates/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── src/
│   ├── simulation/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── datasets/
│   ├── models/
│   ├── training/
│   ├── evaluation/
│   └── visualization/
│
├── notebooks/
├── experiments/
│
├── outputs/
│   ├── models/
│   ├── figures/
│   └── logs/
│
└── docs/
