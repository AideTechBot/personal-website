#!/usr/bin/env python3
"""Fetch standard.site documents from an atproto PDS and emit Jekyll posts.

Resolves the configured handle to a DID and PDS, lists every
`site.standard.document` record in the repo, renders the embedded
`pub.leaflet.content` block structure to HTML, and writes one Jekyll post
per document into _posts/atproto/ (which is gitignored and regenerated on
every build).

Stdlib only — no pip installs needed in CI.
"""

import json
import os
import re
import shutil
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

HANDLE = os.environ.get("ATPROTO_HANDLE", "manoo.dev")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "_posts", "atproto")
PUBLIC_API = "https://public.api.bsky.app"


def get_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mdionne.me-build/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def resolve_identity(handle):
    did = get_json(
        f"{PUBLIC_API}/xrpc/com.atproto.identity.resolveHandle?handle={urllib.parse.quote(handle)}"
    )["did"]
    if did.startswith("did:plc:"):
        doc = get_json(f"https://plc.directory/{did}")
    elif did.startswith("did:web:"):
        domain = did.removeprefix("did:web:")
        doc = get_json(f"https://{domain}/.well-known/did.json")
    else:
        raise ValueError(f"unsupported DID method: {did}")
    pds = next(
        s["serviceEndpoint"]
        for s in doc.get("service", [])
        if s.get("id", "").endswith("atproto_pds")
    )
    return did, pds.rstrip("/")


def list_records(pds, repo, collection):
    records, cursor = [], None
    while True:
        url = (
            f"{pds}/xrpc/com.atproto.repo.listRecords"
            f"?repo={urllib.parse.quote(repo)}&collection={collection}&limit=100"
        )
        if cursor:
            url += f"&cursor={urllib.parse.quote(cursor)}"
        page = get_json(url)
        records.extend(page.get("records", []))
        cursor = page.get("cursor")
        if not cursor or not page.get("records"):
            return records


def blob_cid(blob):
    if not isinstance(blob, dict):
        return None
    ref = blob.get("ref")
    if isinstance(ref, dict) and "$link" in ref:
        return ref["$link"]
    return blob.get("cid")


def blob_url(pds, did, blob):
    cid = blob_cid(blob)
    if not cid:
        return None
    return f"{pds}/xrpc/com.atproto.sync.getBlob?did={urllib.parse.quote(did)}&cid={cid}"


def esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def feature_tags(feature):
    """Map one richtext facet feature to (open_tag, close_tag)."""
    ftype = feature.get("$type", "")
    if ftype.endswith("#link"):
        return f'<a href="{esc(feature.get("uri", ""))}">', "</a>"
    if ftype.endswith("#bold"):
        return "<strong>", "</strong>"
    if ftype.endswith("#italic"):
        return "<em>", "</em>"
    if ftype.endswith("#code"):
        return "<code>", "</code>"
    if ftype.endswith("#underline"):
        return "<u>", "</u>"
    if ftype.endswith("#strikethrough"):
        return "<s>", "</s>"
    if ftype.endswith("#highlight"):
        return "<mark>", "</mark>"
    if ftype.endswith("#didMention"):
        return f'<a href="https://bsky.app/profile/{esc(feature.get("did", ""))}">', "</a>"
    if ftype.endswith("#atMention"):
        href = feature.get("href") or f"https://pdsls.dev/{feature.get('atURI', '')}"
        return f'<a href="{esc(href)}">', "</a>"
    return "", ""


def render_richtext(text, facets):
    """Render plaintext + byte-indexed facets to inline HTML."""
    data = text.encode("utf-8")
    spans = []
    for facet in facets or []:
        index = facet.get("index", {})
        start, end = index.get("byteStart"), index.get("byteEnd")
        if start is None or end is None or start >= end or end > len(data):
            continue
        spans.append((start, end, facet.get("features", [])))
    spans.sort(key=lambda s: (s[0], -s[1]))

    out, pos = [], 0
    for start, end, features in spans:
        if start < pos:  # overlapping facet, skip
            continue
        out.append(esc(data[pos:start].decode("utf-8", "replace")))
        opens, closes = "", ""
        for feature in features:
            open_tag, close_tag = feature_tags(feature)
            opens += open_tag
            closes = close_tag + closes
        out.append(opens + esc(data[start:end].decode("utf-8", "replace")) + closes)
        pos = end
    out.append(esc(data[pos:].decode("utf-8", "replace")))
    return "".join(out).replace("\n", "<br>")


def fetch_bsky_post(at_uri):
    try:
        url = f"{PUBLIC_API}/xrpc/app.bsky.feed.getPosts?uris={urllib.parse.quote(at_uri)}"
        posts = get_json(url).get("posts", [])
        return posts[0] if posts else None
    except Exception:
        return None


