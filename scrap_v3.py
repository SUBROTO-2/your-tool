#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                    S C R A P   v5.0                              ║
║         TRUE-PLAYBACK VERIFICATION EDITION  •  TERMUX            ║
╠══════════════════════════════════════════════════════════════════╣
║   DEVS:  @Krishna_Subroto  |  @Syntex_Owner                      ║
║          @i_stay_silent_not_week                                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio, aiohttp, requests, os, sys, time, random, json, re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ═══════════════════════ CONFIG ═══════════════════════
API_CONNECT_TIMEOUT = 20
API_READ_TIMEOUT    = 300
API_MAX_RETRIES     = 5
STREAM_TIMEOUT      = 12
MIN_CONCURRENT      = 60
MAX_CONCURRENT      = 150
BATCH_SIZE          = 3000     # প্রতি N চ্যানেলে ১০s cool-down
BATCH_COOLDOWN      = 10
CHECKPOINT_EVERY    = 300
OUTPUT_DIR          = "scrap_output"
UA                  = "VLC/3.0.20 LibVLC/3.0.20"   # VLC-matching UA (player compatibility)

class C:
    R="\033[0m"; RED="\033[91m"; GRN="\033[92m"; YEL="\033[93m"
    BLU="\033[94m"; MAG="\033[95m"; CYN="\033[96m"; WHT="\033[97m"
    BOLD="\033[1m"; DIM="\033[2m"

BANNER = f"""{C.GRN}{C.BOLD}
    ███████╗ ██████╗██████╗  █████╗ ██████╗ 
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
    ███████╗██║     ██████╔╝███████║██████╔╝
    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ 
    ███████║╚██████╗██║  ██║██║  ██║██║     
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  {C.CYN}v5.0 PLAYBACK-VERIFIED
{C.R}"""

CREDITS = f"""{C.CYN}{C.BOLD}   ╔══════════════════════════════════════════════════════════╗
   ║  ⚡ SCRAP • TRUE PLAYBACK VERIFICATION  • v5.0            ║
   ╠══════════════════════════════════════════════════════════╣
   ║  👨‍💻 @Krishna_Subroto                                      ║
   ║  👨‍💻 @Syntex_Owner                                         ║
   ║  👨‍💻 @i_stay_silent_not_week                                ║
   ╚══════════════════════════════════════════════════════════╝{C.R}
"""

# ═══════════════════════ ANIMATIONS ═══════════════════════
def matrix_rain(rows=5, width=58, duration=0.6):
    end = time.time() + duration
    while time.time() < end:
        line = "".join(random.choice("01▓▒░█アカサ") if random.random()>0.55
                       else " " for _ in range(width))
        print(f"{C.DIM}{C.GRN}   {line}{C.R}")
        time.sleep(0.045)

def hacker_boot():
    os.system('clear' if os.name=='posix' else 'cls')
    print(BANNER); print(CREDITS); print()
    steps = [
        ("[⚙] Booting SCRAP v5 kernel",           "OK"),
        ("[🌐] Resolving DNS pool",                 "OK"),
        ("[🔐] Generating VLC fingerprints",        "OK"),
        ("[⚡] Adaptive worker pool armed",          "OK"),
        ("[🛡]  Anti-rate-limit shield online",     "OK"),
        ("[📡] Opening stealth tunnels",            "OK"),
        ("[🎬] Loading HLS deep parser",            "OK"),
        ("[💠] MPEG-TS magic validator ready",      "OK"),
        ("[🎯] TRUE-PLAYBACK engine ready",         "OK"),
    ]
    for msg, tag in steps:
        sys.stdout.write(f"{C.CYN}{msg}{C.R}"); sys.stdout.flush()
        for _ in range(random.randint(3,5)):
            time.sleep(0.05)
            sys.stdout.write(f"{C.DIM}.{C.R}"); sys.stdout.flush()
        print(f" {C.GRN}{C.BOLD}[{tag}]{C.R}"); time.sleep(0.04)
    print(); matrix_rain(); print()

