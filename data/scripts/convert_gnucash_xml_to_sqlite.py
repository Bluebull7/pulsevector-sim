#!/usr/bin/env python3
"""Convert a GnuCash XML (.gnucash) file to a GnuCash SQLite (.gnucash) file.

Copies the Chart of Accounts (accounts + hierarchy). Does NOT copy transactions.

Why:
- `piecash` (Python automation library) works best with SQLite books.

Install:
  pip install piecash==1.2.1

Usage:
  python3 convert_gnucash_xml_to_sqlite.py <input_xml.gnucash> <output_sqlite.gnucash>

Notes:
- The created SQLite book's *default* currency is set to the root account's currency
  (falls back to EUR if not found). Individual account commodities are preserved
  when they are CURRENCY commodities.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

from piecash import create_book
from piecash.core.account import Account
from piecash.core.commodity import Commodity


NS = {
    "gnc": "http://www.gnucash.org/XML/gnc",
    "act": "http://www.gnucash.org/XML/act",
    "cmdty": "http://www.gnucash.org/XML/cmdty",
}


@dataclass(frozen=True)
class AcctRec:
    guid: str
    name: str
    type: str
    parent_guid: Optional[str]
    commodity_space: Optional[str]
    commodity_id: Optional[str]


def _findtext(el: ET.Element, path: str) -> str:
    t = el.findtext(path, default="", namespaces=NS)
    return (t or "").strip()


def parse_accounts(xml_path: str) -> Tuple[List[AcctRec], Optional[str], Optional[str]]:
    """Return (accounts, root_guid, template_root_guid)."""
    root = ET.parse(xml_path).getroot()

    accounts: List[AcctRec] = []
    root_guid = None
    template_root_guid = None

    for acct in root.findall(".//gnc:account", NS):
        guid = _findtext(acct, "act:id")
        name = _findtext(acct, "act:name")
        typ = _findtext(acct, "act:type")
        parent_guid = _findtext(acct, "act:parent") or None

        comm = acct.find("act:commodity", NS)
        cspace = cid = None
        if comm is not None:
            cspace = _findtext(comm, "cmdty:space") or None
            cid = _findtext(comm, "cmdty:id") or None

        if typ == "ROOT" and name == "Root Account":
            root_guid = guid
        if typ == "ROOT" and name == "Template Root":
            template_root_guid = guid

        accounts.append(
            AcctRec(
                guid=guid,
                name=name,
                type=typ,
                parent_guid=parent_guid,
                commodity_space=cspace,
                commodity_id=cid,
            )
        )

    return accounts, root_guid, template_root_guid


def get_or_create_currency(book, code: str) -> Commodity:
    """Return a CURRENCY commodity for ISO code (EUR, USD, etc.), creating if missing."""
    code = code.strip().upper()
    for c in book.commodities:
        if c.namespace == "CURRENCY" and c.mnemonic == code:
            return c

    # Minimal metadata; GnuCash can refine this later.
    fullname = {
        "USD": "US Dollar",
        "EUR": "Euro",
        "GBP": "Pound Sterling",
        "JPY": "Japanese Yen",
    }.get(code, code)

    comm = Commodity(
        namespace="CURRENCY",
        mnemonic=code,
        fullname=fullname,
        fraction=100,
        quote_flag=0,
        book=book,
    )
    book.session.add(comm)
    return comm


def detect_default_currency(accts: List[AcctRec], root_guid: Optional[str]) -> str:
    if not root_guid:
        return "EUR"
    rec = next((a for a in accts if a.guid == root_guid), None)
    if rec and rec.commodity_space == "CURRENCY" and rec.commodity_id:
        return rec.commodity_id
    return "EUR"


def build_sqlite_book(xml_path: str, out_path: str) -> None:
    accts, root_guid, template_root_guid = parse_accounts(xml_path)
    default_currency = detect_default_currency(accts, root_guid)

    # Create a fresh SQLite-backed book
    book = create_book(sqlite_file=out_path, currency=default_currency, overwrite=True)

    # Map XML root/template GUIDs to the new book roots
    guid_to_obj: Dict[str, Account] = {}
    if root_guid:
        guid_to_obj[root_guid] = book.root_account
    if template_root_guid:
        guid_to_obj[template_root_guid] = book.root_template

    # Build children lookup for a stable traversal
    children: Dict[Optional[str], List[AcctRec]] = defaultdict(list)
    for a in accts:
        if a.type == "ROOT":
            continue
        children[a.parent_guid].append(a)

    # Depth-first from root_guid when available; otherwise hang everything off Root Account.
    created = 0

    def create_subtree(parent_guid: Optional[str], parent_obj: Account) -> None:
        nonlocal created
        for a in sorted(children.get(parent_guid, []), key=lambda r: r.name):
            commodity = None
            if a.commodity_space == "CURRENCY" and a.commodity_id:
                commodity = get_or_create_currency(book, a.commodity_id)

            acc = Account(
                name=a.name,
                type=a.type,
                commodity=commodity,
                parent=parent_obj,
                book=book,
            )
            book.session.add(acc)
            guid_to_obj[a.guid] = acc
            created += 1
            create_subtree(a.guid, acc)

    # Root-driven creation
    if root_guid and root_guid in guid_to_obj:
        create_subtree(root_guid, guid_to_obj[root_guid])
    else:
        # Fallback: anything without a resolvable parent gets attached to Root Account
        for a in sorted([x for x in accts if x.type != "ROOT"], key=lambda r: r.name):
            parent_obj = guid_to_obj.get(a.parent_guid, book.root_account)
            commodity = None
            if a.commodity_space == "CURRENCY" and a.commodity_id:
                commodity = get_or_create_currency(book, a.commodity_id)
            acc = Account(
                name=a.name,
                type=a.type,
                commodity=commodity,
                parent=parent_obj,
                book=book,
            )
            book.session.add(acc)
            guid_to_obj[a.guid] = acc
            created += 1

    book.save()
    print(f"Wrote {out_path}")
    print(f"Accounts created: {created}")


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python3 convert_gnucash_xml_to_sqlite.py <input_xml.gnucash> <output_sqlite.gnucash>",
            file=sys.stderr,
        )
        return 2

    xml_path, out_path = argv[1], argv[2]
    build_sqlite_book(xml_path, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
