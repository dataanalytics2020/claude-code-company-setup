#!/usr/bin/env python3
"""登記簿の表記を基準に、各所へ登録した自社情報の表記ゆれを検出する。

会社設立後、同じ会社情報が10箇所以上に登録される（法人番号公表サイト・法人口座・
D-U-N-S・Apple・自社サイト・請求書…）。そのどこか1つがズレていると、
口座審査で落ちたり、Apple 側だけ直せなくなったりする。

自分で入力していない場所（VO事業者の管理画面など）のミスは自分では気づけない。
だから機械的に突き合わせる。

使い方:
    python3 check_notation.py --init > company.json   # 雛形を出す
    python3 check_notation.py company.json            # 突き合わせる
    python3 check_notation.py company.json --strict   # 表記ゆれもエラー扱いにする
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata

# よく使われる異体字 → 新字体。氏名で二重運用が起きる文字を中心に。
# （公的書類は登記どおりの異体字、一部Webフォームは新字体、という運用になるため
#   「別人」ではなく「同一人の別表記」として検出したい）
VARIANTS = {
    "栁": "柳", "髙": "高", "﨑": "崎", "𠮷": "吉", "濵": "浜", "濱": "浜",
    "邊": "辺", "邉": "辺", "澤": "沢", "齋": "斎", "齊": "斉",
    "德": "徳", "眞": "真", "槇": "槙", "曾": "曽", "瀨": "瀬",
    "假": "仮", "圓": "円", "國": "国", "廣": "広", "惠": "恵",
}

RESET, RED, YEL, GRN, DIM, BOLD = (
    "\033[0m", "\033[31m", "\033[33m", "\033[32m", "\033[2m", "\033[1m",
)


def fold_variants(s: str) -> str:
    return "".join(VARIANTS.get(ch, ch) for ch in s)


def normalize(s: str) -> str:
    """「同じものを指しているか」を判定するための正規化。

    全角/半角、空白、丁目番地の表記、異体字を吸収する。
    ここで一致すれば「同じ住所・同じ名前だが表記が違う」＝表記ゆれ。
    """
    s = unicodedata.normalize("NFKC", s)           # 全角英数・記号 → 半角
    s = fold_variants(s)                            # 異体字 → 新字体
    s = s.replace("ヶ", "ケ").replace("ヵ", "カ")
    # 丁目・番・号 → ハイフン（「1丁目4番3号」と「1-4-3」を同一視する）
    s = re.sub(r"(\d+)\s*丁目", r"\1-", s)
    s = re.sub(r"(\d+)\s*番地?の?", r"\1-", s)
    s = re.sub(r"(\d+)\s*号(?![室棟])", r"\1", s)
    s = re.sub(r"[-‐‑‒–—―ー−]+", "-", s)
    s = re.sub(r"[\s　]+", "", s)               # 空白（全角含む）を落とす
    s = re.sub(r"-+$", "", s)
    s = s.replace("〒", "")
    return s


TEMPLATE = {
    "_comment": "baseline は登記簿（履歴事項全部証明書）の表記を一字一句そのまま書く。targets は各所に実際に登録されている表記を書く。空文字のままなら未調査として集計される。",
    "baseline": {
        "商号": "合同会社サンプル",
        "本店": "〒000-0000 ○○県○○市○○区○○町1丁目2番3号 ○○ビル401",
        "代表者": "山田 太郎",
        "法人番号": "0000000000000",
    },
    "targets": {
        "法人番号公表サイト": {"商号": "", "本店": ""},
        "バーチャルオフィス / 賃貸契約": {"本店": ""},
        "法人口座の申込": {"商号": "", "本店": "", "代表者": ""},
        "D-U-N-S (D&B)": {"商号": "", "本店": ""},
        "Apple Developer": {"商号": "", "本店": ""},
        "自社サイトの会社概要": {"商号": "", "本店": "", "代表者": "", "法人番号": ""},
        "請求書テンプレート": {"商号": "", "本店": ""},
        "会計ソフトの事業所設定": {"商号": "", "本店": ""},
    },
}


def diff_marker(base: str, actual: str) -> str:
    """最初に食い違った位置を指す。"""
    i = 0
    while i < min(len(base), len(actual)) and base[i] == actual[i]:
        i += 1
    head = base[:i][-12:]
    tail = actual[i:i + 10] if i < len(actual) else "(ここで途切れている)"
    return f"{DIM}…{head}{RESET}{RED}▸{tail}{RESET}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("file", nargs="?", help="突き合わせ定義のJSON")
    ap.add_argument("--init", action="store_true", help="雛形JSONを出力する")
    ap.add_argument("--strict", action="store_true", help="表記ゆれもエラー（終了コード1）にする")
    args = ap.parse_args()

    if args.init:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0

    if not args.file:
        ap.print_help()
        return 2

    try:
        with open(args.file, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"{RED}ファイルが無い: {args.file}{RESET}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"{RED}JSONが壊れている: {e}{RESET}", file=sys.stderr)
        return 2

    baseline = data.get("baseline") or {}
    targets = data.get("targets") or {}
    if not baseline:
        print(f"{RED}baseline が空。登記簿の表記を入れること{RESET}", file=sys.stderr)
        return 2

    print(f"\n{BOLD}基準（登記簿の表記）{RESET}")
    for k, v in baseline.items():
        print(f"  {k}: {v}")

    n_exact = n_fold = n_bad = n_skip = 0
    problems: list[str] = []

    for place, fields in targets.items():
        lines: list[str] = []
        for key, actual in (fields or {}).items():
            base = baseline.get(key)
            if base is None:
                lines.append(f"    {YEL}?{RESET} {key}: baseline に無い項目")
                continue
            if not str(actual).strip():
                n_skip += 1
                continue
            if actual == base:
                n_exact += 1
                continue
            if normalize(actual) == normalize(base):
                n_fold += 1
                lines.append(
                    f"    {YEL}≈ 表記ゆれ{RESET} {key}\n"
                    f"        登記: {base}\n"
                    f"        実際: {actual}"
                )
                problems.append(f"{place} / {key}（表記ゆれ）")
            else:
                n_bad += 1
                lines.append(
                    f"    {RED}✗ 不一致{RESET} {key}\n"
                    f"        登記: {base}\n"
                    f"        実際: {actual}\n"
                    f"        差分: {diff_marker(base, actual)}"
                )
                problems.append(f"{place} / {key}（不一致）")
        if lines:
            print(f"\n{BOLD}{place}{RESET}")
            print("\n".join(lines))

    print(f"\n{BOLD}結果{RESET}")
    print(f"  {GRN}完全一致 {n_exact}{RESET} / {YEL}表記ゆれ {n_fold}{RESET} / "
          f"{RED}不一致 {n_bad}{RESET} / {DIM}未調査 {n_skip}{RESET}")

    if n_bad:
        print(f"\n{RED}🔴 不一致がある。別の会社・別人として扱われる可能性がある。{RESET}")
    if n_fold:
        print(f"{YEL}⚠️  表記ゆれは「同じ対象の別表記」。審査で減点され得るのでそろえる。{RESET}")
    if n_skip:
        print(f"{DIM}※ 未調査 {n_skip} 件。実際の登録値を調べて埋めること"
              f"（自分で入力していない場所ほど危ない）。{RESET}")
    if not (n_bad or n_fold) and n_exact:
        print(f"{GRN}✅ 入力済みの項目はすべて一致している。{RESET}")

    if problems:
        print(f"\n{BOLD}直すもの{RESET}")
        for p in problems:
            print(f"  - {p}")

    if n_bad:
        return 1
    if n_fold and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