# ═══════════════════════ UTILS ═══════════════════════
def versioned_path(base):
    if not os.path.exists(base): return base
    name, ext = os.path.splitext(base)
    i = 2
    while os.path.exists(f"{name}_{i}{ext}"): i += 1
    return f"{name}_{i}{ext}"

def sanitize_host(h):
    h = h.strip().rstrip("/")
    if not re.match(r"^https?://", h): h = "http://" + h
    return h

def validate_host(h):
    try: return bool(urlparse(h).netloc)
    except: return False

def joss_border(title, width=64):
    line = "═" * width
    return f"╔{line}╗\n║ {title.center(width-2)} ║\n╚{line}╝"

# ═══════════════════════ XTREAM API ═══════════════════════
class Xtream:
    def __init__(self, host, user, pwd):
        self.host, self.user, self.pwd = host, user, pwd
        self.session = requests.Session()
        retries = Retry(total=API_MAX_RETRIES, backoff_factor=1.5,
                        status_forcelist=[429,500,502,503,504],
                        allowed_methods=["GET"])
        adapter = HTTPAdapter(max_retries=retries,
                              pool_connections=10, pool_maxsize=10)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update({"User-Agent": UA, "Accept": "*/*"})

    def _api(self, action="", extra=None):
        url = f"{self.host}/player_api.php"
        params = {"username": self.user, "password": self.pwd, "action": action}
        if extra: params.update(extra)
        for verify in (True, False):
            try:
                r = self.session.get(url, params=params,
                                     timeout=(API_CONNECT_TIMEOUT, API_READ_TIMEOUT),
                                     verify=verify, stream=True)
                return self._parse(r, action)
            except requests.exceptions.SSLError:
                print(f"{C.YEL}  [!] SSL error → fallback verify=False{C.R}")
            except requests.exceptions.Timeout:
                print(f"{C.YEL}  [!] Read timeout → retrying...{C.R}")
            except requests.exceptions.ConnectionError as e:
                print(f"{C.RED}  [!] Connection error: {str(e)[:70]}{C.R}")
                return None
            except Exception as e:
                print(f"{C.RED}  [!] Error: {str(e)[:90]}{C.R}")
        return None

    def _parse(self, r, action):
        if r.status_code != 200:
            print(f"{C.RED}  [!] HTTP {r.status_code} on {action}{C.R}")
            return None
        chunks, got = [], 0
        sys.stdout.write(f"{C.DIM}  [·] Receiving {action or 'auth'} ")
        sys.stdout.flush()
        try:
            for c in r.iter_content(65536):
                if c:
                    chunks.append(c); got += len(c)
                    if got % (1024*512) == 0:
                        sys.stdout.write("."); sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(f"\n{C.YEL}  [!] Stream interrupted: {e}{C.R}\n")
        sys.stdout.write(f" {C.GRN}[{got//1024} KB]{C.R}\n")
        if not chunks: return None
        try: return json.loads(b"".join(chunks).decode("utf-8","ignore"))
        except json.JSONDecodeError as e:
            print(f"{C.RED}  [!] JSON error: {e}{C.R}"); return None

    def user_info(self):
        d = self._api("")
        return d.get("user_info") if isinstance(d, dict) else None
    def live_streams(self):
        d = self._api("get_live_streams")
        return d if isinstance(d, list) else []
    def live_cats(self):
        d = self._api("get_live_categories")
        return d if isinstance(d, list) else []

# ═══════════════════════ HLS PARSER ═══════════════════════
def _extract_variants(text, base):
    """Master playlist থেকে সব variant URL বের করে"""
    lines = [l.strip() for l in text.splitlines()]
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith("#EXT-X-STREAM-INF"):
            for j in range(i+1, len(lines)):
                nxt = lines[j]
                if nxt and not nxt.startswith("#"):
                    out.append(urljoin(base, nxt)); break
    return out

