const http = require('node:http');
const path = require('node:path');
const { readFile, stat } = require('node:fs/promises');
const { promisify } = require('node:util');
const { gzip } = require('node:zlib');

const gzipAsync = promisify(gzip);

const siteRoot = path.resolve(__dirname, '..');
const defaultPort = 4173;
const allowedRoots = new Set([
  'css',
  'index.html',
  'js',
  'llms.txt',
  'pages',
  'robots.txt',
  'sitemap.xml',
  'templates',
]);
const mimeTypes = new Map([
  ['.css', 'text/css; charset=utf-8'],
  ['.csv', 'text/csv; charset=utf-8'],
  ['.gif', 'image/gif'],
  ['.html', 'text/html; charset=utf-8'],
  ['.ico', 'image/x-icon'],
  ['.jpeg', 'image/jpeg'],
  ['.jpg', 'image/jpeg'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.md', 'text/markdown; charset=utf-8'],
  ['.png', 'image/png'],
  ['.svg', 'image/svg+xml'],
  ['.txt', 'text/plain; charset=utf-8'],
  ['.webp', 'image/webp'],
  ['.xml', 'application/xml; charset=utf-8'],
]);

function readOption(name) {
  const exactIndex = process.argv.indexOf(name);
  if (exactIndex !== -1) return process.argv[exactIndex + 1];
  return process.argv.find((argument) => argument.startsWith(`${name}=`))?.slice(name.length + 1);
}

const requestedPort = readOption('--port') || process.env.ICT_ATLAS_PORT || defaultPort;
const port = Number.parseInt(requestedPort, 10);
const productionMode = process.argv.includes('--production');

if (!Number.isInteger(port) || port < 1 || port > 65535) {
  console.error(`Port invalide : ${requestedPort}`);
  process.exitCode = 1;
  return;
}

function send(response, statusCode, body, contentType = 'text/plain; charset=utf-8', headers = {}) {
  response.writeHead(statusCode, {
    'Cache-Control': productionMode ? 'no-cache' : 'no-store',
    'Content-Type': contentType,
    'X-Content-Type-Options': 'nosniff',
    ...headers,
  });
  response.end(body);
}

const server = http.createServer(async (request, response) => {
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.setHeader('Allow', 'GET, HEAD');
    send(response, 405, 'Méthode non autorisée');
    return;
  }

  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
  } catch {
    send(response, 400, 'URL invalide');
    return;
  }

  const relativePath = pathname.replace(/^\/+/, '') || 'index.html';
  const segments = relativePath.split('/');
  if (segments.some((segment) => segment.startsWith('.')) || !allowedRoots.has(segments[0])) {
    send(response, 404, 'Page introuvable');
    return;
  }

  let filePath = path.resolve(siteRoot, relativePath);
  if (filePath !== siteRoot && !filePath.startsWith(`${siteRoot}${path.sep}`)) {
    send(response, 403, 'Accès interdit');
    return;
  }

  try {
    let fileStats = await stat(filePath);
    if (fileStats.isDirectory()) filePath = path.join(filePath, 'index.html');
    if (fileStats.isDirectory()) fileStats = await stat(filePath);

    const extension = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes.get(extension) || 'application/octet-stream';
    const etag = `W/"${fileStats.size}-${Math.trunc(fileStats.mtimeMs)}"`;
    const cacheControl = productionMode && extension !== '.html'
      ? 'public, max-age=600'
      : productionMode ? 'no-cache' : 'no-store';
    const responseHeaders = {
      'Cache-Control': cacheControl,
      ETag: etag,
    };

    if (request.headers['if-none-match'] === etag) {
      send(response, 304, undefined, contentType, responseHeaders);
      return;
    }

    let body = request.method === 'HEAD' ? undefined : await readFile(filePath);
    const compressible = /^(?:text\/|application\/(?:javascript|json|xml))/.test(contentType);
    if (productionMode && body?.length >= 1024 && compressible && /\bgzip\b/.test(request.headers['accept-encoding'] || '')) {
      body = await gzipAsync(body, { level: 6 });
      responseHeaders['Content-Encoding'] = 'gzip';
      responseHeaders.Vary = 'Accept-Encoding';
    }
    send(response, 200, body, contentType, responseHeaders);
  } catch (error) {
    send(response, error.code === 'EACCES' ? 403 : 404, error.code === 'EACCES' ? 'Accès interdit' : 'Page introuvable');
  }
});

server.on('error', (error) => {
  if (error.code === 'EADDRINUSE') {
    console.error(`Le port ${port} est déjà utilisé. Essaie : npm run dev -- --port 4174`);
  } else {
    console.error(error.message);
  }
  process.exitCode = 1;
});

server.listen(port, '127.0.0.1', () => {
  console.log(`ICT Atlas est disponible sur http://localhost:${port} (${productionMode ? 'aperçu optimisé' : 'développement'})`);
  console.log('Arrêt du serveur : Ctrl+C');
});

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
