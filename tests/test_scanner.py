"""
Tests for the PulseScanner module
====================================

This demonstrates the testing structure and best practices for CodePulse.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Import the module to test
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.scanner import PulseScanner, FileMetadata, ProjectStructure


@pytest.fixture
def temp_project():
    """Create a temporary project structure for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample Python files
        test_file1 = Path(tmpdir) / "module1.py"
        test_file1.write_text("""
import os
import sys

def hello_world():
    '''Say hello'''
    print("Hello, World!")

class MyClass:
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value
""")
        
        test_file2 = Path(tmpdir) / "module2.py"
        test_file2.write_text("""
from module1 import MyClass

def use_class():
    obj = MyClass()
    return obj.get_value()
""")
        
        # Create subdirectory with file
        subdir = Path(tmpdir) / "subpackage"
        subdir.mkdir()
        test_file3 = subdir / "helper.py"
        test_file3.write_text("""
def helper_function(x, y):
    return x + y
""")
        
        yield tmpdir


class TestPulseScanner:
    """Test suite for PulseScanner"""
    
    def test_scanner_initialization(self, temp_project):
        """Test that scanner initializes correctly"""
        scanner = PulseScanner(temp_project)
        assert scanner.root_path == Path(temp_project).resolve()
        assert scanner.max_depth == 10
        assert scanner.follow_symlinks == False
    
    def test_should_exclude_patterns(self):
        """Test exclusion pattern matching"""
        scanner = PulseScanner(".")
        
        # Test exclusion of __pycache__
        assert scanner.should_exclude(Path("src/__pycache__/module.pyc"))
        
        # Test exclusion of .git
        assert scanner.should_exclude(Path(".git/config"))
        
        # Test that normal files are not excluded
        assert not scanner.should_exclude(Path("src/core/scanner.py"))
    
    def test_file_hash_calculation(self, temp_project):
        """Test file hash calculation"""
        scanner = PulseScanner(temp_project)
        test_file = Path(temp_project) / "module1.py"
        
        hash1 = scanner.calculate_file_hash(test_file)
        hash2 = scanner.calculate_file_hash(test_file)
        
        # Same file should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 character hex string
    
    def test_python_ast_analysis(self, temp_project):
        """Test AST-based Python code analysis"""
        scanner = PulseScanner(temp_project)
        test_file = Path(temp_project) / "module1.py"
        
        analysis = scanner.analyze_python_ast(test_file)
        
        # Check that imports were detected
        assert 'os' in analysis['imports']
        assert 'sys' in analysis['imports']
        
        # Check that function was detected
        function_names = [f['name'] for f in analysis['functions']]
        assert 'hello_world' in function_names
        
        # Check that class was detected
        class_names = [c['name'] for c in analysis['classes']]
        assert 'MyClass' in class_names
        
        # Check that class methods were detected
        myclass = next(c for c in analysis['classes'] if c['name'] == 'MyClass')
        assert '__init__' in myclass['methods']
        assert 'get_value' in myclass['methods']
    
    def test_scan_file(self, temp_project):
        """Test scanning a single file"""
        scanner = PulseScanner(temp_project)
        test_file = Path(temp_project) / "module1.py"
        
        metadata = scanner.scan_file(test_file)
        
        assert metadata is not None
        assert metadata.language == 'Python'
        assert metadata.lines > 0
        assert metadata.size > 0
        assert len(metadata.imports) == 2  # os and sys
        assert len(metadata.functions) == 1  # hello_world
        assert len(metadata.classes) == 1  # MyClass
    
    def test_full_project_scan(self, temp_project):
        """Test scanning an entire project"""
        scanner = PulseScanner(temp_project)
        structure = scanner.scan()
        
        assert structure.total_files >= 3  # At least our 3 test files
        assert structure.total_lines > 0
        assert 'Python' in structure.languages
        assert structure.languages['Python'] >= 3
    
    def test_dependency_graph_building(self, temp_project):
        """Test dependency graph generation"""
        scanner = PulseScanner(temp_project)
        structure = scanner.scan()
        
        # module2 imports from module1
        # Check if dependency was detected
        assert len(structure.dependency_graph) > 0
    
    def test_export_json(self, temp_project):
        """Test JSON export functionality"""
        scanner = PulseScanner(temp_project)
        structure = scanner.scan()
        
        output_file = os.path.join(temp_project, "scan_results.json")
        scanner.export_json(output_file)
        
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0


class TestFileMetadata:
    """Test FileMetadata data class"""
    
    def test_metadata_creation(self):
        """Test creating FileMetadata objects"""
        metadata = FileMetadata(
            path="src/core/scanner.py",
            size=1024,
            lines=50,
            language="Python",
            file_hash="abc123"
        )
        
        assert metadata.path == "src/core/scanner.py"
        assert metadata.size == 1024
        assert metadata.lines == 50
    
    def test_metadata_to_dict(self):
        """Test conversion to dictionary"""
        metadata = FileMetadata(
            path="test.py",
            size=100,
            lines=10,
            language="Python",
            file_hash="xyz"
        )
        
        data = metadata.to_dict()
        assert isinstance(data, dict)
        assert data['path'] == "test.py"
        assert data['language'] == "Python"


class TestProjectStructure:
    """Test ProjectStructure data class"""
    
    def test_structure_creation(self):
        """Test creating ProjectStructure objects"""
        structure = ProjectStructure(root_path="/test/project")
        
        assert structure.root_path == "/test/project"
        assert structure.total_files == 0
        assert structure.total_lines == 0
    
    def test_structure_to_dict(self):
        """Test conversion to dictionary"""
        structure = ProjectStructure(
            root_path="/test",
            total_files=5,
            total_lines=200
        )
        
        data = structure.to_dict()
        assert isinstance(data, dict)
        assert data['total_files'] == 5
        assert data['total_lines'] == 200


# Edge cases and error handling tests
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            scanner = PulseScanner(tmpdir)
            structure = scanner.scan()
            
            assert structure.total_files == 0
            assert structure.total_lines == 0
    
    def test_scan_with_max_depth(self, temp_project):
        """Test max_depth parameter"""
        scanner = PulseScanner(temp_project, max_depth=1)
        structure = scanner.scan()
        
        # Should scan root level files
        assert structure.total_files >= 2
    
    def test_invalid_python_syntax(self):
        """Test handling files with syntax errors"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with invalid syntax
            bad_file = Path(tmpdir) / "bad.py"
            bad_file.write_text("def invalid syntax here")
            
            scanner = PulseScanner(tmpdir)
            analysis = scanner.analyze_python_ast(bad_file)
            
            # Should handle gracefully
            assert analysis['imports'] == []
            assert analysis['functions'] == []


# Performance tests
@pytest.mark.performance
class TestPerformance:
    """Performance-related tests"""
    
    def test_large_file_scanning(self):
        """Test scanning large files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a large file
            large_file = Path(tmpdir) / "large.py"
            content = "\n".join([f"def function_{i}(): pass" for i in range(1000)])
            large_file.write_text(content)
            
            scanner = PulseScanner(tmpdir)
            
            import time
            start = time.time()
            structure = scanner.scan()
            duration = time.time() - start
            
            # Should complete in reasonable time (< 5 seconds)
            assert duration < 5.0
            assert structure.total_files == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
