"""
Thin wrapper around the GitHub REST API, using a Personal Access Token.

This client is intentionally minimal and read-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests


API_ROOT = "https://api.github.com"


@dataclass
class RepoSummary:
  id: int
  name: str
  full_name: str
  html_url: str
  private: bool
  description: Optional[str]
  topics: List[str]
  archived: bool
  pushed_at: Optional[str]
  default_branch: str


class GitHubClient:
  def __init__(self, token: str, api_root: str = API_ROOT) -> None:
    self._api_root = api_root.rstrip("/")
    self._session = requests.Session()
    self._session.headers.update(
      {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-account-presentation-optimizer",
      }
    )

  def _get(self, path: str, params: Optional[dict] = None) -> requests.Response:
    url = f"{self._api_root}/{path.lstrip('/')}"
    resp = self._session.get(url, params=params or {})
    resp.raise_for_status()
    return resp

  def list_repos_for_user(self, username: str) -> Iterable[RepoSummary]:
    page = 1
    per_page = 100
    while True:
      resp = self._get(
        f"users/{username}/repos",
        params={"per_page": per_page, "page": page, "sort": "pushed"},
      )
      data = resp.json()
      if not data:
        break
      for item in data:
        yield RepoSummary(
          id=item["id"],
          name=item["name"],
          full_name=item["full_name"],
          html_url=item["html_url"],
          private=bool(item.get("private")),
          description=item.get("description"),
          topics=item.get("topics") or [],
          archived=bool(item.get("archived")),
          pushed_at=item.get("pushed_at"),
          default_branch=item.get("default_branch") or "main",
        )
      page += 1

  def get_readme_markdown(self, repo_full_name: str) -> Optional[str]:
    """
    Fetch README as raw markdown. Returns None if not present.
    """
    try:
      resp = self._get(
        f"repos/{repo_full_name}/readme",
        params={"accept": "application/vnd.github.raw"},
      )
    except requests.HTTPError as exc:
      if exc.response is not None and exc.response.status_code == 404:
        return None
      raise
    return resp.text
