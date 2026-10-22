#!/usr/bin/env python3
"""NovaVPN Bootstrap — 500 lines → 20000 lines. Then self-destructs."""
import os, sys, time, shutil, py_compile
from pathlib import Path

HERE = Path(__file__).parent.absolute()
MARK = HERE / ".nova_boot_done"
SELF = Path(__file__).absolute()
FILES = {}

# ═══════════════ DATA ═══════════════
THEMES = [
    ("dark","#0a0e1a","#0d1220","#111827","#1f2a44","#e5e7f0","#7a86a8","#00d9ff","#22d47b","#ff3b5c"),
    ("light","#f5f5f7","#eaeaf0","#ffffff","#d1d1d6","#1c1c1e","#6b7280","#0066cc","#34c759","#ff3b30"),
    ("cyber","#000000","#0a0a0a","#0f0f0f","#00ff41","#00ff41","#00aa2a","#00ff41","#00ff41","#ff0040"),
    ("nord","#2e3440","#3b4252","#434c5e","#4c566a","#eceff4","#d8dee9","#88c0d0","#a3be8c","#bf616a"),
    ("gruvbox","#282828","#3c3836","#504945","#665c54","#ebdbb2","#a89984","#83a598","#b8bb26","#fb4934"),
    ("solarized","#002b36","#073642","#586e75","#657b83","#839496","#93a1a1","#268bd2","#859900","#dc322f"),
    ("dracula","#282a36","#343746","#44475a","#6272a4","#f8f8f2","#6272a4","#bd93f9","#50fa7b","#ff5555"),
    ("monokai","#272822","#383830","#49483e","#75715e","#f8f8f2","#a6a590","#a6e22e","#66d9ef","#f92672"),
    ("tokyo","#1a1b26","#24283b","#414868","#565f89","#c0caf5","#9aa5ce","#7aa2f7","#9ece6a","#f7768e"),
    ("catppuccin","#1e1e2e","#181825","#313244","#45475a","#cdd6f4","#a6adc8","#89b4fa","#a6e3a1","#f38ba8"),
    ("onedark","#282c34","#21252b","#2c313c","#3e4451","#abb2bf","#5c6370","#61afef","#98c379","#e06c75"),
    ("material","#263238","#1e272c","#37474f","#455a64","#eceff1","#90a4ae","#82aaff","#c3e88d","#f07178"),
    ("github","#0d1117","#161b22","#21262d","#30363d","#c9d1d9","#8b949e","#58a6ff","#3fb950","#f85149"),
    ("beige","#f5f0e6","#ede8dd","#faf6ee","#d4cdb8","#3a3428","#6b6455","#a67c52","#7a9d54","#c05c3f"),
    ("synthwave","#1a0033","#220044","#2d0055","#6b00aa","#ff00ff","#cc00cc","#00ffff","#00ff88","#ff0088"),
    ("ocean","#0a1e2e","#0f2a3e","#1a3a50","#255070","#c8e0f0","#7a9ab0","#4fc3f7","#66bb6a","#ef5350"),
    ("forest","#0f1a0f","#152015","#1e2e1e","#2d4a2d","#d4e8d4","#7a9a7a","#8bc34a","#66bb6a","#e57373"),
    ("sunset","#2d1b1b","#3a2020","#4a2a2a","#6a3a3a","#ffe8e0","#c8a090","#ff8c42","#8bc34a","#e53935"),
    ("mint","#e0f7f4","#d0f0ec","#ffffff","#b0e0d8","#0a3a35","#5a7a75","#26a69a","#66bb6a","#ef5350"),
    ("crimson","#1a0505","#250808","#330a0a","#550f0f","#ffe0e0","#c08080","#ff4444","#44ff88","#ff8888"),
]
REGIONS = [
    ("US","آمریکا","America/New_York"),("DE","آلمان","Europe/Berlin"),
    ("NL","هلند","Europe/Amsterdam"),("FR","فرانسه","Europe/Paris"),
    ("GB","انگلستان","Europe/London"),("CA","کانادا","America/Toronto"),
    ("JP","ژاپن","Asia/Tokyo"),("SG","سنگاپور","Asia/Singapore"),
    ("IN","هند","Asia/Kolkata"),("TR","ترکیه","Europe/Istanbul"),
    ("AE","امارات","Asia/Dubai"),("KR","کره جنوبی","Asia/Seoul"),
    ("AU","استرالیا","Australia/Sydney"),("BR","برزیل","America/Sao_Paulo"),
    ("IT","ایتالیا","Europe/Rome"),("ES","اسپانیا","Europe/Madrid"),
    ("PL","لهستان","Europe/Warsaw"),("SE","سوئد","Europe/Stockholm"),
    ("NO","نروژ","Europe/Oslo"),("CH","سوئیس","Europe/Zurich"),
    ("AT","اتریش","Europe/Vienna"),("BE","بلژیک","Europe/Brussels"),
    ("DK","دانمارک","Europe/Copenhagen"),("FI","فنلاند","Europe/Helsinki"),
    ("IE","ایرلند","Europe/Dublin"),("PT","پرتغال","Europe/Lisbon"),
    ("CZ","چک","Europe/Prague"),("RO","رومانی","Europe/Bucharest"),
    ("HU","مجارستان","Europe/Budapest"),("GR","یونان","Europe/Athens"),
    ("UA","اوکراین","Europe/Kiev"),("RU","روسیه","Europe/Moscow"),
    ("ZA","آفریقای جنوبی","Africa/Johannesburg"),("EG","مصر","Africa/Cairo"),
    ("NG","نیجریه","Africa/Lagos"),("KE","کنیا","Africa/Nairobi"),
    ("MX","مکزیک","America/Mexico_City"),("AR","آرژانتین","America/Argentina/Buenos_Aires"),
    ("CL","شیلی","America/Santiago"),("CO","کلمبیا","America/Bogota"),
    ("ID","اندونزی","Asia/Jakarta"),("MY","مالزی","Asia/Kuala_Lumpur"),
    ("TH","تایلند","Asia/Bangkok"),("VN","ویتنام","Asia/Ho_Chi_Minh"),
    ("PH","فیلیپین","Asia/Manila"),("HK","هنگ کنگ","Asia/Hong_Kong"),
    ("TW","تایوان","Asia/Taipei"),("NZ","نیوزیلند","Pacific/Auckland"),
    ("IL","اسرائیل","Asia/Jerusalem"),("SA","عربستان","Asia/Riyadh"),
]
PROTOCOLS = [
    ("psiphon","Psiphon","auto"),("wireguard","WireGuard","manual"),
    ("vless","VLESS","uri"),("vmess","VMess","uri"),
    ("trojan","Trojan","uri"),("shadowsocks","Shadowsocks","uri"),
    ("hysteria2","Hysteria2","uri"),("tuic","TUIC","uri"),
    ("socks5","SOCKS5","manual"),("http","HTTP Proxy","manual"),
]
LANGS = {
    "fa":{"app":"NovaVPN","connect":"اتصال","disconnect":"قطع","connecting":"در حال اتصال","connected":"متصل","error":"خطا","ready":"آماده","region":"منطقه","settings":"تنظیمات","about":"درباره","logs":"گزارش","stats":"آمار","themes":"تم","language":"زبان","ok":"تایید","cancel":"لغو","save":"ذخیره","reset":"بازنشانی","update":"به‌روزرسانی"},
    "en":{"app":"NovaVPN","connect":"Connect","disconnect":"Disconnect","connecting":"Connecting","connected":"Connected","error":"Error","ready":"Ready","region":"Region","settings":"Settings","about":"About","logs":"Logs","stats":"Stats","themes":"Themes","language":"Language","ok":"OK","cancel":"Cancel","save":"Save","reset":"Reset","update":"Update"},
    "de":{"app":"NovaVPN","connect":"Verbinden","disconnect":"Trennen","connecting":"Verbinde","connected":"Verbunden","error":"Fehler","ready":"Bereit","region":"Region","settings":"Einstellungen","about":"Über","logs":"Protokoll","stats":"Statistik","themes":"Themen","language":"Sprache","ok":"OK","cancel":"Abbrechen","save":"Speichern","reset":"Zurücksetzen","update":"Aktualisieren"},
    "fr":{"app":"NovaVPN","connect":"Connecter","disconnect":"Déconnecter","connecting":"Connexion","connected":"Connecté","error":"Erreur","ready":"Prêt","region":"Région","settings":"Paramètres","about":"À propos","logs":"Journaux","stats":"Stats","themes":"Thèmes","language":"Langue","ok":"OK","cancel":"Annuler","save":"Enregistrer","reset":"Réinitialiser","update":"Mettre à jour"},
    "es":{"app":"NovaVPN","connect":"Conectar","disconnect":"Desconectar","connecting":"Conectando","connected":"Conectado","error":"Error","ready":"Listo","region":"Región","settings":"Ajustes","about":"Acerca","logs":"Registros","stats":"Estadísticas","themes":"Temas","language":"Idioma","ok":"OK","cancel":"Cancelar","save":"Guardar","reset":"Restablecer","update":"Actualizar"},
}
ENTITIES = ["server","measurement","subscription","region","session","metric","backup","plugin","rule","route","dns","theme","setting","log","user_agent","update_check","diagnostic","speed_test","health_check","kill_switch_event"]
WIDGETS = [
    ("status_card","وضعیت",["status","details","icon"]),
    ("connect_button","اتصال",["state","label"]),
    ("server_list","سرورها",["servers","selected"]),
    ("region_picker","منطقه",["regions","selected"]),
    ("stats_panel","آمار",["upload","download","uptime","latency"]),
    ("log_view","گزارش",["logs"]),
    ("settings_panel","تنظیمات",["options"]),
    ("installer_panel","نصب",["progress","status"]),
    ("ai_panel","هوش مصنوعی",["insights","confidence"]),
    ("genetic_panel","ژنتیک",["generation","best_fitness","population"]),
    ("diagnostics_panel","عیب‌یابی",["results","summary"]),
    ("speed_test_panel","تست سرعت",["download","upload","ping"]),
    ("updater_panel","به‌روزرسانی",["version","available"]),
    ("theme_picker","تم",["themes","current"]),
    ("language_picker","زبان",["langs","current"]),
    ("about_panel","درباره",["version","author","license"]),
]
PANELS = [
    ("main","اصلی"),("settings","تنظیمات"),("diagnostics","عیب‌یابی"),
    ("about","درباره"),("stats","آمار"),("ai","هوش"),("genetic","ژنتیک"),
    ("speedtest","تست سرعت"),("servers","سرورها"),("subscriptions","سابسکریپشن"),
]
TESTS = ["crypto","storage","config","subscription","evaluator","genetic","themes","regions","i18n","event_bus","process","backup","diagnostics","health","speed"]

