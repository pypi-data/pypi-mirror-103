from pathlib import Path


class BlendLogger:
    def __init__(self, write_directory, write_name):

        self.log = open(Path(write_directory, f"{write_name}.log"), "w")

    def write_to_log(self, msg):
        """Write and flush a message to a log"""
        self.log.write(f"{msg}\n")
        self.log.flush()

    def close(self):
        """Close the log via objected rather than attribute"""
        self.log.close()




