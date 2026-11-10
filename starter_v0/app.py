from __future__ import annotations

import json
import os
import secrets
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chat import now_iso, run_model_tool_loop, trim_history, write_transcript  # noqa: E402
from env_loader import load_lab_env  # noqa: E402
from providers import make_provider  # noqa: E402
from tools import load_tool_declarations, to_openai_tools  # noqa: E402
from versioning import artifact_version_dict, build_artifact_version  # noqa: E402

load_lab_env(ROOT)

st.set_page_config(page_title="Veritas AI", page_icon="◈", layout="wide")

st.markdown(
    """
    <style>
      .block-container { max-width: 1050px; padding-top: 2rem; }
      [data-testid="stChatMessage"] { border: 1px solid rgba(128,128,128,.16); border-radius: 16px; }
      .hero { padding: 1.4rem 1.6rem; border-radius: 18px; margin-bottom: 1rem;
              background: linear-gradient(120deg, rgba(14,31,56,.96), rgba(24,69,83,.96));
              color: #f5f7fb; border: 1px solid rgba(190,211,226,.23); }
      .hero h1 { margin: 0 0 .3rem 0; letter-spacing: -.035em; }
      .hero .muted { color: #c6d5df; opacity: 1; }
      .muted { opacity: .72; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>◈ Veritas AI</h1>'
    '<div class="muted">Research &amp; Intelligence Agent · Gather evidence across web, social, and academic sources, then inspect the sources and tool results.</div></div>',
    unsafe_allow_html=True,
)

PROVIDERS = ["openrouter", "openai", "anthropic", "gemini", "ollama"]
KEY_ENV = {
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}
PROMPT_PATH = ROOT / "artifacts" / "system_prompt.md"
TOOLS_PATH = ROOT / "artifacts" / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"


def read_transcript(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def saved_transcripts() -> tuple[list[Path], dict[str, dict[str, Any]]]:
    records: dict[str, dict[str, Any]] = {}
    for path in TRANSCRIPTS_DIR.glob("*.transcript.json"):
        value = read_transcript(path)
        if value is not None:
            records[str(path)] = value
    paths = sorted(
        (Path(name) for name in records),
        key=lambda path: str(records[str(path)].get("updated_at", "")),
        reverse=True,
    )
    return paths, records


def transcript_label(path: Path, record: dict[str, Any]) -> str:
    turns = record.get("turns", [])
    first_user = next((str(turn.get("user", "")).strip() for turn in turns if turn.get("user")), "Empty chat")
    if len(first_user) > 42:
        first_user = first_user[:39] + "…"
    updated = str(record.get("updated_at", ""))[:16].replace("T", " ")
    provider_name = str(record.get("provider", "unknown"))
    return f"{first_user} · {provider_name} · {updated or path.stem}"


def restore_thread(path: Path, record: dict[str, Any]) -> None:
    st.session_state.active_transcript_path = str(path)
    st.session_state.transcript = record
    messages: list[dict[str, Any]] = []
    history: list[dict[str, str]] = []
    for turn in record.get("turns", []):
        user_text = str(turn.get("user", ""))
        if user_text:
            messages.append({"role": "user", "content": user_text})
            history.append({"role": "user", "content": user_text})
        assistant_text = turn.get("assistant_text")
        if not assistant_text and turn.get("error"):
            assistant_text = f"Request error: {turn['error']}"
        if assistant_text:
            messages.append({
                "role": "assistant",
                "content": str(assistant_text),
                "tool_events": turn.get("tool_events", []),
            })
            history.append({"role": "assistant", "content": str(assistant_text)})
    st.session_state.messages = messages
    st.session_state.history = history


def clear_active_thread() -> None:
    st.session_state.active_transcript_path = None
    st.session_state.transcript = None
    st.session_state.messages = []
    st.session_state.history = []


def new_transcript(provider_name: str, model_name: str, version_name: str,
                   history_window: int, max_tool_rounds: int) -> tuple[dict[str, Any], Path]:
    artifact = build_artifact_version(version_name, PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"{version_name}_{provider_name}_{timestamp}_{secrets.token_hex(3)}"
    path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    record = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact),
        "provider": provider_name,
        "model": model_name,
        "system_prompt": str(PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    return record, path


if "active_transcript_path" not in st.session_state:
    st.session_state.active_transcript_path = None
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

thread_paths, thread_records = saved_transcripts()

with st.sidebar:
    st.header("Chats")
    if st.button("＋ New chat", use_container_width=True):
        clear_active_thread()
        st.rerun()

    if thread_paths:
        st.caption("Open a saved conversation")
        for path in thread_paths:
            record = thread_records[str(path)]
            is_active = str(path) == st.session_state.active_transcript_path
            if st.button(
                transcript_label(path, record),
                key=f"open_thread_{path.name}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                restore_thread(path, record)
                provider_value = record.get("provider")
                if provider_value in PROVIDERS:
                    st.session_state.provider_widget = provider_value
                st.session_state.model_widget = str(record.get("model") or "")
                st.session_state.version_widget = str(record.get("version", "v3"))
                st.session_state.history_window_widget = max(1, min(12, int(record.get("history_window", 5))))
                st.session_state.max_rounds_widget = max(1, min(8, int(record.get("max_tool_rounds", 4))))
                st.rerun()
    else:
        st.caption("Your saved chats will appear here.")

    st.divider()
    st.header("Agent setup")
    if "provider_widget" not in st.session_state:
        st.session_state.provider_widget = "openrouter"
    if "model_widget" not in st.session_state:
        st.session_state.model_widget = ""
    if "version_widget" not in st.session_state:
        st.session_state.version_widget = "v3"
    if "history_window_widget" not in st.session_state:
        st.session_state.history_window_widget = 5
    if "max_rounds_widget" not in st.session_state:
        st.session_state.max_rounds_widget = 4

    provider_name = st.selectbox("Model provider", PROVIDERS, key="provider_widget")
    provider = make_provider(provider_name)
    default_model = getattr(provider, "default_model", "")
    model = st.text_input("Model (optional)", placeholder=default_model, key="model_widget")
    version = st.text_input("Prompt version", key="version_widget")
    history_window = st.slider("Conversation memory (turns)", 1, 12, key="history_window_widget")
    max_tool_rounds = st.slider("Maximum tool rounds per message", 1, 8, key="max_rounds_widget")

    st.divider()
    st.caption("Uses the prompt and tool declarations in `artifacts/`.")
    st.caption("Provider keys belong in `starter_v0/.env`; this UI never displays them.")
    if provider_name == "ollama":
        st.caption(f"Ollama endpoint: `{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')}`")
    elif not os.getenv(KEY_ENV[provider_name]):
        st.warning(f"Add `{KEY_ENV[provider_name]}` to `.env` to connect this provider.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        for event in message.get("tool_events", []):
            with st.expander(f"🔧 {event['tool']}"):
                st.json({"arguments": event.get("args", {}), "result": event.get("result", {})})

if not st.session_state.messages:
    st.info("Try: **Compare recent web and arXiv research on tool calling in language models. Show me the sources.**")

prompt = st.chat_input("Ask the research agent…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.transcript is None:
        st.session_state.transcript, st.session_state.active_transcript_path = new_transcript(
            provider_name,
            model.strip() or default_model,
            version.strip() or "v3",
            history_window,
            max_tool_rounds,
        )

    assistant_text = ""
    tool_events: list[dict[str, Any]] = []
    turn: dict[str, Any] = {
        "turn_index": len(st.session_state.transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    with st.chat_message("assistant"):
        try:
            system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
            declarations = to_openai_tools(load_tool_declarations(TOOLS_PATH))
            messages = [
                {"role": "system", "content": system_prompt},
                *trim_history(st.session_state.history, history_window),
                {"role": "user", "content": prompt},
            ]
            with st.spinner("Thinking and using tools if needed…"):
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=declarations,
                    model=model.strip() or None,
                    max_tool_rounds=max_tool_rounds,
                )
            turn.update(result)
            assistant_text = result["assistant_text"]
            tool_events = result.get("tool_events", [])
            st.markdown(assistant_text)
            for event in tool_events:
                with st.expander(f"🔧 {event['tool']}"):
                    st.json({"arguments": event.get("args", {}), "result": event.get("result", {})})
            st.session_state.history.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": assistant_text},
            ])
        except Exception as exc:
            assistant_text = f"I couldn't complete that request: {type(exc).__name__}: {exc}"
            turn.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
            st.error(assistant_text)

    turn["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn)
    st.session_state.transcript.update({
        "provider": provider_name,
        "model": model.strip() or default_model,
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
    })
    transcript_path = Path(st.session_state.active_transcript_path)
    write_transcript(transcript_path, st.session_state.transcript)
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text,
        "tool_events": tool_events,
    })
    st.rerun()
