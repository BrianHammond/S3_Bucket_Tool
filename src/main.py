import sys
import qdarkstyle
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QSettings, Qt
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Form as about_ui
import boto3
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet
import base64

class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings_manager = SettingsManager(self)

        # Populate combo_region with regions
        self.combo_region.addItems([
            "us-east-1 (N. Virginia)",
            "us-east-2 (Ohio)",
            "ap-northeast-1 (Tokyo)",
            "ap-northeast-2 (Seoul)",
            # Add more regions as needed
        ])

        self.settings_manager.load_settings()  # Load settings after combo_region is populated

        # S3 client (will be initialized on connect)
        self.s3 = None
        self.bucket_name = None

        # Menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about.triggered.connect(self.show_about)
        self.action_about_qt.triggered.connect(self.about_qt)

        # Buttons
        self.button_connect.clicked.connect(self.aws_connect)
        self.button_upload.clicked.connect(self.upload_to_bucket)
        self.button_download.clicked.connect(self.download_from_bucket)
        self.button_delete.clicked.connect(self.delete_from_bucket)
        self.button_query.clicked.connect(self.query_bucket)

    def aws_connect(self):
        access_key = self.line_access_key.text().strip()
        secret_key = self.line_secret_key.text().strip()
        self.bucket_name = self.line_bucket_name.text().strip()
        region = self.combo_region.currentText().split()[0].strip()

        if not all([access_key, secret_key, self.bucket_name, region]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields: Access Key, Secret Key, Bucket Name, and Region.")
            self.label_connection.setText("Please fill in all fields.")
            return

        try:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            self.s3.list_buckets()
            success_message = f"Connected to AWS S3 in region {region}."
            QMessageBox.information(self, "Success", success_message)
            self.label_connection.setText(success_message)
            self.initialize_table()
            self.populate_table_from_bucket()
        except ClientError as e:
            error_message = f"Failed to connect to AWS S3: {e}"
            QMessageBox.critical(self, "Connection Error", error_message)
            self.label_connection.setText(error_message)
            self.s3 = None

    def upload_to_bucket(self):
        if self.s3 is None:
            QMessageBox.warning(self, "Not Connected", "Please connect to AWS S3 first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload", "", "All Files (*)")
        if file_path:
            s3_file_name = file_path.split('/')[-1]
            self.upload_file(file_path, s3_file_name)
            self.query_bucket()

    def download_from_bucket(self):
        if self.s3 is None:
            QMessageBox.warning(self, "Not Connected", "Please connect to AWS S3 first.")
            return

        # Get all selected cells
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "No Selection", "Please select at least one cell to download its object.")
            return

        # Extract unique row indices from selected cells
        selected_rows = sorted(set(index.row() for index in selected_indexes))

        # Download each selected object
        downloaded_files = []
        for row_index in selected_rows:
            s3_file_name = self.table.item(row_index, 0).text()  # Column 0 is "Name"
            if s3_file_name in ["Bucket is empty", "Error listing bucket"]:  # Skip placeholders
                continue

            # Prompt user for save location, defaulting to the S3 file name
            local_file_path, _ = QFileDialog.getSaveFileName(self, f"Save {s3_file_name}", s3_file_name, "All Files (*)")
            if not local_file_path:  # User canceled the dialog
                continue

            try:
                self.download_file(s3_file_name, local_file_path)
                downloaded_files.append(local_file_path)
            except ClientError as e:
                QMessageBox.critical(self, "Download Error", f"Error downloading {s3_file_name}: {e}")
                return  # Stop if an error occurs

        if downloaded_files:
            QMessageBox.information(self, "Download Success", f"Downloaded {len(downloaded_files)} object(s) to: {', '.join(downloaded_files)}")

    def delete_from_bucket(self):
        if self.s3 is None:
            QMessageBox.warning(self, "Not Connected", "Please connect to AWS S3 first.")
            return

        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "No Selection", "Please select at least one cell to delete its object.")
            return

        selected_rows = sorted(set(index.row() for index in selected_indexes))
        reply = QMessageBox.question(self, "Confirm Delete",
                                    f"Are you sure you want to delete {len(selected_rows)} object(s)?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        deleted_files = []
        for row_index in selected_rows:
            s3_file_name = self.table.item(row_index, 0).text()
            if s3_file_name in ["Bucket is empty", "Error listing bucket"]:
                continue
            try:
                self.s3.delete_object(Bucket=self.bucket_name, Key=s3_file_name)
                deleted_files.append(s3_file_name)
            except ClientError as e:
                QMessageBox.critical(self, "Delete Error", f"Error deleting {s3_file_name}: {e}")
                return

        if deleted_files:
            QMessageBox.information(self, "Delete Success", f"Deleted {len(deleted_files)} object(s): {', '.join(deleted_files)}")
            self.query_bucket()

    def upload_file(self, local_file_path, s3_file_name):
        try:
            self.s3.upload_file(local_file_path, self.bucket_name, s3_file_name)
            print(f"Success: Uploaded {local_file_path} to s3://{self.bucket_name}/{s3_file_name}")
            QMessageBox.information(self, "Upload Success", f"Uploaded {s3_file_name} to S3.")
        except FileNotFoundError:
            print(f"Error: The file {local_file_path} was not found.")
            QMessageBox.warning(self, "Upload Error", f"The file {local_file_path} was not found.")
        except ClientError as e:
            print(f"Error uploading file: {e}")
            QMessageBox.critical(self, "Upload Error", f"Error uploading file: {e}")

    def download_file(self, s3_file_name, local_file_path):
        try:
            self.s3.download_file(self.bucket_name, s3_file_name, local_file_path)
        except ClientError as e:
            print(f"Error downloading file: {e}")
            QMessageBox.critical(self, "Download Error", f"Error downloading file: {e}")

    def query_bucket(self):
        self.initialize_table()
        self.populate_table_from_bucket()

    def initialize_table(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Last Modified', 'Size', 'Storage Class'])
        # Set selection behavior to select rows, but we'll restrict interaction to "Name" column
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        # Optionally, disable focus on non-Name columns to prevent clicking
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Prevent editing

    def populate_table(self, row, filename, filetype, modified, size, storage_class):
        self.table.insertRow(row)
        
        # "Name" column (selectable)
        name_item = QTableWidgetItem(filename)
        name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Selectable and enabled
        self.table.setItem(row, 0, name_item)
        
        # Other columns (non-selectable)
        type_item = QTableWidgetItem(filetype)
        type_item.setFlags(Qt.ItemIsEnabled)  # Enabled but not selectable
        self.table.setItem(row, 1, type_item)
        
        modified_item = QTableWidgetItem(modified)
        modified_item.setFlags(Qt.ItemIsEnabled)  # Enabled but not selectable
        self.table.setItem(row, 2, modified_item)
        
        size_item = QTableWidgetItem(size)
        size_item.setFlags(Qt.ItemIsEnabled)  # Enabled but not selectable
        self.table.setItem(row, 3, size_item)
        
        storage_item = QTableWidgetItem(storage_class)
        storage_item.setFlags(Qt.ItemIsEnabled)  # Enabled but not selectable
        self.table.setItem(row, 4, storage_item)
        
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def populate_table_from_bucket(self):
        if self.s3 is None:
            return
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for i, obj in enumerate(response['Contents']):
                    filename = obj['Key']
                    filetype = filename.split('.')[-1] if '.' in filename else "Unknown"
                    modified = str(obj['LastModified'])
                    size = str(obj['Size'])
                    storage_class = obj.get('StorageClass', 'STANDARD')
                    self.populate_table(i, filename, filetype, modified, size, storage_class)
            else:
                self.populate_table(0, "Bucket is empty", "-", "-", "-", "-")
        except ClientError as e:
            QMessageBox.critical(self, "List Error", f"Error listing bucket: {e}")
            self.initialize_table()
            self.populate_table(0, "Error listing bucket", "-", "-", "-", "-")

    def dark_mode(self, checked):
        if checked:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        else:
            self.setStyleSheet('')

    def show_about(self):
        self.about_window = AboutWindow(dark_mode=self.action_dark_mode.isChecked())
        self.about_window.show()

    def about_qt(self):
        QApplication.aboutQt()

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        event.accept()

class SettingsManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        # Load or generate the encryption key
        self.key = self.settings.value('encryption_key', None)
        if self.key is None:
            self.key = Fernet.generate_key()  # Generate a new key if none exists
            self.settings.setValue('encryption_key', self.key.decode())  # Store as string
        self.cipher = Fernet(self.key)

    def encrypt_text(self, text):
        """Encrypt the given text using Fernet."""
        if not text:
            return None
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt_text(self, encrypted_text):
        """Decrypt the given encrypted text using Fernet."""
        if not encrypted_text:
            return None
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def load_settings(self):
        size = self.settings.value('window_size', None)
        pos = self.settings.value('window_pos', None)
        dark = self.settings.value('dark_mode')
        aws_region = self.settings.value('aws_region')
        s3_bucket = self.settings.value('s3_bucket')
        encrypted_access_key = self.settings.value('access_key')
        encrypted_secret_key = self.settings.value('secret_key')

        if size is not None:
            self.main_window.resize(size)
        if pos is not None:
            self.main_window.move(pos)
        if dark == 'true':
            self.main_window.action_dark_mode.setChecked(True)
            self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        if aws_region is not None:
            index = self.main_window.combo_region.findText(aws_region)
            if index >= 0:
                self.main_window.combo_region.setCurrentIndex(index)
            else:
                self.main_window.combo_region.setCurrentIndex(0)
        if s3_bucket is not None:
            self.main_window.line_bucket_name.setText(s3_bucket)
        if encrypted_access_key is not None:
            access_key = self.decrypt_text(encrypted_access_key)
            if access_key:
                self.main_window.line_access_key.setText(access_key)
            else:
                self.main_window.line_access_key.setText("")  # Handle decryption failure
        if encrypted_secret_key is not None:
            secret_key = self.decrypt_text(encrypted_secret_key)
            if secret_key:
                self.main_window.line_secret_key.setText(secret_key)
            else:
                self.main_window.line_secret_key.setText("")  # Handle decryption failure

    def save_settings(self):
        self.settings.setValue('window_size', self.main_window.size())
        self.settings.setValue('window_pos', self.main_window.pos())
        self.settings.setValue('dark_mode', self.main_window.action_dark_mode.isChecked())
        self.settings.setValue('aws_region', self.main_window.combo_region.currentText())
        self.settings.setValue('s3_bucket', self.main_window.line_bucket_name.text())
        access_key = self.main_window.line_access_key.text()
        secret_key = self.main_window.line_secret_key.text()
        self.settings.setValue('access_key', self.encrypt_text(access_key))
        self.settings.setValue('secret_key', self.encrypt_text(secret_key))

class AboutWindow(QWidget, about_ui):
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)
        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())