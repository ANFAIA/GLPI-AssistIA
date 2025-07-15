Of course. Here is the Markdown text explaining how to mount an MCP server on a FastAPI application, based on the provided documentation.

***

# Mounting an MCP Server on FastAPI

You can integrate a `gofast-mcp` server directly into a FastAPI application by mounting it as a sub-application. This powerful feature allows you to run both your primary web API and your MCP administrative server within a single, unified application process.

The mounting is done using FastAPI's standard `app.mount()` method, which is designed to combine multiple ASGI-compatible applications.

## The Benefits of Mounting

Mounting your MCP server provides several key advantages:

*   **Unified Application:** Consolidate your services into a single deployable application. You don't need to manage, run, and monitor two separate server processes.
*   **Simplified Deployment:** A single application is easier to containerize, deploy, and scale.
*   **Dedicated Path for Admin Tasks:** You can isolate your administrative endpoints to a specific path (e.g., `/mcp`). This is perfect for exposing internal tools like:
    *   Health checks
    *   Metrics endpoints
    *   Configuration reloads
    *   Other operational tasks
*   **Clean API Separation:** By keeping administrative tasks on a separate path, your main API remains clean and focused solely on its primary business logic.

## How to Mount the MCP Server

The process is straightforward. You create an instance of your `FastAPI` app and your `MCP` server, and then use `app.mount()` to attach the MCP server to a specific path prefix.

### Example Implementation

Here is a complete code example demonstrating how to mount an MCP server at the `/mcp` path.

```python
from fastapi import FastAPI
from mcp import MCP, mcp_route

# 1. Define your MCP routes as you normally would.
#    These are the endpoints that will be part of the MCP server.
@mcp_route()
def health_check():
    """A simple health check endpoint for the MCP server."""
    return {"status": "ok"}

# 2. Create an instance of your MCP server.
#    This object gathers all functions decorated with @mcp_route.
mcp_server = MCP()

# 3. Create an instance of your main FastAPI application.
app = FastAPI()

# 4. Mount the MCP server onto a specific path in your FastAPI app.
#    The first argument is the path prefix where the MCP server will live.
#    The second argument is the MCP application instance.
app.mount("/mcp", mcp_server)

# You can still define your regular FastAPI routes on the main app.
# These will be served separately from the MCP routes.
@app.get("/")
def read_root():
    return {"message": "This is the main FastAPI application"}

```

### How It Works

1.  **Define MCP Routes:** You create functions and decorate them with `@mcp_route()` to register them with the MCP framework.
2.  **Instantiate MCP:** `mcp_server = MCP()` creates an ASGI-compatible application that contains all your registered MCP routes.
3.  **Instantiate FastAPI:** `app = FastAPI()` creates your main web application.
4.  **Mount:** `app.mount("/mcp", mcp_server)` tells FastAPI: "Any request that comes in with a path starting with `/mcp` should be forwarded to and handled by the `mcp_server` application."

### Result

When you run this application, you will have two sets of endpoints available:

*   **Main API Endpoint:** Accessible at `http://127.0.0.1:8000/`
    ```json
    {
      "message": "This is the main FastAPI application"
    }
    ```
*   **MCP Endpoint:** Accessible at `http://127.0.0.1:8000/mcp/health_check`
    ```json
    {
      "status": "ok"
    }
    ```

This elegant approach allows you to leverage the strengths of both FastAPI for building robust APIs and `gofast-mcp` for simple, powerful administrative command endpoints.