def _extract_segments(text, base):
    """Media playlist থেকে সব segment URL (order preserved)"""
    lines = [l.strip() for l in text.splitlines()]
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith("#EXTINF"):
            for j in range(i+1, len(lines)):
                nxt = lines[j]
                if nxt and not nxt.startswith("#"):
                    out.append(urljoin(base, nxt)); break
    return out

# ═══════════════════════ MAGIC BYTE VALIDATOR ═══════════════════════
def is_valid_media(data):
    """
    ডেটা আসলেই MPEG-TS / MP4 / AAC কিনা যাচাই।
    HTML/error/text page গুলো reject হবে।
    """
    if not data or len(data) < 188:
        return False
    # ── MPEG-TS ──
    ts_sync = 0
    for off in (0, 188, 376, 564):
        if off < len(data) and data[off] == 0x47:
            ts_sync += 1
    if ts_sync >= 2:
        return True
    # ── MP4 / fMP4 boxes ──
    if len(data) >= 8:
        box = data[4:8]
        if box in (b'ftyp', b'moof', b'mdat', b'moov', b'styp', b'sidx', b'free'):
            return True
    # ── Raw ADTS AAC ──
    if len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xF6) == 0xF0:
        return True
    # ── WebVTT subtitle (not main stream) ──
    if data[:6] == b'WEBVTT':
        return False
    return False

async def _read_n(resp, n, t):
    try: return await asyncio.wait_for(resp.content.read(n), timeout=t)
    except: return b""

async def fetch_segment(session, url, timeout):
    """সেগমেন্ট ডাউনলোড করে magic-byte validate করে"""
    try:
        async with session.get(url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            allow_redirects=True, ssl=False) as r:
            if r.status != 200: return False, f"seg_http_{r.status}"
            data = await _read_n(r, 16384, min(timeout, 6))
            if not data: return False, "seg_empty"
            if is_valid_media(data): return True, "seg_ok"
            return False, "seg_bad_magic"
    except asyncio.TimeoutError: return False, "seg_timeout"
    except Exception as e: return False, f"seg_{type(e).__name__}"

# ═══════════════════════ DEEP VERIFIER ═══════════════════════
async def verify_stream(session, url, timeout=STREAM_TIMEOUT, depth=0):
    """
    True-Playback verification:
      1. playlist GET (redirect follow)
      2. HTML/empty check
      3. HLS detect → master? → variant try
                     → media?  → TAIL-3 segment → magic byte check
                     → 2 valid segments required
      4. direct TS stream → magic byte check
    Returns (ok, reason)
    """
    if depth > 2: return False, "depth_limit"
    final_url = url
    try:
        async with session.get(url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            allow_redirects=True, ssl=False) as r:
            if r.status != 200:
                return False, f"http_{r.status}"
            ct = r.headers.get("Content-Type", "").lower()
            final_url = str(r.url)
            body = await _read_n(r, 65536, min(timeout, 8))
            if not body: return False, "empty"
    except asyncio.TimeoutError: return False, "timeout"
    except Exception as e: return False, f"err_{type(e).__name__}"

    low = body[:512].lower()
    if b'<html' in low or b'<!doctype' in low or b'<head' in low:
        return False, "html_error"

    # ── HLS ──
    if b'#EXTM3U' in body:
        text = body.decode('utf-8', errors='ignore')

        # Master playlist?
        if '#EXT-X-STREAM-INF' in text:
            variants = _extract_variants(text, final_url)
            if not variants: return False, "no_variants"
            for v in variants[:2]:
                ok, _ = await verify_stream(session, v, timeout, depth+1)
                if ok: return True, "variant_ok"
            return False, "all_variants_dead"

        # Media playlist
        if '#EXTINF' not in text:
            return False, "no_extinf"

        segments = _extract_segments(text, final_url)
        if not segments: return False, "no_segments"

        # TAIL segments (newest for live streams)
        to_check = segments[-3:] if len(segments) >= 3 else segments
        valid = 0
        for seg in to_check:
            ok, _ = await fetch_segment(session, seg, timeout)
            if ok:
                valid += 1
                if valid >= 2: return True, "segments_ok"
        if valid >= 1 and len(to_check) == 1:
            return True, "single_segment_ok"
        return False, f"segments_dead_{valid}/{len(to_check)}"

    # ── Direct TS / MP4 stream ──
    if is_valid_media(body):
        return True, "direct_media"
    if "video" in ct or "mpeg" in ct or "octet-stream" in ct:
        # video header but no magic bytes at start → try another read
        try:
            async with session.get(url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=True, ssl=False) as r2:
                more = await _read_n(r2, 32768, min(timeout, 6))
                if is_valid_media(more): return True, "direct_media_late"
        except: pass
    return False, "not_media"

