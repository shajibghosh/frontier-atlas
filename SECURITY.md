# Security and public indexing policy

FrontierAtlas is a **public, static research catalog**. Its contents are intended to be read by visitors, downloaded, cloned, and indexed by GitHub and search engines. **A public repository and public GitHub Pages website cannot keep included information secret.** `robots.txt`, `noindex`, hidden elements, and Git history rewriting are not reliable secrecy or access-control mechanisms.

## Publication boundary

Only publish the openly shareable material under this repository. The public catalog includes 100 problem summaries and research directions, citations, metadata, open-source site code, static generated HTML, and approved project artwork. It intentionally excludes local copies of editable reports, private research notes, accounts, credentials, raw unpublished data, person-specific information, and temporary build files.

`python scripts/prepublish_audit.py` performs an additional heuristic public-release scan. It is not capable of detecting every credential, personal identifier, malicious dependency, or license issue; manual approval remains necessary.

**Never commit or submit** API keys, personal access tokens, SSH keys, `.env` files, participant or patient data, embargoed manuscripts, private correspondence, internal URLs, or files you lack permission to publish. The `.gitignore` reduces accidental staging, but it does not secure tracked files or Git history. Check `git status`, `git diff --cached`, and the full repository history before publication.

## Website design and search privacy

- Search and faceted filtering run completely in the visitor's browser over an embedded public JSON catalog. They do not use a server-side search index, database, search vendor, API keys, analytics, third-party JavaScript, remote fonts, or tracking pixels.
- Search text remains local to the page; it is not written to the URL or sent to a server by the application. Visitor-initiated clicks on external source links leave this site. Link targets open with `noopener noreferrer` and a `no-referrer` policy.
- The browser stores only optional bookmarks and the preferred theme in `localStorage`; this is not a secure store for secrets. No personal accounts or logins are offered.
- The generated HTML uses a build-time **SHA-256 Content Security Policy** for its local JavaScript/CSS, prohibits all network `connect-src` requests and all embedded frames/objects, disallows inline event-handler code, and escapes catalog content rendered into the DOM.
- Static bibliography URLs must use HTTPS and are checked when the data is validated. Links are bibliographic references, not endorsements. Exported CSV cells are guarded against spreadsheet formula injection.
- GitHub Pages is public hosting, not a confidential document storage service. GitHub and other infrastructure providers may keep routine request logs outside the site's control.

## Supply chain and publishing

The website and data-processing scripts use only Python's standard library and native browser JavaScript. GitHub Actions use the repository's ephemeral `GITHUB_TOKEN`; no secret should be inserted into the source or workflows. The publishing job limits write permissions to Pages deployment (`pages: write`, `id-token: write`), while validation/build uses read-only content access.

Review pull requests and GitHub Actions changes before merging. Keep branch protection or rulesets enabled where available; require review and CI checks if external contributors are accepted. No software or automated test can guarantee the total absence of vulnerabilities or harmful links.

## Vulnerability reporting

Do not post sensitive security information or exploit details in a public issue. Use GitHub's private vulnerability reporting feature if it is enabled, or contact the repository maintainers through a private channel. Do not disclose a private contact address or token in repository files just to enable reporting.

## SEO and indexing

This edition **allows indexing of approved public information** by default. If a later version is intended to be less discoverable, add appropriate crawler directives as a discoverability hint, but do **not** interpret `noindex` or `robots.txt` as a protection against disclosure. To keep information private, do not publish it in a public repository or public Pages deployment.
