"""
MCP Client (Lab 5)
Discovers capabilities from the MCP server and calls them.
Does NOT hard-code capability names — discovers them from the manifest.
"""
from app.mcp.server import MCPServer


class MCPClient:
    """
    MCP Client that discovers capabilities from the server manifest
    before making calls.
    """

    def __init__(self, server: MCPServer = None):
        self._server = server or MCPServer()
        self._capabilities = None

    def discover(self) -> dict:
        """
        Discover capabilities from the MCP server.
        Returns the full capabilities manifest.
        """
        self._capabilities = self._server.discover()
        return self._capabilities

    def list_capabilities(self) -> list:
        """List names of available capabilities."""
        if not self._capabilities:
            self.discover()
        return [c["name"] for c in self._capabilities.get("capabilities", [])]

    def find_capability(self, name: str) -> dict:
        """Find a specific capability by name from discovered manifest."""
        if not self._capabilities:
            self.discover()
        for cap in self._capabilities.get("capabilities", []):
            if cap["name"] == name:
                return cap
        return None

    def call(self, capability_name: str, caller: str, inputs: dict) -> dict:
        """
        Call a capability via the MCP server.

        First checks that the capability exists in the discovered manifest,
        then delegates to the server.
        """
        # Ensure discovery has happened
        if not self._capabilities:
            self.discover()

        # Check capability exists in manifest
        cap = self.find_capability(capability_name)
        if not cap:
            available = self.list_capabilities()
            return {
                "status": "rejected",
                "error": f"Capability '{capability_name}' not found in manifest. Available: {available}"
            }

        # Delegate to server
        return self._server.call(capability_name, caller, inputs)
