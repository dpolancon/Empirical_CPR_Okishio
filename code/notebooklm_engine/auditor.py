"""Authenticated NotebookLM CLI adapter for econometric audits.

This module adapts the working CLI wrapper in COMPOL_DigitalCapitalism to the
installed notebooklm-py 0.5.0 command signatures. The CLI is used deliberately:
it owns the supported cookie/session loading path and avoids duplicating private
NotebookLM RPC details.
"""

from __future__ import annotations

import asyncio
import json
import logging
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

from notebooklm import AuthTokens, NotebookLMClient

logger = logging.getLogger(__name__)


class ThreadResetError(RuntimeError):
    """Raised when the current NotebookLM conversation cannot be deleted."""


class NotebookLMAuditor:
    """Create, populate, and query one NotebookLM audit notebook."""

    def __init__(
        self,
        *,
        command: str = "notebooklm",
        request_timeout: int = 240,
        source_wait_timeout: int = 600,
    ) -> None:
        self.command = command
        self.request_timeout = request_timeout
        self.source_wait_timeout = source_wait_timeout
        self.notebook_id: str | None = None
        self.notebook_title: str | None = None
        self.source_ids: list[str] = []
        self.sources: list[dict[str, Any]] = []
        self._authenticated = False

    def _run_command(
        self,
        arguments: list[str],
        *,
        json_output: bool = True,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        command = [self.command, *arguments]
        if json_output and "--json" not in command:
            command.append("--json")

        logger.debug("Running NotebookLM command: %s", " ".join(command))
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout or max(self.request_timeout, self.source_wait_timeout + 30),
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "NotebookLM CLI not found. Install requirements and run "
                "'notebooklm login'."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"NotebookLM command timed out after {exc.timeout} seconds."
            ) from exc

        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "No error output."
            raise RuntimeError(
                f"NotebookLM command failed with exit code {result.returncode}: {detail}"
            )

        stdout = result.stdout.strip()
        if not stdout:
            return {}
        if not json_output:
            return {"raw_output": stdout}
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"NotebookLM returned non-JSON output: {stdout[:500]}"
            ) from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("NotebookLM returned an unexpected JSON payload.")
        return parsed

    def authenticate(self) -> dict[str, Any]:
        """Verify that stored cookies can fetch a live NotebookLM token."""
        status = self._run_command(["auth", "check", "--test"])
        checks = status.get("checks") or {}
        if status.get("status") != "ok" or checks.get("token_fetch") is not True:
            raise RuntimeError(
                "NotebookLM authentication is missing or stale. Run "
                "'notebooklm login', then retry."
            )
        self._authenticated = True
        return status

    @staticmethod
    def _validate_sources(pdf_paths: Iterable[str | Path], notes_path: str | Path) -> list[Path]:
        paths = [Path(path).expanduser().resolve() for path in pdf_paths]
        notes = Path(notes_path).expanduser().resolve()
        if not paths:
            raise ValueError("At least one PDF path is required.")

        missing = [path for path in paths if not path.is_file()]
        if not notes.exists():
            missing.append(notes)
        if missing:
            formatted = "\n".join(f"- {path}" for path in missing)
            raise FileNotFoundError(f"Required NotebookLM source files are missing:\n{formatted}")

        non_pdfs = [path for path in paths if path.suffix.lower() != ".pdf"]
        if non_pdfs:
            raise ValueError(
                "Every --pdf source must have a .pdf extension: "
                + ", ".join(str(path) for path in non_pdfs)
            )

        if notes.is_dir():
            note_files = sorted(path for path in notes.rglob("*.md") if path.is_file())
            if not note_files:
                raise ValueError(f"Notes directory contains no Markdown files: {notes}")
        elif notes.is_file():
            note_files = [notes]
        else:
            raise ValueError(f"Notes path is neither a file nor a directory: {notes}")
        return [*paths, *note_files]

    @staticmethod
    def _extract_id(payload: dict[str, Any], envelope: str) -> str:
        nested = payload.get(envelope)
        if isinstance(nested, dict) and nested.get("id"):
            return str(nested["id"])
        for key in ("id", f"{envelope}_id", "active_notebook_id", "source_id"):
            if payload.get(key):
                return str(payload[key])
        return ""

    def _add_source_and_wait(self, source_path: Path) -> str:
        if not self.notebook_id:
            raise RuntimeError("No NotebookLM notebook has been set up.")

        added = self._run_command(
            [
                "source",
                "add",
                str(source_path),
                "--notebook",
                self.notebook_id,
                "--timeout",
                str(self.request_timeout),
            ]
        )
        source_id = self._extract_id(added, "source")
        if not source_id:
            raise RuntimeError(f"Could not read source ID after uploading {source_path}.")

        self._run_command(
            [
                "source",
                "wait",
                source_id,
                "--notebook",
                self.notebook_id,
                "--timeout",
                str(self.source_wait_timeout),
            ],
            timeout=self.source_wait_timeout + 30,
        )
        self.source_ids.append(source_id)
        return source_id

    def setup_notebook(
        self,
        notebook_name: str,
        pdf_paths: Iterable[str | Path],
        notes_path: str | Path,
    ) -> str:
        """Create a notebook, upload PDFs plus a note file/folder, and await indexing."""
        if not self._authenticated:
            raise RuntimeError("Call authenticate() before setup_notebook().")
        if self.notebook_id:
            raise RuntimeError("This auditor already has an active notebook.")

        source_paths = self._validate_sources(pdf_paths, notes_path)
        created = self._run_command(["create", notebook_name])
        notebook_id = self._extract_id(created, "notebook")
        if not notebook_id:
            raise RuntimeError("Could not read the new NotebookLM notebook ID.")
        self.notebook_id = notebook_id
        self.notebook_title = notebook_name

        for source_path in source_paths:
            logger.info("Uploading NotebookLM source: %s", source_path)
            self._add_source_and_wait(source_path)
        sources_payload = self._run_command(
            ["source", "list", "--notebook", notebook_id]
        )
        self.sources = [
            dict(source) for source in (sources_payload.get("sources") or [])
        ]
        self.source_ids = [
            str(source["id"]) for source in self.sources if source.get("id")
        ]
        return notebook_id

    def connect_notebook(self, notebook: str) -> str:
        """Resolve an existing notebook by exact ID or exact title."""
        if not self._authenticated:
            raise RuntimeError("Call authenticate() before connect_notebook().")
        if self.notebook_id:
            raise RuntimeError("This auditor already has an active notebook.")
        if not notebook.strip():
            raise ValueError("A notebook ID or exact title is required.")

        payload = self._run_command(["list"])
        notebooks = payload.get("notebooks") or []
        id_matches = [item for item in notebooks if item.get("id") == notebook]
        title_matches = [
            item
            for item in notebooks
            if str(item.get("title", "")).casefold() == notebook.casefold()
        ]
        matches = id_matches or title_matches
        if not matches:
            raise RuntimeError(f"Notebook not found by exact ID or title: {notebook}")
        if len(matches) > 1:
            ids = ", ".join(str(item.get("id")) for item in matches)
            raise RuntimeError(f"Notebook title is ambiguous; use one of these IDs: {ids}")

        notebook_id = str(matches[0]["id"])
        self.notebook_title = str(matches[0].get("title") or notebook)
        sources_payload = self._run_command(
            ["source", "list", "--notebook", notebook_id]
        )
        sources = sources_payload.get("sources") or []
        if not sources:
            raise RuntimeError(f"Notebook has no sources: {notebook}")
        unavailable = [
            str(source.get("title") or source.get("id"))
            for source in sources
            if str(source.get("status", "")).lower() != "ready"
        ]
        if unavailable:
            raise RuntimeError(
                "Notebook contains sources that are not ready: " + ", ".join(unavailable)
            )

        self.notebook_id = notebook_id
        self.sources = [dict(source) for source in sources]
        self.source_ids = [str(source["id"]) for source in sources if source.get("id")]
        return notebook_id

    async def _delete_current_thread(self) -> bool:
        if not self.notebook_id:
            raise RuntimeError("No NotebookLM notebook is connected.")
        auth = await AuthTokens.from_storage()
        async with NotebookLMClient(auth, timeout=float(self.request_timeout)) as client:
            conversation_id = await client.chat.get_conversation_id(self.notebook_id)
            if not conversation_id:
                return False
            return await client.chat.delete_conversation(
                self.notebook_id,
                conversation_id,
            )

    def reset_thread(self, *, retry_delay: float = 30.0) -> bool:
        """Delete the current server conversation, retrying exactly once.

        NotebookLM exposes one current conversation per notebook rather than
        independently addressable thread IDs. Deleting that conversation is
        the public API equivalent of starting a clean chat. A return value of
        ``False`` means there was no prior conversation to delete.
        """
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                deleted = asyncio.run(self._delete_current_thread())
                logger.info(
                    "NotebookLM thread reset complete (conversation_deleted=%s).",
                    deleted,
                )
                return deleted
            except Exception as exc:  # The second failure is promoted below.
                last_error = exc
                if attempt == 0:
                    logger.warning(
                        "NotebookLM thread reset failed; retrying once in %.1f seconds: %s",
                        retry_delay,
                        exc,
                    )
                    time.sleep(retry_delay)

        raise ThreadResetError(
            "NotebookLM thread reset failed twice; aborting to prevent "
            "cross-thread context contamination."
        ) from last_error

    @staticmethod
    def _compose_prompt(system_prompt: str, user_question: str) -> str:
        if not user_question.strip():
            raise ValueError("A user question is required.")
        if system_prompt.strip():
            return f"{system_prompt}\n\n{user_question}"
        return user_question

    def _ask(
        self,
        system_prompt: str,
        user_question: str,
        *,
        source_ids: Iterable[str] | None = None,
        new_thread: bool = False,
    ) -> str:
        if not self.notebook_id:
            raise RuntimeError("Call setup_notebook() before ask_question().")
        prompt = self._compose_prompt(system_prompt, user_question)
        prompt_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".txt",
                delete=False,
                encoding="utf-8",
                newline="\n",
            ) as prompt_file:
                prompt_file.write(prompt)
                prompt_path = Path(prompt_file.name)

            arguments = [
                "ask",
                "--prompt-file",
                str(prompt_path),
                "--notebook",
                self.notebook_id,
                "--timeout",
                str(self.request_timeout),
            ]
            if new_thread:
                # reset_thread() already deletes the prior server conversation.
                # --new prevents a stale CLI context ID from being reused.
                arguments.extend(["--new", "--yes"])
            for source_id in source_ids or []:
                if source_id not in self.source_ids:
                    raise ValueError(
                        f"Source ID is not present in the connected notebook: {source_id}"
                    )
                arguments.extend(["--source", source_id])

            response = self._run_command(arguments)
            answer = response.get("answer")
            if not isinstance(answer, str) or not answer.strip():
                raise RuntimeError("NotebookLM returned an empty answer.")
            return answer
        finally:
            if prompt_path is not None:
                prompt_path.unlink(missing_ok=True)

    def start_new_thread(
        self,
        system_prompt: str,
        user_question: str,
        *,
        source_ids: Iterable[str] | None = None,
    ) -> str:
        """Reset the notebook chat and send the first query in a clean thread."""
        self.reset_thread()
        return self._ask(
            system_prompt,
            user_question,
            source_ids=source_ids,
            new_thread=True,
        )

    def ask_question(
        self,
        system_prompt: str,
        user_question: str,
        *,
        source_ids: Iterable[str] | None = None,
    ) -> str:
        """Continue the current thread with an optional source restriction."""
        return self._ask(
            system_prompt,
            user_question,
            source_ids=source_ids,
            new_thread=False,
        )

    def close(self) -> None:
        """Release local session state while preserving the remote audit notebook."""
        self.notebook_id = None
        self.notebook_title = None
        self.source_ids.clear()
        self.sources.clear()
        self._authenticated = False
