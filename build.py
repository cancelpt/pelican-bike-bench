#!/usr/bin/env python3
"""Static gallery: model families, mask only 中转站 names, unify html to index.html."""
import json, os, re, shutil
from pathlib import Path

ROOT = Path("/mnt/d/Documents/鹈鹕")
THREE = Path("/mnt/c/Users/Ryan/Documents/Codex/2026-09-09/three-js-pbr-cinematic-scene-hdri/outputs/pelican-coastal-ride/dist")
DIST = Path(__file__).parent / "dist"
MAP = Path(__file__).parent / "mapping.json"
DATE_RE = re.compile(r"^\d{4}$")
MS = re.compile(r"(\d+)\s*分\s*(\d+)\s*秒")
MEN = re.compile(r"(\d+)\s*m\s*(\d+)\s*s", re.I)
HOUR = re.compile(r"约?\s*(\d+)\s*小时")
SEC = re.compile(r"(\d+(?:\.\d+)?)\s*s\b", re.I)
OPENAI_ALIAS = {"OpenAI-2": "OpenAI（I*9提供）", "OpenAI-IE9": "OpenAI（I*9提供）"}
RELAY_ALIAS = {"刀": "c"}
FAM_ORDER = ["gpt", "claude", "gemini", "glm", "qwen", "deepseek", "kimi", "seed", "grok", "hy", "longcat", "minimax"]
AGENTS = {"traecode": "TraeCode", "codebuddy": "Codebuddy", "pi": "Pi"}
CHANNELS = {"cursor": "cursor", "antigravity": "antigravity", "ccmax": "ccmax", "gemini-cli": "gemini-cli"}
THINKING = {"极高": "极高", "默认": "默认", "高": "高", "high": "high", "xhigh": "xhigh", "cheat": "cheat", "grok-heavy": "grok-heavy"}
EXTRA = {"官key": "官key", "官定": "官定", "官订": "官订"}
TIER = {"平价", "plus", "pro"}
COMPOUND = ("gemini-cli", "grok-heavy")


def parse_run(name):
    name = name.strip()
    for rx, conv in (
        (MS, lambda m: int(m.group(1)) * 60 + int(m.group(2))),
        (MEN, lambda m: int(m.group(1)) * 60 + int(m.group(2))),
        (HOUR, lambda m: int(m.group(1)) * 3600),
        (SEC, lambda m: int(round(float(m.group(1))))),
    ):
        m = rx.search(name)
        if m:
            return conv(m), name[: m.start()].strip(" -_"), name[m.end() :].strip(" -_")
    return None, name, ""


def run_meta(rel: Path):
    parts = list(rel.parts)
    date = parts[0] if parts and DATE_RE.match(parts[0]) else ""
    search = parts[1:] if date else parts
    secs, channel, note = None, search[-1] if search else rel.name, ""
    for i in range(len(search) - 1, -1, -1):
        s, ch, n = parse_run(search[i])
        if s is not None:
            prefix = "/".join(search[:i])
            secs, channel, note = s, f"{prefix}/{ch}" if prefix else ch, n
            break
    extra = " ".join(x for x in (date, note) if x)
    return channel, secs, extra


def family_of(model: str) -> str:
    m = model.lower()
    for p in FAM_ORDER:
        if m.startswith(p):
            return p
    return re.split(r"[-_]", m)[0]


def mask_relay(tok: str) -> str:
    if tok in RELAY_ALIAS:
        tok = RELAY_ALIAS[tok]
    elif tok.startswith("刀"):
        tok = "c" + tok[len("刀") :]
    return tok[0] + "•" * 6 + tok[-1] if len(tok) > 2 else tok


def tokens(channel: str):
    bits = [p for p in re.split(r"[-/]+", channel) if p]
    out, i = [], 0
    while i < len(bits):
        two = "-".join(bits[i : i + 2]).lower() if i + 1 < len(bits) else ""
        if two in COMPOUND:
            out.append(two)
            i += 2
        else:
            out.append(bits[i])
            i += 1
    return out


def classify(channel: str):
    for k, v in OPENAI_ALIAS.items():
        if channel == k or channel.startswith(k + "-"):
            return dict(relay=v, agent="", channel="", think="", extra="", base=True)
    if channel.lower().startswith("openai"):
        return dict(relay=channel, agent="", channel="", think="", extra="", base=True)
    agent = ch = think = ""
    extras, raw_relay = [], []
    for tok in tokens(channel):
        k = tok.lower()
        if k in AGENTS:
            agent = AGENTS[k]
        elif k in CHANNELS:
            ch = CHANNELS[k]
        elif tok in THINKING or k in THINKING:
            v = THINKING.get(tok, THINKING[k])
            think = f"{think} {v}".strip() if think else v
        elif tok in EXTRA or k in EXTRA:
            extras.append(EXTRA.get(tok, EXTRA[k]))
        elif tok.isdigit() and len(tok) <= 2:
            extras.append(f"#{tok}")
        elif tok in TIER or k in TIER:
            raw_relay.append(tok)
        else:
            raw_relay.append(tok)
    relay = mask_relay("-".join(raw_relay)) if raw_relay else ""
    return dict(relay=relay, agent=agent, channel=ch, think=think, extra=" ".join(extras), base=False)


