# Performance Optimization Guide

Tips and configurations for optimizing your Auto-Rename Bot for better performance and resource usage.

## 📊 Resource Management

### Memory Optimization

#### 1. Adjust Worker Count
Edit `bot.py` to reduce workers for free hosting:

```python
# For free tier hosting (512MB RAM)
workers=50  # Instead of 200

# For medium hosting (1GB RAM)
workers=100

# For production (2GB+ RAM)
workers=200
```

#### 2. Reduce Queue Size
Edit `helper/file_queue.py`:

```python
# For free tier
file_queue = FileProcessingQueue(max_concurrent=2)

# For medium hosting
file_queue = FileProcessingQueue(max_concurrent=5)

# For production
file_queue = FileProcessingQueue(max_concurrent=10)
```

### CPU Optimization

#### 1. Optimize Sleep Threshold
In `bot.py`:

```python
# Increase for lower CPU usage
sleep_threshold=30  # Default is 15

# This adds small delays but reduces CPU load
```

#### 2. Rate Limiting
Adjust rate limits in `helper/rate_limit.py` based on your server capacity:

```python
# Stricter limits for free tier
rename_limiter = RateLimiter(rate=5, per=60)  # 5 per minute
command_limiter = RateLimiter(rate=3, per=10)  # 3 per 10 seconds
```

---

## 🗄️ Database Optimization

### Indexing
Run the setup script after deployment:

```bash
python3 setup_database.py
```

This creates indexes for:
- User queries
- Verification lookups
- Premium user checks
- Force subscribe channels

### Connection Pooling
MongoDB Atlas automatically handles connection pooling, but ensure you're using:
- Maximum pool size: 50 (default is usually enough)
- Minimum pool size: 10

### Query Optimization
The bot uses caching for frequent queries:
- User data: 5 minutes
- Admin list: 10 minutes
- Channel list: 10 minutes
- Verification: 3 minutes

Adjust in `helper/cache.py` if needed.

---

## 🚀 Deployment Optimization

### Docker Optimization

#### Reduce Image Size
In `Dockerfile`:

```dockerfile
# Use slim Python image
FROM python:3.10-slim

# Clean up after installation
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
```

#### Multi-stage Build (Advanced)
```dockerfile
# Builder stage
FROM python:3.10 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "bot.py"]
```

### Railway.app Optimization
- Enable "Auto-scale to zero" for cost savings
- Set memory limit: 512MB for free tier
- Enable health checks

### Render.com Optimization
- Use "Free" instance type
- Enable auto-deploy from GitHub
- Set health check path: `/health`

---

## ⚡ Code Optimization

### Async Operations
Ensure all I/O operations are async:

```python
# Good ✅
async def process_file(file):
    await bot.download_media(file)
    await db.update_user(user_id)

# Bad ❌ (blocks event loop)
def process_file(file):
    bot.download_media(file)  # Synchronous
    db.update_user(user_id)   # Synchronous
```

### Concurrent Processing
Use file queue for concurrent operations:

```python
from helper.file_queue import file_queue

async def rename_file(user_id, file):
    await file_queue.process(
        user_id=user_id,
        task_func=do_rename,
        file=file
    )
```

---

## 🧹 Maintenance

### Regular Cleanup
Run maintenance script weekly:

```bash
python3 maintenance.py
```

This cleans:
- Expired premium users
- Old rate limiter entries
- Expired cache data

### Log Rotation
Logs automatically rotate:
- Max size: 10MB per file
- Keep 5 backup files
- Separate error logs

Manually clean old logs:
```bash
find logs/ -name "*.log.*" -mtime +30 -delete
```

---

## 📈 Monitoring

### Health Checks
Use built-in endpoints:

```bash
# Basic status
curl http://your-bot-url/

# Detailed health check
curl http://your-bot-url/health

# Simple ping
curl http://your-bot-url/ping
```

### System Monitoring
Add to your bot:

```python
from helper.system_monitor import system_monitor

# Get stats
stats = system_monitor.get_all_stats()
print(f"CPU: {stats['cpu_percent']}%")
print(f"Memory: {stats['memory']['percent']}%")
print(f"Uptime: {stats['uptime_string']}")
```

---

## 🎯 Best Practices

### 1. Environment-Specific Configuration

Create different configs for different environments:

```python
# config.py
import os

ENV = os.getenv("ENVIRONMENT", "production")

if ENV == "development":
    WORKERS = 50
    MAX_CONCURRENT = 2
    LOG_LEVEL = "DEBUG"
elif ENV == "production":
    WORKERS = 200
    MAX_CONCURRENT = 5
    LOG_LEVEL = "INFO"
```

### 2. Graceful Degradation

Handle errors gracefully:

```python
try:
    # Try premium feature
    await process_with_watermark(file)
except Exception as e:
    # Fallback to basic processing
    logger.warning(f"Watermark failed, using basic: {e}")
    await process_basic(file)
```

### 3. Resource Limits

Set timeouts for long operations:

```python
async def process_file(file):
    try:
        async with asyncio.timeout(300):  # 5 minutes max
            await do_heavy_processing(file)
    except asyncio.TimeoutError:
        logger.error("Processing timeout")
        # Handle timeout
```

---

## 💾 Storage Optimization

### Temporary Files
Clean up temp files immediately:

```python
import os

try:
    # Process file
    result = await process(temp_file)
finally:
    # Always clean up
    if os.path.exists(temp_file):
        os.remove(temp_file)
```

### Use Streaming
For large files, use streaming instead of loading into memory:

```python
# Stream download
async for chunk in bot.download_media(file, in_memory=False):
    # Process chunk by chunk
    await process_chunk(chunk)
```

---

## 🔍 Debugging Performance

### Profiling
Add timing to critical functions:

```python
import time

async def rename_file(file):
    start = time.time()
    
    # Your code here
    result = await process(file)
    
    duration = time.time() - start
    logger.info(f"Rename took {duration:.2f}s")
    
    return result
```

### Memory Profiling
```python
import psutil
import os

process = psutil.Process(os.getpid())

# Before
mem_before = process.memory_info().rss / 1024 / 1024

# Your operation
await heavy_operation()

# After
mem_after = process.memory_info().rss / 1024 / 1024
logger.info(f"Memory used: {mem_after - mem_before:.2f}MB")
```

---

## ⚙️ Platform-Specific Tips

### Railway.app
- Enable health checks: `/health`
- Set restart policy: "ON_FAILURE"
- Memory limit: 512MB - 1GB

### Render.com
- Use Web Service (not background worker)
- Enable auto-deploy
- Health check path: `/health`

### Koyeb
- Use nano instance for free tier
- Enable auto-scaling
- Set health check interval: 60s

### Heroku
- Use worker dyno type
- Enable log drains
- Set dyno size: "basic" or "standard-1x"

---

## 🎓 Performance Checklist

- [ ] Database indexes created (`setup_database.py`)
- [ ] Appropriate worker count for your server
- [ ] Rate limiting configured
- [ ] Caching enabled and tuned
- [ ] File queue max_concurrent set
- [ ] Log rotation configured
- [ ] Health checks enabled
- [ ] Temporary file cleanup implemented
- [ ] Graceful shutdown handlers
- [ ] Monitoring endpoints accessible
- [ ] Regular maintenance scheduled

---

## 📞 Need Help?

If you're experiencing performance issues:
1. Check logs for errors
2. Monitor resource usage
3. Review rate limits
4. Check database indexes
5. Verify health endpoints

**Remember**: Free hosting has limitations. Upgrade to paid tier if needed for better performance!
