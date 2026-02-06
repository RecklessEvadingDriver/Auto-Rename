from aiohttp import web
import time

# Store bot start time for health checks
start_time = time.time()

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Root endpoint - Basic bot status"""
    return web.json_response({
        "status": "running",
        "bot": "Auto-Rename Bot",
        "version": "2.0"
    })

@routes.get("/health", allow_head=True)
async def health_check_handler(request):
    """Health check endpoint for monitoring services"""
    uptime = time.time() - start_time
    return web.json_response({
        "status": "healthy",
        "uptime_seconds": int(uptime),
        "timestamp": time.time()
    })

@routes.get("/ping", allow_head=True)
async def ping_handler(request):
    """Simple ping endpoint"""
    return web.Response(text="pong")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
