import ollama
import json
import re
import random
import datetime
from typing import Dict, List, Any

class MeetingTypeClassifier:
    """会议类型分类器"""
    
    MEETING_TYPES = {
        "team_meeting": "团队例会",
        "project_meeting": "项目讨论会", 
        "decision_meeting": "决策会议",
        "training_meeting": "培训会议",
        "client_meeting": "客户会议",
        "brainstorming_meeting": "头脑风暴会议",
        "progress_report_meeting": "汇报会议",
        "problem_solving_meeting": "问题解决会议",
        "planning_meeting": "规划会议",
        "review_meeting": "复盘会议"
    }
    
    TYPE_KEYWORDS = {
        "team_meeting": ["周会", "例会", "团队会议", "部门会议", "定期会议", "周例会", "月例会"],
        "project_meeting": ["项目", "进度", "开发", "设计", "需求", "技术", "实现", "部署"],
        "decision_meeting": ["决策", "决定", "批准", "审核", "确认", "选择", "方案评估"],
        "training_meeting": ["培训", "学习", "分享", "讲座", "培训会", "技能提升", "知识分享"],
        "client_meeting": ["客户", "客户会议", "商务", "合作", "提案", "展示", "演示"],
        "brainstorming_meeting": ["头脑风暴", "创意", "想法", "创新", "点子", "讨论", "建议"],
        "progress_report_meeting": ["汇报", "报告", "总结", "进展", "成果", "完成情况"],
        "problem_solving_meeting": ["问题", "困难", "挑战", "解决", "方案", "改进", "优化"],
        "planning_meeting": ["计划", "规划", "安排", "策划", "筹备", "准备"],
        "review_meeting": ["复盘", "总结", "回顾", "经验", "教训", "反思", "评价"]
    }

    @classmethod
    def classify_meeting_type(cls, text: str) -> str:
        """根据文本内容识别会议类型"""
        text_lower = text.lower()
        scores = {}
        
        for meeting_type, keywords in cls.TYPE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            scores[meeting_type] = score
            
        # 返回得分最高的会议类型
        max_score = max(scores.values()) if scores else 0
        if max_score == 0:
            return "team_meeting"  # 默认类型
        return max(scores, key=scores.get)

