"""
System monitoring and resource tracking
Monitors CPU, memory, and disk usage
"""
import os
import psutil
import time
from typing import Dict

class SystemMonitor:
    """Monitor system resources"""
    
    def __init__(self):
        """Initialize system monitor"""
        self.start_time = time.time()
        self.process = psutil.Process(os.getpid())
    
    def get_cpu_usage(self) -> float:
        """
        Get CPU usage percentage
        
        Returns:
            CPU usage as percentage
        """
        try:
            return self.process.cpu_percent(interval=0.1)
        except:
            return 0.0
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get memory usage information
        
        Returns:
            Dictionary with memory statistics
        """
        try:
            mem_info = self.process.memory_info()
            mem_percent = self.process.memory_percent()
            
            return {
                'rss_mb': mem_info.rss / 1024 / 1024,  # Resident Set Size in MB
                'vms_mb': mem_info.vms / 1024 / 1024,  # Virtual Memory Size in MB
                'percent': mem_percent
            }
        except:
            return {'rss_mb': 0, 'vms_mb': 0, 'percent': 0}
    
    def get_disk_usage(self, path: str = '/') -> Dict[str, float]:
        """
        Get disk usage for given path
        
        Args:
            path: Path to check (default: root)
            
        Returns:
            Dictionary with disk statistics
        """
        try:
            disk = psutil.disk_usage(path)
            return {
                'total_gb': disk.total / 1024 / 1024 / 1024,
                'used_gb': disk.used / 1024 / 1024 / 1024,
                'free_gb': disk.free / 1024 / 1024 / 1024,
                'percent': disk.percent
            }
        except:
            return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0, 'percent': 0}
    
    def get_uptime(self) -> int:
        """
        Get bot uptime in seconds
        
        Returns:
            Uptime in seconds
        """
        return int(time.time() - self.start_time)
    
    def get_uptime_string(self) -> str:
        """
        Get formatted uptime string
        
        Returns:
            Formatted uptime (e.g., "2d 5h 30m")
        """
        uptime = self.get_uptime()
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if not parts or seconds > 0:
            parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
    def get_all_stats(self) -> Dict:
        """
        Get all system statistics
        
        Returns:
            Dictionary with all statistics
        """
        return {
            'cpu_percent': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage(),
            'uptime_seconds': self.get_uptime(),
            'uptime_string': self.get_uptime_string()
        }

# Global system monitor instance
system_monitor = SystemMonitor()