def bsky_web_url(at_uri):
    match = re.match(r"at://([^/]+)/app\.bsky\.feed\.post/([^/]+)", at_uri or "")
    if not match:
        return None
    return f"https://bsky.app/profile/{match.group(1)}/post/{match.group(2)}"


ALIGN = {
    "#textAlignCenter": "center",
    "#textAlignRight": "right",
    "#textAlignJustify": "justify",
}


class BlockRenderer:
    def __init__(self, pds, did):
        self.pds = pds
        self.did = did

    def render_pages(self, pages):
        html = []
        for page in pages:
            ptype = page.get("$type", "")
            if ptype == "pub.leaflet.pages.linearDocument":
                for block in page.get("blocks", []):
                    html.append(self.render_block(block))
            # canvas pages have no sane linear HTML representation; skip them
        return "\n".join(part for part in html if part)

    def render_block(self, wrapper):
        block = wrapper.get("block", {})
        style = ""
        align = ALIGN.get(wrapper.get("alignment", ""))
        if align:
            style = f' style="text-align:{align}"'
        btype = block.get("$type", "")
        name = btype.rsplit(".", 1)[-1]
        method = getattr(self, f"block_{name}", None)
        if method:
            return method(block, style)
        return ""

    def block_text(self, block, style):
        size = block.get("textSize")
        cls = f' class="text-{size}"' if size in ("small", "large") else ""
        return f"<p{cls}{style}>{render_richtext(block.get('plaintext', ''), block.get('facets'))}</p>"

    def block_header(self, block, style):
        # document title is the page's h1, so shift header levels down one
        level = min(int(block.get("level", 1)) + 1, 6)
        return f"<h{level}{style}>{render_richtext(block.get('plaintext', ''), block.get('facets'))}</h{level}>"

    def block_blockquote(self, block, style):
        return f"<blockquote{style}><p>{render_richtext(block.get('plaintext', ''), block.get('facets'))}</p></blockquote>"

    def block_code(self, block, style):
        lang = esc(block.get("language", "") or "")
        cls = f' class="language-{lang}"' if lang else ""
        return f"<pre><code{cls}>{esc(block.get('plaintext', ''))}</code></pre>"

    def block_math(self, block, style):
        return f'<div class="math"{style}>\\[{esc(block.get("tex", ""))}\\]</div>'

    def block_horizontalRule(self, block, style):
        return "<hr>"

    def block_image(self, block, style):
        src = blob_url(self.pds, self.did, block.get("image"))
        if not src:
            return ""
        alt = esc(block.get("alt", "") or "")
        ratio = block.get("aspectRatio", {})
        dims = ""
        if ratio.get("width") and ratio.get("height"):
            dims = f' width="{ratio["width"]}" height="{ratio["height"]}"'
        return f'<img src="{esc(src)}" alt="{alt}"{dims} loading="lazy">'

    def block_website(self, block, style):
        src = esc(block.get("src", ""))
        title = render_richtext(block.get("title") or block.get("src", ""), None)
        desc = block.get("description")
        desc_html = f'<span class="website-desc">{esc(desc)}</span>' if desc else ""
        return (
            f'<a class="website-embed" href="{src}">'
            f'<span class="website-title">{title}</span>{desc_html}'
            f'<span class="website-url">{src}</span></a>'
        )

    def block_iframe(self, block, style):
        url = esc(block.get("url", ""))
        height = block.get("height")
        attr = f' height="{height}"' if height else ""
        return f'<iframe src="{url}"{attr} frameborder="0" allowfullscreen loading="lazy"></iframe>'

    def block_bskyPost(self, block, style):
        at_uri = block.get("postRef", {}).get("uri", "")
        web = bsky_web_url(at_uri)
        if not web:
            return ""
        post = fetch_bsky_post(at_uri)
        if post:
            author = post.get("author", {})
            handle = esc(author.get("handle", ""))
            name = esc(author.get("displayName") or handle)
            text = esc(post.get("record", {}).get("text", ""))
            return (
                f'<blockquote class="bsky-embed"><p>{text}</p>'
                f'<footer>&mdash; {name} (@{handle}) &middot; '
                f'<a href="{web}">View on Bluesky</a></footer></blockquote>'
            )
        return f'<p><a href="{web}">View post on Bluesky</a></p>'

    def block_standardSitePost(self, block, style):
        # cross-reference to another standard.site document; link via pdsls
        uri = block.get("postRef", {}).get("uri") or block.get("uri", "")
        if not uri:
            return ""
        return f'<p><a href="https://pdsls.dev/{esc(uri)}">Referenced post</a></p>'

    def block_unorderedList(self, block, style):
        return self.render_list(block.get("children", []), ordered=False)

    def block_orderedList(self, block, style):
        return self.render_list(
            block.get("children", []), ordered=True, start=block.get("startIndex")
        )

    def render_list(self, items, ordered, start=None):
        tag = "ol" if ordered else "ul"
        attr = f' start="{start}"' if ordered and start and start != 1 else ""
        html = [f"<{tag}{attr}>"]
        for item in items:
            content = item.get("content", {})
            inner = self.render_block({"block": content}) or ""
            # list items shouldn't nest a <p>; unwrap simple paragraphs
            if inner.startswith("<p>") and inner.endswith("</p>"):
                inner = inner[3:-4]
            if item.get("checked") is not None:
                checked = " checked" if item["checked"] else ""
                inner = f'<input type="checkbox" disabled{checked}> {inner}'
            nested = ""
            if item.get("children"):
                nested = self.render_list(item["children"], ordered=False)
            elif item.get("orderedListChildren"):
                sub = item["orderedListChildren"]
                nested = self.render_list(
                    sub.get("children", []), ordered=True, start=sub.get("startIndex")
                )
            html.append(f"<li>{inner}{nested}</li>")
        html.append(f"</{tag}>")
        return "".join(html)


