# v0.0.5

Add an LLM-controlled image_url input for autonomous Agents. HTTPS download is handled inside the tool; no workflow download node is required. Keep file inputs as an optional fallback. Return cropped PNG files and metadata. Validate public network targets and redirects, preserve signed URL queries, and cap downloads at 20 MiB. Local SDK tests passed; cloud Agent execution has not been verified.
