# 🔬 Theoretical Memo: Computational Attribution in Maritime Gray-Zone Warfare
**Project:** Computational Attribution and Signaling: A Cross-Theater Empirical Study
**Researcher:** [Chenke(Alex) Bai]
**Date:** January 2026
**Phase:** I - Theoretical Framework & Metric Engineering

---
s
## 1. Research Objectives
* **RQ1:** How can "gray-zone" provocations be computationally identified in the absence of formal declarations of intent?
* **RQ2:** To what extent can physical constraints (**Indices**) be used to cross-validate or debunk manipulated sensory data (**Signals**)?
* **RQ3:** How do attribution models trained on North Sea critical infrastructure incidents generalize to the Caribbean theater?

---

## 2. Theoretical Framework: Jervis’s Signaling Theory
This research operationalizes **Robert Jervis’s (1970)** seminal work, *The Logic of Images in International Relations*, to categorize maritime data streams:

### 2.1 Signals vs. Indices
* **Signals (Manipulable):**
    * *Definition*: Statements or actions issued by an actor to influence the receiver's perception. These are inherently subject to deception as they are under the actor's direct control.
    * *Operationalization*: **AIS (Automatic Identification System) Data**. Ship identity, GPS coordinates, and destination status are "Signals" that can be spoofed or "darkened" (AIS disabling) to create strategic ambiguity.
* **Indices (Inherent/Physical):**
    * *Definition*: Traits or behaviors that the receiver believes are beyond the actor's ability to manipulate for deceptive purposes.
    * *Operationalization*: 
        1. **SAR (Synthetic Aperture Radar) Imagery**: Direct physical evidence of vessel presence/dimensions regardless of AIS status.
        2. **Kinematic Constraints**: Vessel maneuverability limits (max speed/turning radius) dictated by hydrodynamics and engine specifications.
        3. **Corporate Linkage**: Ownership structures retrieved via OpenCorporates API, revealing underlying state-actor affiliations.

### 2.2 Theoretical Logic for Feature Weighting
> **Guiding Principle**: The model shall implement a **Reliability Hierarchy**. When a conflict occurs between a Signal (AIS) and an Index (SAR/Kinematics), the Index is assigned a higher confidence weight in the attribution algorithm.

---

## 3. Core Research Hypotheses (H)

### 🟢 H1: Signal-Index Inconsistency Hypothesis
Gray-zone provocations (e.g., subsea cable interference) are preceded by a statistically significant divergence between a vessel's **declared signal (AIS)** and its **physical index (SAR/Kinematics)**.
* *Metric*: Deviation $\Delta P = |Pos_{AIS} - Pos_{SAR}|$.

### 🔵 H2: Spatial Fingerprint & Non-Economic Trajectory Hypothesis
Interference activities exhibit "non-economic" spatio-temporal signatures—characterized by localized loitering and velocity outliers ($V_d$)—that deviate from the historical baseline of commercial/fishing traffic in critical infrastructure zones.
* *Metric*: High-density dwell time ($S_{dur}$) combined with kinematic anomaly scores.

### 🔴 H3: Attribution Latency & Deterrence Hypothesis
The automated integration of **Ownership Linkage** (mapping technical IDs to political entities) reduces the "Attribution Gap," thereby increasing the perceived cost for the aggressor and enhancing the deterrent effect of digital situational awareness.

---

## 4. Academic Milestones & Literature Mapping
- [ ] **Jervis (1970)**: Extract formal logic for "Costly Signaling" to weigh deceptive vs. honest behavior.
- [ ] **Gartzke & Lindsay (2015)**: Define "Attribution Uncertainty" as a variable in the escalation of cyber-physical conflicts.
-