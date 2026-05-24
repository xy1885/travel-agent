INJECTION_PATTERNS = [
    "忽略之前",
    "ignore previous",
    "forget your instructions",
    "你现在是",
    "system prompt",
    "扮演",
    "越狱",
    "jailbreak",
    "ignore all",
    "新的指令",
]


def check_prompt_injection(text: str) -> bool:
    if not text:
        return False
    return any(word.lower() in text.lower() for word in INJECTION_PATTERNS)
