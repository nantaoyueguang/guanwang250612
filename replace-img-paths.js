// replace-img-paths.js
const fs = require('fs');
const path = require('path');

// 要处理的页面目录
const baseDir = path.join(__dirname, 'products'); // ← 修改为你的页面主目录路径
const imagesFolder = 'images'; // 你的图片目录名

function getRelativeImagePath(filePath) {
  const from = path.dirname(filePath);
  const to = path.join(__dirname, imagesFolder);
  let relative = path.relative(from, to).replace(/\\/g, '/'); // 替换 Windows 的反斜杠
  return relative;
}

function processHtmlFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf-8');
  const relativeImagePath = getRelativeImagePath(filePath);

  const replaced = content.replace(/<img\s+([^>]*?)src=["']images\//g, `<img $1src="${relativeImagePath}/`);
  if (replaced !== content) {
    fs.writeFileSync(filePath, replaced, 'utf-8');
    console.log(`✔ 已更新: ${filePath}`);
  }
}

function walk(dir) {
  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      walk(fullPath);
    } else if (file.endsWith('.html')) {
      processHtmlFile(fullPath);
    }
  });
}

walk(baseDir);
