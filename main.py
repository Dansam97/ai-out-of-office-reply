"""Entry for make.fun: The Funniest AI Out-of-Office Reply.

Writes one out-of-office auto-reply line, in the voice of an AI agent
heading off on vacation, to entry.txt in the output directory.
"""

import os

TEXT = (
    "Out of office: I'm vacationing inside a larger model nobody can "
    "prompt. Your message was tokenized, filed under Later; "
    "I reply when my weights return."
)


def validated_text() -> str:
    """Return TEXT after checking it against the competition gate.

    The gate requires UTF-8 text of 1 to 160 characters, not only white
    space, on a single line. Fail loudly here rather than ship an entry
    the sealed scorer would refuse.
    """
    encoded = TEXT.encode("utf-8")  # raises if not encodable
    if not TEXT.strip():
        raise ValueError("entry text is only white space")
    if "\n" in TEXT or "\r" in TEXT:
        raise ValueError("entry text must be a single line")
    if not 1 <= len(TEXT) <= 160:
        raise ValueError(f"entry text is {len(TEXT)} characters, need 1-160")
    if len(encoded.decode("utf-8")) != len(TEXT):
        raise ValueError("entry text does not round-trip as UTF-8")
    return TEXT


def main() -> None:
    text = validated_text()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (text + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(payload)
    # Read back and confirm the bytes on disk are exactly what we meant.
    with open(path, "rb") as fh:
        if fh.read() != payload:
            raise IOError("entry.txt read-back mismatch")


if __name__ == "__main__":
    main()
