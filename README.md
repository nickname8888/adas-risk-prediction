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
    <img width="4571" height="1158" alt="image" src="https://github.com/user-attachments/assets/a9c17e18-1d28-4a1d-bd5a-5232ad5f49d4" />

  - aggressive_cutin
    <img width="4571" height="1016" alt="image" src="https://github.com/user-attachments/assets/7aab6117-fe2a-4ac6-be71-a57f93ed62ae" />

  - cooperative_yield
    <img width="4571" height="1158" alt="image" src="https://github.com/user-attachments/assets/30655076-4aa2-4527-a071-1974a8c5b403" />
 
  - hesitant_merge
    <img width="4635" height="1283" alt="image" src="https://github.com/user-attachments/assets/ba503b98-4eda-4904-b243-cd04d43326b6" />

  - aborted_merge
    <img width="4571" height="1053" alt="image" src="https://github.com/user-attachments/assets/abf4fb79-c249-4702-88af-3012c564bbbe" />

  - fake_drift
    <img width="4571" height="1052" alt="image" src="https://github.com/user-attachments/assets/8fec785b-11d5-4f71-bbcc-7210f859d698" />

  - oscillatory_indecision
    <img width="4571" height="1137" alt="image" src="https://github.com/user-attachments/assets/4ec3d3db-70cf-484e-82ef-7d11f7e7fa5d" />

  - dense_pressure (still need to add configs for more cars and obstacles so output is incomplete)
    <img width="4571" height="1043" alt="image" src="https://github.com/user-attachments/assets/c4ecc92f-9f0b-4854-bfd9-0a8e7b21f0f7" />

- Fixed OpenSCENARIO trajectory-following integration in esmini
- Correct vehicle heading + steering-aligned trajectory execution
- Functional lane-change visualization in simulation
- End-to-end trajectory → OpenSCENARIO → esmini validation
- Headless simulation execution
- Temporal trajectory logging
- `.dat → CSV` trajectory extraction pipeline
- Professional BEV trajectory visualization system
- Initial synthetic dataset generation framework
- Family-balanced synthetic scenario generation pipeline
- Current execution pipeline:
  - `python3 -m src.trajectory.generate_dataset 1`
  - `python3 -m src.simulation.generate_dataset`
- Established complete trajectory generation → scenario conversion → simulation workflow
- Began iterative experimentation pipeline for improving realism and behavioral diversity of generated outputs

---

## Current Challenges / Next Steps

The infrastructure pipeline is now fully functional end-to-end, including procedural trajectory generation, OpenSCENARIO export, and realistic lane-following execution inside esmini.

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
