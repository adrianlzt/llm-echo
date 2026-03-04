from http.server import HTTPServer, BaseHTTPRequestHandler
import json

RESPONSE = {
    "id": "gen-1772625423-GcC93jjWC3cloYtkEAw0",
    "created": 1772625423,
    "model": "openrouter/anthropic/claude-sonnet-4.5",
    "object": "chat.completion",
    "choices": [
        {
            "finish_reason": "tool_calls",
            "index": 0,
            "message": {
                "content": None,
                "role": "assistant",
                "tool_calls": [
                    {
                        "index": 0,
                        "function": {
                            "arguments": '{"command": "get ns"}',
                            "name": "kubectl_impl",
                        },
                        "id": "toolu_vrtx_01WAti72UVeRBHtnm5UEGkZs",
                        "type": "function",
                    }
                ],
            },
            "provider_specific_fields": {"native_finish_reason": "tool_calls"},
        }
    ],
    "usage": {
        "completion_tokens": 54,
        "prompt_tokens": 1156,
        "total_tokens": 1210,
        "completion_tokens_details": {
            "audio_tokens": 0,
            "reasoning_tokens": 0,
            "image_tokens": 0,
        },
        "prompt_tokens_details": {
            "audio_tokens": 0,
            "cached_tokens": 0,
            "cache_write_tokens": 0,
            "video_tokens": 0,
        },
        "cost": 0.004278,
        "is_byok": False,
        "cost_details": {
            "upstream_inference_cost": 0.004278,
            "upstream_inference_prompt_cost": 0.003468,
            "upstream_inference_completions_cost": 0.00081,
        },
    },
    "provider": "Google",
}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        request_data = json.loads(body)

        if request_data.get("stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            chunk = {
                "id": RESPONSE["id"],
                "object": "chat.completion.chunk",
                "created": RESPONSE["created"],
                "model": RESPONSE["model"],
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": RESPONSE["choices"][0]["message"][
                                "tool_calls"
                            ],
                        },
                        "finish_reason": "tool_calls",
                    }
                ],
            }
            self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
        else:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(RESPONSE).encode())

    def do_GET(self):
        self.do_POST()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8088), Handler)
    print("Server running on http://localhost:8088")
    server.serve_forever()
