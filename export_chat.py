import json
import os
import sys

log_path = r'C:\Users\shour\.gemini\antigravity-ide\brain\5f175ed0-80d2-4c09-a969-5b31e81cc5c6\.system_generated\logs\transcript.jsonl'
output_path = r'd:\Programming\Python\Global AI opportunity Tracker\global-ai-opportunity-tracker-backend\Agent_Chat_Export.md'

try:
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write('# Antigravity Agent Chat Export\n\n')
        for line in lines:
            data = json.loads(line)
            source = data.get('source')
            msg_type = data.get('type')
            content = data.get('content')
            
            if source == 'USER_EXPLICIT' and msg_type == 'USER_INPUT':
                out.write('### 🧑 User\n\n')
                out.write(content.strip() + '\n\n---\n\n')
            elif source == 'MODEL' and msg_type == 'PLANNER_RESPONSE':
                if content and content.strip():
                    out.write('### 🤖 Antigravity Agent\n\n')
                    out.write(content.strip() + '\n\n---\n\n')
    print('Export successful!')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
