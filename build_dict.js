// 从旧 index.html 抽取《胡思辞典》核心数据，生成独立 dict.js（新搜索版引用）
const fs = require("fs");
const path = require("path");

const SRC = path.join(__dirname, "..", "index.html"); // 旧版（聊天形态）
const OUT = path.join(__dirname, "dict.js");

const html = fs.readFileSync(SRC, "utf8");

function extract(re, name){
  const m = html.match(re);
  if(!m){ throw new Error("未找到 " + name); }
  return m[0];
}

const builtin = extract(/const BUILTIN = \{[\s\S]*?\n\};/, "BUILTIN");
const ext     = extract(/const EXT = \{[\s\S]*?\n\};/, "EXT");
const persona = extract(/const PERSONA = `[\s\S]*?`;/, "PERSONA");
const fewshot = extract(/const STYLE_EXAMPLES = \[[^\]]*\];\s*\n\s*const FEWSHOT = [\s\S]*?;/, "FEWSHOT");

const out = `/* 本文件由 redesign/build_dict.js 从旧版自动抽取生成，请勿手改 */
${builtin}

${ext}

${persona}

${fewshot}
`;

fs.writeFileSync(OUT, out, "utf8");
console.log("dict.js 已生成，大小", out.length, "字节");
console.log("BUILTIN 词条数:", (builtin.match(/"[^"]+":/g) || []).length);
