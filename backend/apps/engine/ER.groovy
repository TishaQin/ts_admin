import graphviz



if __name__ == "__main__":

    # 定义测试平台模型关系图
    dot = graphviz.Digraph(comment='测试平台模型关系图', format='png')
    dot.attr(rankdir='LR', size='20,10')

    # 实体节点（简化名称显示）
    models = {
        "Project": "项目",
        "Environment": "环境",
        "Database": "数据库",
        "TestInterface": "单接口",
        "TestSuite": "测试套件",
        "TestCase": "测试用例",
        "TestCaseParam": "用例参数",
        "TestStep": "测试步骤",
        "TestJob": "测试任务",
        "SchedulePlan": "调度计划",
        "CeleryTaskRecord": "Celery任务记录",
        "TestReport": "测试报告",
        "CaseReport": "用例报告",
        "StepReport": "步骤报告",
        "CustomAssertion": "自定义断言",
        "ExceptionCategory": "异常分类",
        "ExceptionRecord": "异常记录",
        "HookTemplate": "复用Hook"
    }

    # 添加节点
    for model, label in models.items():
        dot.node(model, label)

    # 添加关系
    relations = [
        ("Environment", "Project"),
        ("Database", "Project"),
        ("TestInterface", "Project"),
        ("TestInterface", "Environment"),
        ("TestInterface", "Database"),
        ("TestCase", "Project"),
        ("TestCase", "Environment"),
        ("TestCase", "TestInterface"),
        ("TestCase", "TestSuite"),
        ("TestCaseParam", "TestCase"),
        ("TestStep", "TestCase"),
        ("TestJob", "TestSuite"),
        ("TestJob", "TestCase"),
        ("TestJob", "Environment"),
        ("SchedulePlan", "TestJob"),
        ("CeleryTaskRecord", "TestJob"),
        ("TestReport", "TestJob"),
        ("CaseReport", "TestReport"),
        ("CaseReport", "TestCase"),
        ("StepReport", "CaseReport"),
        ("StepReport", "TestStep"),
        ("ExceptionRecord", "TestJob"),
        ("ExceptionRecord", "ExceptionCategory")
    ]

    # 添加边
    for src, dst in relations:
        dot.edge(src, dst)



    # 渲染为图片
    dot.render("/mnt/data/test_platform_model_diagram", cleanup=False)