# ═══════════════ GENERATORS ═══════════════

def gen_themes():
    L = ['"""UI themes — auto-generated."""','THEMES = {']
    for t in THEMES:
        L.append(f'    "{t[0]}": {{"bg":"{t[1]}","bg_alt":"{t[2]}","card":"{t[3]}","border":"{t[4]}","text":"{t[5]}","sub":"{t[6]}","accent":"{t[7]}","success":"{t[8]}","error":"{t[9]}"}},')
    L += ['}','','def get(name):','    return THEMES.get(name, THEMES["dark"])','','def names():','    return list(THEMES.keys())','','def apply(widget, theme_name):','    t = get(theme_name)','    widget.setStyleSheet(f"""','        QWidget {{ background: {t["bg"]}; color: {t["text"]}; }}','        QPushButton {{ background: {t["accent"]}; color: {t["bg"]}; border-radius: 10px; padding: 10px 20px; font-weight: 600; }}','        QLabel {{ color: {t["text"]}; }}','        QFrame {{ background: {t["card"]}; border: 1px solid {t["border"]}; border-radius: 12px; }}','        QTextEdit {{ background: {t["card"]}; color: {t["text"]}; border: 1px solid {t["border"]}; border-radius: 8px; padding: 8px; }}','        QComboBox {{ background: {t["card"]}; color: {t["text"]}; border: 1px solid {t["border"]}; border-radius: 8px; padding: 8px; }}','    """)','','def color(widget_name, theme, key="accent"):','    return get(theme).get(key, "#00d9ff")']
    FILES["ui/themes.py"] = "\n".join(L)

