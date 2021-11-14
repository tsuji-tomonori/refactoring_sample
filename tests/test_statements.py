import json
import unittest
from pathlib import Path

from src.statements import statement


def read_json(path: Path) -> dict:
    with open(str(path), "r", encoding="utf-8") as f:
        result = json.load(f)
    return result


def read_text(path: Path) -> str:
    with open(str(path), "r", encoding="utf-8") as f:
        result = f.read()
    return result


def get_resource_path(file_name: str) -> Path:
    return Path.cwd() / "tests" / "resource" / file_name


class StatementsTest(unittest.TestCase):

    def test_gp(self):
        # 1. 初期化
        suffix = "gp"
        invoices = read_json(get_resource_path(f"invoices_{suffix}.json"))
        plays = read_json(get_resource_path(f"plays_{suffix}.json"))
        # 2. テスト実行
        actual = statement(invoices[0], plays)
        # 3. アサーション
        self.assertEqual(actual, read_text(
            get_resource_path(f"result_{suffix}.txt")))

    def test_error(self):
        # 1. 初期化
        suffix = "err"
        invoices = read_json(get_resource_path(f"invoices_{suffix}.json"))
        plays = read_json(get_resource_path(f"plays_{suffix}.json"))
        # 2. テスト実行
        # 3. アサーション
        with self.assertRaises(Exception):
            statement(invoices[0], plays)

    def test_small(self):
        # 1. 初期化
        suffix = "few"
        invoices = read_json(get_resource_path(f"invoices_{suffix}.json"))
        plays = read_json(get_resource_path(f"plays_{suffix}.json"))
        # 2. テスト実行
        actual = statement(invoices[0], plays)
        # 3. アサーション
        self.assertEqual(actual, read_text(
            get_resource_path(f"result_{suffix}.txt")))

    def test_not_comedy(self):
        # 1. 初期化
        suffix = "not_comedy"
        invoices = read_json(get_resource_path(f"invoices_{suffix}.json"))
        plays = read_json(get_resource_path(f"plays_{suffix}.json"))
        # 2. テスト実行
        actual = statement(invoices[0], plays)
        # 3. アサーション
        self.assertEqual(actual, read_text(
            get_resource_path(f"result_{suffix}.txt")))
