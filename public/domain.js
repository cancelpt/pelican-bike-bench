export const SITE = {
    gpt: "https://openai.com",
    claude: "https://claude.com/",
    gemini: "https://gemini.google.com",
    glm: "https://z.ai/",
    qwen: "https://qwen.ai",
    deepseek: "https://www.deepseek.com",
    kimi: "https://www.moonshot.cn",
    seed: "https://www.volcengine.com",
    grok: "https://x.ai/",
    hy: "https://hunyuan.tencent.com",
    longcat: "https://longcat.chat",
    minimax: "https://minimaxi.com/",
    mimo: "https://mimo.mi.com/",
    muse: "https://ai.meta.com",
    step: "https://www.stepfun.com",
    space: "https://openrouter.ai/stealth",
    beam: "https://reflection.ai",
    pickle: "https://opencode.ai",
    flint: "https://opencode.ai",
    nemotron: "https://build.nvidia.com",
};
export const DISPLAY = {
    "deepseek-v4flash": "deepseek-v4-flash",
    "deepseek-v4.1flash": "deepseek-v4.1-flash",
    "deepseek-v4pro": "deepseek-v4-pro",
    "claude-opus-5-5": "claude-opus-5.5",
    "claude-sonnet-5-5": "claude-sonnet-5.5",
};
export const dispModel = (m) => DISPLAY[m] ?? m;
export const FAM_LAB = {
    gpt: "OpenAI", claude: "Anthropic", gemini: "Google", glm: "Z.ai", qwen: "Qwen",
    deepseek: "DeepSeek", kimi: "Moonshot", seed: "ByteDance", grok: "xAI", hy: "Tencent",
    longcat: "LongCat", minimax: "MiniMax", mimo: "MiMo", muse: "Meta", step: "StepFun",
    space: "Stealth", beam: "Reflection AI", pickle: "Big Pickle", flint: "Flint", nemotron: "NVIDIA",
};
export const famOf = (model) => {
    const m = (model || "").toLowerCase();
    const rules = [
        ["gpt-", "gpt"], ["o1", "gpt"], ["o3", "gpt"], ["o4", "gpt"],
        ["claude", "claude"], ["gemini", "gemini"], ["glm", "glm"],
        ["deepseek", "deepseek"], ["qwen", "qwen"], ["kimi", "kimi"],
        ["seed", "seed"], ["doubao", "seed"], ["grok", "grok"],
        ["hy", "hy"], ["hunyuan", "hy"], ["longcat", "longcat"],
        ["minimax", "minimax"], ["mimo", "mimo"], ["muse", "muse"],
        ["step", "step"], ["space", "space"], ["beam", "beam"],
        ["big-pickle", "pickle"], ["pickle", "pickle"], ["flint", "flint"], ["nemotron", "nemotron"],
    ];
    for (const [pre, fam] of rules)
        if (m.startsWith(pre))
            return fam;
    return "";
};
export const DEF_BADGE = {
    gpt: "OpenAI", claude: "Anthropic", gemini: "Google", glm: "Z.ai", qwen: "Qwen",
    deepseek: "DeepSeek", kimi: "Moonshot", seed: "Volcengine", grok: "xAI", hy: "Tencent",
    longcat: "LongCat", minimax: "MiniMax", mimo: "MiMo", muse: "Meta", step: "StepFun",
    beam: "Reflection AI", pickle: "Big Pickle", flint: "Flint", nemotron: "NVIDIA",
};
export const BADGE_SITE = {
    OpenAI: "https://openai.com",
    Anthropic: "https://claude.com/",
    xAI: "https://x.ai",
    "Z.ai": "https://z.ai",
    MiMo: "https://mimo.mi.com/",
    Meta: "https://ai.meta.com",
    DeepSeek: "https://www.deepseek.com",
    Google: "https://gemini.google.com",
    Moonshot: "https://www.moonshot.cn",
    Qwen: "https://qwen.ai",
    Volcengine: "https://www.volcengine.com",
    LongCat: "https://longcat.chat",
    MiniMax: "https://minimaxi.com/",
    StepFun: "https://www.stepfun.com",
    Tencent: "https://hunyuan.tencent.com",
    "Reflection AI": "https://reflection.ai",
    "Big Pickle": "https://opencode.ai",
    Flint: "https://opencode.ai",
    NVIDIA: "https://build.nvidia.com",
};
export const TOOL_SITE = {
    "Claude Code": "https://claude.com/",
    cursor: "https://cursor.com",
    antigravity: "https://antigravity.google",
    kiro: "https://kiro.dev",
    CodeBuddy: "https://www.codebuddy.ai",
    WorkBuddy: "https://www.workbuddy.ai",
    TraeCode: "https://www.trae.com.cn",
    ZCode: "https://z.ai",
    OpenCode: "https://opencode.ai",
    "OpenCode Free": "https://opencode.ai",
    "OpenCode Go": "https://opencode.ai",
    "MiniMax Code": "https://agent.minimaxi.com",
    OpenRouter: "https://openrouter.ai",
    "SuperGrok Heavy": "https://x.ai",
};
export const AGENT_SITE = {
    "Claude Code": "https://claude.com/",
    Codex: "https://openai.com/codex/",
    "Gemini CLI": "https://geminicli.com/",
    "Grok Build": "https://x.ai/",
    Codebuddy: "https://www.codebuddy.ai",
    WorkBuddy: "https://www.workbuddy.ai",
    TraeCode: "https://www.trae.com.cn/",
    ZCode: "https://z.ai/",
    Pi: "https://pi.dev/",
    OpenCode: "https://opencode.ai",
    "OpenCode Go": "https://opencode.ai",
    "MiniMax Code": "https://agent.minimaxi.com",
    "Kimi Code": "https://www.kimi.com",
};
export const THINK_RANK = {
    关闭: 0, off: 0,
    默认: 1,
    开启: 2, 开启思考: 2,
    low: 3, medium: 4, high: 5, 高: 5,
    极高: 6, xhigh: 6,
    最高: 7, max: 7,
    ultra: 8,
};
export const OPTS = {
    agent: ["Pi", "Codex", "OpenCode", "Claude Code", "Codebuddy", "ZCode", "TraeCode", "Gemini CLI", "Grok Build", "MiniMax Code", "Kimi Code", ""],
    channel: ["官方订阅", "官方API", "OpenRouter", "CodeBuddy", "WorkBuddy", "TraeCode", "ZCode", "OpenCode Free", "OpenCode Go", "cursor", "antigravity", "gemini-cli", "SuperGrok Heavy", ""],
    badge: ["", ...new Set([...Object.keys(BADGE_SITE), ...Object.keys(AGENT_SITE), ...Object.keys(TOOL_SITE)])],
    think: ["关闭", "默认", "开启", "low", "medium", "high", "高", "极高", "最高", "max", "xhigh", "ultra", ""],
};
export function iconKey(url) {
    try {
        return new URL(url ?? "").hostname.replace(/^www\./, "").replace(/\./g, "-");
    }
    catch {
        return "";
    }
}
export const iconFor = (url, prefix = "/") => {
    const k = iconKey(url);
    return k ? `${prefix}public/icons/${k}.png` : "";
};
export const thinkCls = (x) => {
    const t = typeof x === "string" ? x : x?.think;
    const r = t == null ? undefined : THINK_RANK[t];
    if (r == null)
        throw new Error(`未登记的思考强度: ${t}`);
    return `tk${r}`;
};
export const badgeSiteOf = (name) => BADGE_SITE[name]
    || AGENT_SITE[name]
    || TOOL_SITE[name]
    || "";
