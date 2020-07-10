from Sakurajima.utils.downloader import ChunkDownloader
from Sakurajima.utils.merger import FFmpegMerger, ChunkRemover
import pickle

class Kurisu(object):
    def __init__(self):
        self.resume_data = None
        self.chunks_done = []

    def read_resume_data(self):
        with open("chunks\/.resume_data", "rb") as resume_data_file:
            resume_data =pickle.load(resume_data_file)
        with open("chunks\/.chunks_done", "rb") as chunks_done_file:
            chunks_done = pickle.load(chunks_done_file)
        self.chunks_done = chunks_done
        self.resume_data = resume_data

    def resume(self):
        self.read_resume_data()
        for chunk_number, segment in enumerate(self.resume_data["segments"]):
            if chunk_number in self.chunks_done:
                continue
            loaded_file_name = self.resume_data["file_name"]
            file_name = f"chunks\/{loaded_file_name}-{chunk_number}.chunk.ts"
            ChunkDownloader(
                self.resume_data["headers"],
                self.resume_data["cookies"],
                segment,
                file_name
            ).download()

    def merge(self):
        FFmpegMerger(
            self.resume_data["file_name"],
            self.resume_data["total_chunks"]
            ).merge()

    def remove_chunks(self):
        ChunkRemover(
            self.resume_data["file_name"],
            self.resume_data["total_chunks"]
        )