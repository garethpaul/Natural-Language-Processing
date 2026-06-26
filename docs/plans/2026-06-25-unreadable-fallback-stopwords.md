---
title: Unreadable Checked-In Stopword Fallback
type: fix
status: completed
date: 2026-06-25
---

# Unreadable Checked-In Stopword Fallback

## Problem

When NLTK stopwords are unavailable, the detector loads `stop_words.txt`. A
missing, unreadable, or undecodable fallback file raised through the default
detector path instead of producing empty language evidence.

## Decision

The checked-in fallback failure guard treats local fallback I/O and Unicode
decoding failures like an unavailable default corpus: return an empty mapping
so detection yields `unknown`. The direct `load_checked_in_stop_words` helper
remains unchanged so explicit callers can still observe file errors.

## Verification Completed

- Patched the default fallback loader to raise `OSError`; `load_stopword_sets()`
  returned `{}` and `detect_language()` returned `unknown`.
- Verified direct loader calls still raise for a missing explicit path.
- Ran all local Make gates, including the mutation harness and baseline checker.
