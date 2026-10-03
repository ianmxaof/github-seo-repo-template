//! PowerCore GitHub Presentation — desktop shell.
//! Spawns the local FastAPI engine, then opens the same wizard UI in a native window.

use std::net::TcpListener;
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::thread;
use std::time::{Duration, Instant};

use tauri::{AppHandle, Manager, RunEvent, WebviewUrl, WebviewWindowBuilder};

const DEFAULT_PORT: u16 = 18080;
const HEALTH_TIMEOUT_SECS: u64 = 60;

struct BackendState {
  child: Mutex<Option<Child>>,
}

fn find_repo_root() -> Option<PathBuf> {
  if let Ok(p) = std::env::var("POWERCORE_GH_PRESENTATION_ROOT") {
    let pb = PathBuf::from(p);
    if looks_like_product_root(&pb) {
      return Some(pb);
    }
  }

  let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
  if let Some(parent) = manifest.parent() {
    if looks_like_product_root(parent) {
      return Some(parent.to_path_buf());
    }
  }

  if let Ok(exe) = std::env::current_exe() {
    if let Some(dir) = exe.parent() {
      if looks_like_product_root(dir) {
        return Some(dir.to_path_buf());
      }
      if let Some(parent) = dir.parent() {
        if looks_like_product_root(parent) {
          return Some(parent.to_path_buf());
        }
      }
    }
  }

  std::env::current_dir()
    .ok()
    .filter(|cwd| looks_like_product_root(cwd))
}

fn looks_like_product_root(p: &Path) -> bool {
  p.join("backend").join("main.py").is_file() && p.join("web").join("wizard.html").is_file()
}

fn pick_port() -> u16 {
  if let Ok(p) = std::env::var("GH_PRESENTATION_PORT") {
    if let Ok(n) = p.parse::<u16>() {
      return n;
    }
  }
  if port_free(DEFAULT_PORT) {
    return DEFAULT_PORT;
  }
  TcpListener::bind("127.0.0.1:0")
    .ok()
    .and_then(|l| l.local_addr().ok())
    .map(|a| a.port())
    .unwrap_or(DEFAULT_PORT)
}

fn port_free(port: u16) -> bool {
  TcpListener::bind(("127.0.0.1", port)).is_ok()
}

fn health_ok(port: u16) -> bool {
  let url = format!("http://127.0.0.1:{port}/health");
  ureq::get(&url)
    .timeout(Duration::from_secs(2))
    .call()
    .map(|r| r.status() == 200)
    .unwrap_or(false)
}

fn wait_for_health(port: u16) -> Result<(), String> {
  let deadline = Instant::now() + Duration::from_secs(HEALTH_TIMEOUT_SECS);
  while Instant::now() < deadline {
    if health_ok(port) {
      return Ok(());
    }
    thread::sleep(Duration::from_millis(350));
  }
  Err(format!(
    "Local engine on :{port} did not become ready within {HEALTH_TIMEOUT_SECS}s. Is Python 3.13 + deps installed?"
  ))
}

fn spawn_backend(root: &Path, port: u16) -> Result<Child, String> {
  let port_s = port.to_string();

  let attempts: [(&str, Vec<String>); 2] = [
    (
      "py",
      vec![
        "-3.13".into(),
        "-m".into(),
        "uvicorn".into(),
        "main:app".into(),
        "--app-dir".into(),
        "backend".into(),
        "--host".into(),
        "127.0.0.1".into(),
        "--port".into(),
        port_s.clone(),
      ],
    ),
    (
      "python",
      vec![
        "-m".into(),
        "uvicorn".into(),
        "main:app".into(),
        "--app-dir".into(),
        "backend".into(),
        "--host".into(),
        "127.0.0.1".into(),
        "--port".into(),
        port_s,
      ],
    ),
  ];

  let mut last_err = String::from("no python launcher found");
  for (bin, args) in &attempts {
    match Command::new(bin)
      .args(args)
      .current_dir(root)
      .stdin(Stdio::null())
      .stdout(Stdio::null())
      .stderr(Stdio::null())
      .spawn()
    {
      Ok(child) => return Ok(child),
      Err(e) => last_err = format!("{bin}: {e}"),
    }
  }

  Err(format!(
    "Could not start local engine ({last_err}). Run: py -3.13 -m pip install -e . -r backend/requirements.txt"
  ))
}

fn stop_backend(state: &BackendState) {
  if let Ok(mut guard) = state.child.lock() {
    if let Some(mut child) = guard.take() {
      let _ = child.kill();
      let _ = child.wait();
    }
  }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  let port = pick_port();
  let root = find_repo_root().unwrap_or_else(|| {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
      .parent()
      .map(|p| p.to_path_buf())
      .unwrap_or_else(|| PathBuf::from("."))
  });

  let owned_child = if health_ok(port) {
    None
  } else {
    match spawn_backend(&root, port) {
      Ok(c) => Some(c),
      Err(e) => {
        eprintln!("gh-presentation: {e}");
        None
      }
    }
  };

  if let Err(e) = wait_for_health(port) {
    eprintln!("gh-presentation: {e}");
  }

  let wizard_url = format!("http://127.0.0.1:{port}/ui/wizard.html");
  let backend = BackendState {
    child: Mutex::new(owned_child),
  };

  tauri::Builder::default()
    .manage(backend)
    .setup(move |app| {
      let url = wizard_url
        .parse()
        .map_err(|e| format!("bad wizard url: {e}"))?;
      WebviewWindowBuilder::new(app, "main", WebviewUrl::External(url))
        .title("GitHub Presentation — PowerCore")
        .inner_size(1200.0, 800.0)
        .min_inner_size(900.0, 600.0)
        .center()
        .build()?;
      Ok(())
    })
    .build(tauri::generate_context!())
    .expect("error while building tauri application")
    .run(|app_handle: &AppHandle, event| {
      if matches!(event, RunEvent::Exit | RunEvent::ExitRequested { .. }) {
        if let Some(state) = app_handle.try_state::<BackendState>() {
          stop_backend(&state);
        }
      }
    });
}
