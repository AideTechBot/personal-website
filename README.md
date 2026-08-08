This is the repo for my personal website. Live at [https://mdionne.me](https://mdionne.me/?utm_source=Github&utm_medium=Readme&utm_campaign=Aug2024)

To run locally: `docker compose up`, or with Ruby on the host:

```sh
bundle install
bundle exec jekyll serve --livereload
```

On NixOS, `nix-shell -p ruby_3_3 bundler python3` covers both the site and the
fetch script. No `nix-ld` or FHS wrapper is needed — the precompiled `nokogiri`
and `sass-embedded` gems run as-is.

## Blog posts from atproto (standard.site)

Blog posts are no longer committed to this repo as markdown. At build time,
`script/fetch-atproto-posts.py` pulls every
[`site.standard.document`](https://standard.site/docs/lexicons/document) record
from the atproto PDS of [`manoo.dev`](https://bsky.app/profile/manoo.dev),
renders the Leaflet (`pub.leaflet.content`) block content to HTML, and writes
them into `_posts/atproto/` (gitignored) so Jekyll treats them as regular
posts.

Publishing flow:

1. Write and publish a post with any standard.site-compatible tool
   (e.g. [Leaflet](https://leaflet.pub)) using the `manoo.dev` account.
2. The GitHub Actions workflow (`.github/workflows/build-deploy.yml`) rebuilds
   the site daily at 04:23 UTC (and on every push to `master`), picking up new
   posts automatically. Trigger it manually from the Actions tab to publish
   sooner.

Post URLs come from the document title, slugified — "Adding standard.site to my
website" becomes `/adding-standard-site-to-my-website`. A document's `path` is
used instead when it is set to something other than the record key (Leaflet
defaults it to the rkey). Duplicate titles get the record key appended to keep
them distinct.

Bluesky comments: if a document has a `bskyPostRef` (Leaflet's "share to
Bluesky" sets this), replies to that Bluesky post are rendered under the
article via the client-side widget in `_includes/bsky-comments.html`. Legacy
markdown posts can opt in by adding `bsky_uri: at://...` to their front
matter.

Fetch posts locally with `python3 script/fetch-atproto-posts.py` (override the
account with `ATPROTO_HANDLE=...`).

> **One-time setup:** in the repo settings, Pages → Build and deployment →
> Source must be set to **GitHub Actions** (instead of "Deploy from a
> branch"), otherwise the legacy Pages build keeps deploying without the
> atproto posts. The custom domain (mdionne.me) setting is unaffected.
