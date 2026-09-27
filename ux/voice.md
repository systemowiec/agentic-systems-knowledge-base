# Voice interface

> Use when: a user speaks to an application or receives a spoken response.
> Do not use when: the product has no audio channel; do not add voice merely to make it feel "agentic."

Audio APIs and models change quickly.

## Decision

Start from the conversation's needs. For full control over transcription and stages, choose a speech-to-text (STT) → text-based processing → text-to-speech (TTS) chain. For natural, interruptible conversation with low latency, consider a realtime or full-duplex session if the chosen provider supports it. These are **options**, not mandatory stages in a progression from one to the other.

Design separately for time to first useful word, accurate recognition of names and numbers, interruptions, action confirmation, and recording privacy. For a sensitive action, an intent spoken to the model does not replace authorization. Users should know when they are being recorded and how long audio or transcripts are retained.

## Controls

- Test noise, varied accents, silence, interrupted responses, misrecognition of critical details, and tool latency.
- Measure time to a useful answer and task success; a short "checking" utterance is not yet a result.
- For actions with side effects, repeat the recognized critical details and use confirmation appropriate to the risk.
- Provide clear audio state, captions, or a text alternative where the product requires them.

## Sources

- [OpenAI, Voice agents](https://developers.openai.com/api/docs/guides/voice-agents) — comparison of voice architectures and latency measurement; provider-specific details.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) — accessibility of content and controls.
