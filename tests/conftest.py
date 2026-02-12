"""
Pytest configuration and fixtures for tests.
"""
import pytest
from unittest.mock import Mock, MagicMock
from pathlib import Path
import tempfile


@pytest.fixture(autouse=True)
def mock_diagram_renderer(monkeypatch):
    """
    Mock DiagramRenderer to avoid Playwright initialization in tests.
    This makes tests faster and prevents hanging on CI.
    """
    # Create a mock renderer instance
    mock_renderer = MagicMock()
    
    # Mock the render method to return a temporary PNG file
    def mock_render(*args, **kwargs):
        # Create a minimal PNG file
        temp_file = Path(tempfile.mktemp(suffix='.png'))
        # Write minimal valid PNG header
        with open(temp_file, 'wb') as f:
            # PNG signature
            f.write(b'\x89PNG\r\n\x1a\n')
            # IHDR chunk
            f.write(b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01')
            f.write(b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89')
            # IDAT chunk
            f.write(b'\x00\x00\x00\nIDAT\x08\x99c\x00\x01\x00\x00\x05\x00\x01')
            f.write(b'\r\n-\xb4')
            # IEND chunk
            f.write(b'\x00\x00\x00\x00IEND\xaeB`\x82')
        return temp_file
    
    mock_renderer.render_mermaid_to_png = Mock(side_effect=mock_render)
    mock_renderer.renderer_type = 'mock'
    
    # Create a mock class that returns our mock instance
    mock_class = Mock(return_value=mock_renderer)
    
    # Patch DiagramRenderer at the import locations
    monkeypatch.setattr('src.utils.diagram_renderer.DiagramRenderer', mock_class)
    
    yield mock_renderer
