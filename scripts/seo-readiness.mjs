import { readFile } from "node:fs/promises";

const MINIMUM = Number(process.argv[2] || 5);
const PREFERRED = Number(process.argv[3] || 8);
const catalogUrl = new URL("../docs/catalog-reviewed.json", import.meta.url);
const catalog = JSON.parse(await readFile(catalogUrl, "utf8"));
const records = catalog.records || [];

function add(map, key, name) {
  if (!key) return;
  if (!map.has(key)) map.set(key, []);
  map.get(key).push(name);
}

function summarize(map) {
  return [...map.entries()]
    .map(([cluster, names]) => ({
      cluster,
      count: names.length,
      status: names.length >= PREFERRED ? "preferred" : names.length >= MINIMUM ? "ready" : "hold",
      examples: names.slice(0, 12)
    }))
    .sort((a, b) => b.count - a.count || a.cluster.localeCompare(b.cluster));
}

const errors = [];
const dimensions = {
  originGender: new Map(),
  letterGender: new Map(),
  style: new Map(),
  syllables: new Map()
};

for (const [index, record] of records.entries()) {
  for (const field of ["name", "gender", "origin", "meaning", "styles", "syllables", "reviewStatus"]) {
    if (record[field] === undefined || record[field] === null || record[field] === "") {
      errors.push(`Record ${index + 1} (${record.name || "unnamed"}) is missing ${field}`);
    }
  }
  if (record.reviewStatus !== "curated") {
    errors.push(`${record.name}: reviewStatus must be curated`);
  }
  if (!Array.isArray(record.styles)) {
    errors.push(`${record.name}: styles must be an array`);
    continue;
  }

  add(dimensions.originGender, `${record.origin} | ${record.gender}`, record.name);
  add(dimensions.letterGender, `${record.name[0].toUpperCase()} | ${record.gender}`, record.name);
  for (const style of record.styles) add(dimensions.style, style, record.name);
  add(dimensions.syllables, `${record.syllables} syllable${record.syllables === 1 ? "" : "s"}`, record.name);
}

if (records.length !== catalog.recordCount) {
  errors.push(`recordCount says ${catalog.recordCount}, but ${records.length} records were loaded`);
}
if (errors.length) {
  console.error(JSON.stringify({ ok: false, errors }, null, 2));
  process.exitCode = 1;
} else {
  const report = {
    ok: true,
    generatedFrom: "docs/catalog-reviewed.json",
    reviewedRecords: records.length,
    thresholds: { minimum: MINIMUM, preferred: PREFERRED },
    note: "Meaning clusters are intentionally omitted until reviewed records receive explicit literal-meaning taxonomy tags.",
    dimensions: Object.fromEntries(
      Object.entries(dimensions).map(([key, map]) => [key, summarize(map)])
    )
  };
  console.log(JSON.stringify(report, null, 2));
}
