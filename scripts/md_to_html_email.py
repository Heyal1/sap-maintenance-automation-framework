#!/usr/bin/env python3
"""
Convert Markdown report files to styled HTML for email delivery.

Requires: pip install markdown
Usage:
    python3 md_to_html_email.py input.md output.html [--title "Report Title"]
"""

import re
import subprocess
import sys

try:
    import markdown
except ImportError:
    print("'markdown' package not found, installing...", file=sys.stderr)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'markdown'])
    import markdown


CSS_STYLE = """
<style>
  body {
    font-family: -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #24292e;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
  }
  h1 { color: #0366d6; border-bottom: 2px solid #0366d6; padding-bottom: 8px; font-size: 24px; }
  h2 { color: #24292e; border-bottom: 1px solid #e1e4e8; padding-bottom: 6px; margin-top: 24px; font-size: 20px; }
  h3 { color: #586069; margin-top: 20px; font-size: 16px; }
  h4 { color: #6a737d; margin-top: 16px; font-size: 14px; }
  h5 { color: #6a737d; font-size: 13px; font-weight: 600; }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 13px;
  }
  th {
    background-color: #0366d6;
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
  }
  td {
    padding: 6px 12px;
    border: 1px solid #e1e4e8;
  }
  tr:nth-child(even) { background-color: #f6f8fa; }
  tr:hover { background-color: #eaf5ff; }
  code {
    background-color: #f6f8fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 12px;
    font-family: 'SFMono-Regular', Consolas, monospace;
  }
  pre {
    background-color: #f6f8fa;
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 12px;
    border: 1px solid #e1e4e8;
  }
  pre code { background: none; padding: 0; }
  hr { border: none; border-top: 1px solid #e1e4e8; margin: 20px 0; }
  ul, ol { padding-left: 24px; }
  li { margin: 4px 0; }
  details {
    margin: 12px 0;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 8px 12px;
  }
  details summary {
    cursor: pointer;
    font-weight: 600;
    color: #586069;
    padding: 4px 0;
  }
  details[open] summary { margin-bottom: 8px; }
  .status-success { color: #22863a; font-weight: bold; }
  .status-failure { color: #cb2431; font-weight: bold; }
  .status-warning { color: #e36209; font-weight: bold; }
  .status-partial { color: #e36209; font-weight: bold; }
  .status-skipped { color: #6a737d; }
  .status-changed { color: #0366d6; font-weight: bold; }
  .status-unchanged { color: #6a737d; }
  .banner {
    background: linear-gradient(135deg, #0366d6, #0550ae);
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  .banner h1 { color: white; border: none; margin: 0; padding: 0; font-size: 22px; }
  .banner p { color: #c8e1ff; margin: 4px 0 0 0; font-size: 13px; }
  .footer {
    margin-top: 30px;
    padding-top: 12px;
    border-top: 1px solid #e1e4e8;
    color: #6a737d;
    font-size: 12px;
  }
</style>
"""


STATUS_PATTERNS = [
    (r'\bSUCCESS\b', '<span class="status-success">SUCCESS</span>'),
    (r'\bFAILURE\b', '<span class="status-failure">FAILURE</span>'),
    (r'\bFAILED\b', '<span class="status-failure">FAILED</span>'),
    (r'\bPARTIAL\b', '<span class="status-partial">PARTIAL</span>'),
    (r'\bWARNING\b', '<span class="status-warning">WARNING</span>'),
    (r'\bSKIPPED\b', '<span class="status-skipped">SKIPPED</span>'),
    (r'\bCHANGED\b', '<span class="status-changed">CHANGED</span>'),
    (r'\bUNCHANGED\b', '<span class="status-unchanged">UNCHANGED</span>'),
    (r'\bGREEN\b', '<span class="status-success">GREEN</span>'),
    (r'\bRED\b', '<span class="status-failure">RED</span>'),
    (r'\bYELLOW\b', '<span class="status-warning">YELLOW</span>'),
    (r'\bGRAY\b', '<span class="status-skipped">GRAY</span>'),
    (r'\bOK\b', '<span class="status-success">OK</span>'),
    (r'\bDEGRADED\b', '<span class="status-failure">DEGRADED</span>'),
    (r'\bCRITICAL\b', '<span class="status-failure">CRITICAL</span>'),
]