def gen_regions():
    L = ['"""Region data — auto-generated."""','REGIONS = [']
    for code,name,tz in REGIONS: L.append(f'    ("{code}", "{name}", "{tz}"),')
    L += [']','','def names():','    return [(c, n) for c, n, _ in REGIONS]','','def codes():','    return [c for c, _, _ in REGIONS]','','def tz(code):','    for c, _, t in REGIONS:','        if c == code: return t','    return "UTC"','','def label(code):','    for c, n, _ in REGIONS:','        if c == code: return n','    return code']
    FILES["core/regions.py"] = "\n".join(L)

def gen_i18n():
    L = ['"""i18n — auto-generated."""','LANGS = {']
    for lang,d in LANGS.items():
        L.append(f'    "{lang}": {{')
        for k,v in d.items(): L.append(f'        "{k}": "{v}",')
        L.append('    },')
    L += ['}','','_current = "fa"','','def set_lang(lang):','    global _current','    if lang in LANGS: _current = lang','','def get_lang():','    return _current','','def t(key, default=None):','    return LANGS.get(_current, LANGS["fa"]).get(key, default or key)','','def available():','    return list(LANGS.keys())']
    FILES["core/i18n.py"] = "\n".join(L)

def gen_protocols():
    L = ['"""Protocol registry."""','PROTOCOLS = [']
    for code,name,kind in PROTOCOLS: L.append(f'    ("{code}", "{name}", "{kind}"),')
    L += [']','','def all():','    return [(c, n) for c, n, _ in PROTOCOLS]','','def find(code):','    for c, n, k in PROTOCOLS:','        if c == code: return {"code":c, "name":n, "kind":k}','    return None','','def uri_based():','    return [c for c, _, k in PROTOCOLS if k == "uri"]','','def manual():','    return [c for c, _, k in PROTOCOLS if k == "manual"]']
    FILES["core/protocols.py"] = "\n".join(L)