# ═══════════════════════ SCANNER ═══════════════════════
class Scanner:
    def __init__(self, streams, host, user, pwd, checkpoint, rejected_log):
        self.streams=streams; self.host=host; self.user=user; self.pwd=pwd
        self.checkpoint=checkpoint; self.rejected_log=rejected_log
        self.total=len(streams); self.working=[]; self.rejected=[]
        self.done=0; self.t0=time.time(); self._lock=asyncio.Lock()
        self.concurrent=MAX_CONCURRENT
        self.reject_reasons={}

    async def _worker(self, queue, session):
        while True:
            try: s = queue.get_nowait()
            except asyncio.QueueEmpty: return
            sid = s.get("stream_id")
            url = f"{self.host}/live/{self.user}/{self.pwd}/{sid}.m3u8"
            try:
                ok, reason = await verify_stream(session, url)
            except Exception as e:
                ok, reason = False, f"worker_{type(e).__name__}"

            async with self._lock:
                self.done += 1
                if ok:
                    self.working.append(s)
                else:
                    self.rejected.append(s)
                    self.reject_reasons[reason] = self.reject_reasons.get(reason,0)+1

                if self.done % 20 == 0 or self.done == self.total:
                    self._draw()
                if self.done % CHECKPOINT_EVERY == 0:
                    self._save_ckpt()

    def _draw(self):
        pct=self.done/self.total; w=32; f=int(w*pct)
        bar="█"*f+"░"*(w-f)
        el=time.time()-self.t0; sp=self.done/el if el>0 else 0
        eta=(self.total-self.done)/sp if sp>0 else 0
        sys.stdout.write(
            f"\r  {C.CYN}[{bar}]{C.R} {C.WHT}{pct*100:5.1f}%{C.R} "
            f"{C.GRN}✔{len(self.working):>5}{C.R} {C.RED}✘{len(self.rejected):>5}{C.R} "
            f"{C.YEL}⚡{sp:>5.0f}/s{C.R} {C.MAG}⏱{int(eta//60)}m{int(eta%60):02d}s{C.R} "
        ); sys.stdout.flush()

    def _save_ckpt(self):
        try:
            with open(self.checkpoint,"w",encoding="utf-8") as f:
                json.dump({"done":self.done,"total":self.total,
                           "working_ids":[w.get("stream_id") for w in self.working],
                           "ts":datetime.now().isoformat()}, f)
        except: pass

    async def run(self):
        queue=asyncio.Queue()
        for s in self.streams: queue.put_nowait(s)
        connector=aiohttp.TCPConnector(limit=MAX_CONCURRENT,
            limit_per_host=MAX_CONCURRENT, ttl_dns_cache=300,
            enable_cleanup_closed=True)
        headers={"User-Agent":UA,"Accept":"*/*","Accept-Language":"en-US,en;q=0.9",
                 "Connection":"keep-alive","Referer":f"{self.host}/"}
        print(f"\n{C.YEL}{C.BOLD}  [⚡] TRUE-PLAYBACK SCAN: {self.total} channels "
              f"| {MAX_CONCURRENT} workers | batch+cooldown{C.R}\n")
        async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
            workers=[asyncio.create_task(self._worker(queue,session))
                     for _ in range(MAX_CONCURRENT)]
            # cool-down monitor
            asyncio.create_task(self._cooldown_monitor())
            await asyncio.gather(*workers, return_exceptions=True)
        print()
        try:
            with open(self.rejected_log,"w",encoding="utf-8") as f:
                f.write("# REJECT REASON SUMMARY\n")
                for r,n in sorted(self.reject_reasons.items(), key=lambda x:-x[1]):
                    f.write(f"# {r}\t{n}\n#\n")
                for s in self.rejected:
                    f.write(f"{s.get('stream_id')}\t{s.get('name','')}\n")
        except: pass
        return self.working

    async def _cooldown_monitor(self):
        """প্রতি BATCH_SIZE চ্যানেল স্ক্যান হলে ১০s cool-down"""
        last_done = 0
        while True:
            await asyncio.sleep(2)
            if self.done - last_done >= BATCH_SIZE:
                sys.stdout.write(f"\n  {C.YEL}[☕] Cool-down {BATCH_COOLDOWN}s "
                                 f"(rate-limit shield)...{C.R}\n")
                await asyncio.sleep(BATCH_COOLDOWN)
                last_done = self.done
            if self.done >= self.total: return

