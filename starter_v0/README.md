# Source code

Toàn bộ source code của lab nằm trong folder này. Chạy mọi lệnh từ `starter_v0/`.

- File bắt đầu chạy: `run_eval.py` (chạy eval), `chat.py` (chat live), `scripts/preflight_provider.py` (kiểm tra provider).
- Giao diện web: `app.py` (Streamlit chat).
- Cách chạy: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`; `python chat.py --provider openrouter --version v3`; `pytest`.
- Input: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, bộ case `data/*.json`, API key trong `.env` (mẫu ở `.env.example`).
- Output: `runs/*.json` (kết quả eval), `transcripts/*.transcript.json` (chat live), `analysis/*.csv` (nếu chạy `scripts/parse_runs.py`).
- File học viên được sửa: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `data/eval_group.json`, `tools/` (thêm tool mới và đăng ký trong `tools/__init__.py`), `tests/test_tools_todo.py`, code UI và `requirements.txt`. Không sửa nội dung case trong `data/eval_base.json`.

Chi tiết từng bước xem [README.md](../README.md) ở root; cấu hình API key xem [docs/TOOL-SETUP.md](../docs/TOOL-SETUP.md).

## Streamlit live chat

Install dependencies from this folder with `pip install -r requirements.txt`, then launch:

```bash
streamlit run app.py
```

Choose a host address and port with Streamlit flags. For example, bind on all network interfaces and use port 8501:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

For this computer only, use `--server.address 127.0.0.1`; change `--server.port` to any available port you prefer.

Set the selected provider key in `.env` first. The UI uses the same `artifacts/system_prompt.md`, `artifacts/tools.yaml`, provider adapters, tool registry, and transcript format as `chat.py`. Conversations are saved under `transcripts/`.

Use **New chat** in the sidebar to start a separate conversation. Click a saved chat listed below it to reopen its messages and tool results; each conversation is backed by its transcript JSON file.