export const toolIco = (channel, family, badge) => badgeSiteOf(badge) || TOOL_SITE[channel] || (family && SITE[family]) || "";
export const effBadge = (r) => r.badge || DEF_BADGE[r.family] || "";
const RELAY_ALIAS = { "刀": "c" };
export const maskSite = (s) => {
    if (!s)
        return "";
    let tok = RELAY_ALIAS[s] ?? (s.startsWith("刀") ? "c" + s.slice(1) : s);
    return tok.length === 1 ? tok + "••••••" + tok : tok[0] + "•".repeat(6) + tok[tok.length - 1];
};
const ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };
export const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ESC_MAP[c]);
export const fmt = (s) => {
    if (s == null)
        return "--";
    const m = Math.floor(s / 60), x = s % 60;
    return (m ? m + "分" : "") + x + "秒";
};
export const extraLab = (e) => e.replace("由🎸Enderiose提供", "提供人 · 🎸Enderiose");
export const parseSecs = (name) => {
    const n = (s) => Number(s);
    const rules = [
        [/约?\s*(\d+)\s*分\s*(\d+)\s*秒/, (m) => n(m[1]) * 60 + n(m[2])],
        [/约?\s*(\d+)\s*h\s*(\d+)\s*m\s*(\d+)\s*s/i, (m) => n(m[1]) * 3600 + n(m[2]) * 60 + n(m[3])],
        [/约?\s*(\d+)\s*m\s*(\d+)\s*s/i, (m) => n(m[1]) * 60 + n(m[2])],
        [/约?\s*(\d+)\s*小时/, (m) => n(m[1]) * 3600],
        [/约?\s*(\d+)\s*min\b/i, (m) => n(m[1]) * 60],
        [/约?\s*(\d+)\s*m\b/i, (m) => n(m[1]) * 60],
        [/(\d+(?:\.\d+)?)\s*s\b/i, (m) => Math.round(n(m[1]))],
    ];
    for (const [rx, f] of rules) {
        const m = name.match(rx);
        if (m)
            return f(m);
    }
    return null;
};
export const parseRunName = (name) => {
    const secs = parseSecs(name);
    if (secs == null)
        return { secs: null, before: name.trim(), after: "" };
    const DUR = /约?\s*(?:\d+\s*分\s*\d+\s*秒|\d+\s*h\s*\d+\s*m\s*\d+\s*s|\d+\s*m\s*\d+\s*s|\d+\s*小时|\d+\s*min\b|\d+\s*m\b|\d+(?:\.\d+)?\s*s\b)/i;
    const m = DUR.exec(name);
    return {
        secs,
        before: name.slice(0, m.index).replace(/[\s_-]+$/, ""),
        after: name.slice(m.index + m[0].length).replace(/^[\s_-]+/, ""),
    };
};
export const hasNoticeToken = (s) => /\{[mb]\}/i.test(String(s ?? ""));
export const mdInline = (s) => esc(s)
    .replace(/\*\*([^*\n]*\S[^*\n]*)\*\*/g, "<strong>$1</strong>")
    .replace(/(?<!\*)\*(?!\s)([^*\n]*?\S)\*(?!\*)/g, "<em>$1</em>")
    .replace(/~~([^~\n]+)~~/g, "<s>$1</s>")
    .replace(/`([^`\n]+)`/g, "<code>$1</code>");
export const fillNotice = (s, parts) => mdInline(s).replace(/\{([mb])\}/gi, (_all, k) => k.toLowerCase() === "b" ? parts.b : parts.m);
