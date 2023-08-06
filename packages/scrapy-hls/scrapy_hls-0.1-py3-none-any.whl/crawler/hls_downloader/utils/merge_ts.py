import os
import shutil
import subprocess


class MergeUtil:
    @classmethod
    def merge(cls, source_dir: str, target_dir: str, target_filename: str, remove_frag: bool = True):
        os.makedirs(target_dir, exist_ok=True)
        merged = open(os.path.join(target_dir, target_filename), 'w+b')

        for f in sorted(os.listdir(source_dir)):
            with open(os.path.join(source_dir, f), 'rb') as segment:
                shutil.copyfileobj(segment, merged)

        merged.close()

        if remove_frag:
            assert os.path.isdir(source_dir)
            shutil.rmtree(source_dir)

        return merged

    @classmethod
    def convert_to_mp4(cls, source_file, target_file):
        ffmpeg_binary_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'ffmpeg')
        return subprocess.run([ffmpeg_binary_path, '-i', source_file, '-codec', 'copy', target_file],
                              stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
