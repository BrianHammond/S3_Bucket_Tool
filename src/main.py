import sys
import qdarkstyle
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QSettings, Qt, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Dialog as about_ui
import boto3
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet
import os

class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings_manager = SettingsManager(self)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

        # Populate combo_region with regions
        self.combo_region.addItems([
            "us-east-1 (N. Virginia)",
            "us-east-2 (Ohio)",
            "us-west-1 (N. California)",
            "us-west-2 (Oregon)",
            "ca-central-1 (Canada Central)",
            "ca-west-1 (Calgary)",
            "sa-east-1 (São Paulo)",
            "eu-west-1 (Ireland)",
            "eu-west-2 (London)",
            "eu-west-3 (Paris)",
            "eu-central-1 (Frankfurt)",
            "eu-south-1 (Milan)",
            "eu-south-2 (Spain)",
            "eu-north-1 (Stockholm)",
            "eu-central-2 (Zurich)",
            "ap-southeast-1 (Singapore)",
            "ap-southeast-2 (Sydney)",
            "ap-southeast-3 (Jakarta)",
            "ap-southeast-4 (Melbourne)",
            "ap-southeast-5 (Malaysia)",
            "ap-northeast-1 (Tokyo)",
            "ap-northeast-2 (Seoul)",
            "ap-northeast-3 (Osaka)",
            "ap-south-1 (Mumbai)",
            "ap-south-2 (Hyderabad)",
            "ap-east-1 (Hong Kong)",
            "me-south-1 (Bahrain)",
            "me-central-1 (UAE)",
            "af-south-1 (Cape Town)",
            "il-central-1 (Tel Aviv)",
        ])

        self.settings_manager.load_settings()

        # S3 client (will be initialized on connect)
        self.s3 = None
        self.bucket_name = None

        # Menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about.triggered.connect(self.about_window)
        self.action_about_qt.triggered.connect(self.about_qt)

        # Buttons
        self.button_connect.clicked.connect(self.connect_to_aws)
        self.button_upload.clicked.connect(self.upload_to_bucket)
        self.button_download.clicked.connect(self.download_from_bucket)
        self.button_delete.clicked.connect(self.delete_from_bucket)
        self.button_query.clicked.connect(self.query_bucket)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event to accept files."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event to upload dropped files to S3."""
        # Check if S3 is connected
        if self.s3 is None:
            QMessageBox.warning(self, "Not Connected", "Please connect to AWS S3 first.")
            event.ignore()
            return

        # Get mime data
        mime_data = event.mimeData()
        
        # Check if there are URLs; if not, ignore the event
        if not mime_data.hasUrls():
            event.ignore()
            return

        # Process each URL
        uploaded_files = []
        for url in mime_data.urls():
            local_file_path = url.toLocalFile()
            
            # Skip if not a file
            if not os.path.isfile(local_file_path):
                continue
                
            s3_file_name = os.path.basename(local_file_path)
            reply = QMessageBox.question(
                self, 
                "Confirm Upload", 
                f"Do you want to upload {s3_file_name} to the bucket?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            # Upload only if user confirms
            if reply == QMessageBox.Yes:
                print(f"uploading {s3_file_name} to {self.line_bucket_name.text()}, this may take some time depending on the file size")
                self.upload_file(local_file_path, s3_file_name)
                uploaded_files.append(s3_file_name)

        # Refresh table if any files were uploaded
        if uploaded_files:
            self.query_bucket()
        
        event.acceptProposedAction()

    def connect_to_aws(self):
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
            success_message = f"Connected to {self.bucket_name} in {region}."
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
            s3_file_name = os.path.basename(file_path)
            self.upload_file(file_path, s3_file_name)
            self.query_bucket()

    def download_from_bucket(self):
        if self.s3 is None:
            QMessageBox.warning(self, "Not Connected", "Please connect to AWS S3 first.")
            return

        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "No Selection", "Please select at least one cell to download its object.")
            return

        selected_rows = sorted(set(index.row() for index in selected_indexes))
        downloaded_files = []
        for row_index in selected_rows:
            s3_file_name = self.table.item(row_index, 0).text()
            if s3_file_name in ["Bucket is empty", "Error listing bucket"]:
                continue

            local_file_path, _ = QFileDialog.getSaveFileName(self, f"Save {s3_file_name}", s3_file_name, "All Files (*)")
            if not local_file_path:
                continue

            try:
                self.download_file(s3_file_name, local_file_path)
                downloaded_files.append(local_file_path)
            except ClientError as e:
                QMessageBox.critical(self, "Download Error", f"Error downloading {s3_file_name}: {e}")
                return

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
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

    def populate_table(self, row, filename, filetype, modified, size, storage_class):
        self.table.insertRow(row)
        name_item = QTableWidgetItem(filename)
        name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row, 0, name_item)
        
        type_item = QTableWidgetItem(filetype)
        type_item.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(row, 1, type_item)
        
        modified_item = QTableWidgetItem(modified)
        modified_item.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(row, 2, modified_item)
        
        size_item = QTableWidgetItem(size)
        size_item.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(row, 3, size_item)
        
        storage_item = QTableWidgetItem(storage_class)
        storage_item.setFlags(Qt.ItemIsEnabled)
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

    def about_window(self): # loads the About window
        about_window = AboutWindow(dark_mode=self.action_dark_mode.isChecked())
        about_window.exec()

    def about_qt(self):
        QApplication.aboutQt()

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        event.accept()

class SettingsManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.key = self.settings.value('encryption_key', None)
        if self.key is None:
            self.key = Fernet.generate_key()
            self.settings.setValue('encryption_key', self.key.decode())
        self.cipher = Fernet(self.key)

    def encrypt_text(self, text):
        if not text:
            return None
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt_text(self, encrypted_text):
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
                self.main_window.line_access_key.setText("")
        if encrypted_secret_key is not None:
            secret_key = self.decrypt_text(encrypted_secret_key)
            if secret_key:
                self.main_window.line_secret_key.setText(secret_key)
            else:
                self.main_window.line_secret_key.setText("")

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

class AboutWindow(QDialog, about_ui): 
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)
        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        self.button_ok.clicked.connect(self.accept)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())