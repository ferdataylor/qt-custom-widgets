import sys
import os
import logging
from datetime import datetime
from functools import partial
from typing import List, Dict, Any, Optional, Callable, Union
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QPushButton, QComboBox, QSlider, QLineEdit,
    QScrollArea, QFileDialog, QFrame, QSizePolicy, QSpacerItem,
    QGroupBox, QGridLayout, QButtonGroup, QRadioButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QObject, QThread
from PySide6.QtGui import QPixmap, QFont, QIcon

# Python 3.9 compatibility check
if sys.version_info < (3, 9):
    raise RuntimeError("This application requires Python 3.9 or higher")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# CONSTANTS
# ============================================================================

class UIConstants:
    """UI constants for consistent styling and spacing"""
    
    # Spacing constants
    SPACING_SMALL = 8
    SPACING_MEDIUM = 16
    SPACING_LARGE = 24
    SPACING_XLARGE = 32
    
    # Layout margins
    MARGIN_SMALL = 8
    MARGIN_MEDIUM = 16
    MARGIN_LARGE = 24
    
    # Widget dimensions
    BUTTON_HEIGHT = 40
    BUTTON_RADIUS = 20
    INPUT_HEIGHT = 48
    SLIDER_HANDLE_SIZE = 20
    ICON_BUTTON_SIZE = 48
    
    # Gallery settings
    GALLERY_COLUMNS = 4
    GALLERY_ITEM_SIZE = 120
    
    # Window dimensions
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    HEADER_HEIGHT = 200
    FOOTER_HEIGHT = 120
    MIN_TAB_HEIGHT = 500


# ============================================================================
# MATERIAL DESIGN STYLING SYSTEM
# ============================================================================

