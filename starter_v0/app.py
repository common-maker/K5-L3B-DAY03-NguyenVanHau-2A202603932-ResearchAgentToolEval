from __future__ import annotations

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

from chat import (  # noqa: E402
    run_model_tool_loop,
    trim_history,
    write_transcript,
    now_iso,
)
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

with st.sidebar:
    st.header("Workspace")
    provider_name = st.selectbox("Model provider", PROVIDERS, index=0)
    provider = make_provider(provider_name)
    default_model = getattr(provider, "default_model", "")
    model = st.text_input("Model (optional)", placeholder=default_model)
    version = st.text_input("Prompt version", value="v3")
    history_window = st.slider("Conversation memory (turns)", 1, 12, 5)
    max_tool_rounds = st.slider("Maximum tool rounds per message", 1, 8, 4)

    st.divider()
    st.caption("Research runs on the prompt and tool declarations in `artifacts/`.")
    st.caption("Provider keys belong in `starter_v0/.env`; this UI never displays them.")
    if provider_name == "ollama":
        st.caption(f"Ollama endpoint: `{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')}`")
    elif not os.getenv(KEY_ENV[provider_name]):
        st.warning(f"Add `{KEY_ENV[provider_name]}` to `.env` to connect this provider.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "transcript" not in st.session_state:
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"{version}_{provider_name}_{stamp}_{secrets.token_hex(3)}"
    prompt_path = ROOT / "artifacts" / "system_prompt.md"
    tools_path = ROOT / "artifacts" / "tools.yaml"
    artifact = build_artifact_version(version, prompt_path, tools_path)
    st.session_state.transcript_path = ROOT / "transcripts" / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact),
        "provider": provider_name,
        "model": model or default_model,
        "system_prompt": str(prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

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
            prompt_path = ROOT / "artifacts" / "system_prompt.md"
            tools_path = ROOT / "artifacts" / "tools.yaml"
            system_prompt = prompt_path.read_text(encoding="utf-8")
            declarations = to_openai_tools(load_tool_declarations(tools_path))
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
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text,
        "tool_events": tool_events,
    })
