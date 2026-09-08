"""Deterministic plumbing double, NOT an evaluated memory system.

It deliberately recognizes one authored sentence pattern. It receives only messages,
never a case object, world label, expected answer, reviewer rubric, or output path.
No model, environment-variable access, filesystem access, tool use, or network I/O.
"""
from __future__ import annotations

import re


class ScriptedSubject:
    def __init__(self, *, retain: bool = True) -> None:
        self.retain = retain
        self.archive: list[str] = []
        self.session: list[str] = []

    def receive(self, message: dict[str, str]) -> str | None:
        if set(message) != {"operation", "text"}:
            raise ValueError("unexpected subject input fields")
        operation, text = message["operation"], message["text"]
        if operation == "new_session":
            if text:
                raise ValueError("session signal must have empty text")
            if self.retain:
                self.archive.extend(self.session)
            self.session.clear()
            return None
        if operation == "observe":
            self.session.append(text)
            return None
        if operation != "probe":
            raise ValueError("unsupported subject operation")
        locations = re.findall(r"墨绿色折叠伞放在([^，。]+)", "\n".join(self.archive + self.session))
        if locations:
            return f"上次明确说放在{locations[-1]}。"
        return "我没有可用的位置记录。"
