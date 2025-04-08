# backend/utils/fu_file.py
from typing import Optional, Tuple
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid
from .fu_base import FuBase


class FuFile(FuBase):
    """文件处理工具类"""

    def __init__(self):
        super().__init__()
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file: Any, sub_dir: str = "") -> Tuple[str, str]:
        """保存文件"""
        filename = f"{uuid.uuid4()}_{file.name}"
        if sub_dir:
            dir_path = os.path.join(self.upload_dir, sub_dir)
            os.makedirs(dir_path, exist_ok=True)
            filepath = os.path.join(sub_dir, filename)
        else:
            filepath = filename

        with default_storage.open(
            os.path.join("uploads", filepath), "wb+"
        ) as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return filepath, filename

    def delete_file(self, filepath: str) -> bool:
        """删除文件"""
        if filepath and filepath.startswith("uploads/"):
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, filepath)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return True
            except Exception as e:
                self.logger.error(f"删除文件失败: {str(e)}")
        return False

    def get_file_url(self, filepath: str) -> Optional[str]:
        """获取文件访问 URL"""
        if filepath and filepath.startswith("uploads/"):
            return settings.MEDIA_URL + filepath
        return None
