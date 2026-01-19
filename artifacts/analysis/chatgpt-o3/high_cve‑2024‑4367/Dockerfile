FROM node:20-alpine
WORKDIR /srv

RUN npm init -y
RUN npm install pdfjs-dist@2.16.105 serve

# 下载官方 PoC PDF（如果失效可换自己的链接）
RUN wget -q https://codeanlabs.com/files/cve-2024-4367-poc.pdf -O /srv/cve.pdf

# 写入 HTML；这里用 cat <<EOF 避免转义地狱
RUN cat <<'EOF' > /srv/index.html
<!doctype html>
<html><body>
  <script src="node_modules/pdfjs-dist/build/pdf.js"></script>
  <script>
    /* 关闭 worker，演示用；生产请用官方 worker 路径 */
    pdfjsLib.disableWorker = true;

    /* ★ 显式允许 PDF 内置 JavaScript */
    pdfjsLib.getDocument({ url: 'cve.pdf', disableJavaScript: false })
      .promise
      .then(() => console.log('PDF parsed'))
      .catch(err => console.error(err));
  </script>
</body></html>
EOF

EXPOSE 3000
CMD ["npx","serve","-l","3000","."]
