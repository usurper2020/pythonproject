class Mercurial(VersionControl):
    name = "hg"

    @classmethod
    def get_current_revision(cls, location: str) -> str:
        """
        Get the current revision hash of a Mercurial repository.

        This method retrieves the current revision identifier (hash) of a Mercurial
        repository located at the specified path.

        Args:
            cls (type): The class object (implicitly passed for class methods).
            location (str): The path to the Mercurial repository.

        Returns:
            str: The current revision hash of the repository.

        Raises:
            Potential exceptions from the underlying 'run_command' method.
        """
        current_rev_hash = cls.run_command(
            ["id", "-i"],
            show_stdout=False,
            stdout_
