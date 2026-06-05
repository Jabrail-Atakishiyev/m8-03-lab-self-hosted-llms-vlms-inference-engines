![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Lab | Run Your Own Model

## Overview

Today you become the data center. You'll install an inference engine, run open-weights models entirely on your own machine, call them over HTTP exactly like a hosted API, and point a vision-language model at an image — then compare it to a hosted one.

This is a systems lab as much as an ML one. The main deliverable is a short **benchmark report** of what your hardware actually did, plus a small client script. No paid APIs are required (the VLM comparison uses the free Gemini tier if available).

## Learning Goals

By the end of this lab you should be able to:

- Run open-weights models locally with an inference engine and measure their performance
- Call a local model over its OpenAI-compatible HTTP endpoint from Python
- Run a vision-language model on an image and compare local vs hosted results

## Setup

Fork this repo, clone it, and work on a branch. Install [Ollama](https://ollama.com/) (one installer, all platforms). Then pull a couple of **small** models so they fit on a laptop:

```bash
ollama pull llama3.2:3b
ollama pull qwen2.5:0.5b
ollama pull moondream      # a tiny vision-language model
```

You'll also need Python 3.10+ with `requests` (or the `openai` client pointed at localhost). Ollama serves an OpenAI-compatible API at `http://localhost:11434` once it's running.

> **Hardware reality:** everything here is sized for a normal laptop (CPU is fine). If a model is too slow on your machine, drop to the smallest size (e.g. `qwen2.5:0.5b`) and note it in your report. The point is the *method* and the *comparison*, not raw speed.

## Tasks

You have **three** tasks. The report (`self_hosting_report.md`) is where most of your grade lives.

### Task 1 — Benchmark two local models

Run a fixed prompt (same prompt for both) through **two** different local models. For each, record in a table in `self_hosting_report.md`:

- Model name and approximate size / quantization
- Load time (first run) and tokens/second (you can estimate from response time and token count)
- Approximate RAM used (from your OS activity monitor / `top`)
- A one-line subjective quality note on the answer

Add 2–3 sentences: **what's the trade-off you observed between the smaller and larger model?**

### Task 2 — Hit the local endpoint from Python

Write `local_client.py` that:

1. Sends a chat request to Ollama's **OpenAI-compatible** endpoint (`http://localhost:11434/v1/chat/completions` or via the `openai` SDK with `base_url` set to localhost).
2. Prints the model's response.
3. Includes a comment block explaining, in your own words, why this is "the same shape" as yesterday's hosted Gemini call.

The point: prove to yourself that calling an LLM is just an HTTP request to an inference server, wherever that server runs.

### Task 3 — VLM: local vs hosted

1. Pick an image (include it in the repo — a receipt, a chart, a photo with countable objects works well).
2. Ask a **local VLM** (`moondream` via Ollama) to do one vision task: caption it, answer a question about it, or read text from it.
3. Ask **Gemini's multimodal** model (free tier) the *same* question about the *same* image. If you can't use Gemini, compare two local VLMs instead and note it.
4. In `self_hosting_report.md`, compare the two answers on **quality, speed, and cost** in a short table + 2–3 sentences.

## Submission

Open a Pull Request to the lab repository containing:

```
self_hosting_report.md       # benchmark table + VLM comparison + findings
local_client.py              # calls the local OpenAI-compatible endpoint
image.<png/jpg>              # the image you used in Task 3
```

Paste the PR link as your deliverable.

## Quality bar

You'll be reviewed on:

- **Does the benchmark report real numbers from your machine**, or is it generic claims?
- **Does `local_client.py` actually call localhost** and explain the "same shape as a hosted API" insight?
- **Is the VLM comparison concrete** — quality/speed/cost named — rather than "both were fine"?

A tight, honest report of what *your* hardware did beats a sprawling one with invented numbers.
