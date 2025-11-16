from flask import Flask, request, send_file
from flask_cors import CORS  # 解决前端跨域问题
import os
from model_client import extract_meeting_info
from word_generator import generate_meeting_word

# 初始化Flask应用
app = Flask(__name__, static_folder='../frontend', static_url_path='')
# 允许跨域：开发环境下允许所有来源（生产环境需限制为前端地址）
CORS(app, resources=r"/*")

# 设置静态文件目录
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# 根路径返回前端页面
@app.route('/')
def index():
    return app.send_static_file('index.html')

# 定义接口：接收前端POST请求，生成会议记录Word
@app.route('/generate-meeting', methods=['POST'])
def generate_meeting():
    try:
        # 1. 获取前端传递的JSON数据
        request_data = request.get_json()
        input_text = request_data.get("input_text")
        if not input_text:
            return {"error": "请传递会议描述文本"}, 400  # 400：请求参数错误

        # 2. 调用模型提取会议关键信息
        meeting_info = extract_meeting_info(input_text)

        # 3. 生成Word文档
        word_path = generate_meeting_word(meeting_info)

        # 4. 返回Word文件给前端（作为附件下载）
        return send_file(
            word_path,
            as_attachment=True,  # 强制下载
            download_name="会议记录.docx",  # 前端下载的文件名
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # Word文件MIME类型
        )

    except Exception as e:
        # 异常处理：返回错误信息与500状态码（服务器内部错误）
        return {"error": str(e)}, 500

# 启动服务（仅开发环境使用debug模式）
if __name__ == "__main__":
    # 确保临时目录存在
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    # 启动服务：地址127.0.0.1，端口5000（需与前端script.js中的地址一致）
    app.run(host="127.0.0.1", port=5000, debug=True)