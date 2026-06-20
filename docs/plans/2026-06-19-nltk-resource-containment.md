# NLTK Resource Containment Review

Status: completed

## Scope

Deep-review PR #17 against NLTK 3.9.4 resource decoding, encoded and repeated
encoding, dot segments, Unicode separators, absolute/drive/UNC paths, symlink
resolution, directory and ZIP loaders, configured-root bounds, and the fixed
`corpora/stopwords` integration.

## Root Cause

NLTK 3.9.4 checks encoded resource names before `url2pathname()` decodes them.
Its strict path sentinel catches many decoded escapes, but its private allowed
root provider always trusts the entire system temporary directory. Encoded
absolute paths, encoded `..` segments, and symlinks could therefore read any
otherwise-readable file under that directory even with `ENFORCE = True`.

## Work Completed

- Install strict enforcement before importing NLTK tokenizers or corpora.
- Replace the implicit allowlist with explicit `nltk.data.path` and
  `NLTK_DATA` roots.
- Reject filesystem roots and bound the allowlist to 64 unique roots with
  4,096 characters per root.
- Pin NLTK 3.9.4 while the integration depends on its private sentinel shape.
- Cover percent encoding, repeated encoding, encoded dot segments, Unicode
  separators, POSIX absolute paths, Windows drive and UNC forms, symlink
  escapes, ZIP traversal, and legitimate directory and ZIP resource names.

## Verification Completed

- Focused red tests reproduced five unauthorized temp-directory reads before
  the fix and passed after it.
- Legitimate directory and ZIP resources remained loadable from an explicitly
  configured root.
- The full supported Python matrix, Make gates, dependency checks, hostile
  mutations, hosted checks, and changed-tree secret scan were completed before
  merge.

## Residual Risk

Explicitly configured NLTK data roots are trusted. NLTK may allocate a large
trusted corpus or ZIP member before this sample normalizes provider output, and
Windows-native case-folding behavior is covered by NLTK's platform code rather
than a Windows hosted job. Replace this private containment override when a
stable upstream patched release is available.
