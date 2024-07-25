from bot import (
    LOGGER,
    pkg_info
)
from bot.helper.ext_utils.status_utils import (
    get_readable_file_size,
    MirrorStatus,
    get_readable_time
)
from subprocess import run as frun
from time import time
from bot.helper.ext_utils.files_utils import get_path_size


class SampleVideoStatus:
    def __init__(self, listener, gid):
        self.listener = listener
        self._gid = gid
        self._size = self.listener.size
        self._start_time = time()
        self._proccessed_bytes = 0
        self.engine = f"FFmpeg v{self._eng_ver()}"

    def _eng_ver(self):
        _engine = frun(
            [
                pkg_info["pkgs"][2],
                "-version"
            ],
            capture_output=True,
            text=True
        )
        return _engine.stdout.split("\n")[0].split(" ")[2].split("-")[0]

    def gid(self):
        return self._gid

    def speed_raw(self):
        try:
            return self._proccessed_bytes / (time() - self._start_time)
        except:
            return "0"

    async def progress_raw(self):
        await self.processed_raw()
        try:
            return self._proccessed_bytes / self._size * 100
        except:
            return 0

    async def progress(self):
        return f"{round(await self.progress_raw(), 2)}%"

    def speed(self):
        try:
            return f"{get_readable_file_size(self.speed_raw())}/s" # type: ignore
        except:
            return "-"

    def name(self):
        return self.listener.name

    def size(self):
        return get_readable_file_size(self._size)

    def eta(self):
        try:
            seconds = (self._size - self._proccessed_bytes) / self.speed_raw()
            return get_readable_time(seconds)
        except:
            return "-"

    def status(self):
        return MirrorStatus.STATUS_SAMVID

    async def processed_raw(self):
        try:
            if self.listener.newDir:
                self._proccessed_bytes = await get_path_size(self.listener.newDir)
            else:
                self._proccessed_bytes = await get_path_size(self.listener.dir) - self._size
        except:
            return "-"

    def processed_bytes(self):
        try:
            return get_readable_file_size(self._proccessed_bytes)
        except:
            return "0"

    def task(self):
        return self

    async def cancel_task(self):
        LOGGER.info(f"Cancelling Sample Video: {self.listener.name}")
        self.listener.isCancelled = True
        if (
            self.listener.suproc is not None
            and self.listener.suproc.returncode is None
        ):
            self.listener.suproc.kill()
        await self.listener.onUploadError("Creating sample video stopped by user!")
