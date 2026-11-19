# ITAI-2374 Robotics & Artificial Intelligence Portfolio

**Student:** Maria Jose Viveros Riquelme  
**Course:** ITAI-2374 — Robot Operating Systems & Platforms  
**Platform:** SunFounder PiDog V2 with Raspberry Pi

## Overview

This repository documents coursework, laboratory experiments, the midterm demonstration, and the final robotics project. It separates source code, experimental evidence, reports, and project documentation to make the work easier to review and reproduce.

> **Work in progress.** Directories are being prepared; code, results, and evidence will be added only after review.

## Repository structure

| Directory | Purpose |
| --- | --- |
| [Assignments](Assignments/) | Written assignments and course exercises |
| [Labs](Labs/) | Laboratory work, scripts, observations, and reports |
| [Midterm_Project](Midterm_Project/) | PiDog assembly, calibration, demonstrations, and evaluation evidence |
| [Final_Project](Final_Project/) | Final PiDog project: design, implementation, testing, and demonstration |
| [Documentation](Documentation/) | Hardware notes, setup procedures, troubleshooting, and references |

## Robotics platform

- **Robot:** SunFounder PiDog V2
- **Compute:** Raspberry Pi 5
- **Programming:** Python
- **Working capabilities:** Movement, camera-based computer vision, microphone/speech processing, ultrasonic distance sensing, touch interactions
- **Known hardware limitations:** IMU SH3001 and RGB strip initialization have failed during testing. Project code must not depend on either component unless they are independently verified as working.

## Final project — planned scope

The final project is being developed around a voice- and vision-assisted interactive PiDog. Candidate components include:

- English and Spanish voice interaction
- Camera-based gesture recognition
- PiDog motion and personalized behavior
- Ultrasonic-distance safety behavior
- Documentation of limitations and live-demo results

These are **planned features, not claims of completed functionality**.

## Evidence and reproducibility

Each lab or project section will distinguish objective, setup, procedure, observed results, evidence, troubleshooting, and conclusions. Screenshots and videos will be linked when available.

## Security

Do **not** commit OpenAI API keys, access tokens, passwords, private configuration files, or personal records. Review all scripts and screenshots before publishing. The repository's `.gitignore` helps prevent accidental inclusion, but it does not replace a manual security check.

## References

- [SunFounder PiDog documentation](https://docs.sunfounder.com/projects/pidog/en/latest/)

---

*Academic coursework portfolio — under development.*
