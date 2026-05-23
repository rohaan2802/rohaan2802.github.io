/**
 * Static dev server with dynamic port selection.
 * Prefers 8080; frees a busy preferred port on Windows/macOS/Linux, then picks any free port.
 */
import { createServer } from "node:http";
import { readFileSync, statSync, existsSync } from "node:fs";
import { join, extname, normalize } from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import net from "node:net";

const ROOT = normalize(join(fileURLToPath(import.meta.url), "..", ".."));
const PREFERRED = [8080, 5500, 3000, 5173, 8888, 9000];
const HOST = "127.0.0.1";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".pdf": "application/pdf",
  ".xml": "application/xml",
  ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json",
};

function isPortFree(port) {
  return new Promise((resolve) => {
    const tester = net.createServer();
    tester.once("error", () => resolve(false));
    tester.once("listening", () => tester.close(() => resolve(true)));
    tester.listen(port, HOST);
  });
}

function killPort(port) {
  try {
    if (process.platform === "win32") {
      const out = execSync(`netstat -ano -p tcp | findstr :${port}`, {
        encoding: "utf8",
        stdio: ["pipe", "pipe", "ignore"],
      });
      const pids = new Set();
      for (const line of out.split(/\r?\n/)) {
        if (!line.includes("LISTENING")) continue;
        const parts = line.trim().split(/\s+/);
        const pid = parts[parts.length - 1];
        if (pid && /^\d+$/.test(pid) && pid !== "0") pids.add(pid);
      }
      for (const pid of pids) {
        try {
          execSync(`taskkill /PID ${pid} /F`, { stdio: "ignore" });
          console.log(`Freed port ${port} (stopped PID ${pid})`);
        } catch {
          /* ignore */
        }
      }
      return pids.size > 0;
    }
    if (process.platform === "darwin") {
      execSync(`lsof -ti tcp:${port} | xargs kill -9 2>/dev/null`, {
        shell: true,
        stdio: "ignore",
      });
      return true;
    }
    execSync(`fuser -k ${port}/tcp 2>/dev/null`, { shell: true, stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

async function findPort() {
  for (const port of PREFERRED) {
    if (await isPortFree(port)) return port;
    console.log(`Port ${port} is in use — attempting to free it…`);
    killPort(port);
    await new Promise((r) => setTimeout(r, 400));
    if (await isPortFree(port)) return port;
  }

  for (let port = 3000; port <= 9999; port++) {
    if (await isPortFree(port)) return port;
  }

  console.log("No free port found in range — freeing common dev ports…");
  for (const port of PREFERRED) killPort(port);
  await new Promise((r) => setTimeout(r, 500));
  for (const port of PREFERRED) {
    if (await isPortFree(port)) return port;
  }

  return new Promise((resolve, reject) => {
    const s = net.createServer();
    s.listen(0, HOST, () => {
      const port = s.address().port;
      s.close(() => resolve(port));
    });
    s.on("error", reject);
  });
}

function safePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?")[0]);
  const rel = normalize(join(ROOT, decoded === "/" ? "index.html" : decoded));
  if (!rel.startsWith(ROOT)) return null;
  return rel;
}

function serve(req, res) {
  const rel = safePath(new URL(req.url, `http://${HOST}`).pathname);
  if (!rel) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }
  let file = rel;
  try {
    if (existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
    if (!existsSync(file)) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }
    const body = readFileSync(file);
    res.writeHead(200, { "Content-Type": MIME[extname(file).toLowerCase()] || "application/octet-stream" });
    res.end(body);
  } catch (err) {
    res.writeHead(500);
    res.end(String(err.message || err));
  }
}

const port = await findPort();
const server = createServer(serve);

server.listen(port, HOST, () => {
  const url = `http://${HOST}:${port}/`;
  console.log("Starting portfolio dev server…");
  console.log(`SERVER_READY:${url}`);
  console.log(`Serving ${ROOT}`);
  console.log(`Press Ctrl+C to stop.`);
});

server.on("error", (err) => {
  console.error(err);
  process.exit(1);
});

process.on("SIGINT", () => server.close(() => process.exit(0)));
process.on("SIGTERM", () => server.close(() => process.exit(0)));