def colorize_status(html_text):
    """Add color CSS classes to known status keywords in rendered HTML."""
    for pattern, replacement in STATUS_PATTERNS:
        html_text = re.sub(pattern, replacement, html_text)
    return html_text


def clean_table_blanks(md_text):
    """Remove blank lines within markdown tables (Jinja2 template artifact).

    Jinja2 control blocks ({% for %}, {% if %}, {% set %}) leave blank lines
    between table rows after rendering. python-markdown breaks tables at blank
    lines, so we collapse them here.
    """
    lines = md_text.split('\n')
    result = []
    for i, line in enumerate(lines):
        if line.strip() == '':
            # look back for a table row
            prev = next((result[j].strip() for j in range(len(result) - 1, -1, -1)
                         if result[j].strip()), None)
            # look ahead for a table row
            nxt = next((lines[j].strip() for j in range(i + 1, len(lines))
                        if lines[j].strip()), None)
            if (prev and prev.startswith('|') and prev.endswith('|') and
                    nxt and nxt.startswith('|') and nxt.endswith('|')):
                continue  # skip blank line between table rows
        result.append(line)
    return '\n'.join(result)


def convert_details_blocks(md_text):
    """Convert <details>/<summary> blocks to markdown-compatible format.

    Email clients don't support <details>/<summary> HTML tags. Instead,
    extract the content, let markdown process it normally, then wrap it
    in email-friendly styled divs during post-processing.
    """
    # Replace <details>/<summary> with marker comments that survive markdown
    # processing, so we can style them in post-processing.
    def replace_block(m):
        summary_text = m.group(1).strip()
        inner_content = m.group(2).strip()
        # Use HTML comments as markers + render inner content as normal markdown
        return (
            f'\n<!-- details-start -->\n'
            f'<!-- details-summary:{summary_text} -->\n\n'
            f'{inner_content}\n\n'
            f'<!-- details-end -->\n'
        )

    return re.sub(
        r'<details>\s*\n\s*<summary>(.*?)</summary>\s*\n(.*?)</details>',
        replace_block, md_text, flags=re.DOTALL,
    )


def style_details_sections(html_text):
    """Convert detail markers to email-compatible styled sections."""
    # Replace markers with styled divs
    html_text = re.sub(
        r'<!-- details-start -->\s*',
        '<div style="margin:12px 0;border:1px solid #e1e4e8;border-radius:6px;padding:0;">',
        html_text,
    )
    html_text = re.sub(
        r'<!-- details-summary:(.*?) -->\s*',
        r'<div style="background:#f6f8fa;padding:8px 12px;font-weight:600;color:#586069;'
        r'border-bottom:1px solid #e1e4e8;border-radius:6px 6px 0 0;">\1</div>'
        r'<div style="padding:8px 12px;">',
        html_text,
    )
    html_text = re.sub(
        r'\s*<!-- details-end -->',
        '</div></div>',
        html_text,
    )
    return html_text


def md_to_html(md_text, title="SAP Report"):
    """Convert markdown text to styled HTML using python-markdown."""
    md_text = clean_table_blanks(md_text)
    md_text = convert_details_blocks(md_text)

    body = markdown.markdown(
        md_text,
        extensions=['extra', 'sane_lists', 'toc'],
        output_format='html5',
    )

    body = colorize_status(body)
    body = style_details_sections(body)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{CSS_STYLE}
</head>
<body>
<div class="banner">
  <h1>{title}</h1>
  <p>Generated by SAP Maintenance Automation Framework</p>
</div>
{body}
<div class="footer">
  This report was automatically generated. For questions, contact the SAP Basis team.
</div>
</body>
</html>"""


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.md output.html [--title 'Title']")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    title = "SAP Report"
    if '--title' in sys.argv:
        idx = sys.argv.index('--title')
        if idx + 1 < len(sys.argv):
            title = sys.argv[idx + 1]

    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = md_to_html(md_content, title)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Converted: {input_file} -> {output_file}")