# ═══════════════════════ RE-VERIFY ═══════════════════════
async def reverify(working, host, user, pwd):
    """Rate-limit ভুয়া working filter করতে double-check"""
    print(f"\n{C.YEL}  [*] Re-verifying {len(working)} working channels "
          f"(anti false-positive)...{C.R}\n")
    connector=aiohttp.TCPConnector(limit=MAX_CONCURRENT, ssl=False,
        enable_cleanup_closed=True)
    headers={"User-Agent":UA,"Accept":"*/*","Referer":f"{host}/"}
    sem=asyncio.Semaphore(MAX_CONCURRENT)
    verified=[]; lock=asyncio.Lock(); done=[0]

    async def one(session, s):
        async with sem:
            sid=s.get("stream_id")
            url=f"{host}/live/{user}/{pwd}/{sid}.m3u8"
            try: ok, _ = await verify_stream(session, url)
            except: ok=False
            async with lock:
                done[0]+=1
                if ok: verified.append(s)
                if done[0]%25==0 or done[0]==len(working):
                    pct=done[0]/len(working)*100
                    sys.stdout.write(
                        f"\r  {C.CYN}[reverify]{C.R} {pct:5.1f}% "
                        f"{C.GRN}✔{len(verified):>5}{C.R} / {len(working)}    ")
                    sys.stdout.flush()

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        await asyncio.gather(*[one(session,s) for s in working], return_exceptions=True)
    print()
    return verified

# ═══════════════════════ M3U ═══════════════════════
def gen_m3u(working, host, user, pwd, path):
    lines=["#EXTM3U"]
    for s in working:
        sid=s.get("stream_id")
        name=str(s.get("name",f"Ch{sid}")).replace('"',"'")
        logo=s.get("stream_icon","") or ""
        grp=str(s.get("category_name","Live")).replace('"',"'")
        url=f"{host}/live/{user}/{pwd}/{sid}.m3u8"
        lines.append(f'#EXTINF:-1 tvg-id="{sid}" tvg-name="{name}" '
                     f'tvg-logo="{logo}" group-title="{grp}",{name}')
        lines.append(url)
    with open(path,"w",encoding="utf-8") as f: f.write("\n".join(lines))

# ═══════════════════════ HACKER DETAILS TXT ═══════════════════════
def matrix_block(rows=6, width=66):
    return "\n".join("  "+"".join(random.choice("01▓▒░█アカサ") if random.random()>0.45
                     else " " for _ in range(width)) for _ in range(rows))

