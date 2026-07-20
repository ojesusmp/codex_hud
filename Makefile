.PHONY: test audit verify install uninstall

test:
	python3 -m unittest discover -s tests -v

audit:
	python3 scripts/validate_public.py

verify:
	python3 -m py_compile bin/codex-hud tests/test_hud.py scripts/validate_public.py
	python3 -m unittest discover -s tests -v
	python3 scripts/validate_public.py
	bash -n install.sh uninstall.sh

install:
	./install.sh

uninstall:
	./uninstall.sh
