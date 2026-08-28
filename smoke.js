const fs = require("fs");
const code = fs.readFileSync(__dirname + "/dict.js", "utf8");
const test = `
  console.log("BUILTIN entries:", Object.keys(BUILTIN).length);
  console.log("sample 咖啡:", BUILTIN["咖啡"]);
  console.log("EXT 咖啡:", EXT["咖啡"]);
  function normalize(raw){let s=(raw||"").trim().replace(/\\s+/g,"");s=s.replace(/[？?。.，,.！!~～]/g,"");s=s.replace(/^(什么是|什么叫|查一下|查询|解释一下|解释|说说|告诉我|请问|我想知道)/,"");return s;}
  function parseEntry(text){let t=text||"";const bi=t.indexOf("【");if(bi>0)t=t.slice(bi);const m=t.match(/^【(.+?)】，?(.*)$/s);if(m)return {pos:m[1],def:m[2]};return {pos:"名词",def:text};}
  console.log("parse 咖啡:", JSON.stringify(parseEntry(BUILTIN["咖啡"])));
  function dailyWord(){const now=new Date();const start=new Date(now.getFullYear(),0,0);const doy=Math.floor((now-start)/86400000);const keys=Object.keys(BUILTIN);return keys[(doy*7+13)%keys.length];}
  console.log("daily word today:", dailyWord());
  console.log("FEWSHOT len:", FEWSHOT.length);
  console.log("PERSONA ok:", PERSONA.length > 100);
`;
eval(code + test);
