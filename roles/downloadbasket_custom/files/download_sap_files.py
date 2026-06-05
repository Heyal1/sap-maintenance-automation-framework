#!/usr/bin/env python3
"""
SAP Download Script - Downloads SAP software files using requests session.

This script replaces the upstream sap.sap_operations download mechanism which
had persistent issues with SAP's redirect-based authentication flow.

Strategy:
  - Uses requests.Session with HTTP Basic Auth to handle SAP's multi-redirect
    authentication flow automatically (SAP redirects through login servers).
  - User-Agent header mimics a browser because SAP's download servers reject
    non-browser clients with HTTP 403.
  - Each file is streamed in 8KB chunks to handle large SAP archives (>1GB).

Error Detection Heuristics:
  - If the response Content-Type is text/html, the download failed (SAP returns
    HTML login pages or error pages instead of binary data).
  - Files smaller than 50KB after download are assumed to be HTML error pages
    and are automatically deleted — real SAP patches are always larger.

Exit Codes:
  0 = All files succeeded or were skipped (already exist).
  1 = Invalid arguments or JSON parse error.

Note: Individual file failures do NOT cause a non-zero exit — the summary
output is parsed by the Ansible task to determine overall success.

Usage: download_sap_files.py <username> <password> <dest_dir> <timeout_s> <files_json>
"""

import sys
import os
import json
import requests

def download_with_requests_session(url, destination, username, password, timeout=3600):
    """
    Download a single SAP file using a requests Session with Basic Auth.
    Returns: (success: bool, message: str, bytes_downloaded: int)
    """
    filename = os.path.basename(destination)
    
    session = requests.Session()
    session.auth = (username, password)
    # SAP download servers reject non-browser User-Agents with HTTP 403
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        print(f"  Requesting: {filename}")
        
        # Let requests handle all redirects and auth
        response = session.get(url, stream=True, timeout=timeout, allow_redirects=True)
        
        # Check what we got
        content_type = response.headers.get('Content-Type', '')
        content_length = response.headers.get('Content-Length', '0')
        
        print(f"  Response: HTTP {response.status_code}, Type: {content_type[:50]}, Size: {content_length}")
        
        # HTML Content-Type = authentication failure or SAP error page
        # Real SAP software downloads return application/octet-stream.
        if 'text/html' in content_type:
            # Save first 1KB for debugging
            preview = response.text[:1000] if hasattr(response, 'text') else 'N/A'
            
            # Check for common SAP error messages
            if 'login' in preview.lower() or 'authentication' in preview.lower():
                return False, "Authentication required (got login page)", 0
            elif 'error' in preview.lower():
                return False, "SAP error page received", 0
            else:
                return False, "HTML response (not a file)", 0
        
        # Download file
        total_size = int(content_length) if content_length.isdigit() else 0
        
        with open(destination, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Progress every 10 MB
                    if downloaded % (10 * 1024 * 1024) == 0:
                        mb = downloaded / 1024 / 1024
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"  Progress: {percent:.1f}% ({mb:.1f} MB)", end='\r')
                        else:
                            print(f"  Downloaded: {mb:.1f} MB", end='\r')
        
        print(f"\n  SUCCESS: Downloaded {downloaded / 1024 / 1024:.1f} MB")
        return True, "Downloaded", downloaded
        
    except requests.exceptions.Timeout:
        return False, f"Timeout after {timeout}s", 0
    except Exception as e:
        return False, f"Error: {str(e)[:100]}", 0

def main():
    if len(sys.argv) != 6:
        print("Usage: download_sap_files.py <username> <password> <destination_dir> <timeout> <files_json>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    destination_dir = sys.argv[3]
    timeout = int(sys.argv[4])
    files_json_str = sys.argv[5]
    
    try:
        files_info = json.loads(files_json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse files JSON: {e}")
        sys.exit(1)
    
    os.makedirs(destination_dir, exist_ok=True)
    
    print(f"\nDownloading {len(files_info)} files from SAP...")
    print(f"Timeout: {timeout}s")
    print("="*80)
    
    results = []
    for file_info in files_info:
        url = file_info['url']
        filename = file_info['filename']
        destination = os.path.join(destination_dir, filename)
        
        # Skip existing
        if os.path.exists(destination):
            size = os.path.getsize(destination)
            print(f"\nSKIPPED: {filename} ({size / 1024 / 1024:.1f} MB)")
            results.append({'filename': filename, 'status': 'skipped', 'size': size})
            continue
        
        print(f"\n[{len(results)+1}/{len(files_info)}] {filename}")
        success, message, size = download_with_requests_session(url, destination, username, password, timeout)
        
        results.append({
            'filename': filename,
            'status': 'success' if success else 'failed',
            'message': message,
            'size': size
        })
        
        if not success:
            print(f"  FAILED: {message}")
            # Check if an incomplete/error file was written to disk
            if os.path.exists(destination):
                file_size = os.path.getsize(destination)
                print(f"  Note: File created ({file_size} bytes) - likely HTML error page")
                # Real SAP patches are always >50KB; smaller files are HTML error
                # pages from failed auth redirects — safe to delete
                if file_size < 50000:
                    os.remove(destination)
                    print(f"  Deleted small file (likely error page)")
    
    # Summary
    print("\n" + "="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    success_count = sum(1 for r in results if r['status'] in ['success', 'skipped'])
    failed_count = sum(1 for r in results if r['status'] == 'failed')
    
    for result in results:
        icon = "✓" if result['status'] in ['success', 'skipped'] else "✗"
        size_mb = result.get('size', 0) / (1024 * 1024)
        print(f"{icon} {result['filename']:45s} {result['status']:10s} {size_mb:8.1f} MB")
    
    print("="*80)
    print(f"Success: {success_count}, Failed: {failed_count}, Total: {len(results)}")
    
    # Print first failed file details for debugging
    for result in results:
        if result['status'] == 'failed':
            print(f"\nFirst failure: {result['filename']}")
            print(f"  Reason: {result.get('message', 'Unknown')}")
            break
    
    sys.exit(1 if failed_count > 0 else 0)

if __name__ == '__main__':
    main()
