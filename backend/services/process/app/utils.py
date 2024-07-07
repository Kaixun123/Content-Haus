from app.config import Config

config = Config()

class Utils:
    @staticmethod
    def ensure_gcs_path(file_path):
        """
        Ensure the file path is a valid Google Cloud Storage path.

        Parameters
        ----------
        file_path : str
            The file path to check and modify if necessary.

        Returns
        -------
        str
            The file path, modified to be a valid Google Cloud Storage path if it wasn't already.
        """
        if not file_path.startswith("gs://"):
            return f"gs://{config['bucket.name']}/{file_path}"
        return file_path