class MaterialDesignStyles:
    """Material Design styling system for PySide6"""
    
    # Material Design Color Palette
    COLORS = {
        # Primary Colors
        'primary': '#1976D2',           # Blue 700
        'primary_light': '#42A5F5',     # Blue 400
        'primary_dark': '#1565C0',      # Blue 800
        'primary_variant': '#0D47A1',   # Blue 900
        
        # Secondary Colors
        'secondary': '#26A69A',         # Teal 400
        'secondary_light': '#4DB6AC',   # Teal 300
        'secondary_dark': '#00695C',    # Teal 800
        
        # Surface Colors
        'background': '#FAFAFA',        # Grey 50
        'surface': '#FFFFFF',           # White
        'surface_variant': '#F5F5F5',   # Grey 100
        'surface_container': '#EEEEEE', # Grey 200
        
        # Text Colors
        'on_primary': '#FFFFFF',
        'on_secondary': '#FFFFFF',
        'on_surface': '#212121',        # Grey 900
        'on_surface_variant': '#757575', # Grey 600
        'on_background': '#212121',
        
        # State Colors
        'error': '#F44336',             # Red 500
        'warning': '#FF9800',           # Orange 500
        'success': '#4CAF50',           # Green 500
        'info': '#2196F3',              # Blue 500
        
        # Outline and Divider
        'outline': '#E0E0E0',           # Grey 300
        'outline_variant': '#BDBDBD',   # Grey 400
        'divider': '#E0E0E0',
        
        # Hover and Focus States
        'hover_overlay': 'rgba(0, 0, 0, 0.04)',
        'focus_overlay': 'rgba(25, 118, 210, 0.12)',
        'pressed_overlay': 'rgba(0, 0, 0, 0.12)',
    }
    
    # Typography Scale
    TYPOGRAPHY = {
        'headline_large': 'font-size: 32px; font-weight: 400; line-height: 40px;',
        'headline_medium': 'font-size: 28px; font-weight: 400; line-height: 36px;',
        'headline_small': 'font-size: 24px; font-weight: 400; line-height: 32px;',
        'title_large': 'font-size: 22px; font-weight: 400; line-height: 28px;',
        'title_medium': 'font-size: 16px; font-weight: 500; line-height: 24px;',
        'title_small': 'font-size: 14px; font-weight: 500; line-height: 20px;',
        'body_large': 'font-size: 16px; font-weight: 400; line-height: 24px;',
        'body_medium': 'font-size: 14px; font-weight: 400; line-height: 20px;',
        'body_small': 'font-size: 12px; font-weight: 400; line-height: 16px;',
        'label_large': 'font-size: 14px; font-weight: 500; line-height: 20px;',
        'label_medium': 'font-size: 12px; font-weight: 500; line-height: 16px;',
        'label_small': 'font-size: 11px; font-weight: 500; line-height: 16px;',
    }
    
    # Elevation Shadows
    ELEVATION = {
        'level_0': 'border: none;',
        'level_1': '''
            border: 1px solid rgba(0, 0, 0, 0.12);
            background: rgba(0, 0, 0, 0.02);
        ''',
        'level_2': '''
            border: 1px solid rgba(0, 0, 0, 0.12);
            background: rgba(0, 0, 0, 0.04);
        ''',
        'level_3': '''
            border: 1px solid rgba(0, 0, 0, 0.12);
            background: rgba(0, 0, 0, 0.06);
        ''',
        'level_4': '''
            border: 1px solid rgba(0, 0, 0, 0.12);
            background: rgba(0, 0, 0, 0.08);
        ''',
    }
    
    @classmethod
    def get_base_styles(cls) -> str:
        """Get base application styles"""
        return f"""
        /* Main Application */
        QMainWindow {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['on_background']};
            {cls.TYPOGRAPHY['body_medium']}
        }}
        
        QWidget {{
            background-color: transparent;
            color: {cls.COLORS['on_surface']};
            {cls.TYPOGRAPHY['body_medium']}
        }}
        """
    
    @classmethod
    def get_button_styles(cls) -> str:
        """Get button styling"""
        return f"""
        /* Buttons */
        QPushButton {{
            background-color: {cls.COLORS['primary']};
            color: {cls.COLORS['on_primary']};
            border: none;
            border-radius: {UIConstants.BUTTON_RADIUS}px;
            padding: {UIConstants.SPACING_SMALL}px {UIConstants.SPACING_LARGE}px;
            {cls.TYPOGRAPHY['label_large']}
            min-height: {UIConstants.BUTTON_HEIGHT - 16}px;
        }}
        
        QPushButton:hover {{
            background-color: {cls.COLORS['primary_light']};
        }}
        
        QPushButton:pressed {{
            background-color: {cls.COLORS['primary_dark']};
        }}
        
        QPushButton:disabled {{
            background-color: {cls.COLORS['outline']};
            color: {cls.COLORS['on_surface_variant']};
        }}
        
        /* Secondary Buttons */
        QPushButton[class="secondary"] {{
            background-color: {cls.COLORS['secondary']};
            color: {cls.COLORS['on_secondary']};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background-color: {cls.COLORS['secondary_light']};
        }}
        
        /* Outlined Buttons */
        QPushButton[class="outlined"] {{
            background-color: transparent;
            color: {cls.COLORS['primary']};
            border: 1px solid {cls.COLORS['outline']};
        }}
        
        QPushButton[class="outlined"]:hover {{
            background-color: {cls.COLORS['focus_overlay']};
            border-color: {cls.COLORS['primary']};
        }}
        
        /* Text Buttons */
        QPushButton[class="text"] {{
            background-color: transparent;
            color: {cls.COLORS['primary']};
            border: none;
            padding: {UIConstants.SPACING_SMALL}px {UIConstants.SPACING_MEDIUM - 4}px;
        }}
        
        QPushButton[class="text"]:hover {{
            background-color: {cls.COLORS['focus_overlay']};
        }}
        
        /* Icon Buttons */
        QPushButton[class="icon"] {{
            background-color: transparent;
            color: {cls.COLORS['on_surface_variant']};
            border: none;
            border-radius: {UIConstants.ICON_BUTTON_SIZE // 2}px;
            padding: {UIConstants.SPACING_SMALL}px;
            min-width: {UIConstants.ICON_BUTTON_SIZE}px;
            max-width: {UIConstants.ICON_BUTTON_SIZE}px;
            min-height: {UIConstants.ICON_BUTTON_SIZE}px;
            max-height: {UIConstants.ICON_BUTTON_SIZE}px;
        }}
        
        QPushButton[class="icon"]:hover {{
            background-color: {cls.COLORS['hover_overlay']};
        }}
        """
    
    @classmethod
    def get_label_styles(cls) -> str:
        """Get label styling"""
        return f"""
        /* Labels */
        QLabel {{
            color: {cls.COLORS['on_surface']};
            {cls.TYPOGRAPHY['body_medium']}
            background: transparent;
        }}
        
        QLabel[class="headline"] {{
            {cls.TYPOGRAPHY['headline_medium']}
            color: {cls.COLORS['on_surface']};
        }}
        
        QLabel[class="title"] {{
            {cls.TYPOGRAPHY['title_medium']}
            color: {cls.COLORS['on_surface']};
        }}
        
        QLabel[class="subtitle"] {{
            {cls.TYPOGRAPHY['body_large']}
            color: {cls.COLORS['on_surface_variant']};
        }}
        
        QLabel[class="caption"] {{
            {cls.TYPOGRAPHY['body_small']}
            color: {cls.COLORS['on_surface_variant']};
        }}
        """
    
    @classmethod
    def get_input_styles(cls) -> str:
        """Get input field styling"""
        return f"""
        /* Input Fields */
        QLineEdit {{
            background-color: {cls.COLORS['surface_variant']};
            color: {cls.COLORS['on_surface']};
            border: none;
            border-bottom: 1px solid {cls.COLORS['outline']};
            border-radius: 4px 4px 0px 0px;
            padding: {UIConstants.SPACING_MEDIUM}px {UIConstants.SPACING_MEDIUM - 4}px {UIConstants.SPACING_SMALL}px {UIConstants.SPACING_MEDIUM - 4}px;
            {cls.TYPOGRAPHY['body_large']}
        }}
        
        QLineEdit:focus {{
            border-bottom: 2px solid {cls.COLORS['primary']};
            background-color: {cls.COLORS['surface']};
        }}
        
        QLineEdit:disabled {{
            background-color: {cls.COLORS['surface_container']};
            color: {cls.COLORS['on_surface_variant']};
        }}
        """
    
    @classmethod
    def get_combobox_styles(cls) -> str:
        """Get combobox styling"""
        return f"""
        /* Combo Boxes */
        QComboBox {{
            background-color: {cls.COLORS['surface_variant']};
            color: {cls.COLORS['on_surface']};
            border: none;
            border-bottom: 1px solid {cls.COLORS['outline']};
            border-radius: 4px 4px 0px 0px;
            padding: {UIConstants.SPACING_MEDIUM - 4}px;
            {cls.TYPOGRAPHY['body_large']}
            min-height: {UIConstants.SPACING_LARGE}px;
        }}
        
        QComboBox:focus {{
            border-bottom: 2px solid {cls.COLORS['primary']};
            background-color: {cls.COLORS['surface']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: {UIConstants.SPACING_LARGE + 4}px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {cls.COLORS['on_surface_variant']};
            width: 0px;
            height: 0px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['on_surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 4px;
            {cls.ELEVATION['level_2']}
        }}
        """
    
    @classmethod
    def get_slider_styles(cls) -> str:
        """Get slider styling"""
        return f"""
        /* Sliders */
        QSlider::groove:horizontal {{
            background: {cls.COLORS['outline']};
            height: 4px;
            border-radius: 2px;
        }}
        
        QSlider::handle:horizontal {{
            background: {cls.COLORS['primary']};
            border: none;
            width: {UIConstants.SLIDER_HANDLE_SIZE}px;
            height: {UIConstants.SLIDER_HANDLE_SIZE}px;
            border-radius: {UIConstants.SLIDER_HANDLE_SIZE // 2}px;
            margin: -{UIConstants.SPACING_SMALL}px 0;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: {cls.COLORS['primary_light']};
        }}
        
        QSlider::sub-page:horizontal {{
            background: {cls.COLORS['primary']};
            border-radius: 2px;
        }}
        """
    
    @classmethod
    def get_tab_styles(cls) -> str:
        """Get tab widget styling"""
        return f"""
        /* Tabs */
        QTabWidget::pane {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: {UIConstants.SPACING_MEDIUM - 4}px;
            margin-top: -1px;
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            color: {cls.COLORS['on_surface_variant']};
            padding: {UIConstants.SPACING_MEDIUM - 4}px {UIConstants.SPACING_LARGE}px;
            {cls.TYPOGRAPHY['title_small']}
            border: none;
            border-radius: 0px;
            min-width: 90px;
        }}
        
        QTabBar::tab:selected {{
            color: {cls.COLORS['primary']};
            background-color: {cls.COLORS['focus_overlay']};
            border-bottom: 3px solid {cls.COLORS['primary']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {cls.COLORS['hover_overlay']};
        }}
        """
    
    @classmethod
    def get_container_styles(cls) -> str:
        """Get container and group box styling"""
        return f"""
        /* Group Boxes */
        QGroupBox {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: {UIConstants.SPACING_MEDIUM - 4}px;
            margin-top: {UIConstants.SPACING_MEDIUM - 4}px;
            padding-top: {UIConstants.SPACING_MEDIUM - 4}px;
            {cls.TYPOGRAPHY['body_medium']}
        }}
        
        QGroupBox::title {{
            color: {cls.COLORS['on_surface']};
            {cls.TYPOGRAPHY['title_small']}
            subcontrol-origin: margin;
            left: {UIConstants.SPACING_MEDIUM}px;
            padding: 0 {UIConstants.SPACING_SMALL}px 0 {UIConstants.SPACING_SMALL}px;
            background-color: {cls.COLORS['surface']};
        }}
        
        QGroupBox::indicator {{
            width: {UIConstants.SPACING_MEDIUM}px;
            height: {UIConstants.SPACING_MEDIUM}px;
            border-radius: {UIConstants.SPACING_SMALL}px;
            border: 2px solid {cls.COLORS['outline']};
            background-color: {cls.COLORS['surface']};
        }}
        
        QGroupBox::indicator:checked {{
            background-color: {cls.COLORS['primary']};
            border-color: {cls.COLORS['primary']};
        }}
        
        /* Scroll Areas */
        QScrollArea {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: {UIConstants.SPACING_SMALL}px;
        }}
        
        QScrollBar:vertical {{
            background: {cls.COLORS['surface_variant']};
            width: {UIConstants.SPACING_MEDIUM - 4}px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {cls.COLORS['outline_variant']};
            border-radius: 6px;
            min-height: {UIConstants.SPACING_LARGE + 4}px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {cls.COLORS['on_surface_variant']};
        }}
        
        /* Cards and Surfaces */
        QWidget[class="card"] {{
            background-color: {cls.COLORS['surface']};
            border-radius: {UIConstants.SPACING_MEDIUM - 4}px;
            {cls.ELEVATION['level_1']}
        }}
        
        QWidget[class="elevated_card"] {{
            background-color: {cls.COLORS['surface']};
            border-radius: {UIConstants.SPACING_MEDIUM - 4}px;
            {cls.ELEVATION['level_3']}
        }}
        
        QWidget[class="header"] {{
            background-color: {cls.COLORS['surface']};
            border-bottom: 1px solid {cls.COLORS['outline']};
        }}
        
        QWidget[class="footer"] {{
            background-color: {cls.COLORS['surface_variant']};
            border-top: 1px solid {cls.COLORS['outline']};
        }}
        
        /* Custom Image Labels */
        QLabel[class="image_item"] {{
            background-color: {cls.COLORS['surface_variant']};
            border: 2px solid {cls.COLORS['outline']};
            border-radius: {UIConstants.SPACING_SMALL}px;
            padding: {UIConstants.SPACING_SMALL}px;
        }}
        
        QLabel[class="image_item_selected"] {{
            background-color: {cls.COLORS['focus_overlay']};
            border: 3px solid {cls.COLORS['primary']};
            border-radius: {UIConstants.SPACING_SMALL}px;
            padding: {UIConstants.SPACING_SMALL}px;
        }}
        
        QLabel[class="preview"] {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: {UIConstants.SPACING_SMALL}px;
            padding: {UIConstants.SPACING_MEDIUM}px;
        }}
        """
    
    @classmethod
    def get_app_stylesheet(cls) -> str:
        """Get the complete application stylesheet"""
        return (
            cls.get_base_styles() +
            cls.get_button_styles() +
            cls.get_label_styles() +
            cls.get_input_styles() +
            cls.get_combobox_styles() +
            cls.get_slider_styles() +
            cls.get_tab_styles() +
            cls.get_container_styles()
        )
    
    @classmethod
    def apply_material_theme(cls, app: QApplication) -> None:
        """Apply Material Design theme to the application"""
        try:
            app.setStyleSheet(cls.get_app_stylesheet())
            
            # Set application font with fallback
            try:
                font = QFont("Roboto", 14)
            except Exception:
                font = QFont("Arial", 14)  # Fallback font
            app.setFont(font)
            
            logger.info("Material Design theme applied successfully")
        except Exception as e:
            logger.error(f"Failed to apply Material Design theme: {e}")
            # Continue with default styling


# ============================================================================
# STYLED UI COMPONENTS  
# ============================================================================