def render_content(doc, pds, did):
    content = doc.get("content")
    if isinstance(content, dict) and content.get("$type") == "pub.leaflet.content":
        pages = content.get("pages", [])
        if content.get("blobPages"):
            url = blob_url(pds, did, content["blobPages"])
            if url:
                try:
                    pages = get_json(url)
                except Exception as e:
                    print(f"  warning: failed to fetch blobPages: {e}", file=sys.stderr)
        return BlockRenderer(pds, did).render_pages(pages)
    # unknown content format: fall back to the plaintext representation
    text = doc.get("textContent", "")
    if text:
        return "\n".join(
            f"<p>{esc(par)}</p>" for par in re.split(r"\n\s*\n", text) if par.strip()
        )
    return ""


def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_-]+", "-", value).strip("-")


def doc_slug(doc, rkey):
    path = (doc.get("path") or "").strip("/")
    if path:
        return slugify(path.split("/")[-1]) or rkey
    return slugify(doc.get("title", "")) or rkey


def existing_slugs():
    posts_dir = os.path.join(os.path.dirname(__file__), "..", "_posts")
    slugs = set()
    for name in os.listdir(posts_dir):
        match = re.match(r"\d{4}-\d{2}-\d{2}-(.+)\.\w+$", name)
        if match:
            slugs.add(match.group(1))
    return slugs


def yaml_str(value):
    return json.dumps(value, ensure_ascii=False)


def write_post(doc, uri, pds, did, taken_slugs):
    rkey = uri.rsplit("/", 1)[-1]
    published = doc.get("publishedAt", "")
    date_part = published[:10]
    if not re.match(r"\d{4}-\d{2}-\d{2}", date_part):
        print(f"  skipping {rkey}: bad publishedAt {published!r}", file=sys.stderr)
        return None

    body = render_content(doc, pds, did)
    if not body.strip():
        # metadata-only document (content hosted elsewhere); nothing to render
        print(f"  skipping {rkey}: no inline content", file=sys.stderr)
        return None

    slug = doc_slug(doc, rkey)
    if slug in taken_slugs:
        slug = f"{slug}-{rkey}"
    taken_slugs.add(slug)

    front = ["---", "layout: post", f"title: {yaml_str(doc.get('title', 'Untitled'))}"]
    front.append(f"date: {published}")
    if doc.get("updatedAt"):
        front.append(f"modified: {doc['updatedAt']}")
    if doc.get("description"):
        front.append(f"description: {yaml_str(doc['description'])}")
    if doc.get("tags"):
        front.append(f"tags: [{', '.join(yaml_str(t) for t in doc['tags'])}]")
    front.append(f"atproto_uri: {yaml_str(uri)}")
    bsky_ref = doc.get("bskyPostRef", {})
    if bsky_ref.get("uri"):
        front.append(f"bsky_uri: {yaml_str(bsky_ref['uri'])}")
    front.append("---")

    filename = f"{date_part}-{slug}.html"
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(front) + "\n\n" + body + "\n")
    return filename


def main():
    print(f"Resolving {HANDLE}...")
    did, pds = resolve_identity(HANDLE)
    print(f"  did: {did}\n  pds: {pds}")

    docs = list_records(pds, did, "site.standard.document")
    print(f"Found {len(docs)} site.standard.document record(s)")

    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    taken = existing_slugs()

    count = 0
    for record in docs:
        doc = record.get("value", {})
        filename = write_post(doc, record["uri"], pds, did, taken)
        if filename:
            print(f"  wrote {filename}")
            count += 1
    print(f"Done: {count} post(s) generated in _posts/atproto/")


if __name__ == "__main__":
    main()
