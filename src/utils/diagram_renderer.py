"""
Utility for rendering Mermaid diagrams to images.
"""

import tempfile
import subprocess
from pathlib import Path
from typing import Optional
import base64
import logging

logger = logging.getLogger(__name__)


class DiagramRenderer:
    """
    Renders Mermaid diagrams to various image formats.
    Uses either mermaid-cli (mmdc) or playwright for headless rendering.
    """
    
    def __init__(self):
        self.renderer_type = self._detect_renderer()
        
    def _detect_renderer(self) -> str:
        """Detect available rendering method."""
        # Check for mermaid-cli
        try:
            subprocess.run(
                ['mmdc', '--version'],
                capture_output=True,
                check=True,
                timeout=5
            )
            logger.info("Using mermaid-cli (mmdc) for diagram rendering")
            return 'mmdc'
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Check for playwright
        try:
            import playwright
            logger.info("Using playwright for diagram rendering")
            return 'playwright'
        except ImportError:
            pass
        
        logger.warning("No diagram renderer available. Diagrams will be shown as code.")
        return 'none'
    
    def render_mermaid_to_png(
        self,
        mermaid_code: str,
        output_path: Optional[Path] = None,
        background_color: str = 'white',
        width: int = 800
    ) -> Optional[Path]:
        """
        Render Mermaid diagram to PNG image.
        
        Args:
            mermaid_code: Mermaid diagram code
            output_path: Output file path (if None, creates temp file)
            background_color: Background color
            width: Image width in pixels
            
        Returns:
            Path to generated PNG file or None if rendering failed
        """
        if self.renderer_type == 'none':
            logger.warning("No renderer available")
            return None
        
        # Create output path if not provided
        if output_path is None:
            temp_dir = tempfile.mkdtemp()
            output_path = Path(temp_dir) / "diagram.png"
        else:
            output_path = Path(output_path)
        
        try:
            if self.renderer_type == 'mmdc':
                return self._render_with_mmdc(mermaid_code, output_path, background_color, width)
            elif self.renderer_type == 'playwright':
                return self._render_with_playwright(mermaid_code, output_path, background_color, width)
        except Exception as e:
            logger.error(f"Failed to render diagram: {e}")
            return None
    
    def _render_with_mmdc(
        self,
        mermaid_code: str,
        output_path: Path,
        background_color: str,
        width: int
    ) -> Optional[Path]:
        """Render using mermaid-cli."""
        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
            f.write(mermaid_code)
            input_file = Path(f.name)
        
        try:
            # Run mmdc command
            cmd = [
                'mmdc',
                '-i', str(input_file),
                '-o', str(output_path),
                '-b', background_color,
                '-w', str(width)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            
            if output_path.exists():
                logger.info(f"Diagram rendered to {output_path}")
                return output_path
            else:
                logger.error(f"Output file not created: {output_path}")
                return None
                
        except subprocess.CalledProcessError as e:
            logger.error(f"mmdc command failed: {e.stderr}")
            return None
        except subprocess.TimeoutExpired:
            logger.error("mmdc command timed out")
            return None
        finally:
            # Clean up input file
            input_file.unlink(missing_ok=True)
    
    def _render_with_playwright(
        self,
        mermaid_code: str,
        output_path: Path,
        background_color: str,
        width: int
    ) -> Optional[Path]:
        """Render using playwright headless browser."""
        try:
            from playwright.sync_api import sync_playwright
            
            # HTML template for rendering
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
                <script>
                    mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
                </script>
                <style>
                    body {{ 
                        background-color: {background_color}; 
                        margin: 20px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    .mermaid {{
                        max-width: {width}px;
                    }}
                </style>
            </head>
            <body>
                <div class="mermaid">
                {mermaid_code}
                </div>
            </body>
            </html>
            """
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={'width': width + 40, 'height': 800})
                page.set_content(html_template)
                
                # Wait for mermaid to render
                page.wait_for_timeout(2000)
                
                # Get the diagram element and take screenshot
                element = page.query_selector('.mermaid')
                if element:
                    element.screenshot(path=str(output_path))
                    logger.info(f"Diagram rendered to {output_path}")
                    browser.close()
                    return output_path
                else:
                    logger.error("Could not find mermaid element")
                    browser.close()
                    return None
                    
        except Exception as e:
            logger.error(f"Playwright rendering failed: {e}")
            return None
    
    def render_to_base64(self, mermaid_code: str) -> Optional[str]:
        """
        Render Mermaid diagram to base64 encoded PNG.
        
        Args:
            mermaid_code: Mermaid diagram code
            
        Returns:
            Base64 encoded PNG image or None
        """
        png_path = self.render_mermaid_to_png(mermaid_code)
        if png_path and png_path.exists():
            try:
                with open(png_path, 'rb') as f:
                    image_data = f.read()
                    return base64.b64encode(image_data).decode('utf-8')
            finally:
                # Clean up temp file
                png_path.unlink(missing_ok=True)
        return None
