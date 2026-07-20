# Releasing

1. Ensure `main` is current and clean.
2. Update `VERSION` in `bin/codex-hud`.
3. Move changelog entries from Unreleased into a dated semantic-version section.
4. Run:

   ```bash
   python3 -m py_compile bin/codex-hud tests/test_hud.py
   python3 -m unittest discover -s tests -v
   NO_COLOR=1 bin/codex-hud
   ```

5. Open and merge a release pull request.
6. Create a signed or annotated tag named `vX.Y.Z`.
7. Publish GitHub release notes derived from the changelog.
8. Confirm the CI workflow succeeds for the tag and default branch.