class MaterialButton(QPushButton):
    """Material Design button with different variants"""
    def __init__(self, text: str, button_type: str = "filled", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setProperty("class", button_type)
        
    @staticmethod
    def filled(text: str, parent: Optional[QWidget] = None) -> 'MaterialButton':
        """Create a filled/primary button"""
        return MaterialButton(text, "filled", parent)
        
    @staticmethod
    def outlined(text: str, parent: Optional[QWidget] = None) -> 'MaterialButton':
        """Create an outlined button"""
        return MaterialButton(text, "outlined", parent)
        
    @staticmethod
    def text_button(text: str, parent: Optional[QWidget] = None) -> 'MaterialButton':
        """Create a text button"""
        return MaterialButton(text, "text", parent)
        
    @staticmethod
    def icon_button(text: str, parent: Optional[QWidget] = None) -> 'MaterialButton':
        """Create an icon button"""
        button = MaterialButton(text, "icon", parent)
        button.setFixedSize(UIConstants.ICON_BUTTON_SIZE, UIConstants.ICON_BUTTON_SIZE)
        return button


class MaterialLabel(QLabel):
    """Material Design label with typography variants"""
    def __init__(self, text: str = "", label_type: str = "body", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setProperty("class", label_type)
        
    @staticmethod
    def headline(text: str, parent: Optional[QWidget] = None) -> 'MaterialLabel':
        """Create a headline label"""
        return MaterialLabel(text, "headline", parent)
        
    @staticmethod
    def title(text: str, parent: Optional[QWidget] = None) -> 'MaterialLabel':
        """Create a title label"""
        return MaterialLabel(text, "title", parent)
        
    @staticmethod
    def subtitle(text: str, parent: Optional[QWidget] = None) -> 'MaterialLabel':
        """Create a subtitle label"""
        return MaterialLabel(text, "subtitle", parent)
        
    @staticmethod
    def caption(text: str, parent: Optional[QWidget] = None) -> 'MaterialLabel':
        """Create a caption label"""
        return MaterialLabel(text, "caption", parent)


class MaterialCard(QWidget):
    """Material Design card container"""
    def __init__(self, elevated: bool = False, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setProperty("class", "elevated_card" if elevated else "card")
        
        # Set up layout with proper spacing
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            UIConstants.MARGIN_MEDIUM, UIConstants.MARGIN_MEDIUM, 
            UIConstants.MARGIN_MEDIUM, UIConstants.MARGIN_MEDIUM
        )
        self.layout.setSpacing(UIConstants.SPACING_MEDIUM - 4)
        
    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the card"""
        if widget is not None:
            self.layout.addWidget(widget)
        
    def add_layout(self, layout: Union[QVBoxLayout, QHBoxLayout, QGridLayout]) -> None:
        """Add a layout to the card"""
        if layout is not None:
            self.layout.addLayout(layout)


# ============================================================================
# API COMMUNICATION LAYER STUBS
# ============================================================================

class HeadshotData:
    """Data model for a headshot image"""
    def __init__(self, file_path: str, metadata: Dict[str, Any] = None):
        self.file_path = file_path
        self.metadata = metadata or {}
        self.thumbnail_path: Optional[str] = None
        self.is_selected: bool = False
        self.edit_settings: Dict[str, Any] = {}
        
    def __repr__(self):
        return f"HeadshotData(file_path='{self.file_path}')"


class APIResponse:
    """Standard API response wrapper"""
    def __init__(self, success: bool, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error


class HeadshotAPIClient(QObject):
    """Client for communicating with headshot processing API"""
    
    # Signals for async operations
    images_loaded = Signal(list)  # List[HeadshotData]
    image_processed = Signal(object)  # HeadshotData
    batch_processed = Signal(list)  # List[HeadshotData]
    error_occurred = Signal(str)  # Error message
    progress_updated = Signal(int)  # Progress percentage
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        super().__init__()
        self.base_url = base_url
        self.session_token: Optional[str] = None
        
    def authenticate(self, username: str, password: str) -> APIResponse:
        """Authenticate with the API"""
        # TODO: Implement actual API authentication
        print(f"API: Authenticating user {username}")
        return APIResponse(success=True, data={"token": "mock_token_12345"})
        
    def load_images_from_directory(self, directory_path: str) -> APIResponse:
        """Load and process images from directory"""
        # TODO: Implement actual API call
        print(f"API: Loading images from {directory_path}")
        mock_images = [
            HeadshotData(f"{directory_path}/image_{i}.jpg") 
            for i in range(1, 13)
        ]
        return APIResponse(success=True, data=mock_images)
        
    def get_image_metadata(self, image_path: str) -> APIResponse:
        """Get metadata for a specific image"""
        # TODO: Implement actual API call
        print(f"API: Getting metadata for {image_path}")
        mock_metadata = {
            "width": 1920,
            "height": 1080,
            "file_size": 2048576,
            "created_date": "2024-01-15",
            "camera_model": "Canon EOS R5"
        }
        return APIResponse(success=True, data=mock_metadata)
        
    def apply_preset(self, image_data: HeadshotData, preset_name: str) -> APIResponse:
        """Apply a preset to an image"""
        # TODO: Implement actual API call
        print(f"API: Applying preset '{preset_name}' to {image_data.file_path}")
        return APIResponse(success=True, data=image_data)
        
    def batch_apply_settings(self, images: List[HeadshotData], settings: Dict[str, Any]) -> APIResponse:
        """Apply settings to multiple images"""
        # TODO: Implement actual API call
        print(f"API: Batch applying settings to {len(images)} images")
        return APIResponse(success=True, data=images)
        
    def adjust_hue(self, image_data: HeadshotData, hue_value: int) -> APIResponse:
        """Adjust hue of an image"""
        # TODO: Implement actual API call
        print(f"API: Adjusting hue to {hue_value} for {image_data.file_path}")
        return APIResponse(success=True, data=image_data)
        
    def save_edited_image(self, image_data: HeadshotData, output_path: str = None) -> APIResponse:
        """Save edited image"""
        # TODO: Implement actual API call
        save_path = output_path or image_data.file_path
        print(f"API: Saving edited image to {save_path}")
        return APIResponse(success=True, data={"saved_path": save_path})
        
    def get_similar_images(self, reference_image: HeadshotData, threshold: float = 0.8) -> APIResponse:
        """Find similar images using AI/ML"""
        # TODO: Implement actual API call
        print(f"API: Finding similar images to {reference_image.file_path}")
        mock_similar = [
            HeadshotData(f"similar_image_{i}.jpg") 
            for i in range(1, 4)
        ]
        return APIResponse(success=True, data=mock_similar)


class ImageProcessor(QObject):
    """Handles image processing operations"""
    
    # Signals for processing updates
    processing_started = Signal()
    processing_finished = Signal(object)  # HeadshotData
    processing_progress = Signal(int)  # Progress percentage
    processing_error = Signal(str)  # Error message
    
    def __init__(self, api_client: HeadshotAPIClient):
        super().__init__()
        self.api_client = api_client
        
    def process_single_image(self, image_data: HeadshotData, settings: Dict[str, Any]):
        """Process a single image with given settings"""
        # TODO: Implement actual processing logic
        print(f"Processing: {image_data.file_path} with settings {settings}")
        self.processing_started.emit()
        
        # Simulate processing time
        for progress in range(0, 101, 20):
            self.processing_progress.emit(progress)
            
        self.processing_finished.emit(image_data)
        
    def process_batch(self, images: List[HeadshotData], settings: Dict[str, Any]):
        """Process multiple images with given settings"""
        # TODO: Implement actual batch processing logic
        print(f"Batch processing: {len(images)} images")
        
        for i, image_data in enumerate(images):
            progress = int((i + 1) / len(images) * 100)
            self.processing_progress.emit(progress)
            self.process_single_image(image_data, settings)


class PresetManager(QObject):
    """Manages image editing presets"""
    
    # Signals for preset operations
    presets_loaded = Signal(list)  # List of preset names
    preset_applied = Signal(str)  # Preset name
    preset_saved = Signal(str)  # Preset name
    
    def __init__(self, api_client: HeadshotAPIClient):
        super().__init__()
        self.api_client = api_client
        self.presets: Dict[str, Dict[str, Any]] = {}
        
    def load_presets(self) -> List[str]:
        """Load available presets from API"""
        # TODO: Implement actual API call
        print("Loading presets from API")
        mock_presets = {
            "Portrait Enhance": {"brightness": 10, "contrast": 15, "saturation": 5},
            "Studio Light": {"brightness": 20, "contrast": 10, "warmth": 8},
            "Natural Look": {"brightness": 5, "contrast": 5, "saturation": 2}
        }
        self.presets = mock_presets
        preset_names = list(mock_presets.keys())
        self.presets_loaded.emit(preset_names)
        return preset_names
        
    def apply_preset(self, preset_name: str, image_data: HeadshotData) -> bool:
        """Apply a preset to an image"""
        if preset_name not in self.presets:
            return False
            
        settings = self.presets[preset_name]
        response = self.api_client.apply_preset(image_data, preset_name)
        
        if response.success:
            self.preset_applied.emit(preset_name)
            return True
        return False
        
    def save_preset(self, preset_name: str, settings: Dict[str, Any]) -> bool:
        """Save a new preset"""
        # TODO: Implement actual API call to save preset
        print(f"Saving preset '{preset_name}' with settings {settings}")
        self.presets[preset_name] = settings
        self.preset_saved.emit(preset_name)
        return True
        
    def get_preset_settings(self, preset_name: str) -> Optional[Dict[str, Any]]:
        """Get settings for a specific preset"""
        return self.presets.get(preset_name)


class FileManager(QObject):
    """Manages file operations and directory scanning"""
    
    # Signals for file operations
    directory_scanned = Signal(list)  # List[str] of file paths
    files_loaded = Signal(list)  # List[HeadshotData]
    file_saved = Signal(str)  # File path
    scan_progress = Signal(int)  # Progress percentage
    
    def __init__(self, api_client: HeadshotAPIClient):
        super().__init__()
        self.api_client = api_client
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        
    def scan_directory(self, directory_path: str) -> List[str]:
        """Scan directory for supported image files"""
        # TODO: Implement actual directory scanning
        print(f"Scanning directory: {directory_path}")
        
        # Mock file discovery
        mock_files = [
            os.path.join(directory_path, f"headshot_{i:03d}.jpg")
            for i in range(1, 25)
        ]
        
        self.directory_scanned.emit(mock_files)
        return mock_files
        
    def load_images(self, file_paths: List[str]) -> List[HeadshotData]:
        """Load images from file paths"""
        # TODO: Implement actual image loading
        print(f"Loading {len(file_paths)} images")
        
        images = []
        for i, file_path in enumerate(file_paths):
            # Simulate loading progress
            progress = int((i + 1) / len(file_paths) * 100)
            self.scan_progress.emit(progress)
            
            image_data = HeadshotData(file_path)
            # Get metadata from API
            metadata_response = self.api_client.get_image_metadata(file_path)
            if metadata_response.success:
                image_data.metadata = metadata_response.data
                
            images.append(image_data)
            
        self.files_loaded.emit(images)
        return images
        
    def save_image(self, image_data: HeadshotData, output_path: str = None) -> bool:
        """Save an image to disk"""
        response = self.api_client.save_edited_image(image_data, output_path)
        if response.success:
            self.file_saved.emit(response.data["saved_path"])
            return True
        return False


class SettingsManager:
    """Manages application settings and preferences"""
    
    def __init__(self):
        self.settings: Dict[str, Any] = {
            "last_directory": "",
            "auto_save": True,
            "preview_quality": "high",
            "batch_size": 10,
            "api_timeout": 30
        }
        
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
        
    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
        
    def save_settings(self):
        """Save settings to disk"""
        # TODO: Implement actual settings persistence
        print(f"Saving settings: {self.settings}")
        
    def load_settings(self):
        """Load settings from disk"""
        # TODO: Implement actual settings loading
        print("Loading settings from disk")


# ============================================================================
# API SERVICE COORDINATOR
# ============================================================================

class APIService(QObject):
    """Main coordinator for all API communication"""
    
    # Signals for high-level operations
    service_ready = Signal()
    service_error = Signal(str)
    operation_completed = Signal(str, object)  # operation_name, result
    
    def __init__(self):
        super().__init__()
        
        # Initialize API components
        self.api_client = HeadshotAPIClient()
        self.image_processor = ImageProcessor(self.api_client)
        self.preset_manager = PresetManager(self.api_client)
        self.file_manager = FileManager(self.api_client)
        self.settings_manager = SettingsManager()
        
        # Connect internal signals
        self._connect_signals()
        
    def _connect_signals(self):
        """Connect internal API signals"""
        self.api_client.error_occurred.connect(self.service_error.emit)
        self.image_processor.processing_error.connect(self.service_error.emit)
        
    def initialize(self) -> bool:
        """Initialize the API service"""
        try:
            # TODO: Implement actual initialization
            print("Initializing API service...")
            self.settings_manager.load_settings()
            self.preset_manager.load_presets()
            self.service_ready.emit()
            return True
        except Exception as e:
            self.service_error.emit(f"Failed to initialize API service: {str(e)}")
            return False
            
    def shutdown(self):
        """Cleanup and shutdown API service"""
        print("Shutting down API service...")
        self.settings_manager.save_settings()
        
    # Convenience methods for UI components
    def load_directory(self, directory_path: str):
        """Load all images from a directory"""
        files = self.file_manager.scan_directory(directory_path)
        images = self.file_manager.load_images(files)
        self.operation_completed.emit("load_directory", images)
        
    def apply_batch_edits(self, images: List[HeadshotData], settings: Dict[str, Any]):
        """Apply edits to multiple images"""
        self.image_processor.process_batch(images, settings)
        self.operation_completed.emit("batch_edit", images)


# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

class SectionWidget(QWidget):
    """Base class for reusable UI sections with Material Design styling"""
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
    def create_label_widget(self, text: str, label_type: str = "body", **kwargs) -> MaterialLabel:
        """Create a standardized Material Design label widget"""
        try:
            if label_type == "headline":
                return MaterialLabel.headline(text, self)
            elif label_type == "title":
                return MaterialLabel.title(text, self)
            elif label_type == "subtitle":
                return MaterialLabel.subtitle(text, self)
            elif label_type == "caption":
                return MaterialLabel.caption(text, self)
            else:
                return MaterialLabel(text, "body", self)
        except Exception as e:
            logger.error(f"Error creating label widget: {e}")
            return MaterialLabel(text, "body", self)  # Fallback
        
    def create_button_widget(self, text: str, button_type: str = "filled", 
                           callback: Optional[Callable] = None, **kwargs) -> MaterialButton:
        """Create a standardized Material Design button widget"""
        try:
            if button_type == "outlined":
                button = MaterialButton.outlined(text, self)
            elif button_type == "text":
                button = MaterialButton.text_button(text, self)
            elif button_type == "icon":
                button = MaterialButton.icon_button(text, self)
            else:
                button = MaterialButton.filled(text, self)
                
            if callback:
                button.clicked.connect(callback)
            return button
        except Exception as e:
            logger.error(f"Error creating button widget: {e}")
            # Return basic button as fallback
            button = QPushButton(text, self)
            if callback:
                button.clicked.connect(callback)
            return button
        
    def create_combobox_widget(self, items: List[str], callback: Optional[Callable] = None) -> QComboBox:
        """Create a standardized Material Design combobox widget"""
        try:
            combobox = QComboBox(self)
            if items:  # Check if items list is not empty
                combobox.addItems(items)
            if callback:
                combobox.currentTextChanged.connect(callback)
            return combobox
        except Exception as e:
            logger.error(f"Error creating combobox widget: {e}")
            return QComboBox(self)  # Return empty combobox as fallback
        
    def create_slider_widget(self, min_val: int, max_val: int, default_val: int, 
                           callback: Optional[Callable] = None) -> Dict[str, QWidget]:
        """Create a standardized Material Design slider with value field"""
        try:
            slider = QSlider(Qt.Horizontal, self)
            slider.setRange(min_val, max_val)
            slider.setValue(default_val)
            
            value_field = QLineEdit(str(default_val), self)
            value_field.setMaximumWidth(80)
            
            # Use partial to avoid lambda closure issues
            if callback:
                slider.valueChanged.connect(callback)
            
            # Connect slider to value field safely
            slider.valueChanged.connect(partial(self._update_slider_value_field, value_field))
            
            return {'slider': slider, 'value_field': value_field}
        except Exception as e:
            logger.error(f"Error creating slider widget: {e}")
            # Return basic widgets as fallback
            return {
                'slider': QSlider(Qt.Horizontal, self),
                'value_field': QLineEdit("0", self)
            }
            
    def _update_slider_value_field(self, value_field: QLineEdit, value: int) -> None:
        """Safely update slider value field"""
        try:
            if value_field is not None:
                value_field.setText(str(value))
        except Exception as e:
            logger.error(f"Error updating slider value field: {e}")
        
    def create_button_row(self, button_configs: List[Dict[str, Any]], 
                         spacing: int = UIConstants.SPACING_SMALL) -> QHBoxLayout:
        """Create a row of Material Design buttons from configuration"""
        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        
        try:
            for config in button_configs:
                if not isinstance(config, dict) or 'text' not in config:
                    logger.warning(f"Invalid button config: {config}")
                    continue
                    
                button = self.create_button_widget(
                    config['text'], 
                    config.get('button_type', 'filled'),
                    config.get('callback')
                )
                layout.addWidget(button)
        except Exception as e:
            logger.error(f"Error creating button row: {e}")
            
        return layout
        
    def create_form_section(self, title: str, widgets: List[QWidget], 
                          as_card: bool = True) -> QWidget:
        """Create a Material Design form section with title and widgets"""
        try:
            if as_card:
                section = MaterialCard(parent=self)
            else:
                section = QWidget(self)
                layout = QVBoxLayout(section)
                layout.setContentsMargins(
                    UIConstants.MARGIN_MEDIUM, UIConstants.MARGIN_MEDIUM, 
                    UIConstants.MARGIN_MEDIUM, UIConstants.MARGIN_MEDIUM
                )
                layout.setSpacing(UIConstants.SPACING_MEDIUM - 4)
                section.layout = layout
                
            if title:
                title_label = self.create_label_widget(title, "title")
                if hasattr(section, 'add_widget'):
                    section.add_widget(title_label)
                else:
                    section.layout.addWidget(title_label)
                
            for widget in widgets:
                if widget is not None:
                    if hasattr(section, 'add_widget'):
                        section.add_widget(widget)
                    else:
                        section.layout.addWidget(widget)
                        
            return section
        except Exception as e:
            logger.error(f"Error creating form section: {e}")
            return QWidget(self)  # Return empty widget as fallback
        
    def create_input_field(self, placeholder: str = "", callback: Optional[Callable] = None) -> QLineEdit:
        """Create a Material Design input field"""
        try:
            field = QLineEdit(self)
            field.setPlaceholderText(placeholder)
            if callback:
                field.textChanged.connect(callback)
            return field
        except Exception as e:
            logger.error(f"Error creating input field: {e}")
            return QLineEdit(self)  # Return basic field as fallback


class MaterialCollapsibleGroupBox(QGroupBox):
    """Material Design collapsible group box widget"""
    def __init__(self, title: str = "", parent: Optional[QWidget] = None):
        super().__init__(title, parent)
        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.toggle_content)
        
        # Create content widget with error handling
        try:
            self.content_widget = MaterialCard(parent=self)
            layout = QVBoxLayout(self)
            layout.addWidget(self.content_widget)
        except Exception as e:
            logger.error(f"Error initializing collapsible group box: {e}")
            self.content_widget = QWidget(self)
        
    def toggle_content(self) -> None:
        """Toggle content visibility"""
        try:
            if self.content_widget is not None:
                self.content_widget.setVisible(self.isChecked())
        except Exception as e:
            logger.error(f"Error toggling content: {e}")
        
    def set_content_layout(self, layout: Union[QVBoxLayout, QHBoxLayout, QGridLayout]) -> None:
        """Set content layout"""
        try:
            if self.content_widget is not None and layout is not None:
                self.content_widget.setLayout(layout)
        except Exception as e:
            logger.error(f"Error setting content layout: {e}")
        
    def add_widget(self, widget: QWidget) -> None:
        """Add widget to the collapsible content"""
        try:
            if self.content_widget is not None and widget is not None:
                if hasattr(self.content_widget, 'add_widget'):
                    self.content_widget.add_widget(widget)
                else:
                    # Fallback for basic QWidget
                    if self.content_widget.layout() is None:
                        self.content_widget.setLayout(QVBoxLayout())
                    self.content_widget.layout().addWidget(widget)
        except Exception as e:
            logger.error(f"Error adding widget to collapsible group: {e}")
        
    def add_layout(self, layout: Union[QVBoxLayout, QHBoxLayout, QGridLayout]) -> None:
        """Add layout to the collapsible content"""
        try:
            if self.content_widget is not None and layout is not None:
                if hasattr(self.content_widget, 'add_layout'):
                    self.content_widget.add_layout(layout)
                else:
                    # Fallback for basic QWidget
                    if self.content_widget.layout() is None:
                        self.content_widget.setLayout(QVBoxLayout())
                    self.content_widget.layout().addLayout(layout)
        except Exception as e:
            logger.error(f"Error adding layout to collapsible group: {e}")


class MaterialImageLabel(QLabel):
    """Material Design image label with selection support"""
    clicked = Signal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setMinimumSize(UIConstants.GALLERY_ITEM_SIZE, UIConstants.GALLERY_ITEM_SIZE)
        self.setProperty("class", "image_item")
        self.setAlignment(Qt.AlignCenter)
        self.setText("No Image")
        self.selected = False
        
    def mousePressEvent(self, event) -> None:
        """Handle mouse press events"""
        try:
            if event.button() == Qt.LeftButton:
                self.clicked.emit()
            super().mousePressEvent(event)
        except Exception as e:
            logger.error(f"Error in mouse press event: {e}")
        
    def set_selected(self, selected: bool) -> None:
        """Set selection state with style refresh"""
        try:
            self.selected = selected
            if selected:
                self.setProperty("class", "image_item_selected")
            else:
                self.setProperty("class", "image_item")
            # Force style refresh
            self.style().unpolish(self)
            self.style().polish(self)
        except Exception as e:
            logger.error(f"Error setting selection state: {e}")


class MaterialColumnWidget(SectionWidget):
    """Material Design column widget with percentage-based sizing"""
    def __init__(self, width_percentage: int = 50, as_card: bool = False, 
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.width_percentage = width_percentage
        
        if as_card:
            self.setProperty("class", "card")
            
        self._setup_sizing()
        
    def _setup_sizing(self) -> None:
        """Setup size constraints based on percentage"""
        try:
            if self.width_percentage <= 30:
                self.setMaximumWidth(350)
            elif self.width_percentage <= 50:
                self.setMaximumWidth(500)
            # No constraint for larger percentages
        except Exception as e:
            logger.error(f"Error setting up sizing: {e}")


# ============================================================================
# TAB CLASSES WITH REUSED COMPONENTS
# ============================================================================

class BaseTab(SectionWidget):
    """Base class for all tabs with Material Design styling"""
    def __init__(self, api_service: APIService, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.api_service = api_service
        self.preview_label: Optional[QLabel] = None  # Initialize explicitly
        self.setup_ui()
        self._connect_api_signals()
        
    def setup_ui(self) -> None:
        """Override in subclasses"""
        pass
        
    def _connect_api_signals(self) -> None:
        """Override in subclasses"""
        pass
        
    def create_two_column_layout(self, left_width: int = 30, right_width: int = 70, 
                               left_as_card: bool = True, right_as_card: bool = True) -> tuple:
        """Create standard two-column layout with Material Design cards"""
        try:
            main_layout = QHBoxLayout(self)
            main_layout.setSpacing(UIConstants.SPACING_MEDIUM)
            
            left_widget = MaterialColumnWidget(left_width, left_as_card, self)
            right_widget = MaterialColumnWidget(right_width, right_as_card, self)
            
            main_layout.addWidget(left_widget)
            main_layout.addWidget(right_widget)
            
            return left_widget, right_widget
        except Exception as e:
            logger.error(f"Error creating two column layout: {e}")
            # Return basic widgets as fallback
            return QWidget(self), QWidget(self)


class HeadshotGalleryTab(BaseTab):
    """First tab: Headshots Gallery with Material Design"""
    def __init__(self, api_service: APIService, parent: Optional[QWidget] = None):
        self.gallery_items: List[MaterialImageLabel] = []
        self.headshot_data: List[HeadshotData] = []
        super().__init__(api_service, parent)
        
    def _connect_api_signals(self) -> None:
        """Connect API signals for gallery operations"""
        try:
            self.api_service.file_manager.files_loaded.connect(self.on_images_loaded)
            self.api_service.preset_manager.presets_loaded.connect(self.on_presets_loaded)
            self.api_service.preset_manager.preset_applied.connect(self.on_preset_applied)
        except Exception as e:
            logger.error(f"Error connecting API signals in gallery tab: {e}")
        
    def on_images_loaded(self, images: List[HeadshotData]) -> None:
        """Handle when images are loaded from API"""
        try:
            self.headshot_data = images if images else []
            self.refresh_gallery()
        except Exception as e:
            logger.error(f"Error handling loaded images: {e}")
        
    def on_presets_loaded(self, preset_names: List[str]) -> None:
        """Handle when presets are loaded from API"""
        logger.info(f"Loaded presets: {preset_names}")
        
    def on_preset_applied(self, preset_name: str) -> None:
        """Handle when a preset is applied"""
        logger.info(f"Preset '{preset_name}' applied successfully")
        self.refresh_gallery()
        
    def refresh_gallery(self) -> None:
        """Refresh the gallery display with current data"""
        logger.info(f"Refreshing gallery with {len(self.headshot_data)} images")
        
    def apply_preset_to_selected(self, preset_name: str) -> None:
        """Apply preset to selected images"""
        try:
            selected_images = [data for data in self.headshot_data if data.is_selected]
            for image_data in selected_images:
                self.api_service.preset_manager.apply_preset(preset_name, image_data)
        except Exception as e:
            logger.error(f"Error applying preset to selected images: {e}")
            
    def submit_gallery_settings(self) -> None:
        """Submit current gallery form settings"""
        try:
            settings = {
                "filter_type": "example_filter",
                "sort_order": "date_desc",
                "enable_feature": True
            }
            selected_images = [data for data in self.headshot_data if data.is_selected]
            if selected_images:
                self.api_service.apply_batch_edits(selected_images, settings)
        except Exception as e:
            logger.error(f"Error submitting gallery settings: {e}")
            
    def reset_gallery_settings(self) -> None:
        """Reset all gallery form controls to defaults"""
        logger.info("Resetting gallery settings to defaults")
        
    def setup_ui(self) -> None:
        """Main UI setup for gallery tab"""
        try:
            left_widget, right_widget = self.create_two_column_layout()
            
            # Build left column sections
            self._build_left_column(left_widget)
            
            # Build right column (gallery)
            self._build_right_column(right_widget)
        except Exception as e:
            logger.error(f"Error setting up gallery UI: {e}")
        
    def _build_left_column(self, parent_widget: MaterialColumnWidget) -> None:
        """Build the left column with all controls"""
        try:
            layout = QVBoxLayout(parent_widget)
            layout.setSpacing(UIConstants.SPACING_MEDIUM)
            
            # Top section with pulldowns
            top_section = self._build_top_pulldowns()
            layout.addWidget(top_section)
            
            # Presets section
            presets_section = self._build_presets_section()
            layout.addWidget(presets_section)
            
            # Form controls section
            form_section = self._build_form_controls()
            layout.addWidget(form_section)
            
            # Bottom buttons
            buttons_section = self._build_action_buttons()
            layout.addWidget(buttons_section)
            
            layout.addStretch()
        except Exception as e:
            logger.error(f"Error building left column: {e}")
        
    def _build_top_pulldowns(self) -> MaterialCard:
        """Build top section with pulldown lists"""
        try:
            section = MaterialCard(parent=self)
            
            section.add_widget(self.create_label_widget("Filters", "title"))
            section.add_widget(self.create_combobox_widget(["All Types", "Portrait", "Landscape"]))
            section.add_widget(self.create_combobox_widget(["Date: Newest", "Date: Oldest", "Name: A-Z"]))
            
            return section
        except Exception as e:
            logger.error(f"Error building top pulldowns: {e}")
            return MaterialCard(parent=self)
        
    def _build_presets_section(self) -> MaterialCard:
        """Build presets section with buttons"""
        try:
            section = MaterialCard(parent=self)
            
            section.add_widget(self.create_label_widget("Presets (optional)", "title"))
            
            preset_buttons = [
                {'text': 'Portrait Enhance', 'button_type': 'outlined', 
                 'callback': partial(self.apply_preset_to_selected, "Portrait Enhance")},
                {'text': 'Studio Light', 'button_type': 'outlined',
                 'callback': partial(self.apply_preset_to_selected, "Studio Light")},
                {'text': 'Natural Look', 'button_type': 'outlined',
                 'callback': partial(self.apply_preset_to_selected, "Natural Look")}
            ]
            
            button_row = self.create_button_row(preset_buttons)
            button_widget = QWidget()
            button_widget.setLayout(button_row)
            section.add_widget(button_widget)
            
            return section
        except Exception as e:
            logger.error(f"Error building presets section: {e}")
            return MaterialCard(parent=self)
        
    def _build_form_controls(self) -> MaterialCard:
        """Build form controls section"""
        try:
            section = MaterialCard(parent=self)
            
            section.add_widget(self.create_label_widget("Advanced Options", "title"))
            
            # Three pulldowns
            section.add_widget(self.create_combobox_widget([f"Quality {j+1}" for j in range(5)]))
            section.add_widget(self.create_combobox_widget([f"Style {j+1}" for j in range(5)]))
            section.add_widget(self.create_combobox_widget([f"Format {j+1}" for j in range(5)]))
            
            # Yes/No section
            yn_section = self._build_yes_no_section()
            section.add_widget(yn_section)
            
            # Final pulldowns
            section.add_widget(self.create_combobox_widget([f"Output {j+1}" for j in range(4)]))
            section.add_widget(self.create_combobox_widget([f"Compression {j+1}" for j in range(4)]))
            
            return section
        except Exception as e:
            logger.error(f"Error building form controls: {e}")
            return MaterialCard(parent=self)
        
    def _build_yes_no_section(self) -> QWidget:
        """Build Yes/No button section"""
        try:
            section = QWidget()
            layout = QHBoxLayout(section)
            layout.setSpacing(UIConstants.SPACING_SMALL)
            
            label = self.create_label_widget("Enable auto-processing:")
            layout.addWidget(label)
            layout.addStretch()
            
            no_btn = self.create_button_widget("No", "outlined")
            yes_btn = self.create_button_widget("Yes", "filled")
            layout.addWidget(no_btn)
            layout.addWidget(yes_btn)
            
            return section
        except Exception as e:
            logger.error(f"Error building yes/no section: {e}")
            return QWidget()
        
    def _build_action_buttons(self) -> MaterialCard:
        """Build action buttons section"""
        try:
            section = MaterialCard(parent=self)
            
            button_configs = [
                {'text': 'Reset All', 'button_type': 'outlined', 'callback': self.reset_gallery_settings},
                {'text': 'Apply Settings', 'button_type': 'filled', 'callback': self.submit_gallery_settings}
            ]
            
            for config in button_configs:
                button = self.create_button_widget(config['text'], config['button_type'], config['callback'])
                section.add_widget(button)
            
            return section
        except Exception as e:
            logger.error(f"Error building action buttons: {e}")
            return MaterialCard(parent=self)
        
    def _build_right_column(self, parent_widget: MaterialColumnWidget) -> None:
        """Build the right column with gallery"""
        try:
            layout = QVBoxLayout(parent_widget)
            
            # Header
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.addWidget(self.create_label_widget("Image Gallery", "title"))
            header_layout.addStretch()
            header_layout.addWidget(self.create_label_widget("Select images (Ctrl+Click for multiple)", "caption"))
            layout.addWidget(header_widget)
            
            # Scroll area for gallery
            scroll_area = QScrollArea()
            scroll_area.setProperty("class", "card")
            gallery_widget = QWidget()
            gallery_layout = QGridLayout(gallery_widget)
            gallery_layout.setSpacing(UIConstants.SPACING_MEDIUM - 4)
            
            # Sample gallery items - Fixed lambda closure issue
            for i in range(12):
                img_label = MaterialImageLabel()
                img_label.setText(f"Image {i+1}")
                # Use partial to fix lambda closure issue
                img_label.clicked.connect(partial(self.select_image, i))
                gallery_layout.addWidget(img_label, i // UIConstants.GALLERY_COLUMNS, i % UIConstants.GALLERY_COLUMNS)
                self.gallery_items.append(img_label)
            
            scroll_area.setWidget(gallery_widget)
            scroll_area.setWidgetResizable(True)
            layout.addWidget(scroll_area)
        except Exception as e:
            logger.error(f"Error building right column: {e}")
        
    def select_image(self, index: int) -> None:
        """Handle image selection with Ctrl key support and bounds checking"""
        try:
            # Improved bounds checking
            if index < 0 or index >= len(self.gallery_items) or index >= len(self.headshot_data):
                logger.warning(f"Image selection index out of bounds: {index}")
                return
                
            modifiers = QApplication.keyboardModifiers()
            
            if modifiers == Qt.ControlModifier:
                # Toggle selection with Ctrl
                current_state = self.headshot_data[index].is_selected
                self.headshot_data[index].is_selected = not current_state
                self.gallery_items[index].set_selected(not current_state)
            else:
                # Single selection - clear all others first
                for i, data in enumerate(self.headshot_data):
                    data.is_selected = False
                    if i < len(self.gallery_items):
                        self.gallery_items[i].set_selected(False)
                
                # Select the clicked item
                self.headshot_data[index].is_selected = True
                self.gallery_items[index].set_selected(True)
        except Exception as e:
            logger.error(f"Error selecting image at index {index}: {e}")


class EditorTab(BaseTab):
    """Second tab: Editor with Material Design"""
    def __init__(self, api_service: APIService, parent: Optional[QWidget] = None):
        self.current_image: Optional[HeadshotData] = None
        self.edit_settings: Dict[str, Any] = {}
        super().__init__(api_service, parent)
        
    def _connect_api_signals(self) -> None:
        """Connect API signals for editor operations"""
        try:
            self.api_service.image_processor.processing_finished.connect(self.on_processing_finished)
            self.api_service.image_processor.processing_progress.connect(self.on_processing_progress)
            self.api_service.api_client.image_processed.connect(self.on_image_processed)
        except Exception as e:
            logger.error(f"Error connecting API signals in editor tab: {e}")
        
    def on_processing_finished(self, image_data: HeadshotData) -> None:
        """Handle when image processing is complete"""
        try:
            logger.info(f"Processing finished for {image_data.file_path}")
            self.refresh_preview()
        except Exception as e:
            logger.error(f"Error handling processing finished: {e}")
        
    def on_processing_progress(self, progress: int) -> None:
        """Handle processing progress updates"""
        logger.info(f"Processing progress: {progress}%")
        
    def on_image_processed(self, image_data: HeadshotData) -> None:
        """Handle when an image is processed by API"""
        try:
            if image_data == self.current_image:
                self.refresh_preview()
        except Exception as e:
            logger.error(f"Error handling image processed: {e}")
            
    def set_current_image(self, image_data: HeadshotData) -> None:
        """Set the current image for editing"""
        try:
            self.current_image = image_data
            self.load_image_settings()
            self.refresh_preview()
        except Exception as e:
            logger.error(f"Error setting current image: {e}")
        
    def load_image_settings(self) -> None:
        """Load settings for the current image"""
        try:
            if self.current_image:
                self.edit_settings = self.current_image.edit_settings.copy()
                self.update_ui_from_settings()
        except Exception as e:
            logger.error(f"Error loading image settings: {e}")
            
    def update_ui_from_settings(self) -> None:
        """Update UI controls to match current settings"""
        logger.info(f"Updating UI with settings: {self.edit_settings}")
        
    def refresh_preview(self) -> None:
        """Refresh the image preview"""
        try:
            if self.preview_label is not None:
                if self.current_image:
                    self.preview_label.setText(f"Image Preview\n{self.current_image.file_path}")
                else:
                    self.preview_label.setText("Image Preview\nNo image selected")
        except Exception as e:
            logger.error(f"Error refreshing preview: {e}")
        
    def apply_similar_settings(self) -> None:
        """Find and apply similar image settings"""
        try:
            if self.current_image:
                response = self.api_service.api_client.get_similar_images(self.current_image)
                if response.success:
                    logger.info(f"Found {len(response.data)} similar images")
        except Exception as e:
            logger.error(f"Error applying similar settings: {e}")
                
    def reset_editor_settings(self) -> None:
        """Reset all editor settings to defaults"""
        try:
            self.edit_settings.clear()
            self.update_ui_from_settings()
            if self.current_image:
                self.current_image.edit_settings.clear()
            logger.info("Reset editor settings to defaults")
        except Exception as e:
            logger.error(f"Error resetting editor settings: {e}")
        
    def save_current_edits(self) -> None:
        """Save current edits to the image"""
        try:
            if self.current_image:
                self.current_image.edit_settings = self.edit_settings.copy()
                save_response = self.api_service.file_manager.save_image(self.current_image)
                if save_response:
                    logger.info(f"Saved edits for {self.current_image.file_path}")
                else:
                    logger.warning("Failed to save edits")
        except Exception as e:
            logger.error(f"Error saving current edits: {e}")
                
    def on_slider_changed(self, parameter_name: str, value: int) -> None:
        """Handle slider value changes"""
        try:
            self.edit_settings[parameter_name] = value
            if self.current_image:
                # Apply setting in real-time
                settings = {parameter_name: value}
                self.api_service.image_processor.process_single_image(self.current_image, settings)
        except Exception as e:
            logger.error(f"Error handling slider change: {e}")
            
    def setup_ui(self) -> None:
        """Main UI setup for editor tab"""
        try:
            left_widget, right_widget = self.create_two_column_layout()
            
            # Build left column with collapsible sections
            self._build_left_column(left_widget)
            
            # Build right column with preview
            self._build_right_column(right_widget)
        except Exception as e:
            logger.error(f"Error setting up editor UI: {e}")
        
    def _build_left_column(self, parent_widget: MaterialColumnWidget) -> None:
        """Build the left column with collapsible sections"""
        try:
            layout = QVBoxLayout(parent_widget)
            layout.setSpacing(UIConstants.SPACING_MEDIUM)
            
            # Create 3 collapsible sections
            section_configs = [
                {"title": "Basic Adjustments", "params": ["Brightness", "Contrast", "Saturation", "Exposure"]},
                {"title": "Color Grading", "params": ["Highlights", "Shadows", "Whites", "Blacks"]},
                {"title": "Details & Effects", "params": ["Clarity", "Texture", "Vibrance", "Dehaze"]}
            ]
            
            for config in section_configs:
                section = self._build_collapsible_section(config["title"], config["params"])
                layout.addWidget(section)
            
            # Bottom buttons
            buttons_section = self._build_editor_buttons()
            layout.addWidget(buttons_section)
            
            layout.addStretch()
        except Exception as e:
            logger.error(f"Error building left column: {e}")
        
    def _build_collapsible_section(self, title: str, parameters: List[str]) -> MaterialCollapsibleGroupBox:
        """Build a single collapsible section with controls"""
        try:
            group_box = MaterialCollapsibleGroupBox(title, self)
            
            # Add parameter controls
            for param in parameters:
                param_widget = QWidget()
                param_layout = QHBoxLayout(param_widget)
                param_layout.setContentsMargins(0, 4, 0, 4)
                
                # Parameter label
                label = self.create_label_widget(param, "body")
                label.setMinimumWidth(80)
                param_layout.addWidget(label)
                
                # Slider controls with proper callback using partial
                slider_controls = self.create_slider_widget(
                    -100, 100, 0, 
                    partial(self.on_slider_changed, param)
                )
                
                param_layout.addWidget(slider_controls['slider'])
                param_layout.addWidget(slider_controls['value_field'])
                
                group_box.add_widget(param_widget)
            
            return group_box
        except Exception as e:
            logger.error(f"Error building collapsible section: {e}")
            return MaterialCollapsibleGroupBox(title, self)
        
    def _build_editor_buttons(self) -> MaterialCard:
        """Build editor action buttons"""
        try:
            section = MaterialCard(parent=self)
            
            section.add_widget(self.create_label_widget("Actions", "title"))
            
            button_configs = [
                {'text': 'Find Similar', 'button_type': 'outlined', 'callback': self.apply_similar_settings},
                {'text': 'Reset All', 'button_type': 'outlined', 'callback': self.reset_editor_settings},
                {'text': 'Save Changes', 'button_type': 'filled', 'callback': self.save_current_edits}
            ]
            
            for config in button_configs:
                button = self.create_button_widget(config['text'], config['button_type'], config['callback'])
                section.add_widget(button)
                
            return section
        except Exception as e:
            logger.error(f"Error building editor buttons: {e}")
            return MaterialCard(parent=self)
        
    def _build_right_column(self, parent_widget: MaterialColumnWidget) -> None:
        """Build the right column with preview"""
        try:
            layout = QVBoxLayout(parent_widget)
            
            # Header
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.addWidget(self.create_label_widget("Image Preview", "title"))
            header_layout.addStretch()
            layout.addWidget(header_widget)
            
            # Preview area
            self.preview_label = QLabel("Image Preview\nSelect an image from the gallery")
            self.preview_label.setAlignment(Qt.AlignCenter)
            self.preview_label.setProperty("class", "preview")
            self.preview_label.setMinimumHeight(400)
            
            layout.addWidget(self.preview_label)
        except Exception as e:
            logger.error(f"Error building right column: {e}")


class HueTab(BaseTab):
    """Third tab: Hue adjustment with Material Design"""
    def __init__(self, api_service: APIService, parent: Optional[QWidget] = None):
        self.current_image: Optional[HeadshotData] = None
        self.hue_slider: Optional[QSlider] = None
        self.hue_value: Optional[QLineEdit] = None
        super().__init__(api_service, parent)
        
    def _connect_api_signals(self) -> None:
        """Connect API signals for hue operations"""
        try:
            self.api_service.api_client.image_processed.connect(self.on_hue_applied)
        except Exception as e:
            logger.error(f"Error connecting API signals in hue tab: {e}")
        
    def on_hue_applied(self, image_data: HeadshotData) -> None:
        """Handle when hue adjustment is applied"""
        try:
            if image_data == self.current_image:
                self.update_preview()
        except Exception as e:
            logger.error(f"Error handling hue applied: {e}")
            
    def set_current_image(self, image_data: HeadshotData) -> None:
        """Set the current image for hue adjustment"""
        try:
            self.current_image = image_data
            self.update_preview()
        except Exception as e:
            logger.error(f"Error setting current image: {e}")
        
    def update_preview(self) -> None:
        """Update the hue preview"""
        try:
            if self.preview_label is not None:
                if self.current_image and self.hue_slider is not None:
                    hue_value = self.hue_slider.value()
                    self.preview_label.setText(f"Hue Preview\n{self.current_image.file_path}\nHue: {hue_value}°")
                else:
                    self.preview_label.setText("Hue Preview\nNo image selected")
        except Exception as e:
            logger.error(f"Error updating preview: {e}")
            
    def update_hue(self, value: int) -> None:
        """Update hue in real-time"""
        try:
            if self.hue_value is not None:
                self.hue_value.setText(str(value))
            
            # Apply hue adjustment via API if image is loaded
            if self.current_image:
                response = self.api_service.api_client.adjust_hue(self.current_image, value)
                if response.success:
                    self.update_preview()
            else:
                if self.preview_label is not None:
                    self.preview_label.setText(f"Hue Preview\nNo image selected\nHue: {value}°")
        except Exception as e:
            logger.error(f"Error updating hue: {e}")
            
    def update_slider_from_text(self, text: str) -> None:
        """Update slider when text field changes"""
        try:
            value = int(text)
            if -180 <= value <= 180 and self.hue_slider is not None:
                self.hue_slider.setValue(value)
        except ValueError:
            pass  # Invalid input, ignore
        except Exception as e:
            logger.error(f"Error updating slider from text: {e}")
            
    def reset_hue(self) -> None:
        """Reset hue to default"""
        try:
            if self.hue_slider is not None:
                self.hue_slider.setValue(0)
        except Exception as e:
            logger.error(f"Error resetting hue: {e}")
        
    def setup_ui(self) -> None:
        """Main UI setup for hue tab"""
        try:
            left_widget, right_widget = self.create_two_column_layout()
            
            # Build left column with hue controls
            self._build_left_column(left_widget)
            
            # Build right column with preview
            self._build_right_column(right_widget)
        except Exception as e:
            logger.error(f"Error setting up hue UI: {e}")
        
    def _build_left_column(self, parent_widget: MaterialColumnWidget) -> None:
        """Build the left column with hue controls"""
        try:
            layout = QVBoxLayout(parent_widget)
            layout.setSpacing(UIConstants.SPACING_MEDIUM)
            
            # Hue controls section
            hue_section = self._build_hue_controls()
            layout.addWidget(hue_section)
            
            # Reset button section
            reset_section = self._build_reset_section()
            layout.addWidget(reset_section)
            
            layout.addStretch()
        except Exception as e:
            logger.error(f"Error building left column: {e}")
        
    def _build_hue_controls(self) -> MaterialCard:
        """Build hue adjustment controls"""
        try:
            section = MaterialCard(parent=self)
            
            section.add_widget(self.create_label_widget("Hue Adjustment", "title"))
            
            # Hue slider controls
            slider_widget = QWidget()
            slider_layout = QHBoxLayout(slider_widget)
            slider_layout.setContentsMargins(0, UIConstants.SPACING_SMALL, 0, UIConstants.SPACING_SMALL)
            
            slider_controls = self.create_slider_widget(-180, 180, 0, self.update_hue)
            self.hue_slider = slider_controls['slider']
            self.hue_value = slider_controls['value_field']
            
            # Connect text field to slider safely
            if self.hue_value is not None:
                self.hue_value.textChanged.connect(self.update_slider_from_text)
            
            slider_layout.addWidget(self.create_label_widget("Hue:", "body"))
            slider_layout.addWidget(self.hue_slider)
            slider_layout.addWidget(self.hue_value)
            slider_layout.addWidget(self.create_label_widget("°", "caption"))
            
            section.add_widget(slider_widget)
            
            # Add some helpful text
            help_text = self.create_label_widget(
                "Adjust the hue to change the overall color tone of the image. "
                "Values range from -180° to +180°.", 
                "caption"
            )
            help_text.setWordWrap(True)
            section.add_widget(help_text)
            
            return section
        except Exception as e:
            logger.error(f"Error building hue controls: {e}")
            return MaterialCard(parent=self)
        
    def _build_reset_section(self) -> MaterialCard:
        """Build reset button section"""
        try:
            section = MaterialCard(parent=self)
            
            section.add_widget(self.create_label_widget("Reset", "title"))
            
            reset_btn = self.create_button_widget("Reset to Default", "outlined", self.reset_hue)
            section.add_widget(reset_btn)
            
            return section
        except Exception as e:
            logger.error(f"Error building reset section: {e}")
            return MaterialCard(parent=self)
        
    def _build_right_column(self, parent_widget: MaterialColumnWidget) -> None:
        """Build the right column with preview"""
        try:
            layout = QVBoxLayout(parent_widget)
            
            # Header
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.addWidget(self.create_label_widget("Live Preview", "title"))
            header_layout.addStretch()
            header_layout.addWidget(self.create_label_widget("Changes apply in real-time", "caption"))
            layout.addWidget(header_widget)
            
            # Preview area
            self.preview_label = QLabel("Hue Preview\nSelect an image from the gallery")
            self.preview_label.setAlignment(Qt.AlignCenter)
            self.preview_label.setProperty("class", "preview")
            self.preview_label.setMinimumHeight(400)
            
            layout.addWidget(self.preview_label)
        except Exception as e:
            logger.error(f"Error building right column: {e}")


# ============================================================================
# MAIN WINDOW WITH REUSED COMPONENTS
# ============================================================================

class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Headshot Viewer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize API service
        self.api_service = APIService()
        self.current_directory: Optional[str] = None
        
        self.setup_ui()
        self.setup_timer()
        self._connect_api_signals()
        
        # Initialize API service
        self.api_service.initialize()
        
    def _connect_api_signals(self):
        """Connect main window to API signals"""
        self.api_service.service_ready.connect(self.on_service_ready)
        self.api_service.service_error.connect(self.on_service_error)
        self.api_service.operation_completed.connect(self.on_operation_completed)
        self.api_service.file_manager.files_loaded.connect(self.on_images_loaded)
        
    def on_service_ready(self):
        """Handle when API service is ready"""
        print("API service is ready")
        self.setEnabled(True)
        
    def on_service_error(self, error_message: str):
        """Handle API service errors"""
        print(f"API Service Error: {error_message}")
        
    def on_operation_completed(self, operation_name: str, result: Any):
        """Handle completed API operations"""
        print(f"Operation '{operation_name}' completed with result: {type(result)}")
        
    def on_images_loaded(self, images: List[HeadshotData]):
        """Handle when images are loaded from directory"""
        print(f"Loaded {len(images)} images from directory")
        if hasattr(self, 'gallery_tab'):
            self.gallery_tab.on_images_loaded(images)
            
    def get_selected_images(self) -> List[HeadshotData]:
        """Get currently selected images from gallery"""
        if hasattr(self, 'gallery_tab'):
            return [data for data in self.gallery_tab.headshot_data if data.is_selected]
        return []
        
    def set_current_image_for_editing(self, image_data: HeadshotData):
        """Set current image for editor and hue tabs"""
        if hasattr(self, 'editor_tab'):
            self.editor_tab.set_current_image(image_data)
        if hasattr(self, 'hue_tab'):
            self.hue_tab.set_current_image(image_data)
            
    def setup_ui(self):
        """Main UI setup"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Build main sections
        header_widget = self._build_header()
        tabs_widget = self._build_tabs()
        footer_widget = self._build_footer()
        
        main_layout.addWidget(header_widget)
        main_layout.addWidget(tabs_widget)
        main_layout.addWidget(footer_widget)
        
    def _build_header(self):
        """Build header section (20% of view)"""
        header_widget = QWidget()
        header_widget.setMaximumHeight(160)
        header_layout = QHBoxLayout(header_widget)
        
        # Build header sections
        title_section = self._build_header_title()
        directory_section = self._build_header_directory()
        load_section = self._build_header_load()
        
        header_layout.addWidget(title_section)
        header_layout.addWidget(directory_section)
        header_layout.addWidget(load_section)
        
        return header_widget
        
    def _build_header_title(self):
        """Build header title section"""
        section = QWidget()
        section.setMinimumWidth(400)
        layout = QVBoxLayout(section)
        
        title_label = QLabel("Headshot Viewer Application")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        return section
        
    def _build_header_directory(self):
        """Build directory chooser section"""
        section = QWidget()
        layout = QVBoxLayout(section)
        
        dir_label = QLabel("Directory:")
        self.dir_button = QPushButton("Choose Directory")
        self.dir_button.clicked.connect(self.choose_directory)
        self.dir_path_label = QLabel("No directory selected")
        
        layout.addWidget(dir_label)
        layout.addWidget(self.dir_button)
        layout.addWidget(self.dir_path_label)
        
        return section
        
    def _build_header_load(self):
        """Build load button section"""
        section = QWidget()
        layout = QVBoxLayout(section)
        
        self.load_button = QPushButton("Load Selected\nHeadshots")
        self.load_button.clicked.connect(self.load_headshots)
        layout.addWidget(self.load_button)
        
        return section
        
    def _build_tabs(self):
        """Build tab widget section (40% of view)"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setMaximumHeight(320)
        
        # Create tab instances with API service
        self.gallery_tab = HeadshotGalleryTab(self.api_service)
        self.editor_tab = EditorTab(self.api_service)
        self.hue_tab = HueTab(self.api_service)
        
        # Add tabs
        self.tab_widget.addTab(self.gallery_tab, "Headshots Gallery")
        self.tab_widget.addTab(self.editor_tab, "Editor")
        self.tab_widget.addTab(self.hue_tab, "Hue")
        
        # Connect tab changes
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        return self.tab_widget
        
    def on_tab_changed(self, index: int):
        """Handle tab changes and sync current image"""
        selected_images = self.get_selected_images()
        if selected_images:
            current_image = selected_images[0]
            if index == 1:  # Editor tab
                self.editor_tab.set_current_image(current_image)
            elif index == 2:  # Hue tab
                self.hue_tab.set_current_image(current_image)
                
    def _build_footer(self):
        """Build footer section (20% of view)"""
        footer_widget = QWidget()
        footer_widget.setMaximumHeight(160)
        footer_layout = QHBoxLayout(footer_widget)
        
        # Build footer sections
        author_section = self._build_footer_author()
        nav_section = self._build_footer_navigation()
        time_section = self._build_footer_time()
        
        footer_layout.addWidget(author_section)
        footer_layout.addWidget(nav_section)
        footer_layout.addWidget(time_section)
        
        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self.update_page_counter)
        
        return footer_widget
        
    def _build_footer_author(self):
        """Build author information section"""
        section = QWidget()
        layout = QVBoxLayout(section)
        
        author_label = QLabel("Author Information")
        author_label.setFont(QFont("Arial", 10, QFont.Bold))
        author_detail = QLabel("Headshot Viewer v1.0\nDeveloped with PySide6")
        
        layout.addWidget(author_label)
        layout.addWidget(author_detail)
        
        return section
        
    def _build_footer_navigation(self):
        """Build navigation controls section"""
        section = QWidget()
        layout = QHBoxLayout(section)
        
        # Navigation buttons
        home_btn = QPushButton("🏠")
        home_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(0))
        
        left_btn = QPushButton("◀")
        left_btn.clicked.connect(self.previous_tab)
        
        self.page_label = QLabel("1 of 3")
        self.page_label.setAlignment(Qt.AlignCenter)
        
        right_btn = QPushButton("▶")
        right_btn.clicked.connect(self.next_tab)
        
        layout.addWidget(home_btn)
        layout.addWidget(left_btn)
        layout.addWidget(self.page_label)
        layout.addWidget(right_btn)
        
        return section
        
    def _build_footer_time(self):
        """Build time display section"""
        section = QWidget()
        layout = QVBoxLayout(section)
        
        self.time_label = QLabel()
        self.update_time()
        layout.addWidget(self.time_label)
        
        return section
        
    def setup_timer(self):
        """Setup timer for updating timestamp"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)  # Update every minute
        
    def choose_directory(self):
        """Open directory chooser dialog"""
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if directory:
            self.current_directory = directory
            self.dir_path_label.setText(directory)
            
            # Save directory and load images
            self.api_service.settings_manager.set_setting("last_directory", directory)
            self.api_service.load_directory(directory)
            
    def load_headshots(self):
        """Load selected headshots"""
        selected_images = self.get_selected_images()
        if selected_images:
            print(f"Loading {len(selected_images)} selected headshots")
            if len(selected_images) > 0:
                self.set_current_image_for_editing(selected_images[0])
        else:
            print("No headshots selected")
            
        # Load directory if no current directory
        if not self.current_directory:
            if hasattr(self, 'dir_path_label') and self.dir_path_label.text() != "No directory selected":
                self.current_directory = self.dir_path_label.text()
                self.api_service.load_directory(self.current_directory)
                
    def previous_tab(self):
        """Navigate to previous tab"""
        current = self.tab_widget.currentIndex()
        if current > 0:
            self.tab_widget.setCurrentIndex(current - 1)
        else:
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            
    def next_tab(self):
        """Navigate to next tab"""
        current = self.tab_widget.currentIndex()
        if current < self.tab_widget.count() - 1:
            self.tab_widget.setCurrentIndex(current + 1)
        else:
            self.tab_widget.setCurrentIndex(0)
            
    def update_page_counter(self):
        """Update page counter in footer"""
        current = self.tab_widget.currentIndex() + 1
        total = self.tab_widget.count()
        self.page_label.setText(f"{current} of {total}")
        
    def update_time(self):
        """Update the last updated time"""
        now = datetime.now()
        time_str = now.strftime("Last updated: %b %d %Y @ %I:%M %p")
        self.time_label.setText(time_str)
        
    def closeEvent(self, event):
        """Handle application close event"""
        self.api_service.shutdown()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()