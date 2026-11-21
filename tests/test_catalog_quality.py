#!/usr/bin/env python3
"""Unit tests for metadata catalog integrity checks (stdlib only)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_catalog import check_catalog  # noqa: E402


def item(id, title, url, **extra):
    return {
        "id": id,
        "category": "Testing",
        "title": title,
        "source_url": url,
        "pdf_status": "not downloaded",
        "pdf_available_at_source": True,
        "year": 2024,
        **extra,
    }


class CatalogTests(unittest.TestCase):
    def codes(self, records):
        return [x["code"] for x in check_catalog(records)["errors"]]

    def test_valid_records(self):
        records = [
            item("RSP-001", "Motor A", "https://example.edu/a.pdf"),
            item("RSP-002", "Motor B", "https://example.edu/b.pdf"),
        ]
        self.assertEqual(self.codes(records), [])

    def test_duplicate_identifier(self):
        a = item("RSP-001", "Motor A", "https://example.edu/a.pdf")
        b = item("RSP-001", "Motor B", "https://example.edu/b.pdf")
        self.assertIn("duplicate_id", self.codes([a, b]))

    def test_duplicate_title_normalized(self):
        a = item("RSP-001", "Motor: A", "https://example.edu/a.pdf")
        b = item("RSP-002", "motor a!", "https://example.edu/b.pdf")
        self.assertIn("duplicate_title", self.codes([a, b]))

    def test_duplicate_source_strips_download_query(self):
        a = item("RSP-001", "Motor A", "https://example.edu/a.pdf")
        b = item("RSP-002", "Motor B", "https://example.edu/a.pdf?download=1")
        self.assertIn("duplicate_source", self.codes([a, b]))

    def test_duplicate_doi(self):
        a = item("RSP-001", "Motor A", "https://example.edu/a.pdf", doi="10.1234/test")
        b = item("RSP-002", "Motor B", "https://example.edu/b.pdf", doi="10.1234/TEST")
        self.assertIn("duplicate_doi", self.codes([a, b]))

    def test_no_pdf_requires_correct_status(self):
        a = item("RSP-001", "Motor A", "https://example.edu/a", pdf_available_at_source=False)
        self.assertIn("pdf_availability_conflict", self.codes([a]))
        a["pdf_status"] = "not available"
        self.assertEqual(self.codes([a]), [])

    def test_no_pdf_citation_is_valid(self):
        a = item("RSP-001", "Motor A", "https://ntrs.nasa.gov/citations/12345678",
                 pdf_available_at_source=False, pdf_status="not available")
        self.assertEqual(self.codes([a]), [])

    def test_citation_page_cannot_be_verified_pdf(self):
        a = item("RSP-001", "Motor A", "https://ntrs.nasa.gov/citations/12345678")
        self.assertIn("citation_page_marked_as_pdf", self.codes([a]))

    def test_bad_year(self):
        a = item("RSP-001", "Motor A", "https://example.edu/a.pdf", year=2101)
        self.assertIn("invalid_publication_year", self.codes([a]))


if __name__ == "__main__":
    unittest.main()
