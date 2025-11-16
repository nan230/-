// 绑定生成按钮点击事件
document.getElementById('generate-btn').addEventListener('click', async () => {
    // 获取DOM元素
    const inputText = document.getElementById('meeting-input').value.trim();
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const downloadLink = document.getElementById('download-link');

    // 输入校验：若为空则提示
    if (!inputText) {
        alert('请输入会议描述内容，例如会议时间、地点、参会者、议题等！');
        return;
    }

    // 显示加载状态，隐藏结果
    loading.style.display = 'inline-block';
    result.style.display = 'none';

    try {
        // 调用后端Flask接口（注意地址与后端一致）
        const response = await fetch('/generate-meeting', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // 传递JSON格式数据
            },
            body: JSON.stringify({ input_text: inputText }), // 发送用户输入的文本
        });

        // 处理后端返回的Word文件流
        if (!response.ok) throw new Error('生成失败，请检查后端服务是否启动');
        const blob = await response.blob(); // 转换为文件流
        const url = window.URL.createObjectURL(blob); // 创建临时下载链接

        // 显示结果，设置下载链接
        downloadLink.href = url;
        loading.style.display = 'none';
        result.style.display = 'block';

    } catch (error) {
        // 异常处理：提示错误并打印日志
        loading.style.display = 'none';
        alert(`操作失败：${error.message}`);
        console.error('错误详情：', error);
    }
});