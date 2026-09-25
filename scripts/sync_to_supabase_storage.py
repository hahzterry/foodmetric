"""
sync_to_supabase_storage.py — Cloud Storage Sync Engine (Zero-Cost, No Credit Card)
=====================================================================================
Sync all MP4 videos from web/public/videos/ to Supabase Storage (1GB Free Tier, no card required).
Completely decouples the video repository from Git to keep the source code ultra-lightweight.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = PROJECT_ROOT / "web" / "public" / "videos"
CDN_LINKS_JSON = PROJECT_ROOT / "web" / "public" / "data" / "video_cdn_links.json"

def load_env_vars():
    """Reads environment variables from .env.local if present."""
    env_file = PROJECT_ROOT / ".env.local"
    if not env_file.exists():
        env_file = PROJECT_ROOT / "web" / ".env.local"
    
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def main():
    load_env_vars()
    supabase_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key or "your-project" in supabase_url:
        print("=" * 70)
        print("[!] SUPABASE ENVIRONMENT VARIABLES NOT CONFIGURED")
        print("=" * 70)
        print("To sync videos to Supabase Storage (1GB Free, $0, no credit card):")
        print("1. Open the .env.local file in the project root.")
        print("2. Enter your Supabase project details:")
        print("   NEXT_PUBLIC_SUPABASE_URL=https://<project-id>.supabase.co")
        print("   SUPABASE_SERVICE_ROLE_KEY=<service-role-secret-key>")
        print("3. Run again: python scripts/sync_to_supabase_storage.py")
        print("=" * 70)
        return

    try:
        from supabase import create_client, Client
    except ImportError:
        print("[!] Installing supabase library...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase"])
        from supabase import create_client, Client

    print(f"[*] Connecting to Supabase Storage: {supabase_url}...")
    client: Client = create_client(supabase_url, supabase_key)

    # US-specific bucket name
    bucket_name = "foodmetric-us-videos"

    # Check or create public bucket
    try:
        buckets = client.storage.list_buckets()
        existing = [b.name for b in buckets]
        if bucket_name not in existing:
            print(f"[*] Creating new public storage bucket: '{bucket_name}'...")
            client.storage.create_bucket(bucket_name, options={"public": True})
            print(f"[✓] Successfully created bucket: {bucket_name}")
        else:
            print(f"[✓] Bucket '{bucket_name}' is ready.")
    except Exception as e:
        print(f"[!] Bucket check error: {e}")

    # Upload each video to Supabase Storage
    video_files = sorted(VIDEOS_DIR.glob("*.mp4"))
    print(f"[*] Found {len(video_files)} video files to sync...")

    success_count = 0
    cdn_links: Dict[str, str] = {}

    for idx, v_file in enumerate(video_files, 1):
        file_name = v_file.name
        file_size_mb = v_file.stat().st_size / (1024 * 1024)
        print(f"[{idx}/{len(video_files)}] Uploading {file_name} ({file_size_mb:.2f} MB)...")

        try:
            with open(v_file, "rb") as f:
                file_bytes = f.read()

            # Upload (upsert) - Fixed: pass boolean True instead of string "true"
            client.storage.from_(bucket_name).upload(
                path=file_name,
                file=file_bytes,
                file_options={"content-type": "video/mp4", "upsert": True}
            )
            
            public_url = client.storage.from_(bucket_name).get_public_url(file_name)
            cdn_links[file_name] = public_url
            print(f"  ✓ Uploaded: {public_url}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Error uploading {file_name}: {e}")

    # Export CDN links map for Next.js frontend consumption
    if cdn_links:
        CDN_LINKS_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(CDN_LINKS_JSON, "w", encoding="utf-8") as f:
            json.dump(cdn_links, f, ensure_ascii=False, indent=2)
        print(f"[✓] Exported CDN links map to: {CDN_LINKS_JSON}")

    print("\n" + "=" * 70)
    print(f"[✓] SYNC COMPLETE: {success_count}/{len(video_files)} videos uploaded to Supabase CDN!")
    print("=" * 70)

if __name__ == "__main__":
    main()
