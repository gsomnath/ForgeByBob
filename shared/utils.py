import os
import uuid
from datetime import datetime, timezone
from typing import Optional, List
from pathlib import Path


def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get current UTC timestamp (timezone-aware)."""
    return datetime.now(timezone.utc)


def sanitize_folder_name(name: str) -> str:
    """Convert blog title to valid folder name."""
    # Replace spaces with underscores and remove invalid characters
    sanitized = name.replace(" ", "_")
    # Keep only alphanumeric characters, underscores, and hyphens
    sanitized = "".join(c for c in sanitized if c.isalnum() or c in "_-")
    return sanitized.lower()


def create_blog_folder_structure(base_path: str, blog_title: str) -> str:
    """Create the folder structure for a new blog."""
    folder_name = sanitize_folder_name(blog_title)
    blog_path = Path(base_path) / folder_name
    
    # Create main blog directory
    blog_path.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (blog_path / "request").mkdir(exist_ok=True)
    (blog_path / "reference").mkdir(exist_ok=True)
    (blog_path / "final").mkdir(exist_ok=True)
    
    return str(blog_path)


def get_next_version_number(blog_folder: str) -> int:
    """Get the next version number for a blog."""
    final_folder = Path(blog_folder) / "final"
    if not final_folder.exists():
        return 1
    
    # Count existing version files
    version_files = list(final_folder.glob("v*.md"))
    if not version_files:
        return 1
    
    # Extract version numbers and find the maximum
    versions = []
    for file in version_files:
        try:
            version_str = file.stem[1:]  # Remove 'v' prefix
            versions.append(int(version_str))
        except ValueError:
            continue
    
    return max(versions) + 1 if versions else 1


def save_blog_version(blog_folder: str, content: str, version: int) -> str:
    """Save a blog version to the final folder."""
    final_folder = Path(blog_folder) / "final"
    final_folder.mkdir(exist_ok=True)
    
    version_file = final_folder / f"v{version}.md"
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(version_file)


def save_prompt(blog_folder: str, prompt: str, filename: Optional[str] = None) -> str:
    """Save a prompt to the request folder."""
    request_folder = Path(blog_folder) / "request"
    request_folder.mkdir(exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prompt_{timestamp}.txt"
    
    prompt_file = request_folder / filename
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    return str(prompt_file)


def list_blog_versions(blog_folder: str) -> List[dict]:
    """List all versions of a blog."""
    final_folder = Path(blog_folder) / "final"
    if not final_folder.exists():
        return []
    
    versions = []
    version_files = sorted(final_folder.glob("v*.md"))
    
    for file in version_files:
        try:
            version_num = int(file.stem[1:])  # Remove 'v' prefix
            stat = file.stat()
            versions.append({
                "version": version_num,
                "file_path": str(file),
                "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                "size": stat.st_size
            })
        except ValueError:
            continue
    
    return sorted(versions, key=lambda x: x["version"], reverse=True)


def read_file_content(file_path: str) -> Optional[str]:
    """Read content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception:
        return None


def ensure_directory_exists(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)
