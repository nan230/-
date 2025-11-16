import ollama
import json

def extract_meeting_info(input_text):
    """
    调用Ollama模型提取会议关键信息
    :param input_text: 用户输入的会议描述文本
    :return: 结构化字典（含会议主题、地点、参会者等字段）
    """
    # 设计Prompt：引导模型按JSON格式输出，确保字段与Word模板匹配
    prompt = f"""
    请从以下会议描述中提取关键信息，严格按照JSON格式返回，字段必须包含：
    - meeting_topic: 会议主题（如“下季度产品推广方案”）
    - meeting_location: 会议地点（如“公司三楼大会议室”）
    - meeting_time: 会议时间（如“下周三下午三点”，无则填“无”）
    - participants: 参会人员（用逗号分隔，如“李明、张娜、王磊”）
    - meeting_duration: 会议时长（如“约两小时”，无则填“无”）
    - agenda: 会议议程（数组格式，每个元素含title、leader、preparation、participants字段，无则填空数组）
      - title: 议题标题（如“讨论下季度产品推广方案”）
      - leader: 负责人（如“李明”）
      - preparation: 会前准备（如“准备相关数据”，无则填“无”）
      - participants: 参与人员（如“全体参会者（赵晓雨参与讨论）”，无则填“无”）
    - global_preparation: 全局会前准备（如“提前将会议资料发到群里”，无则填“无”）
    
    会议描述：{input_text}
    
    注意事项：
    1. 若某字段无信息，必须填“无”，不可省略字段；
    2. 议程需提取所有讨论事项，不可遗漏；
    3. 仅返回JSON字符串，不额外添加任何文字（如“好的”“以下是结果”等）；
    4. 确保JSON格式正确（无语法错误，引号用双引号）。
    """

    try:
        # 检查可用的模型并选择合适的模型
        try:
            # 首先尝试使用 llama3 系列模型
            response = ollama.chat(
                model="llama3:8b",
                messages=[{"role": "user", "content": prompt}]
            )
        except:
            try:
                # 如果没有 llama3:8b，尝试使用 phi3
                response = ollama.chat(
                    model="phi3:mini",
                    messages=[{"role": "user", "content": prompt}]
                )
            except:
                # 如果都没有，尝试默认模型
                response = ollama.chat(
                    model="llama3",
                    messages=[{"role": "user", "content": prompt}]
                )

        # 解析模型返回的JSON字符串
        model_output = response["message"]["content"].strip()
        meeting_info = json.loads(model_output)

        # 补充默认值：若模型漏填字段，手动设为“无”
        required_fields = [
            "meeting_topic", "meeting_location", "meeting_time", 
            "participants", "meeting_duration", "agenda", "global_preparation"
        ]
        for field in required_fields:
            if field not in meeting_info:
                meeting_info[field] = "无"
            # 特殊处理agenda：若为非数组，转为空数组
            if field == "agenda" and not isinstance(meeting_info[field], list):
                meeting_info[field] = []

        return meeting_info

    except json.JSONDecodeError:
        raise Exception("模型返回格式错误，无法解析为JSON")
    except ollama.APIError as e:
        raise Exception(f"模型调用失败：{str(e)}（请检查Ollama服务是否启动）")
    except Exception as e:
        raise Exception(f"信息提取失败：{str(e)}")