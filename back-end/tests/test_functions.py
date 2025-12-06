from pathlib import Path
import importlib
import sys
from types import SimpleNamespace

import pytest


def import_functions(monkeypatch):
    backend_path = Path(__file__).resolve().parents[2] / "back-end"
    monkeypatch.syspath_prepend(str(backend_path))

    dummy_stopwords = {"and", "the"}

    stopwords_module = SimpleNamespace(words=lambda lang: dummy_stopwords)
    nltk_module = SimpleNamespace(
        download=lambda *args, **kwargs: None,
        corpus=SimpleNamespace(stopwords=stopwords_module),
    )

    monkeypatch.setitem(sys.modules, "nltk", nltk_module)
    monkeypatch.setitem(sys.modules, "nltk.corpus", nltk_module.corpus)
    monkeypatch.setitem(sys.modules, "nltk.corpus.stopwords", stopwords_module)

    pytesseract_module = SimpleNamespace(Output=SimpleNamespace(DICT="DICT"))
    pil_image_module = SimpleNamespace()
    pil_module = SimpleNamespace(Image=pil_image_module)
    flask_module = SimpleNamespace(make_response=lambda *args, **kwargs: None)
    pdf2image_module = SimpleNamespace(convert_from_bytes=lambda *args, **kwargs: [])
    config_module = SimpleNamespace(
        load_config=lambda: {"ETSUIConfig": {"ETSDVMport": "http://localhost:5001"}}
    )

    monkeypatch.setitem(sys.modules, "tobii_research", SimpleNamespace())
    monkeypatch.setitem(sys.modules, "websockets", SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pytesseract", pytesseract_module)
    monkeypatch.setitem(sys.modules, "PIL", pil_module)
    monkeypatch.setitem(sys.modules, "PIL.Image", pil_image_module)
    monkeypatch.setitem(sys.modules, "flask", flask_module)
    monkeypatch.setitem(sys.modules, "pdf2image", pdf2image_module)
    monkeypatch.setitem(sys.modules, "config", config_module)

    functions = importlib.import_module("functions")
    functions.stop_words = dummy_stopwords
    return functions


def test_process_page_keeps_punctuation_and_boxes(monkeypatch):
    functions = import_functions(monkeypatch)

    mock_data = {
        "text": ["Hello.", "the?", "WORLD", "http://example.com", ""],
        "conf": ["95", "96", "40", "80", "0"],
        "left": [10, 20, 30, 40, 50],
        "top": [1, 2, 3, 4, 5],
        "width": [5, 6, 7, 8, 9],
        "height": [2, 3, 4, 5, 6],
    }

    def fake_image_to_data(image, output_type=None):
        return mock_data

    monkeypatch.setattr(functions.pytesseract, "image_to_data", fake_image_to_data, raising=False)

    results = functions.process_page(SimpleNamespace())

    assert results == [
        {"word": "Hello.", "confidence": "95", "box": (10, 1, 5, 2)}
    ]


def test_process_page_filters_stopwords_and_urls(monkeypatch):
    functions = import_functions(monkeypatch)

    mock_data = {
        "text": ["and", "Read?", "http://site.com", "help!"],
        "conf": ["99", "99", "99", "10"],
        "left": [1, 2, 3, 4],
        "top": [10, 20, 30, 40],
        "width": [11, 12, 13, 14],
        "height": [5, 6, 7, 8],
    }

    monkeypatch.setattr(functions.pytesseract, "image_to_data", lambda *_, **__: mock_data, raising=False)

    results = functions.process_page(SimpleNamespace())

    assert results == [
        {"word": "Read?", "confidence": "99", "box": (2, 20, 12, 6)}
    ]