def gen_logger():
    L = ['"""Logger."""','import logging, sys','from pathlib import Path','from logging.handlers import RotatingFileHandler','','LOG_DIR = Path.home() / ".novavpn" / "logs"','LOG_DIR.mkdir(parents=True, exist_ok=True)','','def get(name, level="INFO"):','    log = logging.getLogger(name)','    if log.handlers: return log','    log.setLevel(getattr(logging, level, logging.INFO))','    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")','    fh = RotatingFileHandler(LOG_DIR / "app.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")','    fh.setFormatter(fmt)','    log.addHandler(fh)','    ch = logging.StreamHandler(sys.stdout)','    ch.setFormatter(fmt)','    log.addHandler(ch)','    return log']
    FILES["core/logger.py"] = "\n".join(L)

def gen_constants():
    L = ['"""Constants."""','import platform','from pathlib import Path','','APP = "NovaVPN"','VERSION = "1.0.0"','HOME = Path.home() / ".novavpn"','CONFIGS = HOME / "configs"','KEYS = HOME / "keys"','LOGS = HOME / "logs"','DATA = HOME / "data"','BIN = HOME / "bin"','for d in (CONFIGS, KEYS, LOGS, DATA, BIN): d.mkdir(parents=True, exist_ok=True)','','IS_WIN = platform.system() == "Windows"','IS_MAC = platform.system() == "Darwin"','IS_LINUX = platform.system() == "Linux"','','SOCKS_PORT = 1080','HTTP_PORT = 8080','MTU = 1420','KEEPALIVE = 25','TIMEOUT = 60','','DEFAULT_SETTINGS = {','    "theme": "dark", "language": "fa", "auto_connect": False,','    "kill_switch": False, "system_proxy": True, "minimize_to_tray": True,','    "dns_primary": "1.1.1.1", "dns_secondary": "8.8.8.8",','    "log_level": "INFO", "region": "", "last_protocol": "psiphon",','}']
    FILES["core/constants.py"] = "\n".join(L)

