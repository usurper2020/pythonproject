from pip._internal.vcs import VersionControl

class Mercurial(VersionControl):
    name = "hg"

    @classmethod
    def get_current_revision(cls, location: str) -> str:
        current_rev_hash = cls.run_command(
            ["id", "-i"],
            show_stdout=False,
            stdout_
