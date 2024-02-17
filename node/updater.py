import subprocess
import threading
import time
import logging
logger = logging.getLogger("updater")

UPDATE_BRANCHES = ["main", "develop", "release"]

class Updater:
    def __init__(self):
        self.update_available = False

        # Get current branch
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
        self.current_branch = result.stdout.strip()
        print(f"Current branch: {self.current_branch}")

    def check_for_updates(self):
        if self.current_branch not in UPDATE_BRANCHES:
            logger.warning(f"You are not on an update branch. Skipping update check.")
            return

        # Fetch latest changes from remote repository
        subprocess.run(["git", "fetch"])

        # Get latest commit hashes for local and remote branches
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
        remote_commit = subprocess.check_output(["git", "rev-parse", f"origin/{self.current_branch}"]).strip()

        # Compare commit hashes
        if local_commit != remote_commit:
            logger.info("Updates available!")
            self.update_available = True
        else:
            logger.info("No updates available.")
            self.update_available = False
    
    def update(self):
        if self.update_available:
            try:
                subprocess.run(["git", "pull", "origin", self.current_branch])
                subprocess.run(["./scripts/install.sh"])
            except Exception as e:
                logger.exception("Exception while updating")
        else:
            logger.warning("Cannot update, no updates available")

    def start(self):
        run_thread = threading.Thread(target=self.run, daemon=True)
        run_thread.start()
    
    def run(self):
        while True:
            self.check_for_updates()
            time.sleep(3600)    # Check every hour