import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from shared.utils import (
    sanitize_folder_name, create_blog_folder_structure,
    get_next_version_number, save_blog_version
)


def test_sanitize_folder_name():
    """Test folder name sanitization."""
    assert sanitize_folder_name("My Blog Post") == "my_blog_post"
    assert sanitize_folder_name("Blog with @#$ symbols!") == "blog_with_symbols"
    assert sanitize_folder_name("UPPERCASE") == "uppercase"


def test_create_blog_folder_structure(tmp_path):
    """Test blog folder structure creation."""
    blog_path = create_blog_folder_structure(str(tmp_path), "Test Blog")
    
    blog_folder = Path(blog_path)
    assert blog_folder.exists()
    assert (blog_folder / "request").exists()
    assert (blog_folder / "reference").exists()
    assert (blog_folder / "final").exists()


def test_get_next_version_number(tmp_path):
    """Test version number generation."""
    blog_folder = tmp_path / "test_blog"
    blog_folder.mkdir()
    
    # No versions exist
    assert get_next_version_number(str(blog_folder)) == 1
    
    # Create a version file
    final_folder = blog_folder / "final"
    final_folder.mkdir()
    (final_folder / "v1.md").write_text("content")
    
    assert get_next_version_number(str(blog_folder)) == 2


def test_save_blog_version(tmp_path):
    """Test saving blog versions."""
    blog_folder = tmp_path / "test_blog"
    content = "# Test Blog\n\nThis is test content."
    
    version_file = save_blog_version(str(blog_folder), content, 1)
    
    assert Path(version_file).exists()
    assert Path(version_file).read_text(encoding='utf-8') == content
