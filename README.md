![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F9%9F%A4%97-Hugging%20Face-FFD21E)
![Meta](https://img.shields.io/badge/Meta-0081FB?style=flat&logo=meta&logoColor=white)
![Status](https://img.shields.io/badge/Phase%202-Cleared-brightgreen)

# Apex_Predators_OpenEnv
An OpenEnv reinforcement learning environment that trains AI agents to autonomously clean, impute, and preprocess messy datasets for machine learning readiness.

### Core Features:
* **Autonomous Cleaning:** Handles missing values and outliers.
* **Multi-Mode Deployment:** Fully compatible with `uv` and `openenv-core`.
* **Dockerized:** Optimized for high-speed training on Hugging Face Spaces.
```
+----------------------+         +-------------------+         +----------------------+
|                      |  PING   |                   |   API   |                      |
|    inference.py      | ------> |   LiteLLM Proxy   | ------> |    Meta / OpenAI     |
|   (Orchestrator)     | <------ |  (Auth & Routing) | <------ |     (Evaluation)     |
|                      |         |                   |         |                      |
+----------+-----------+         +-------------------+         +----------------------+
           |
           | Action / Observation Loop
           v
+---------------------------------------------+
|             ApexDataCleanerEnv              |
|                                             |
|  [1] Tuple Stripper: Handles broken API     |
|      responses from the grader.             |
|                                             |
|  [2] Chaos Shield: try/except blocks        |
|      deflecting garbage data injections.    |
|                                             |
|  [3] Epsilon Clamper (1e-6): Mathematically |
|      guarantees scores stay strictly within |
|      the (0.0, 1.0) phase validation bound. |
|                                             |
+----------+----------------------------------+
           |
           | Validated Trajectory
           v
+----------------------+
|   System Log Output  |
|                      |
|  > [START] task_x    |
|  > [STEP] action_y   |
|  > [END] score_z     |
+----------------------+
```
