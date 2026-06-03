import threading
from signal_bridge import _ReportBridge


# ---------- 千问大模型分析器 ----------
class QwenAnalyzer:
    def __init__(self, api_key=""):
        self.api_key = api_key
        self.api_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        self._bridge = _ReportBridge()

    def analyze(self, prompt, callback=None):
        if not self.api_key:
            if callback:
                callback("错误：请先设置千问 API Key")
            return
        threading.Thread(target=self._call_api, args=(prompt, callback), daemon=True).start()

    def _call_api(self, prompt, callback):
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "qwen-plus",
                "messages": [
                    {"role": "system", "content": "你是一个专业的智能视觉分析助手，擅长分析目标检测数据并生成专业报告。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            resp = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                answer = data['choices'][0]['message']['content']
                if callback:
                    callback(answer)
            else:
                if callback:
                    callback(f"API 请求失败 (HTTP {resp.status_code}): {resp.text}")
        except Exception as e:
            if callback:
                callback(f"千问 API 调用失败: {str(e)}")
