# Chapter 5: Model Context Protocol (MCP)

## Prerequisites

This chapter uses `uv` for package management, which is significantly faster than traditional tools.

### Installation

You can install `uv` on most systems using a simple command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup

1. **Initialize Project** (if starting fresh):
   ```bash
   uv init
   ```

2. **Add Dependencies**:
   ```bash
   uv add requests feedparser fastmcp dspy
   ```

## Example Scripts in Chapter 5

This chapter introduces the Model Context Protocol (MCP), demonstrating how to connect to MCP servers and build agents.

- [example-1-connect-to-playwright.py](example-1-connect-to-playwright.py): Connecting to a Playwright MCP server.
- [example-2-react-agent-mcp-server.py](example-2-react-agent-mcp-server.py): Building a trivial ReAct agent that uses an MCP server.
- [example-3-fastmcp-server.py](example-3-fastmcp-server.py): Creating a fast MCP server.
- [example-3-fastmcp-client.py](example-3-fastmcp-client.py): Client for the fast MCP server.

## How to Run

To run any example, use `uv run` which handles the virtual environment automatically.

### Running the Playwright Example

First, ensure the Playwright MCP server is running (in a separate terminal):

```bash
npx @playwright/mcp@latest --port 8931
```

Then run the client script:

```bash
uv run example-1-connect-to-playwright.py
```

```bash
$ uv run example-1-connect-to-playwright.py
  - browser_close: Close the page
  - browser_resize: Resize the browser window
  - browser_console_messages: Returns all console messages
  - browser_handle_dialog: Handle a dialog
  - browser_evaluate: Evaluate JavaScript expression on page or element
  - browser_file_upload: Upload one or multiple files
  - browser_fill_form: Fill multiple form fields
  - browser_install: Install the browser specified in the config. Call this if you get an error about the browser not being installed.
  - browser_press_key: Press a key on the keyboard
  - browser_type: Type text into editable element
  - browser_navigate: Navigate to a URL
  - browser_navigate_back: Go back to the previous page
  - browser_network_requests: Returns all network requests since loading the page
  - browser_run_code: Run Playwright code snippet
  - browser_take_screenshot: Take a screenshot of the current page. You can't perform actions based on the screenshot, use browser_snapshot for actions.
  - browser_snapshot: Capture accessibility snapshot of the current page, this is better than screenshot
  - browser_click: Perform click on a web page
  - browser_drag: Perform drag and drop between two elements
  - browser_hover: Hover over element on page
  - browser_select_option: Select an option in a dropdown
  - browser_tabs: List, create, close, or select a browser tab.
  - browser_wait_for: Wait for text to appear or disappear or a specified time to pass
```

```bash
$ uv run example-2-react-agent-mcp-server.py https://dspyweekly.com
[
  {
    "failed_url": "https://pbs.twimg.com/profile_images/1947048150218235904/IFIuHpKr_400x400.jpg",
    "status_code": 404,
    "reason": "URL Not Found"
  }
],
[
  {
    "console_errors": "Failed to load resource: the server responded with a status of 404 () @ https://pbs.twimg.co...",
    "fixes": "The URL for the twitter profile image is broken. The link to the profile image needs to be updated."
  }
]
tool_name_0: browser_navigate
tool_name_1: browser_network_requests
tool_name_2: finish
```

### Running the FastMCP Example

You can run the server and client in separate terminals.

**Server:**
```bash
uv run example-3-fastmcp-server.py
```

```bash
ank@Ankurs-MacBook-Air chapter-05 % uv run example-3-fastmcp-server.py
[11/24/25 23:29:20] WARNING  Using non-secure cookies for development; deploy with    oauth_proxy.py:827
                             HTTPS for production.                                                      


            ╭──────────────────────────────────────────────────────────────────────────────╮            
            │                                                                              │            
            │                         ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█                        │            
            │                         █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀                        │            
            │                                                                              │            
            │                                FastMCP 2.13.1                                │            
            │                                                                              │            
            │                                                                              │            
            │                  🖥  Server name: GitHub Secured App                          │            
            │                                                                              │            
            │                  📦 Transport:   HTTP                                        │            
            │                  🔗 Server URL:  http://127.0.0.1:8000/mcp                   │            
            │                                                                              │            
            │                  📚 Docs:        https://gofastmcp.com                       │            
            │                  🚀 Hosting:     https://fastmcp.cloud                       │            
            │                                                                              │            
            ╰──────────────────────────────────────────────────────────────────────────────╯            


                    INFO     Starting MCP server 'GitHub Secured App' with transport      server.py:2055
                             'http' on http://127.0.0.1:8000/mcp                                        
INFO:     Started server process [32575]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Client:**
```bash
uv run example-3-fastmcp-client.py
```

```bash
ank@Ankurs-MacBook-Air chapter-05 % uv run example-3-fastmcp-client.py

[11/23/25 10:28:57] INFO     OAuth authorization     oauth.py:247
                             URL:                                
                             http://localhost:8000/a             
                             uthorize?response_type=             
                             code&client_id=d9624             
                             -dc81-4580-98a1-cd545ca             
                             5bdd4&redirect_uri=http             
                             %3A%2F%2Flocalhost%3A54             
                             610%2Fcallback&state=Gr             
                             iKlpeY9_8aqunexL_aJ3gcR             
                             S9ocmiWZX7pgrzdbV4&code             
                             _challenge=_wCKLtZqyckX             
                             WTrye98dk5HfsddaD0y3l8             
                             w2XHW6cU&code_challenge             
                             _method=S256&resource=h             
                             ttp%3A%2F%2F127.0.0.1%3             
                             A8000&scope=user                    
                    INFO     🎧 OAuth callback       oauth.py:267
                             server started on                   
                             http://localhost:54610              
Discovered 2 tools: ['get_user_info', 'list_starred_repos']

Calling get_user_info...
[TextContent(type='text', text='{"github_user":"originalankur","name":"Ankur Gupta","email":null}', annotations=None, meta=None)]

Calling list_starred_repos...
[TextContent(type='text', text='[{"name":"davidkimai/Context-Engineering","description":"\\"Context engineering is the delicate art and science of filling the context window with just the right information for the next step.\\" — Andrej Karpathy. A frontier, first-principles handbook inspired by Karpathy and 3Blue1Brown for moving beyond prompt engineering to the wider discipline of context design, orchestration, and optimization.","stars":7751,"language":"Python","url":"https://github.com/davidkimai/Context-Engineering"},{"name":"HuangOwen/Awesome-LLM-Compression","description":"Awesome LLM compression research papers and tools.","stars":1713,"language":null,"url":"https://github.com/HuangOwen/Awesome-LLM-Compression"}]', annotations=None, meta=None)]
----
```