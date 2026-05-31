"""
EmailPlugin - 邮件发送插件
基于 smtplib，支持 SMTP 邮件发送
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List
from ..interfaces.IPlugin import IPlugin, PluginType


class EmailPlugin(IPlugin):
    """
    邮件发送插件
    功能: 发送邮件、HTML邮件、带附件邮件
    """

    @property
    def name(self) -> str:
        return "email_sender"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def plugin_type(self) -> PluginType:
        return PluginType.NOTIFICATION

    @property
    def description(self) -> str:
        return "邮件发送插件，支持SMTP发送文本/HTML邮件"

    @property
    def dependencies(self) -> List[str]:
        return []

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        self.config = config or {}
        self.smtp_server = self.config.get("smtp_server", "")
        self.smtp_port = self.config.get("smtp_port", 587)
        self.username = self.config.get("username", "")
        self.password = self.config.get("password", "")
        return True

    def execute(self, task_params: Dict[str, Any]) -> Dict[str, Any]:
        action = task_params.get("action", "send")

        if action == "send":
            return self._send_email(task_params)
        else:
            return {"error": f"不支持的操作: {action}"}

    def _send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """发送邮件"""
        to = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")
        html = params.get("html", False)

        if not all([to, subject, body]):
            return {"error": "收件人、主题、内容不能为空"}

        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to
            msg['Subject'] = subject

            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type, 'utf-8'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            return {"success": True, "to": to, "subject": subject}

        except Exception as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        return bool(self.smtp_server and self.username)

    def shutdown(self) -> bool:
        return True
