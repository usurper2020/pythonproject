import os
from typing import Optional, Tuple
from pip._internal.vcs import VersionControl

class Git(VersionControl):
    name = "git"

    @classmethod
    def get_current_revision(cls, location: str, rev: Optional[str] = None) -> str:
        if rev is None:
            rev = "HEAD"
        current_rev = cls.run_command(
            ["rev-parse", rev],
            show_stdout=False,
            stdout_only=True,
            cwd=location,
        )
        return current_rev.strip()

    @classmethod
    def get_subdirectory(cls, location: str) -> Optional[str]:
        """
        Return the path to Python project root, relative to the repo root.
        Return None if the project root is in the repo root.
        """
        # Find the repo root
        git_dir = cls.run_command(
            ["rev-parse", "--git-dir"],
            show_stdout=False,
            stdout_only=True,
            cwd=location,
        ).strip()
        if not os.path.isabs(git_dir):
            git_dir = os.path.join(location, git_dir)
        repo_root = os.path.abspath(os.path.join(git_dir, ".."))
        return find_path_to_project_root_from_repo_root(location, repo_root)

    @classmethod
    def get_url_rev_and_auth(cls, url: str) -> Tuple[str, Optional[str], AuthInfo]:
        """
        Prefixes stub URLs like 'user@hostname:user/repo.git' with 'ssh://'.
        That's required because although they use SSH they sometimes don't
        work with a ssh:// scheme (e.g. GitHub). But we need a scheme for
        parsing.
        """
        if "://" not in url:
            url = "ssh://" + url.replace(":", "/", 1)
        return super().get_url_rev_and_auth(url)
