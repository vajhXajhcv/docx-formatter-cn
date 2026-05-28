/**
 * Node.js wrapper for docx-formatter-cn.
 * Provides a docx-skill-like API for AI Agents.
 *
 * Usage:
 *   node skill/scripts/new_doc.js <input.md> [output.docx] [template]
 *
 * Requires Python 3.10+ and dependencies installed.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function convert(inputPath, outputPath, template = '课程论文') {
  const repoRoot = path.resolve(__dirname, '../..');
  const pythonModule = path.join(repoRoot, 'src');

  if (!fs.existsSync(inputPath)) {
    throw new Error(`Input file not found: ${inputPath}`);
  }

  const cmd = `python -m docx_formatter.cli convert "${inputPath}" -o "${outputPath}" -t "${template}"`;

  try {
    execSync(cmd, {
      cwd: repoRoot,
      env: { ...process.env, PYTHONPATH: pythonModule },
      stdio: 'inherit',
    });
    return outputPath;
  } catch (e) {
    throw new Error(`Conversion failed: ${e.message}`);
  }
}

function quickDoc(mdContent, outputPath, template = '课程论文') {
  const tmp = path.join(process.cwd(), `.tmp_${Date.now()}.md`);
  fs.writeFileSync(tmp, mdContent, 'utf-8');
  try {
    convert(tmp, outputPath, template);
  } finally {
    try { fs.unlinkSync(tmp); } catch (_) {}
  }
  return outputPath;
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log('Usage: node new_doc.js <input.md> [output.docx] [template]');
    process.exit(1);
  }
  const [input, output, tmpl] = args;
  convert(input, output || 'output.docx', tmpl || '课程论文');
}

module.exports = { convert, quickDoc };
