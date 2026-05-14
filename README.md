# ADAS Risk Prediction
## Scenario-Based Driver Intent & Risk Prediction using Synthetic Traffic Simulation and Temporal Deep Learning

<img width="626" height="429" alt="image" src="https://github.com/user-attachments/assets/26e3834d-e5de-4d9a-b253-5110152e7846" />

---

# Overview

This project explores trajectory-based driver intent prediction and anticipatory risk estimation using synthetic highway interaction scenarios.

Using OpenSCENARIO/OpenDRIVE simulation and temporal deep learning, the framework generates structured traffic interactions, extracts temporal vehicle trajectories, and studies whether behaviors learned in simulation can generalize to real-world traffic.

Current focus areas:
- trajectory-based interaction modeling
- driver intent prediction
- dangerous maneuver anticipation
- uncertainty-aware behavior generation
- sim-to-real transfer

---

# Current Status

## Completed

- OpenSCENARIO + esmini simulation pipeline
- Procedural highway scenario generation
- Multiple interaction families:
  - safe_merge
  - aggressive_cutin
  - hesitant_merge
  - aborted_merge
  - fake_drift
  - oscillatory_indecision
  - dense_pressure
- Headless simulation execution
- Temporal trajectory logging
- `.dat → CSV` trajectory extraction pipeline
- Professional BEV trajectory visualization system
- Initial synthetic dataset generation framework

---

## Current Challenges / Next Steps

The infrastructure pipeline is functional, but current behavior families are still too simplistic and geometrically similar.

<img width="4571" height="1118" alt="image" src="https://github.com/user-attachments/assets/5889482e-6aa1-4af5-9974-8e699e59dcb6" />



Main research problems currently being addressed:

- Designing behaviorally distinct trajectory families
- Modeling realistic uncertainty and hesitation
- Creating multi-stage temporal interaction policies
- Generating ambiguous driver intent patterns
- Adding interaction-aware traffic dynamics
- Improving realism of lane-change behaviors
- Building meaningful temporal learning signals instead of metadata-only labels

Future work includes:
- trajectory primitive engine
- multi-agent interaction modeling
- transformer-based temporal learning
- uncertainty-aware prediction
- sim-to-real transfer evaluation using highD

---

# Research Goals

The project focuses on four main directions:

## 1. Synthetic Interaction Generation
Generate structured highway interaction scenarios using OpenSCENARIO/OpenDRIVE.

Examples:
- aggressive cut-ins
- hesitant merges
- aborted lane changes
- fake merge drifts
- dense traffic pressure scenarios

---

## 2. Temporal Behavior Learning
Learn interaction dynamics between vehicles over time using sequential deep learning models.

Planned models:
- LSTM
- GRU
- Temporal Transformers
- Multi-agent encoders

---

## 3. Anticipatory Risk Prediction
Predict dangerous maneuvers before they fully unfold.

Example:
> Will a neighboring vehicle perform a dangerous merge within the next 2 seconds?

---

## 4. Sim-to-Real Transfer
Evaluate whether synthetic trajectory-based behavior learning transfers to real-world highway traffic behavior.

Real-world validation will use the highD dataset.

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

# Project Structure

```text
adas-risk-prediction/
│
├── scenarios/
├── src/
│   ├── simulation/
│   ├── preprocessing/
│   ├── models/
│   ├── training/
│   └── visualization/
│
├── outputs/
│   ├── logs/
│   ├── trajectory_csv/
│   └── figures/
│
├── data/
├── experiments/
└── docs/