def gen_event_bus():
    L = ['"""Simple pub/sub event bus."""','import threading','','class EventBus:','    def __init__(self):','        self._subs = {}','        self._lock = threading.RLock()','    def on(self, event, cb):','        with self._lock: self._subs.setdefault(event, []).append(cb)','    def off(self, event, cb):','        with self._lock:','            if event in self._subs and cb in self._subs[event]: self._subs[event].remove(cb)','    def emit(self, event, *args, **kwargs):','        with self._lock: cbs = list(self._subs.get(event, []))','        for cb in cbs:','            try: cb(*args, **kwargs)','            except Exception: pass','    def clear(self):','        with self._lock: self._subs.clear()','','bus = EventBus()']
    FILES["core/event_bus.py"] = "\n".join(L)

def gen_config():
    L = ['"""Config manager."""','import json','from pathlib import Path','from core.constants import HOME, DEFAULT_SETTINGS','','_file = HOME / "settings.json"','_data = dict(DEFAULT_SETTINGS)','','def load():','    global _data','    if _file.exists():','        try: _data.update(json.loads(_file.read_text(encoding="utf-8")))','        except Exception: pass','    return _data','','def save():','    _file.write_text(json.dumps(_data, ensure_ascii=False, indent=2), encoding="utf-8")','','def get(key, default=None):','    return _data.get(key, default if default is not None else DEFAULT_SETTINGS.get(key))','','def set(key, val):','    _data[key] = val; save()','','def all():','    return dict(_data)','','def reset():','    global _data','    _data = dict(DEFAULT_SETTINGS); save()','','load()']
    FILES["core/config.py"] = "\n".join(L)

def gen_storage():
    L = ['"""SQLite storage — auto-generated CRUD for all entities."""','import sqlite3, json, time','from pathlib import Path','from core.constants import DATA','','class Storage:','    def __init__(self, db=None):','        self.path = db or (DATA / "app.db")','        self.path.parent.mkdir(parents=True, exist_ok=True)','        self._conn = sqlite3.connect(self.path, check_same_thread=False)','        self._conn.row_factory = sqlite3.Row','        self._init()','    def _init(self):']
    for e in ENTITIES:
        L.append(f'        self._conn.execute("CREATE TABLE IF NOT EXISTS {e} (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, ts REAL)")')
    L.append('        self._conn.commit()')
    for e in ENTITIES:
        L += [f'    def save_{e}(self, data):', f'        cur = self._conn.execute("INSERT INTO {e} (data, ts) VALUES (?, ?)", (json.dumps(data, default=str), time.time()))', '        self._conn.commit()', '        return cur.lastrowid',
              f'    def get_{e}(self, id):', f'        r = self._conn.execute("SELECT * FROM {e} WHERE id=?", (id,)).fetchone()', '        return json.loads(r["data"]) if r else None',
              f'    def list_{e}(self, limit=100):', f'        rs = self._conn.execute("SELECT * FROM {e} ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()', '        return [json.loads(r["data"]) for r in rs]',
              f'    def delete_{e}(self, id):', f'        self._conn.execute("DELETE FROM {e} WHERE id=?", (id,))', '        self._conn.commit()',
              f'    def count_{e}(self):', f'        return self._conn.execute("SELECT COUNT(*) FROM {e}").fetchone()[0]']
    L += ['    def close(self):','        self._conn.close()','','_instance = None','def get():','    global _instance','    if _instance is None: _instance = Storage()','    return _instance']
    FILES["core/storage.py"] = "\n".join(L)