def read_note(src: Path) -> str:
    for p in src.iterdir():
        if p.is_file() and p.name.lower() == "note.txt":
            t = p.read_text(encoding="utf-8", errors="replace").strip()
            if t.startswith("Total cost:") or t == "仍然调用了无头浏览器做视觉检查":
                return ""
            return t
    return ""


def model_sort_key(name):
    key = []
    for p in re.split(r"(\d+(?:\.\d+)*)", name):
        if re.fullmatch(r"\d+(?:\.\d+)*", p):
            nums = [int(x) for x in p.split(".")]
            key.append(tuple(-x for x in nums + [0] * (4 - len(nums))))
        else:
            key.append(p.lower())
    return tuple(key)


def pick_html(htmls):
    return "index.html" if "index.html" in htmls else sorted(htmls)[0]


def unify_html(dst: Path, html_name: str):
    src = dst / html_name
    dest = dst / "index.html"
    if src.resolve() != dest.resolve():
        if dest.exists():
            dest.unlink()
        src.replace(dest)
    for p in dst.rglob("*.html"):
        if p.name != "index.html":
            p.unlink()


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    items, mapping = [], {}
    for model in sorted([p for p in ROOT.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
        for dirpath, _, filenames in os.walk(model):
            htmls = [f for f in filenames if f.lower().endswith(".html")]
            if not htmls:
                continue
            src = Path(dirpath)
            rel = src.relative_to(model)
            channel, secs, note = run_meta(rel)
            lab = classify(channel)
            blurb = read_note(src)
            if model.name == "gemini-3.8-flash" and not blurb:
                blurb = "唯一有声音的"
            items.append(
                dict(
                    model=model.name,
                    family=family_of(model.name),
                    dir=str(src.relative_to(ROOT)),
                    site=channel,
                    secs=secs,
                    note=note,
                    blurb=blurb,
                    html=pick_html(htmls),
                    **lab,
                )
            )
            mapping.setdefault(model.name, []).append(
                dict(raw=channel, s=secs, note=note, **{k: lab[k] for k in ("relay", "agent", "channel", "think", "extra")})
            )

    def sort_key(x):
        fo = FAM_ORDER.index(x["family"]) if x["family"] in FAM_ORDER else 99
        return (fo, 0 if x["model"] == "gpt-6-astra" else 1, model_sort_key(x["model"]), 0 if x["base"] else 1, x["secs"] is None, x["secs"] or 0)

    from collections import Counter
    items.sort(key=sort_key)
    for i, it in enumerate(items, 1):
        dst = DIST / f"s{i:02d}"
        shutil.copytree(ROOT / it["dir"], dst)
        unify_html(dst, it["html"])
        for p in list(dst.rglob("*")):
            if p.is_file() and p.name.lower() == "note.txt":
                p.unlink()
        it["file"] = f"./{dst.name}/index.html"
    if THREE.exists():
        shutil.copytree(THREE, DIST / "3d")
    public = [
        {k: it[k] for k in ("family", "model", "relay", "agent", "channel", "think", "extra", "secs", "note", "blurb", "base", "file")}
        for it in items
    ]
    (DIST / "index.html").write_text(TEMPLATE.replace("__DATA__", json.dumps(public, ensure_ascii=False)), encoding="utf-8")
    MAP.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
    n_models = len({it["model"] for it in items})
    n_fam = len({it["family"] for it in items})
    leftover = [p for p in DIST.rglob("*.html") if p.name != "index.html" and "3d" not in p.parts]
    cnt = Counter(it["model"] for it in items)
    astra = [it for it in items if it["model"] == "gpt-6-astra"]
    assert n_models == 30 and len(items) == 61 and not leftover, (n_models, len(items), leftover[:5])
    assert len(astra) == 19 and astra[0]["base"] and astra[1]["base"] and astra[2]["base"]
    assert not any(t in (it["extra"] or "") for it in items for t in ("plus", "pro", "平价"))
    assert any(it["model"] == "deepseek-v4pro" and "display: flex" in (it["blurb"] or "") for it in items)
    assert any(it["model"] == "gemini-3.8-flash" and it["blurb"] == "唯一有声音的" for it in items)
    claude_models = list(dict.fromkeys(it["model"] for it in items if it["family"] == "claude"))
    assert claude_models.index("claude-fable-5.1") < claude_models.index("claude-fable-5")
    assert not any("Total cost:" in (it["blurb"] or "") or (it["blurb"] or "") == "仍然调用了无头浏览器做视觉检查" for it in items)
    assert any(it["agent"] == "TraeCode" and it["think"] == "极高" and not it["relay"] for it in items)
    assert any(it["channel"] == "cursor" and it["relay"] for it in items)
    return len(items), n_models, n_fam


TEMPLATE = r"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>鹈鹕骑自行车 · 模型对比</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:1rem}
.shot{width:100%;height:340px;border:0;background:#fff}
.time{color:#9a3412;font-variant-numeric:tabular-nums}
.chip .badge{font-variant-numeric:tabular-nums}
.blurb{white-space:pre-wrap;font-size:.85rem}
.card.base{border-color:var(--bs-success)}
.ico{width:18px;height:18px;border-radius:4px;background:#fff;border:1px solid #dee2e6}
.ico-lg{width:36px;height:36px;border-radius:8px;background:#fff;border:1px solid #dee2e6}
.region{border:1px solid #dee2e6;border-radius:1rem;padding:1rem 1.1rem;background:#f8f9fa}
.model-block{border-top:1px solid #dee2e6;padding-top:1rem;margin-top:1rem}
.model-block:first-of-type{border-top:0;padding-top:0;margin-top:0}
</style></head><body class="bg-white text-dark">
<div class="container-fluid py-3">
  <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
    <div>
      <h1 class="h4 mb-1">鹈鹕骑自行车 · 模型对比</h1>
      <p class="text-secondary small mb-0">创建一个HTML，内容是SVG绘制一个鹈鹕骑自行车的2D动画，你不需要任何测试</p>
    </div>
  </div>
  <div class="d-flex flex-wrap gap-2 mb-3" id="f"></div>
  <div id="g"></div>
</div>
<script>
const D=__DATA__, CAP=3;
const SITE={gpt:"https://openai.com",claude:"https://www.anthropic.com",gemini:"https://gemini.google.com",glm:"https://z.ai/",qwen:"https://qwen.ai",deepseek:"https://www.deepseek.com",kimi:"https://www.moonshot.cn",seed:"https://www.volcengine.com",grok:"https://x.ai/",hy:"https://hunyuan.tencent.com",longcat:"https://longcat.chat",minimax:"https://minimaxi.com/"};
const LAB={gpt:"OpenAI",claude:"Anthropic",gemini:"Google",glm:"Z.ai",qwen:"Qwen",deepseek:"DeepSeek",kimi:"Moonshot",seed:"ByteDance",grok:"xAI",hy:"Tencent",longcat:"LongCat",minimax:"MiniMax"};
const ico=u=>`https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=${encodeURIComponent(u)}&size=256`;
let fam=D[0].family, model="", open=new Set();
const fams=[...new Set(D.map(x=>x.family))];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const fmt=s=>s==null?"?":`${Math.floor(s/60)}分${s%60}秒`;
const title=x=>x.relay||x.agent||x.channel||"?";
const img=(f,cls)=>SITE[f]?`<img class="${cls}" src="${ico(SITE[f])}" alt="" width="${cls==="ico-lg"?36:18}" height="${cls==="ico-lg"?36:18}">`:"";
const chip=(label,n,on,attr,f)=>`<button type="button" class="btn btn-sm chip ${on?"btn-primary":"btn-outline-secondary"} d-inline-flex align-items-center gap-2" ${attr}>${f?img(f,"ico"):""}<span class="name">${esc(label)}</span><span class="badge rounded-pill text-bg-dark">${n}次</span></button>`;
const tags=x=>[x.agent&&x.relay?["primary",x.agent]:null,x.channel?["success",x.channel]:null,x.think?["warning",x.think]:null,x.extra?["secondary",x.extra]:null].filter(Boolean)
  .map(([c,t])=>`<span class="badge text-bg-${c}">${esc(t)}</span>`).join(" ");
const card=x=>`<div class="card h-100${x.base?" base":""}">
  <div class="card-header py-2 d-flex justify-content-between align-items-start gap-2" onclick="window.open('${x.file}','_blank')" style="cursor:pointer">
    <div>
      <div><span class="fw-semibold">${esc(title(x))}</span> <span class="time font-monospace">${fmt(x.secs)}</span>${x.note?` <span class="text-secondary small">${esc(x.note)}</span>`:""}</div>
      <div class="d-flex flex-wrap gap-1 mt-1">${tags(x)}</div>
      ${x.blurb?`<div class="alert alert-warning py-1 px-2 mt-2 mb-0 blurb">${esc(x.blurb)}</div>`:""}
    </div>
    <a class="btn btn-sm btn-outline-info flex-shrink-0" href="${x.file}" target="_blank">独览</a>
  </div>
  <iframe class="shot" loading="lazy" src="${x.file}"></iframe>
</div>`;
const P3="创建新目录来实现：用 Three.js 制作一个电影级实时渲染风格的三维展示场景，内容是一只写实鹈鹕骑着自行车在海边公路上高速前进。重点突出高精度角色建模、复杂机械细节与高级实时光影效果：鹈鹕需拥有真实可信的长喙、喉囊、羽毛结构和身体比例，骑行动作自然且富有表演性；自行车需具备完整精细的机械结构，包括车架、轮组、链条传动、踏板、刹车和把手细节。材质采用高质量 PBR，羽毛、金属、橡胶、塑料和沥青路面都应体现明显而准确的材质差异。画面设置为室外 cinematic scene，使用 HDRI 天空环境、低角度太阳光、长阴影、轮廓光、地面反射和空气透视，辅以景深、Bloom、Motion Blur、SSAO、体积雾等后处理，构建具有强烈速度感、空间层次感与视觉冲击力的演示效果。";
const astra3d=()=>`<div class="card mb-3">
  <div class="card-body py-3">
    <div class="d-flex flex-wrap justify-content-between align-items-start gap-2">
      <div>
        <span class="fw-semibold">3D 鹈鹕 · 逐风海岸</span>
        <span class="time font-monospace ms-2">47分15秒</span>
        <span class="badge text-bg-secondary ms-1">$12</span>
      </div>
      <a class="btn btn-sm btn-outline-info flex-shrink-0" href="./3d/" target="_blank">打开 3D</a>
    </div>
    <div class="blurb text-secondary mt-2 mb-0">${esc(P3)}</div>
  </div>
</div>`;
function vis(ms, md){ return open.has(md)||ms.length<=CAP?ms:ms.slice(0,CAP); }
function render(){
  const inFam=D.filter(x=>x.family===fam);
  const mods=[...new Set(inFam.map(x=>x.model))];
  if(model && !mods.includes(model)) model="";
  const shown=model?mods.filter(m=>m===model):mods;
  document.getElementById("f").innerHTML=fams.map(f=>{
    const n=D.filter(x=>x.family===f).length;
    return chip(LAB[f]||f,n,f===fam,`data-f="${esc(f)}"`,f);
  }).join("");
  document.getElementById("g").innerHTML=`<section class="region">
    <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
      <div class="d-flex align-items-center gap-2">${img(fam,"ico-lg")}<h2 class="h5 mb-0">${esc(LAB[fam]||fam)}</h2><span class="badge rounded-pill text-bg-secondary">${inFam.length}次</span></div>
      <div class="d-flex flex-wrap gap-2" id="m">${chip("全部",inFam.length,!model,'data-m=""')}${mods.map(md=>{
        const n=inFam.filter(x=>x.model===md).length;
        return chip(md,n,model===md,`data-m="${esc(md)}"`);
      }).join("")}</div>
    </div>
    ${shown.map(md=>{
      const ms=inFam.filter(x=>x.model===md);
      const vs=vis(ms,md);
      const rest=ms.length-vs.length;
      return `<div class="model-block">
        <div class="d-flex align-items-center gap-2 mb-2">
          <h3 class="h6 mb-0">${esc(md)}</h3>
          <span class="badge rounded-pill text-bg-secondary">${ms.length}次</span>
          ${rest?`<button type="button" class="btn btn-sm btn-outline-secondary ms-auto" data-x="${esc(md)}">展开其余 ${rest} 次</button>`:""}
          ${open.has(md)&&ms.length>CAP?`<button type="button" class="btn btn-sm btn-outline-secondary ms-auto" data-c="${esc(md)}">收起</button>`:""}
        </div>
        ${md==="gpt-6-astra"?astra3d():""}
        <div class="grid">${vs.map(card).join("")}</div>
      </div>`;
    }).join("")}
  </section>`;
}
document.getElementById("f").onclick=e=>{const b=e.target.closest("button[data-f]");if(!b)return;fam=b.dataset.f;model="";open.clear();render();};
document.body.addEventListener("click",e=>{
  const m=e.target.closest("button[data-m]");
  if(m){model=m.dataset.m;open.clear();render();return;}
  const x=e.target.closest("button[data-x]");
  if(x){open.add(x.dataset.x);render();return;}
  const c=e.target.closest("button[data-c]");
  if(c){open.delete(c.dataset.c);render();}
});
render();
</script></body></html>
"""

if __name__ == "__main__":
    n, m, f = build()
    print(f"{n} runs / {m} models / {f} families -> {DIST}")
