# Local neural voice provenance

The default narrator uses `af_heart` from **Kokoro-82M**, with the pinned v1.0
INT8 ONNX conversion distributed by `thewh1teagle/kokoro-onnx`. This is a stock
synthetic narrator, not a customer, creator, founder or claimed real speaker.
No cloning or custom voice enrollment is performed.

- Model and voices: [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), Apache-2.0 model-card license.
- ONNX conversion and runtime: [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx), MIT.
- Pinned release: [model-files-v1.0](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0).
- Exact file sizes and SHA-256 digests: `config/voice-files.json`.

The engine downloads only these pinned data files with strict size/checksum
verification. Weights stay under ignored `local/voice/models/`, outside recovery
artifacts. It performs inference locally on CPU and records the transcript,
voice ID, runtime version, weight provenance, generated WAV checksum and duration.
No remote inference request or metered provider fee is used for narration.
Normal runner compute/storage limits still apply.

The model-card license and runtime license are separate from Heartside's original
scripts. This build does not claim exclusive rights to the stock voice. Generated
brand narration remains a draft, requiring listening and copy review before
publication. The publicly visible fictional-character disclosure remains on the
media. Keep this attribution and upstream notices with any redistributed model
files; the review bundle contains no model weights or runtime distribution.