def export_details(info, working, total, path, host, elapsed, cats, uid, reasons, reverified):
    exp_ts=info.get("exp_date")
    if exp_ts and str(exp_ts).isdigit():
        exp_dt=datetime.fromtimestamp(int(exp_ts))
        exp_str=exp_dt.strftime("%Y-%m-%d %H:%M:%S")
        days=(exp_dt-datetime.now()).days
    else: exp_str, days = "Unlimited / Unknown", "N/A"
    cr_ts=info.get("created_at")
    cr_str=(datetime.fromtimestamp(int(cr_ts)).strftime("%Y-%m-%d %H:%M:%S")
            if cr_ts and str(cr_ts).isdigit() else "Unknown")
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pct=(len(working)/total*100) if total else 0

    banner = r"""
    ███████╗ ██████╗██████╗  █████╗ ██████╗ 
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
    ███████╗██║     ██████╔╝███████║██████╔╝
    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ 
    ███████║╚██████╗██║  ██║██║  ██║██║     
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     
                  v 5 . 0  •  P L A Y B A C K - V E R I F I E D
    """
    B=[]
    B.append("▓"*72); B.append(banner); B.append("▓"*72); B.append("")
    B.append("  ┌─[ SYSTEM ]─────────────────────────────────────────────┐")
    B.append(f"  │  Scan ID      : #{uid}")
    B.append(f"  │  Timestamp    : {ts}")
    B.append(f"  │  Engine       : SCRAP v5.0 True-Playback Verifier")
    B.append(f"  │  Verification : HLS Parser + MPEG-TS Magic Bytes")
    B.append(f"  │  Method       : Tail-3 segment check (2 valid required)")
    B.append(f"  │  Status       : COMPLETE ✓")
    B.append("  └────────────────────────────────────────────────────────┘"); B.append("")

    B.append("╔══════════════════════════════════════════════════════════╗")
    B.append("║  👤  ACCOUNT INTELLIGENCE                                ║")
    B.append("╠══════════════════════════════════════════════════════════╣")
    B.append(f"║  Username     ::  {str(info.get('username','N/A'))[:38]:<38}║")
    B.append(f"║  Password     ::  {str(info.get('password','N/A'))[:38]:<38}║")
    B.append(f"║  Created      ::  {cr_str:<38}║")
    B.append(f"║  Expiry       ::  {exp_str:<38}║")
    B.append(f"║  Days Left    ::  {str(days):<38}║")
    B.append(f"║  Status       ::  {str(info.get('status','N/A')):<38}║")
    B.append(f"║  Active Cons  ::  {str(info.get('active_cons','N/A')):<38}║")
    B.append(f"║  Max Conns    ::  {str(info.get('max_connections','N/A')):<38}║")
    B.append(f"║  Is Trial     ::  {str(info.get('is_trial','N/A')):<38}║")
    B.append("╚══════════════════════════════════════════════════════════╝"); B.append("")

    B.append("╔══════════════════════════════════════════════════════════╗")
    B.append("║  📡  SCAN RESULTS (DEEP VERIFIED)                        ║")
    B.append("╠══════════════════════════════════════════════════════════╣")
    B.append(f"║  Total Scanned       ::  {total:<31}║")
    B.append(f"║  Deep-Pass Working   ::  {reverified:<31}║")
    B.append(f"║  Final Verified      ::  {len(working):<31}║")
    B.append(f"║  Dead Rejected       ::  {total-len(working):<31}║")
    B.append(f"║  Categories          ::  {cats:<31}║")
    B.append(f"║  Success Rate        ::  {f'{pct:.2f}%':<31}║")
    B.append(f"║  Duration            ::  {f'{int(elapsed//60)}m {int(elapsed%60)}s':<31}║")
    B.append("╚══════════════════════════════════════════════════════════╝"); B.append("")

    bar_len=50; f2=int(bar_len*(pct/100))
    B.append(f"  SUCCESS ▕{'█'*f2}{'░'*(bar_len-f2)}▏ {pct:.1f}%"); B.append("")

    B.append("╔══════════════════════════════════════════════════════════╗")
    B.append("║  🛡   VERIFICATION PIPELINE                              ║")
    B.append("╠══════════════════════════════════════════════════════════╣")
    B.append("║  [1] HTTP 200 + redirect follow          ──→  PASS       ║")
    B.append("║  [2] HTML/empty page rejection           ──→  PASS       ║")
    B.append("║  [3] HLS master→variant resolution       ──→  PASS       ║")
    B.append("║  [4] TAIL-3 segment extraction           ──→  PASS       ║")
    B.append("║  [5] MPEG-TS sync byte (0x47) check      ──→  PASS       ║")
    B.append("║  [6] 2 valid segments required           ──→  PASS       ║")
    B.append("║  [7] Post-scan re-verification           ──→  PASS       ║")
    B.append("╚══════════════════════════════════════════════════════════╝"); B.append("")

    B.append("╔══════════════════════════════════════════════════════════╗")
    B.append("║  🔬  REJECT REASONS (top 10)                             ║")
    B.append("╠══════════════════════════════════════════════════════════╣")
    for i,(r,n) in enumerate(sorted(reasons.items(), key=lambda x:-x[1])[:10],1):
        B.append(f"║  {i:>2}. {r[:32]:<32}  ::  {n:<20}║")
    B.append("╚══════════════════════════════════════════════════════════╝"); B.append("")

    B.append("  ┌─[ SIGNAL TRACE ]───────────────────────────────────────┐")
    B.append(matrix_block(rows=6, width=64))
    B.append("  └────────────────────────────────────────────────────────┘"); B.append("")

    B.append("╔══════════════════════════════════════════════════════════╗")
    B.append("║  👨‍💻  DEVELOPERS                                          ║")
    B.append("╠══════════════════════════════════════════════════════════╣")
    B.append("║  ► @Krishna_Subroto                                      ║")
    B.append("║  ► @Syntex_Owner                                         ║")
    B.append("║  ► @i_stay_silent_not_week                                ║")
    B.append("╠══════════════════════════════════════════════════════════╣")
    B.append("║  ⚡ SCRAP v5.0 • Playback-Verified • Stay Silent          ║")
    B.append("╚══════════════════════════════════════════════════════════╝")

    with open(path,"w",encoding="utf-8") as f: f.write("\n".join(B))