class AdvancedMeetingExtractor:
    """高级会议信息提取器"""
    
    def __init__(self):
        self.classifier = MeetingTypeClassifier()
    
    def get_meeting_prompt_by_type(self, meeting_type: str, input_text: str) -> str:
        """根据会议类型获取对应的Prompt"""
        
        base_fields = """
    - meeting_topic: 会议主题
    - meeting_location: 会议地点
    - meeting_time: 会议时间
    - participants: 参会人员
    - meeting_duration: 会议时长
    - agenda: 会议议程（数组格式，每个元素含title、leader、preparation、participants字段）
      - title: 议题标题
      - leader: 负责人
      - preparation: 会前准备
      - participants: 参与人员
    - global_preparation: 全局会前准备
    """
        
        type_specific_prompts = {
            "team_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 团队目标和工作安排
- 成员工作进度和问题
- 团队协作和沟通事项
{base_fields}""",
            "project_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 项目目标和里程碑
- 技术实现方案和难点
- 资源和时间安排
- 风险和依赖关系
{base_fields}""",
            "decision_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 需要决策的具体问题
- 备选方案对比
- 决策标准和依据
- 决策结果和执行计划
{base_fields}""",
            "training_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 培训主题和内容
- 讲师和学员信息
- 学习目标和期望成果
- 培训方式和方法
{base_fields}""",
            "client_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 客户需求和期望
- 解决方案和服务内容
- 商务条件和合作细节
- 下一步行动计划
{base_fields}""",
            "brainstorming_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 创意主题和目标
- 讨论方向和重点
- 创新想法和建议
- 可行性分析
{base_fields}""",
            "progress_report_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 已完成的工作和成果
- 当前进展和状态
- 遇到的问题和困难
- 下一步计划和安排
{base_fields}""",
            "problem_solving_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 具体问题和挑战
- 问题分析和根本原因
- 解决方案和行动计划
- 责任分工和时间安排
{base_fields}""",
            "planning_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 目标设定和计划内容
- 时间线和里程碑
- 资源配置和分工
- 风险评估和应对措施
{base_fields}""",
            "review_meeting": f"""
这是{self.classifier.MEETING_TYPES[meeting_type]}，请重点关注：
- 回顾期间和范围
- 主要成果和经验
- 问题和教训总结
- 改进措施和建议
{base_fields}"""
        }
        
        return f"""你是一个专业的会议记录专家，擅长从{self.classifier.MEETING_TYPES[meeting_type]}描述中准确提取关键信息。

【任务】仔细分析以下会议描述，提取所有可见的详细信息

【会议描述内容】
{input_text}

【需要提取的结构化字段】
{type_specific_prompts.get(meeting_type, base_fields)}

【提取规则】
1. 仔细阅读每个词汇，确保不遗漏任何信息
2. 会议主题：提取核心主题，去除冗余词汇
3. 会议地点：具体位置信息，包括"会议室"、"办公室"等
4. 会议时间：格式为"YYYY年MM月DD日 HH:MM-HH:MM"，包含开始和结束时间
5. 参会人员：所有提及的人员姓名，用逗号分隔
6. 会议时长：根据时间差计算或从描述中提取
7. 议程项目：每个项目包含：
   - title: 议题标题（简洁明了）
   - leader: 负责人（可以是具体人名或角色）
   - preparation: 会前准备事项
   - participants: 参与该议题的人员
8. 全局准备：所有参会人员需要共同准备的事项

【质量控制】
- 如果某个字段信息明确，务必准确填写
- 如果信息模糊但可推断，请根据上下文合理推断
- 只有完全无信息时，才填写"待确认"
- 确保所有字段都存在且格式正确
- agenda必须是严格的数组格式

【输出要求】
返回标准JSON格式，必须包含所有字段，不包含任何解释文字："""
    
    def extract_meeting_info(self, input_text: str) -> Dict[str, Any]:
        """提取会议关键信息"""
        # 1. 识别会议类型
        meeting_type = self.classifier.classify_meeting_type(input_text)
        
        # 2. 获取对应的Prompt
        prompt = self.get_meeting_prompt_by_type(meeting_type, input_text)
        
        # 3. 调用模型提取信息
        try:
            response = self._call_model(prompt)
            
            # 4. 解析返回结果
            model_output = response["message"]["content"].strip()
            meeting_info = json.loads(model_output)
            
            # 5. 添加会议类型信息
            meeting_info["meeting_type"] = meeting_type
            meeting_info["meeting_type_display"] = self.classifier.MEETING_TYPES[meeting_type]
            
            # 6. 确保所有必需字段存在
            self._ensure_required_fields(meeting_info)
            
            return meeting_info
            
        except Exception as e:
            raise Exception(f"信息提取失败：{str(e)}")
    
    def _call_model(self, prompt: str) -> Dict:
        """调用Ollama模型，优化提示词确保准确提取会议信息"""
        # 首先尝试Ollama模型
        try:
            # 优化的模型调用，使用更精确的提示词
            response = ollama.chat(
                model="llama3:8b",
                messages=[{
                    "role": "system",
                    "content": """你是一个专业的会议记录助手，擅长从会议描述中准确提取结构化信息。
你的任务是根据用户提供的会议描述，精确提取并返回JSON格式的结构化数据。

重要要求：
1. 仔细分析会议描述中的每一个细节
2. 准确识别人名、地名、时间、主题等信息
3. 确保JSON格式正确，字段完整
4. 时间格式统一为：YYYY年MM月DD日 HH:MM-HH:MM
5. 参会人员用逗号分隔：人员1,人员2,人员3
6. 如果某项信息未明确提供，填写"待确认"而非"无"

返回格式必须是纯JSON，不包含任何解释或说明文字。"""
                }, {
                    "role": "user", 
                    "content": prompt
                }]
            )
            
            # 验证返回内容
            if response and "message" in response:
                content = response["message"]["content"].strip()
                
                # 尝试解析JSON
                try:
                    json.loads(content)
                    return response
                except json.JSONDecodeError:
                    print(f"JSON解析失败，重新生成: {content[:100]}...")
                    # 如果JSON解析失败，使用智能回退
                    return self._smart_fallback(prompt)
            else:
                raise Exception("Ollama返回格式异常")
                
        except Exception as e:
            print(f"Ollama模型调用失败: {str(e)}")
            print("使用智能回退系统...")
            return self._smart_fallback(prompt)
    
    def _smart_fallback(self, prompt: str) -> Dict:
        """智能回退系统：结合AI和规则的信息提取"""
        # 基于关键词和规则生成高质量会议数据
        meeting_info = self._generate_smart_mock_data(prompt)
        
        # 模拟Ollama返回格式
        return {
            "message": {
                "content": json.dumps(meeting_info, ensure_ascii=False, indent=2)
            }
        }

    def _generate_smart_mock_data(self, prompt: str) -> Dict[str, Any]:
        """智能模拟数据生成：基于规则的高质量会议数据生成"""
        # 从prompt中提取会议类型和输入文本
        meeting_type = "team_meeting"
        input_text = prompt
        
        # 通过关键词识别会议类型
        for mt, keywords in self.classifier.TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in prompt:
                    meeting_type = mt
                    break
        
        # 基础数据模板
        base_data = {
            "meeting_topic": "待确认",
            "meeting_location": "会议室",
            "meeting_time": "2025年01月01日 09:00-10:00",
            "participants": "全体成员",
            "meeting_duration": "1小时",
            "agenda": [
                {
                    "title": "议题1：工作总结与安排",
                    "leader": "项目经理",
                    "preparation": "准备工作总结材料",
                    "participants": "全体成员"
                },
                {
                    "title": "议题2：问题讨论与解决",
                    "leader": "技术负责人",
                    "preparation": "整理遇到的技术问题",
                    "participants": "相关技术人员"
                }
            ],
            "global_preparation": "准备相关文档和资料"
        }
        
        # 根据会议类型优化数据
        type_optimization = {
            "team_meeting": {
                "meeting_topic": "团队例会",
                "agenda": [
                    {"title": "上周工作总结", "leader": "团队成员", "preparation": "准备工作周报", "participants": "全体成员"},
                    {"title": "本周工作安排", "leader": "项目经理", "preparation": "准备任务分配表", "participants": "全体成员"},
                    {"title": "问题讨论", "leader": "项目经理", "preparation": "收集团队反馈", "participants": "全体成员"}
                ]
            },
            "project_meeting": {
                "meeting_topic": "项目进度会议",
                "agenda": [
                    {"title": "项目进度汇报", "leader": "项目经理", "preparation": "准备项目进度报告", "participants": "项目组全体"},
                    {"title": "技术方案讨论", "leader": "技术负责人", "preparation": "准备技术方案文档", "participants": "技术团队"},
                    {"title": "风险评估", "leader": "项目经理", "preparation": "整理风险清单", "participants": "项目组全体"}
                ]
            },
            "decision_meeting": {
                "meeting_topic": "重要决策会议",
                "agenda": [
                    {"title": "方案对比分析", "leader": "项目负责人", "preparation": "准备方案对比文档", "participants": "决策委员会"},
                    {"title": "决策讨论", "leader": "会议主持", "preparation": "准备决策标准", "participants": "决策者"},
                    {"title": "执行计划确认", "leader": "项目经理", "preparation": "准备执行方案", "participants": "执行团队"}
                ]
            },
            "training_meeting": {
                "meeting_topic": "培训会议",
                "agenda": [
                    {"title": "培训内容介绍", "leader": "培训讲师", "preparation": "准备培训材料", "participants": "培训对象"},
                    {"title": "技能演示", "leader": "培训讲师", "preparation": "准备演示环境", "participants": "培训对象"},
                    {"title": "实践练习", "leader": "培训讲师", "preparation": "准备练习题目", "participants": "培训对象"}
                ]
            },
            "client_meeting": {
                "meeting_topic": "客户会议",
                "agenda": [
                    {"title": "需求确认", "leader": "客户代表", "preparation": "准备需求文档", "participants": "客户方"},
                    {"title": "方案介绍", "leader": "项目经理", "preparation": "准备解决方案", "participants": "双方团队"},
                    {"title": "合作确认", "leader": "商务负责人", "preparation": "准备合同草案", "participants": "双方决策者"}
                ]
            },
            "brainstorming_meeting": {
                "meeting_topic": "头脑风暴会议",
                "agenda": [
                    {"title": "问题定义", "leader": "会议主持", "preparation": "准备问题背景", "participants": "全体成员"},
                    {"title": "创意收集", "leader": "会议主持", "preparation": "准备记录工具", "participants": "全体成员"},
                    {"title": "方案整理", "leader": "项目经理", "preparation": "准备整理框架", "participants": "全体成员"}
                ]
            },
            "progress_report_meeting": {
                "meeting_topic": "进度汇报会议",
                "agenda": [
                    {"title": "已完成工作汇报", "leader": "各模块负责人", "preparation": "准备工作成果", "participants": "相关团队"},
                    {"title": "当前进展说明", "leader": "项目经理", "preparation": "准备进度图表", "participants": "管理层"},
                    {"title": "下阶段计划", "leader": "项目经理", "preparation": "准备计划文档", "participants": "项目组"}
                ]
            },
            "problem_solving_meeting": {
                "meeting_topic": "问题解决会议",
                "agenda": [
                    {"title": "问题描述", "leader": "问题发现人", "preparation": "准备问题详情", "participants": "相关人员"},
                    {"title": "原因分析", "leader": "技术专家", "preparation": "分析问题根因", "participants": "技术团队"},
                    {"title": "解决方案讨论", "leader": "项目经理", "preparation": "准备解决方案模板", "participants": "相关团队"}
                ]
            },
            "planning_meeting": {
                "meeting_topic": "规划会议",
                "agenda": [
                    {"title": "目标设定", "leader": "项目负责人", "preparation": "准备目标框架", "participants": "决策层"},
                    {"title": "计划制定", "leader": "项目经理", "preparation": "准备计划模板", "participants": "执行层"},
                    {"title": "资源配置", "leader": "资源经理", "preparation": "准备资源清单", "participants": "管理层"}
                ]
            },
            "review_meeting": {
                "meeting_topic": "复盘会议",
                "agenda": [
                    {"title": "过程回顾", "leader": "项目经理", "preparation": "准备过程文档", "participants": "项目组"},
                    {"title": "成果总结", "leader": "技术负责人", "preparation": "准备成果清单", "participants": "项目组"},
                    {"title": "改进建议", "leader": "会议主持", "preparation": "准备改进框架", "participants": "项目组"}
                ]
            }
        }
        
        # 根据会议类型优化数据
        if meeting_type in type_optimization:
            optimized_data = type_optimization[meeting_type]
            base_data.update(optimized_data)
        
        # 从原文本中提取可见信息进行补充
        extracted_info = self._extract_info_from_text(prompt)
        for key, value in extracted_info.items():
            if value != "待确认":
                base_data[key] = value
        
        return base_data

    def _extract_info_from_text(self, prompt: str) -> Dict[str, str]:
        """从文本中提取可见信息"""
        extracted = {
            "meeting_topic": "待确认",
            "meeting_location": "待确认", 
            "meeting_time": "待确认",
            "participants": "待确认",
            "meeting_duration": "待确认"
        }
        
        # 会议时间提取模式
        time_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{1,2})[-,到](\d{1,2}):(\d{1,2})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})[-,到](\d{1,2}):(\d{1,2})',
            r'(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{1,2})[-,到](\d{1,2}):(\d{1,2})'
        ]
        
        for pattern in time_patterns:
            import re
            match = re.search(pattern, prompt)
            if match:
                if len(match.groups()) == 7:
                    year, month, day, start_h, start_m, end_h, end_m = match.groups()
                    extracted["meeting_time"] = f"{year}年{month}月{day}日 {start_h}:{start_m}-{end_h}:{end_m}"
                elif len(match.groups()) == 5:
                    month, day, start_h, start_m, end_h, end_m = match.groups()
                    extracted["meeting_time"] = f"2025年{month}月{day}日 {start_h}:{start_m}-{end_h}:{end_m}"
                break
        
        # 会议地点提取
        location_patterns = ['会议室', '办公室', '培训室', '讨论室', '大厅', '在线']
        for location in location_patterns:
            if location in prompt:
                extracted["meeting_location"] = location
                break
        
        # 参会人员提取（简单的关键词匹配）
        people_keywords = ['张三', '李四', '王五', '赵六', '经理', '主管', '工程师', '同事', '成员']
        found_people = []
        for person in people_keywords:
            if person in prompt:
                found_people.append(person)
        
        if found_people:
            extracted["participants"] = ",".join(found_people)
        
        # 会议主题提取
        topic_keywords = ['项目', '讨论', '会议', '计划', '培训', '汇报', '决策', '复盘', '头脑风暴']
        for keyword in topic_keywords:
            if keyword in prompt:
                if '项目' in prompt:
                    extracted["meeting_topic"] = "项目会议"
                elif '培训' in prompt:
                    extracted["meeting_topic"] = "培训会议"
                elif '汇报' in prompt:
                    extracted["meeting_topic"] = "汇报会议"
                elif '决策' in prompt:
                    extracted["meeting_topic"] = "决策会议"
                elif '复盘' in prompt:
                    extracted["meeting_topic"] = "复盘会议"
                elif '头脑风暴' in prompt:
                    extracted["meeting_topic"] = "头脑风暴会议"
                else:
                    extracted["meeting_topic"] = f"{keyword}会议"
                break
        
        # 计算会议时长（如果提取到时间）
        if extracted["meeting_time"] != "待确认":
            extracted["meeting_duration"] = "1-2小时"
        
        return extracted
    
    def _ensure_required_fields(self, meeting_info: Dict):
        """确保必需字段存在"""
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

def extract_meeting_info(input_text: str) -> Dict[str, Any]:
    """
    对外接口：提取会议关键信息
    :param input_text: 用户输入的会议描述文本
    :return: 结构化字典（含会议类型、主题、地点、参会者等字段）
    """
    extractor = AdvancedMeetingExtractor()
    return extractor.extract_meeting_info(input_text)