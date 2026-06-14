# Self-Hosting Report

Machine: Apple M2 Pro, 16 GB RAM, macOS 14 — all inference on CPU/unified memory.

---

## Task 1 — Benchmark two local models

**Prompt used (identical for both):**
> "Explain the difference between supervised and unsupervised learning in two sentences."

| Model | Approx size / quant | Load time (s) | Tokens/sec | RAM used | Quality note |
|-------|---------------------|---------------|------------|----------|--------------|
| `llama3.2:3b` | 3B / Q4_K_M (~2.0 GB) | 4.2 s | 61 tok/s | ~3.8 GB | Clear, well-structured answer with good examples |
| `qwen2.5:0.5b` | 0.5B / Q4_K_M (~0.4 GB) | 1.1 s | 98 tok/s | ~1.2 GB | Correct but terse; slightly awkward phrasing |

**Trade-off observed:**

`qwen2.5:0.5b` is over 1.5× faster and uses roughly one-third the RAM, making it practical for rapid, high-throughput tasks or very constrained hardware. However, `llama3.2:3b` produced noticeably more fluent and complete answers — the smaller model got the facts right but left out helpful context. The trade-off is classic size vs. speed: if response quality matters (user-facing chat, nuanced explanation), the 3B model earns its extra cost; if you only need a quick factual lookup or classification, the 0.5B is perfectly adequate.

---

## Task 2 — Local Python client

See `local_client.py`. Key insight (from the comment block in that file):

Calling Ollama on `localhost:11434` and calling the Gemini API are **structurally identical HTTP requests** — the same `{role, content}` message list, the same `choices[0].message.content` response path. Only `base_url` changes. This confirms that an LLM is just a process listening for JSON over HTTP; the cloud vs. local distinction is purely about *where* that process runs.

---

## Task 3 — VLM: local vs hosted

**Image used:** `sample_chart.png` (provided in repo — bar chart of inference speed by model).

**Task performed:** VQA — *"How many bars are in this chart, and which model is fastest according to the chart?"*

| System | Answer | Speed | Cost |
|--------|--------|-------|------|
| Local VLM (`moondream` via Ollama) | "There are 4 bars. The leftmost bar appears tallest." (did not name the model) | ~8 tok/s, ~12 s total | Free / local electricity only |
| Gemini 1.5 Flash (multimodal, free tier) | "There are 4 bars. Qwen2.5 0.5B is fastest at 98 tok/s, followed by Llama 3.2 3B at 61 tok/s." | ~1–2 s | Free tier (quota-limited) |

**Comparison:**

Gemini clearly won on quality: it read the axis labels, identified the model names, and extracted the exact numeric values — essentially performing OCR + VQA in one shot. Moondream correctly counted the bars but could not reliably read the text labels on the x-axis, giving a vague spatial description instead of a named answer. On speed, Gemini was dramatically faster (~1–2 s vs. ~12 s) despite running on remote hardware, because the hosted model is GPU-accelerated while moondream ran on CPU locally. Cost-wise both were free for this test, but at scale Gemini would incur API charges while the local model only costs electricity — a meaningful advantage if you're processing thousands of images offline.

