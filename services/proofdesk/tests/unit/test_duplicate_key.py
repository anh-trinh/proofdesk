"""The duplicate key identifies the same invoice however its fields were formatted."""

from datetime import date

from proofdesk.validation.dedup import duplicate_key
from tests.factories import ex, make_invoice


def test_same_invoice_in_different_formatting_has_the_same_key() -> None:
    plain = make_invoice(
        seller_tax_id=ex("51824753556"), invoice_number=ex("INV-0123"), series=ex("c26taa")
    )
    messy = make_invoice(
        seller_tax_id=ex("51 824 753 556"), invoice_number=ex(" inv 0123 "), series=ex("C26TAA")
    )
    assert duplicate_key(plain) == duplicate_key(messy)


def test_a_different_number_gives_a_different_key() -> None:
    assert duplicate_key(make_invoice()) != duplicate_key(make_invoice(invoice_number=ex("9")))


def test_a_different_seller_gives_a_different_key() -> None:
    other = make_invoice(seller_tax_id=ex("0123456789"))
    assert duplicate_key(make_invoice()) != duplicate_key(other)


def test_a_different_date_gives_a_different_key() -> None:
    other = make_invoice(issue_date=ex(date(2026, 11, 6)))
    assert duplicate_key(make_invoice()) != duplicate_key(other)


def test_key_is_a_hash_and_does_not_contain_the_inputs() -> None:
    key = duplicate_key(make_invoice())
    assert key is not None
    assert len(key) == 64
    assert "0000123" not in key


def test_missing_part_gives_no_key() -> None:
    assert duplicate_key(make_invoice(invoice_number=ex(None))) is None