def gen_crypto():
    L = ['"""Crypto: WireGuard keys, base64, hashes."""','import base64, hashlib, os, secrets, uuid','','def wg_keypair():','    priv = os.urandom(32); pub_placeholder = priv','    return base64.b64encode(priv).decode(), base64.b64encode(hashlib.sha256(priv).digest()).decode()','','def uuid4():','    return str(uuid.uuid4())','','def short_id(n=8):','    return secrets.token_hex(n // 2)','','def random_password(n=16):','    return secrets.token_urlsafe(n)','','def b64_decode(s):','    s = "".join(s.split()); s += "=" * (-len(s) % 4)','    try: return base64.urlsafe_b64decode(s).decode("utf-8", "replace")','    except Exception: return None','','def b64_encode(s):','    return base64.b64encode(s.encode()).decode()','','def sha256(s):','    return hashlib.sha256(s.encode()).hexdigest()','','def mask(s, visible=4):','    if not s or len(s) <= visible * 2: return "*" * len(s)','    return s[:visible] + "*" * (len(s) - visible * 2) + s[-visible:]']
    FILES["core/crypto.py"] = "\n".join(L)

def gen_subscription():
    L = ['"""Subscription parser for VLESS/VMess/Trojan/SS/Hy2/TUIC URIs."""','import json','from urllib.parse import urlparse, parse_qs, unquote','from core.crypto import b64_decode','','def parse(uri):','    uri = uri.strip()','    if uri.startswith("vless://"): return _vless(uri)','    if uri.startswith("vmess://"): return _vmess(uri)','    if uri.startswith("trojan://"): return _trojan(uri)','    if uri.startswith("ss://"): return _ss(uri)','    if uri.startswith(("hysteria2://","hy2://")): return _hy2(uri)','    if uri.startswith("tuic://"): return _tuic(uri)','    return None','','def _vless(u):','    p = urlparse(u); q = {k:v[0] for k,v in parse_qs(p.query).items()}','    return {"protocol":"vless","host":p.hostname,"port":p.port or 443,"uuid":p.username,"security":q.get("security","none"),"sni":q.get("sni",""),"fingerprint":q.get("fp",""),"network":q.get("type","tcp"),"ws_path":q.get("path","/"),"ws_host":q.get("host",""),"flow":q.get("flow",""),"public_key":q.get("pbk",""),"short_id":q.get("sid",""),"name":unquote(p.fragment or f"vless-{p.hostname}")}','','def _vmess(u):','    d = b64_decode(u[8:])','    if not d: return None','    j = json.loads(d)','    return {"protocol":"vmess","host":j.get("add"),"port":int(j.get("port",443)),"uuid":j.get("id"),"security":"tls" if j.get("tls")=="tls" else "none","sni":j.get("sni",""),"network":j.get("net","tcp"),"ws_path":j.get("path","/"),"ws_host":j.get("host",""),"name":j.get("ps","vmess")}','','def _trojan(u):','    p = urlparse(u); q = {k:v[0] for k,v in parse_qs(p.query).items()}','    return {"protocol":"trojan","host":p.hostname,"port":p.port or 443,"password":unquote(p.username or ""),"security":"tls","sni":q.get("sni",""),"network":q.get("type","tcp"),"ws_path":q.get("path","/"),"name":unquote(p.fragment or f"trojan-{p.hostname}")}','','def _ss(u):','    rest = u[5:]','    if "#" in rest: rest, name = rest.split("#", 1); name = unquote(name)','    else: name = "ss"','    if "@" in rest:','        cred, hp = rest.rsplit("@", 1)','        dec = b64_decode(cred)','        if not dec: return None','        method, pwd = dec.split(":", 1); host, port = hp.rsplit(":", 1)','    else:','        dec = b64_decode(rest);','        if not dec: return None','        cred, hp = dec.rsplit("@", 1); method, pwd = cred.split(":", 1); host, port = hp.rsplit(":", 1)','    return {"protocol":"shadowsocks","host":host,"port":int(port),"method":method,"password":pwd,"name":name}','','def _hy2(u):','    p = urlparse(u); q = {k:v[0] for k,v in parse_qs(p.query).items()}','    return {"protocol":"hysteria2","host":p.hostname,"port":p.port or 
