import pymsteams
from config.config import web_hook

teams_message = pymsteams.connectorcard(web_hook)
with open("reports/markdown/report.md") as f:
    report = f.read()
print(report)
teams_message.text(report)
teams_message.send()