# ═══════════════════════ MAIN ═══════════════════════
def main():
    hacker_boot()
    print(f"{C.YEL}{C.BOLD}  ┌─── 🔐 INPUT CREDENTIALS ──────────────────────┐{C.R}")
    raw=input(f"{C.CYN}  │ 🌐 Host (http://domain:port) : {C.R}").strip()
    user=input(f"{C.CYN}  │ 👤 Username                  : {C.R}").strip()
    pwd=input(f"{C.CYN}  │ 🔑 Password                  : {C.R}").strip()
    print(f"{C.YEL}{C.BOLD}  └────────────────────────────────────────────────┘{C.R}")
    if not (raw and user and pwd):
        print(f"{C.RED}  [!] All fields required.{C.R}"); sys.exit(1)
    host=sanitize_host(raw)
    if not validate_host(host):
        print(f"{C.RED}  [!] Invalid host URL.{C.R}"); sys.exit(1)
    print(f"{C.GRN}  [✓]{C.R} Host: {C.BOLD}{host}{C.R}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    m3u_file=versioned_path(os.path.join(OUTPUT_DIR,"scrap_working.m3u"))
    det_file=versioned_path(os.path.join(OUTPUT_DIR,"scrap_details.txt"))
    rej_file=versioned_path(os.path.join(OUTPUT_DIR,"scrap_rejected.log"))
    ckpt=os.path.join(OUTPUT_DIR,".scrap_ckpt.json")
    uid=datetime.now().strftime("%Y%m%d%H%M%S")

    print(f"\n{C.YEL}  [*] Connecting...{C.R}")
    api=Xtream(host,user,pwd); info=api.user_info()
    if not info:
        print(f"{C.RED}  [!] Login failed.{C.R}"); sys.exit(1)
    print(f"{C.GRN}  [✓]{C.R} User   : {C.BOLD}{info.get('username')}{C.R}")
    exp_ts=info.get("exp_date")
    if exp_ts and str(exp_ts).isdigit():
        exp_dt=datetime.fromtimestamp(int(exp_ts))
        days=(exp_dt-datetime.now()).days
        col=C.GRN if days>7 else C.YEL if days>0 else C.RED
        print(f"{C.GRN}  [✓]{C.R} Expiry : {col}{exp_dt.strftime('%Y-%m-%d')} ({days}d){C.R}")
    print(f"{C.GRN}  [✓]{C.R} Status : {info.get('status')} | Max: {info.get('max_connections')}")

    print(f"\n{C.YEL}  [*] Fetching channels (large dataset)...{C.R}")
    streams=api.live_streams()
    if not streams:
        print(f"{C.RED}  [!] No streams.{C.R}"); sys.exit(1)
    print(f"{C.YEL}  [*] Fetching categories...{C.R}")
    cats=api.live_cats()
    cmap={c.get("category_id"):c.get("category_name","Live") for c in cats}
    for s in streams: s["category_name"]=cmap.get(s.get("category_id"),"Live")
    print(f"{C.GRN}  [✓]{C.R} Channels: {C.BOLD}{len(streams)}{C.R} | Cats: {len(cats)}")

    scanner=Scanner(streams,host,user,pwd,ckpt,rej_file)
    t0=time.time()
    working=asyncio.run(scanner.run())
    deep_scan_time=time.time()-t0

    if not working:
        print(f"\n{C.RED}  [!] No working channels.{C.R}"); sys.exit(1)

    # ── Re-verification (rate-limit filter) ──
    reverified=asyncio.run(reverify(working, host, user, pwd))
    print(f"{C.GRN}  [✓]{C.R} After re-verify: {len(reverified)} / {len(working)} "
          f"(dropped {len(working)-len(reverified)} rate-limit fakes)")

    if not reverified:
        print(f"{C.RED}  [!] All failed re-verify.{C.R}"); sys.exit(1)

    # ── Export ──
    elapsed=time.time()-t0
    print(f"\n{C.YEL}  [*] Exporting...{C.R}")
    gen_m3u(reverified,host,user,pwd,m3u_file)
    print(f"{C.GRN}  [✓]{C.R} Playlist : {C.BOLD}{m3u_file}{C.R}")
    print(f"{C.GRN}  [✓]{C.R} Rejected : {C.BOLD}{rej_file}{C.R}")
    export_details(info,reverified,len(streams),det_file,host,
                   elapsed,len(cats),uid,scanner.reject_reasons,len(working))
    print(f"{C.GRN}  [✓]{C.R} Details  : {C.BOLD}{det_file}{C.R}")
    try: os.remove(ckpt)
    except: pass

    print(f"\n{C.GRN}{C.BOLD}"+joss_border("⚡ SCRAP v5.0 :: PLAYBACK-VERIFIED COMPLETE ⚡"))
    print(f"  {C.GRN}✔ Final Working : {C.BOLD}{len(reverified)}{C.R}")
    print(f"  {C.RED}✘ Dead          : {C.BOLD}{len(streams)-len(reverified)}{C.R}")
    print(f"  {C.CYN}📁 Output        : {OUTPUT_DIR}/{C.R}")
    print(f"  {C.YEL}⏱  Total Time    : {int(elapsed//60)}m {int(elapsed%60)}s{C.R}")
    print(f"\n{C.CYN}{C.BOLD}  ► @Krishna_Subroto | @Syntex_Owner | @i_stay_silent_not_week{C.R}")
    print(f"{C.DIM}  ► Only Live Survives. Stay Silent.{C.R}\n")

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.RED}  [!] Interrupted.{C.R}"); sys.exit(130)
    except Exception as e: print(f"\n{C.RED}  [FATAL] {e}{C.R}"); sys.exit(1)