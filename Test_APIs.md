host means
127.0.0.1 / localhost

Loopback address, means “this computer itself”.

Only your own machine can connect, so it’s safe for local dev.

In browser you can directly use: http://127.0.0.1:8000 or http://localhost:8000.

0.0.0.0

Special wildcard address: “listen on all network interfaces on this machine”.

Used only on the server side (bind/listen), not as a destination to visit in a browser.

This allows:

You (same PC) to connect via 127.0.0.1 / localhost.

Other devices on same network to connect via your PC’s LAN IP (e.g. 192.168.x.x).

So when you run:

bash
uvicorn main_2:app --host 0.0.0.0 --port 8000
it means: “Start the server and listen on every IP of this machine on port 8000,” and Uvicorn prints that as Uvicorn running on http://0.0.0.0:8000.

Why the log shows 0.0.0.0:8000
Uvicorn just echoes the bind address you gave via --host.
​

0.0.0.0 here is a signal to you: “this server is accessible from any interface” (loopback, LAN, etc.), not a real remote address.

Many frameworks (Node dev servers, Jekyll, etc.) do the same: they show 0.0.0.0 to indicate “open to all interfaces”.

Why you should not use http://0.0.0.0:8000 in browser
In IPv4, 0.0.0.0 is non‑routable as a destination; it means “no particular address”, so browsers treat it as invalid and show errors like ERR_ADDRESS_INVALID.

StackOverflow explicitly notes that 0.0.0.0 “isn't technically allowed as a destination address,” while localhost/127.0.0.1 are for outgoing client connections.

So the rule:

Server side (your uvicorn command):

--host 127.0.0.1 → only your machine can access.

--host 0.0.0.0 → any device that can reach your machine can access (useful for testing on phone / other PC).

Client side (browser / Postman):

On same PC: http://127.0.0.1:8000 or http://localhost:8000.

From other device on LAN: http://<your-PC-LAN-IP>:8000 (e.g. http://192.168.1.5:8000).

Never use http://0.0.0.0:8000.

#######################################################################################
Test  API
Open  browser and visit:

Root endpoint: http://127.0.0.1:8000/

Should show welcome message

Health endpoint: http://127.0.0.1:8000/health

Should show health status

Interactive docs: http://127.0.0.1:8000/docs

This is FastAPI's superpower! Auto-generated, interactive API documentation

You can test endpoints directly from browser

Based on OpenAPI (Swagger) standard

Alternative docs: http://127.0.0.1:8000/redoc

Another doc style, cleaner for reading