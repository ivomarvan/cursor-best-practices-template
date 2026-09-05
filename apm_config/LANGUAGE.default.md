# Communication Language — Default Configuration

English is the default communication language shipped with the template. A consuming
project overrides this file **in full** by creating `doc/apm_config/LANGUAGE.user.md` —
see the Config Resolution mechanism in `rules/20-project-design-rules.mdc`. The
install/migration script's `--lang` parameter seeds `LANGUAGE.user.md` automatically on
first install (see `scripts/install-into-project.sh`).

## Active Setting

| Parameter | Value |
|-----|----|
| `<communication-language>` | English |
| `<lang-code>` | `en` |

> `<lang-code>` = `en` → omit `<!-- <lang-code>: ... -->` translation comments; English
> text is already the communication language.
