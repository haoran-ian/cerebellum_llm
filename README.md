# Cerebellum Model Examples

This directory contains examples for accessing the `qwen3.8-27b` model on Cerebellum through an SSH tunnel, using either the OpenAI-compatible API directly or the LLaMEA framework.

## 1. Establish an SSH Tunnel

Replace `USERNAME` with your SSH username and run the following command in a separate local terminal:

```bash
ssh -N -T \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -J USERNAME@ssh.liacs.nl \
  -L 127.0.0.1:18000:127.0.0.1:8000 \
  USERNAME@cerebellum
```

This forwards local port `18000` to port `8000` on Cerebellum through the `ssh.liacs.nl` jump host. Keep this terminal open while running the examples.

## 2. Configure Authentication and Check the Service

In another terminal, set the API key provided for the model service:

```bash
export VLLM_API_KEY="your-api-key"
```

For PowerShell, use:

```powershell
$env:VLLM_API_KEY = "your-api-key"
```

### List Available Models

Query the model list through the local tunnel:

```bash
curl -s http://127.0.0.1:18000/v1/models \
  -H "Authorization: Bearer $VLLM_API_KEY" \
  | python -m json.tool
```

Confirm that the response contains a model entry with the following ID:

```json
{
  "id": "qwen3.8-27b"
}
```

The examples use `http://127.0.0.1:18000/v1` as the API base URL.

## 3. Set Up the Python Environment

The commands below create a Python 3.12 environment.

### Install uv

On Linux or macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows, use PowerShell:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Install LLaMEA

Create and activate a virtual environment, then clone and install the
`cerebellum` branch of the project:

```bash
uv venv --python 3.12
source .venv/bin/activate
git clone -b cerebellum https://github.com/haoran-ian/LLaMEA.git
cd LLaMEA && uv pip install . && cd ..
```

The activation command above is for Bash. In PowerShell, activate the
environment with `.venv\Scripts\Activate.ps1` instead.

## 4. Run the Examples

### Direct API Call

[general_example.py](general_example.py) requests NumPy-based differential
evolution code through the OpenAI client. It prints the generated code,
elapsed time, input and output token counts, total tokens, and end-to-end
output throughput. If the server omits usage data, it prints a message
indicating that token usage is unavailable.

```bash
python general_example.py
```

### LLaMEA Integration

[llamea_example.py](llamea_example.py) connects `Cerebellum_LLM` to LLaMEA
to demonstrate algorithm generation and iterative evaluation. It uses
random fitness values for demonstration rather than running the BBOB
benchmark mentioned in its task prompt.

```bash
python llamea_example.py
```

### Thinking Mode

Both examples disable thinking by default. For `Cerebellum_LLM`, control
this behavior at initialization:

```python
llm = Cerebellum_LLM(
    api_key=vllm_api_key,
    enable_thinking=False,
)
```

Set `enable_thinking=True` to enable thinking, or `None` to use the server
default. In `general_example.py`, the equivalent setting is passed via
`extra_body["chat_template_kwargs"]["enable_thinking"]`.
